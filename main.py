from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

# Пробуем взять из переменных окружения, иначе из .env
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    from dotenv import load_dotenv
    load_dotenv()
    BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не найден ни в окружении, ни в .env")

# Тексты на трёх языках
texts = {
    "ru": {
        "welcome": (
            "Привет! 👋\n"
            "🎲  Это игра в ВСЁ ИЛИ НИЧЕГО!\n"
            "Чистая удача и твоя аура, крути рулетку каждые 24 часа и получай призы🎁\n\n"
            "🎁  Тебе могут выпасть абсолютно рандомные\n"
            "оружия Murder Mystery 2\n"
            "Редкость оружия: Godly🔥"
        ),
        "rules": (
            "📖  Правила игры:\n"
            "1️⃣  Ты крутишь рулетку 1 раз в 24 часа!\n"
            "2️⃣  Шанс 50% на выигрыш и 50% на проигрыш!\n"
            "3️⃣  При выигрыше ты выбираешь 1 из 3 призов!\n"
            "4️⃣  При проигрыше возвращайся завтра!\n\n"
            "🎯  Удачи!"
        ),
        "btn_rules": "📖 Правила",
        "btn_spin": "🎰 Крутить рулетку",
        "btn_channel": "📢 Наш канал",
        "already_spun": "⏳ Ты уже крутил рулетку!\nСледующий спин через 23ч 58мин⏳",
        "channel_text": "📢 Наш канал: @starpetsgg\nНажми на кнопку ниже, чтобы перейти!",
    },
    "en": {
        "welcome": (
            "Hello! 👋\n"
            "🎲 This is ALL OR NOTHING game!\n"
            "Pure luck and your aura, spin the roulette every 24 hours and get prizes🎁\n\n"
            "🎁 You can get absolutely random\n"
            "Murder Mystery 2 weapons\n"
            "Weapon rarity: Godly🔥"
        ),
        "rules": (
            "📖 Game Rules:\n"
            "1️⃣ You spin the roulette once every 24 hours!\n"
            "2️⃣ 50% chance to win and 50% chance to lose!\n"
            "3️⃣ If you win, you choose 1 of 3 prizes!\n"
            "4️⃣ If you lose, come back tomorrow!\n\n"
            "🎯 Good luck!"
        ),
        "btn_rules": "📖 Rules",
        "btn_spin": "🎰 Spin the roulette",
        "btn_channel": "📢 Our channel",
        "already_spun": "⏳ You've already spun the roulette!\nNext spin in 23h 58min⏳",
        "channel_text": "📢 Our channel: @starpetsgg\nClick the button below to go!",
    },
    "es": {
        "welcome": (
            "¡Hola! 👋\n"
            "🎲 ¡Este es el juego de TODO O NADA!\n"
            "Pura suerte y tu aura, gira la ruleta cada 24 horas y obtén premios🎁\n\n"
            "🎁 Puedes obtener armas completamente aleatorias\n"
            "de Murder Mystery 2\n"
            "Rareza del arma: Godly🔥"
        ),
        "rules": (
            "📖 Reglas del juego:\n"
            "1️⃣ ¡Giras la ruleta 1 vez cada 24 horas!\n"
            "2️⃣ ¡50% de probabilidad de ganar y 50% de perder!\n"
            "3️⃣ Si ganas, eliges 1 de 3 premios!\n"
            "4️⃣ Si pierdes, ¡vuelve mañana!\n\n"
            "🎯 ¡Buena suerte!"
        ),
        "btn_rules": "📖 Reglas",
        "btn_spin": "🎰 Girar la ruleta",
        "btn_channel": "📢 Nuestro canal",
        "already_spun": "⏳ ¡Ya has girado la ruleta!\nPróximo giro en 23h 58min⏳",
        "channel_text": "📢 Nuestro canal: @starpetsgg\n¡Haz clic en el botón de abajo para ir!",
    },
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """При /start — выбор языка"""
    keyboard = [
        [
            InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
            InlineKeyboardButton("🇪🇸 Español", callback_data="lang_es"),
        ]
    ]
    await update.message.reply_text(
        "🌍 Выбери язык / Choose language / Elige idioma:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, lang: str):
    """Показать главное меню с тремя кнопками"""
    t = texts[lang]
    keyboard = [
        [InlineKeyboardButton(t["btn_rules"], callback_data="show_rules")],
        [InlineKeyboardButton(t["btn_spin"], callback_data="spin")],
        [InlineKeyboardButton(t["btn_channel"], callback_data="channel")],
    ]

    if update.callback_query:
        await update.callback_query.edit_message_text(
            t["welcome"],
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    else:
        await update.message.reply_text(
            t["welcome"],
            reply_markup=InlineKeyboardMarkup(keyboard),
        )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    lang = context.user_data.get("lang", "ru")
    t = texts[lang]

    # --- Пользователь выбрал язык ---
    if data.startswith("lang_"):
        lang = data.split("_")[1]
        context.user_data["lang"] = lang
        await show_main_menu(update, context, lang)
        return

    # --- Показать правила ---
    if data == "show_rules":
        await query.edit_message_text(
            t["rules"],
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад / Back / Atrás", callback_data="back_to_menu")],
            ]),
        )
        return

    # --- Крутить рулетку ---
    if data == "spin":
        await query.edit_message_text(
            t["already_spun"],
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад / Back / Atrás", callback_data="back_to_menu")],
            ]),
        )
        return

    # --- Наш канал (Ссылка) ---
    if data == "channel":
        keyboard = [
            [
                InlineKeyboardButton(
                    "🔗 Перейти в канал / Go to channel / Ir al canal",
                    url="https://t.me/starpetsgg",
                )
            ],
            [InlineKeyboardButton("🔙 Назад / Back / Atrás", callback_data="back_to_menu")],
        ]
        await query.edit_message_text(
            t["channel_text"],
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return

    # --- Назад в меню ---
    if data == "back_to_menu":
        await show_main_menu(update, context, lang)
        return


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("🤖 Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()