import logging

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import LabeledPrice, Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, Update, Message
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    PreCheckoutQueryHandler,
    CallbackQueryHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
PAYMENT_PROVIDER_TOKEN = "284685063:TEST:NTdhNmVhZjNhNjU0"

keyboard = [
    [InlineKeyboardButton("S'abonner", callback_data="3")],
]

reply_markup = InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        #[
        #    InlineKeyboardButton("Option 1", callback_data="1"),
        #    InlineKeyboardButton("Option 2", callback_data="2"),
        #],
        [KeyboardButton("ℹ️ Information"), KeyboardButton("📝 S'abonner")],
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    intro_message = """
👋 Hello! Je suis Salix Nigra bot, je serai votre interlocuteur.

Cliquez sur S’abonner ci-dessous pour commencer à recevoir immédiatement Mes signaux de trading eInvestors! 📈

⭐️ eInvestors Bot Trading Signals ⭐️

📈2-4 Signaux journaliers
📈Forex Uniquement
📈1000+ VIP Membres
📈Day Trades & Swing Trades
📈TP & SL sur chaque position
📈Analyses Forex d'Anselme et Rosine
📈Copieur de trading pour MT4 et MT5 pour tous les membres VIP (signaux de trading automatique de n’importe où dans le monde!) 🗺
📈Aperçu exclusif des projets dans lesquels Anselme investit (Actions, ETF, matières premières et idées d'investissement)

Mars  -19% ✅
Avril +0.49% ✅
Mai +5.42% ✅
Juin +6.88% ✅
Juillet -3.6% ✅
August +13.42% ✅
September -30.27% ✅

✅ Risk 1-3% per trade ✅

❌ Pas de remboursement 

❌ Pas de partage de contenus

L’abonnement ne se renouvelle pas automatiquement

Nous offrons nos robots de trading pour prendre automatiquement nos signaux de trading, ce qui signifie que vous n’avez pas à placer nos transactions manuellement!

✅ Prends ton temps, et profite ✅

Choisis parmi nos plans ci-dessous, il n’y a pas de codes promo disponibles. Après avoir payé, vous obtiendrez un lien vers le canal 📈 VIP. Cliquez sur les informations en bas pour voir combien de jours il reste dans votre abonnement et accéder à VIP.

⚠️Envoie-moi un e-mail si vous souhaitez payer via crypto⚠️

Si vous payez via PayPal, cela prend parfois quelques minutes, n’achetez pas deux fois. ⚠️

Si vous avez besoin d’aide, envoyez un courriel à Anselme ici: anselme.nkondog@salixnigra.com 📧

Si vous ne voyez pas le bouton S’abonner,  clique ici 👉🏽 /Abonnement"""
    await update.message.reply_text(intro_message, reply_markup=reply_markup)

async def abonnement(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Subscription"""

    intro_message = """Clique pour commencer la procédure d'abonnement aux signaux."""

    await update.message.reply_text(intro_message, reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    if query.data == "3":
        keyboard = [
            [
            InlineKeyboardButton("Mensuel", callback_data="40"),
            InlineKeyboardButton("Annuel", callback_data="200"),
            InlineKeyboardButton("A vie", callback_data="500"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        intro_message = """
Choisis l’un des tarifs présentés:

Mensuel (30 jours) - $40.0
Annuel (365 jours) - $200.0
A vie 🏆 (♾ éternellement) - $500.0
"""
        await query.edit_message_text(intro_message, reply_markup=reply_markup)
    elif query.data == "40" or query.data == "200" or query.data == "500":
        label = "Mensuel" if query.data == "40" else "Annuel" if query.data == "200" else "A vie"
        """Sends an invoice without shipping-payment."""
        chat_id = query.message.chat.id
        title = "eInvestor Trading Signal Bot"
        description = "Abonnes-toi au signaux de trading et intégre le groupe d'analyses et discussions sur le trading des eInvestors"
        # select a payload just for you to recognize its the donation from your bot
        payload = "Custom-Payload"
        # In order to get a provider_token see https://core.telegram.org/bots/payments#getting-a-token
        currency = "USD"
        # price in dollars
        price = int(query.data)
        # price * 100 so as to include 2 decimal points
        prices = [LabeledPrice(label, price * 100)]

        # optionally pass need_name=True, need_phone_number=True,
        # need_email=True, need_shipping_address=True, is_flexible=True
        await context.bot.send_invoice(
            chat_id, title, description, payload, PAYMENT_PROVIDER_TOKEN, currency, prices
        )

    else:
        await query.edit_message_text(text=f"Selected option: {query.data}")

# after (optional) shipping, it's the pre-checkout
async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Answers the PreQecheckoutQuery"""
    query = update.pre_checkout_query
    # check the payload, is this from your bot?
    if query.invoice_payload != "Custom-Payload":
        # answer False pre_checkout_query
        await query.answer(ok=False, error_message="Something went wrong...")
    else:
        await query.answer(ok=True)
        print(query)


# finally, after contacting the payment provider...
async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Confirms the successful payment."""
    # do something after successfully receiving payment?
    keyboard = [[InlineKeyboardButton("⭐️ Rejoins le groupe ⭐️", url="https://t.me/+DO2w2iQvujljNTA0"),]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    payment_message = """
✅ L’abonnement a été payé et activé avec succès!

1. Après avoir rejoint le canal en utilisant le bouton ci-dessus, clique sur le message épinglé pour accéder à la zone des membres. C’est ici que tu télécharges le copytrader gratuit et accèdes à tous nos documents secrets.🆓

2. Si tu as besoin de vérifier ton abonnement, reviens à ce bot (@mySalixBot) et clique sur informations. C’est également là que vous pouvez accéder au canal de signaux si tu le quittes accidentellement. 🔑
"""
    await update.message.reply_text(payment_message, reply_markup=reply_markup)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    userSelection = update.message.text.split(" ")[-1].lower()
    print(userSelection)
    if userSelection == "information":
        await update.message.reply_text("Votre abonnement est à ce niveau")
    if userSelection == "s'abonner":
        subs_message = """Clique pour commencer la procédure d'abonnement aux signaux."""

        await update.message.reply_text(subs_message, reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text("Use /start to test this bot.")


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("5693377576:AAGkLB6mocl9D8qS3ip4EUcUlub346wGJ1w").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("abonnement", abonnement))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Pre-checkout handler to final check
    application.add_handler(PreCheckoutQueryHandler(precheckout_callback))

    # Success! Notify your user!
    application.add_handler(
        MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback)
    )

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()