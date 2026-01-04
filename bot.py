import uuid
import os
from solana_check import payment_received
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from database import add_user

TOKEN = "8254959529:AAFWi22T4M3sjBpOw1DX6bJ6fVZiGEmzTLw"
SOLANA_ADDRESS = "9SoDErVydBbUeZe66w26HzPyWHdebuevukFgPgQwvtV6"

# -------------------------
# Fonctions utilitaires
# -------------------------
def generate_memo(user_id):
    return f"ZK-{user_id}-{uuid.uuid4().hex[:6]}"

def generate_txt(memo):
    folder = "files"
    os.makedirs(folder, exist_ok=True)
    filename = os.path.join(folder, f"access_{memo}.txt")
    content = f"""
Merci pour ton achat 🙏

Voici ton accès personnel à la formation.

Code unique :
{memo}

Ce fichier est strictement personnel.
"""
    with open(filename, "w") as f:
        f.write(content)

    print(f"[DEBUG] Fichier créé : {filename}")
    return filename

# -------------------------
# Commande /start
# -------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💳 Acheter la formation (1€)", callback_data="buy")]
    ]
    await update.message.reply_text(
        "🎓 Formation privée\nPrix : 1€ en SOL",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# -------------------------
# Gestion bouton
# -------------------------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "buy":
        user_id = query.from_user.id
        memo = generate_memo(user_id)
        add_user(user_id, memo)

        text = f"""
💳 Paiement en SOL

Adresse :
{SOLANA_ADDRESS}

Montant :
≈ 1€

🧾 MEMO OBLIGATOIRE :
{memo}

⏳ Vérification du paiement...
"""
        await query.edit_message_text(text)

        # SIMULATION paiement
        if await payment_received(memo):
            filename = generate_txt(memo)
            await context.bot.send_document(
                chat_id=user_id,
                document=open(filename, "rb")
            )
            print(f"[DEBUG] Fichier envoyé à {user_id}")

# -------------------------
# Main
# -------------------------
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.run_polling()

