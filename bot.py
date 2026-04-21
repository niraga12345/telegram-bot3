from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import asyncio

BOT_TOKEN = "8740431916:AAFqL9POKq70q-C0bUlERvbgVoUyj5h5_lE"

groups = set()
users = set()  # inbox users

# =========================
# GROUP MESSAGES
# =========================
messages = ["Hii mn girl chat karanna kemathi kawuda" , "boy kenek ib enna" , "kawuda inne video call ganna mn girl" , "gedara kawuruth nh video call gamud" , "math asay mool wenna wiswasawantha kollek ennako" , "mawa mool karanna puluwan walma wal boy kenek enna" , "juce yanakam uranna puluwan boy kenek enna" , "boy kenek nedda mool wenna asa man girl" , "meet wenna asay mn mata hodata fuck karanna puluwan katada" , "mage kukku bonna asa kawuda" , "mawa mool karala sepaganna asa kawuda" , "juce yanawa balanna asa boy kenek enna" , "mama asay sex karanna boy kenek one hodata walkollek one"]
msg_index = 0

async def track_groups(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat and chat.type in ["group", "supergroup"]:
        if chat.id not in groups:
            groups.add(chat.id)
            print("Group added:", chat.id)

async def send_messages(app):
    global msg_index

    while True:
        if groups:
            current_msg = messages[msg_index]

            for group_id in list(groups):
                try:
                    await app.bot.send_message(chat_id=group_id, text=current_msg)
                except Exception as e:
                    print("Group Error:", e)

            msg_index = (msg_index + 1) % len(messages)

        await asyncio.sleep(600)

# =========================
# INBOX LOOP DATA 🔥
# =========================
inbox_messages = [
    {
        "text": "හායි බබා ...මාත් එක්ක වීඩියෝ කොල් ගන්න ආස ද මන් වීඩියෝ කොල් ගන්නෙ ගෲප් එකට මෙම්බර්ස්ලා දහයක් ඇඩ් කලොත් විතරයි. 😘පහල ලින්ක් එකෙන් ජොයින් වෙලා මෙම්බර්ස්ලා දහයක් ඇඩ් කරලා මට මැසෙජ් එකක් දන්න 🥰 \n\ https://t.me/+Su8HqG2QGE5kOGY9",
        "button": ("👉 Join වෙන්න", "https://t.me/+Su8HqG2QGE5kOGY9")
    },
    {
        "text": "හායි බබා ...මාත් එක්ක වීඩියෝ කොල් ගන්න ආස ද මන් වීඩියෝ කොල් ගන්නෙ ගෲප් එකට මෙම්බර්ස්ලා දහයක් ඇඩ් කලොත් විතරයි. 😘පහල ලින්ක් එකෙන් ජොයින් වෙලා මෙම්බර්ස්ලා දහයක් ඇඩ් කරලා මට මැසෙජ් එකක් දන්න 🥰 \n\ https://t.me/+PMWeu4toRts2Y2U1",
        "button": ("👉 Join වෙන්න", "https://t.me/+PMWeu4toRts2Y2U1")
    },
    {
      "text": "හායි බබා ...මාත් එක්ක වීඩියෝ කොල් ගන්න ආස ද මන් වීඩියෝ කොල් ගන්නෙ ගෲප් එකට මෙම්බර්ස්ලා දහයක් ඇඩ් කලොත් විතරයි. 😘පහල ලින්ක් එකෙන් ජොයින් වෙලා මෙම්බර්ස්ලා දහයක් ඇඩ් කරලා මට මැසෙජ් එකක් දන්න 🥰 \n\ https://t.me/+HP_ByJhOn6xmOTc1",
        "button": ("👉 Join වෙන්න", "https://t.me/+HP_ByJhOn6xmOTc1")
    }
]

inbox_index = 0

# =========================
# TRACK INBOX USERS
# =========================
async def track_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type == "private":
        if chat.id not in users:
            users.add(chat.id)
            print("User added:", chat.id)

# =========================
# INBOX AUTO LOOP 🔥
# =========================
async def send_inbox_messages(app):
    global inbox_index

    while True:
        if users:
            data = inbox_messages[inbox_index]

            for user_id in list(users):
                try:
                    user = await app.bot.get_chat(user_id)
                    name = user.first_name or "යාළුවා"

                    text = data["text"].format(name=name)

                    keyboard = [
                        [InlineKeyboardButton(data["button"][0], url=data["button"][1])]
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)

                    await app.bot.send_message(
                        chat_id=user_id,
                        text=text,
                        reply_markup=reply_markup
                    )

                except Exception as e:
                    print("Inbox Error:", e)

            inbox_index = (inbox_index + 1) % len(inbox_messages)

        await asyncio.sleep(600)  # 10 minute

# =========================
# BUILD APP
# =========================
app = ApplicationBuilder().token(BOT_TOKEN).build()

# group detect
app.add_handler(MessageHandler(filters.ALL & ~filters.ChatType.PRIVATE, track_groups))

# inbox detect
app.add_handler(MessageHandler(filters.ChatType.PRIVATE, track_users))

# background tasks
async def post_init(app):
    asyncio.create_task(send_messages(app))        # group loop
    asyncio.create_task(send_inbox_messages(app))  # inbox loop

app.post_init = post_init

print("Bot running...")
app.run_polling()
