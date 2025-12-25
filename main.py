from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random

# Stockage des points des joueurs (en mémoire)
players = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in players:
        players[user_id] = 100

    await update.message.reply_text(
        "🎮 Bienvenue dans LuckyBet (jeu de pari virtuel) !\n\n"
        "🪙 Tu commences avec 100 points.\n"
        "Parie avec : /bet mise nombre(1-10)\n"
        "Exemple : /bet 20 7\n\n"
        "Voir ton solde : /score"
    )

async def bet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in players:
        players[user_id] = 100

    try:
        mise = int(context.args[0])
        choix = int(context.args[1])
    except:
        await update.message.reply_text(
            "❌ Mauvais format.\nUtilise : /bet mise nombre"
        )
        return

    if mise <= 0:
        await update.message.reply_text("❌ La mise doit être positive.")
        return

    if mise > players[user_id]:
        await update.message.reply_text("❌ Tu n’as pas assez de points.")
        return

    if choix < 1 or choix > 10:
        await update.message.reply_text("❌ Choisis un nombre entre 1 et 10.")
        return

    resultat = random.randint(1, 10)

    if choix == resultat:
        players[user_id] += mise
        await update.message.reply_text(
            f"🎉 GAGNÉ !\n"
            f"Nombre tiré : {resultat}\n"
            f"+{mise} points 🪙\n"
            f"Solde : {players[user_id]}"
        )
    else:
        players[user_id] -= mise
        await update.message.reply_text(
            f"❌ PERDU\n"
            f"Nombre tiré : {resultat}\n"
            f"-{mise} points 🪙\n"
            f"Solde : {players[user_id]}"
        )

async def score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    solde = players.get(user_id, 100)
    await update.message.reply_text(f"🪙 Ton solde actuel : {solde} points")

# ⚠️ REMPLACE TON_TOKEN_ICI par le token de BotFather
app = ApplicationBuilder().token(8209777676:AAG7TUPoNq0JhEokryZ4ufzLNtEzlRLkltY).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("bet", bet))
app.add_handler(CommandHandler("score", score))

app.run_polling()
