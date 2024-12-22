import logging

import stripe
from django.utils import timezone

from BaseBillet.models import LigneArticle, Product, Membership, Price, Configuration
from BaseBillet.tasks import send_to_ghost, send_membership_invoice_to_email, send_sale_to_laboutik
from BaseBillet.templatetags.tibitags import dround
from fedow_connect.fedow_api import FedowAPI
from root_billet.models import RootConfiguration

logger = logging.getLogger(__name__)



def update_membership_state_after_stripe_paiement(ligne_article):
    paiement_stripe = ligne_article.paiement_stripe
    membership = paiement_stripe.membership.first()

    price: Price = ligne_article.pricesold.price
    membership.contribution_value = ligne_article.pricesold.prix

    if price.free_price:
        # Le montant a été entré dans stripe, on ne l'a pas entré à la création
        stripe.api_key = RootConfiguration.get_solo().get_stripe_api()
        # recherche du checkout
        checkout_session = stripe.checkout.Session.retrieve(
            paiement_stripe.checkout_session_id_stripe,
            stripe_account=Configuration.get_solo().get_stripe_connect_account()
        )
        # Mise à jour du montant
        ligne_article.amount = checkout_session['amount_total']
        contribution = dround(checkout_session['amount_total'])
        membership.contribution_value=contribution

    membership.last_contribution = timezone.now().date()
    membership.stripe_paiement.add(paiement_stripe)

    if paiement_stripe.invoice_stripe:
        membership.last_stripe_invoice = paiement_stripe.invoice_stripe

    if paiement_stripe.subscription:
        membership.stripe_id_subscription = paiement_stripe.subscription
        membership.status = Membership.AUTO

    membership.save()
    logger.info(f"    update_membership_state_after_paiement : Mise à jour de la fiche membre OK")
    return membership


def send_membership_to_ghost(membership: Membership):
    # Envoyer à ghost :
    if membership.newsletter:
        send_to_ghost.delay(membership.pk)
        logger.info(f"    update_membership_state_after_paiement : Envoi de la confirmation à Ghost DELAY")
    return True


### END MEMBERSHIP TRIGGER ####

### SEND TO LABOUTIK for comptabilité ###



# Pour usage en CLI :
# def send_sale_from_membership_to_laboutik(membership: Membership):
#     """
#     for m in Membership.objects.filter(stripe_paiement__isnull=False):
#         send_sale_from_membership_to_laboutik(m)
#     """
#     config = Configuration.get_solo()
#     if config.check_serveur_cashless():
#         if membership.stripe_paiement.exists():
#             stripe_paiement:Paiement_stripe = membership.stripe_paiement.first()
#             if stripe_paiement.lignearticles.exists():
#                 ligne_article : LigneArticle = stripe_paiement.lignearticles.first()
#                 if ligne_article.status in [LigneArticle.PAID, LigneArticle.VALID]:
#                     send_sale_to_laboutik(ligne_article)


### END SEND TO LABOUTIK

# MACHINE A ETAT pour les ventes
class ActionArticlePaidByCategorie:
    """
    Trigged action by categorie when Article is PAID
    """

    def __init__(self, ligne_article: LigneArticle):
        self.ligne_article = ligne_article
        self.categorie = self.ligne_article.pricesold.productsold.categorie_article

        if self.categorie == Product.NONE:
            self.categorie = self.ligne_article.pricesold.productsold.product.categorie_article

        self.data_for_cashless = {}
        if ligne_article.paiement_stripe:
            self.data_for_cashless = {
                'uuid_commande': ligne_article.paiement_stripe.uuid,
                'email': ligne_article.paiement_stripe.user.email
            }

        try:
            # on met en majuscule et on rajoute _ au début du nom de la catégorie.
            trigger_name = f"_{self.categorie.upper()}"
            logger.info(
                f"category_trigger launched - ligne_article : {self.ligne_article} - trigger_name : {trigger_name}")
            trigger = getattr(self, f"trigger{trigger_name}")
            trigger()
        except AttributeError as exc:
            logger.info(f"Pas de trigger pour la categorie {self.categorie} - ERROR : {exc} - {type(exc)}")
        except Exception as exc:
            logger.error(f"category_trigger {self.categorie.upper()} ERROR : {exc} - {type(exc)}")

    # Category DON
    def trigger_D(self):
        # On a besoin de valider la ligne article pour que le paiement soit validé
        self.ligne_article.status = LigneArticle.VALID
        logger.info(f"TRIGGER DON")

    # Category BILLET
    def trigger_B(self):
        logger.info(f"TRIGGER BILLET")

    # Category Free Reservation
    def trigger_F(self):
        logger.info(f"TRIGGER FREE RESERVATION")

    # Category RECHARGE_CASHLESS
    def trigger_R(self):
        logger.info(f"TRIGGER RECHARGE_CASHLESS")

    # Category RECHARGE_FEDERATED
    def trigger_S(self):
        logger.info(f"TRIGGER RECHARGE_FEDERATED")

    # Categorie ADHESION
    def trigger_A(self):
        logger.info(f"TRIGGER ADHESION PAID")

        # On va chercher l'article vendu et l'adhésion associéé
        ligne_article: LigneArticle = self.ligne_article
        membership = ligne_article.membership


        # Refresh en cas de prix libre, le prix est mis à jour par le update membership.
        if ligne_article.paiement_stripe:
            membership: Membership = update_membership_state_after_stripe_paiement(ligne_article)

        email_sended = send_membership_invoice_to_email(membership)

        # TODO: a séparer et ajouter dans un objet "connect"
        # ghost_sended = send_membership_to_ghost(membership)

        logger.info(f"TRIGGER ADHESION PAID -> envoi à Fedow")
        # L'adhésion possède désormais une transaction fedow associé
        # Attention, réalise membership.save()
        fedowAPI = FedowAPI()
        serialized_transaction = fedowAPI.membership.create(membership=membership)

        logger.info(f"TRIGGER ADHESION PAID -> envoi à LaBoutik")
        laboutik_sended = send_sale_to_laboutik(self.ligne_article)

        # Si tout est passé plus haut, on VALID La ligne :
        # Tout ceci se déroule dans un pre_save signal.pre_save_signal_status()
        logger.info(f"TRIGGER ADHESION PAID -> set VALID")
        self.ligne_article.status = LigneArticle.VALID
