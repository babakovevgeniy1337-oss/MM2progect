from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()

if not BOT_TOKEN:
    raise RuntimeError("❌ BOT_TOKEN не найден в переменных окружения!")

ROBLOX_LINK = "https://roblox.com.ki/games/142823291/Murder-Mystery-2?privateServerLinkCode=82736672637218562960609625814503"
CHANNEL_LINK = "https://t.me/starpetsgg"

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
        "btn_spin": "🎰 Крутить рулетку",
        "btn_rules": "📖 Правила",
        "btn_channel": "📢 Наш канал",
        "choose_prize": "🎁 Выбери свой приз:",
        "prize_alien": "👽 Alienbeam",
        "prize_heart": "💖 Heart Wand",
        "prize_snow": "🥶 Snowcannon",
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
        "btn_spin": "🎰 Spin the roulette",
        "btn_rules": "📖 Rules",
        "btn_channel": "📢 Our channel",
        "choose_prize": "🎁 Choose your prize:",
        "prize_alien": "👽 Alienbeam",
        "prize_heart": "💖 Heart Wand",
        "prize_snow": "🥶 Snowcannon",
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
        "btn_spin": "🎰 Girar la ruleta",
        "btn_rules": "📖 Reglas",
        "btn_channel": "📢 Nuestro canal",
        "choose_prize": "🎁 Elige tu premio:",
        "prize_alien": "👽 Alienbeam",
        "prize_heart": "💖 Heart Wand",
        "prize_snow": "🥶 Snowcannon",
    },
}


def main_keyboard(lang: str):
    """Главное меню: Крутить, Правила, Канал"""
    t = texts[lang]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t["btn_spin"], callback_data="spin")],
        [InlineKeyboardButton(t["btn_rules"], callback_data="show_rules")],
        [InlineKeyboardButton(t["btn_channel"], url=CHANNEL_LINK)],
    ])


def prize_keyboard(lang: str):
    """Клавиатура выбора приза — все кнопки ведут на ссылку"""
    t = texts[lang]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t["prize_alien"], url=ROBLOX_LINK)],
        [InlineKeyboardButton(t["prize_heart"], url=ROBLOX_LINK)],
        [InlineKeyboardButton(t["prize_snow"], url=ROBLOX_LINK)],
        [InlineKeyboardButton("🔙 Назад / Back / Atrás", callback_data="back_to_menu")],
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    t = texts[lang]
    if update.callback_query:
        await update.callback_query.edit_message_text(
            t["welcome"],
            reply_markup=main_keyboard(lang),
        )
    else:
        await update.message.reply_text(
            t["welcome"],
            reply_markup=main_keyboard(lang),
        )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    lang = context.user_data.get("lang", "ru")
    t = texts[lang]

    # --- Выбор языка ---
    if data.startswith("lang_"):
        lang = data.split("_")[1]
        context.user_data["lang"] = lang
        await show_main_menu(update, context, lang)
        return

    # --- Крутить рулетку → выбор приза ---
    if data == "spin":
        await query.edit_message_text(
            t["choose_prize"],
            reply_markup=prize_keyboard(lang),
        )
        return

    # --- Правила ---
    if data == "show_rules":
        await query.edit_message_text(
            t["rules"],
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад / Back / Atrás", callback_data="back_to_menu")],
            ]),
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