import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Bot Token ကို ဒီမှာထည့်ပါ
TOKEN = "8203493135:AAE535KyrDNSml3W4NveuK-R8KQbTwDKxJY"

# Leaderboard အတွက် အမှတ်မှတ်ထားဖို့ (မှတ်ချက် - Bot Restart ကျရင် ဒါတွေ ပျက်သွားနိုင်ပါတယ်)
user_scores = {}

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("🎮 အကန့်အသတ်မရှိ ဆော့လို့ရတဲ့ ဂိမ်းကနေ ကြိုဆိုပါတယ်!\n/play ကို နှိပ်ပြီး ဂိမ်းစဆော့ပါ။ Leaderboard ကြည့်ဖို့ /top ကို နှိပ်ပါ။")

async def play(update: Update, context: CallbackContext):
    secret_number = random.randint(1, 100)
    context.user_data['secret_number'] = secret_number
    context.user_data['attempts'] = 0
    await update.message.reply_text("🔢 ၁ ကနေ ၁၀၀ ကြားထဲက ကိန်းဂဏန်းတစ်ခုကို ငါစဉ်းစားထားတယ်။ ခန့်မှန်းကြည့်ပါ!")

async def guess(update: Update, context: CallbackContext):
    if 'secret_number' not in context.user_data:
        return

    try:
        user_guess = int(update.message.text)
        context.user_data['attempts'] += 1
        secret = context.user_data['secret_number']

        if user_guess < secret:
            await update.message.reply_text("📉 နည်းနေသေးတယ်! ပိုကြီးတဲ့ နံပါတ် ခန့်မှန်းကြည့်။")
        elif user_guess > secret:
            await update.message.reply_text("📈 များနေပြီ! ပိုငယ်တဲ့ နံပါတ် ခန့်မှန်းကြည့်။")
        else:
            attempts = context.user_data['attempts']
            user_name = update.message.from_user.first_name
            
            # Leaderboard အတွက် မှတ်ခြင်း
            if user_name not in user_scores or attempts < user_scores[user_name]:
                user_scores[user_name] = attempts

            await update.message.reply_text(f"🎉 ဝမ်းသာပါတယ် {user_name}! {attempts} ကြိမ်နဲ့ မှန်အောင် ခန့်မှန်းနိုင်သွားပြီ။")
            del context.user_data['secret_number']
    except ValueError:
        await update.message.reply_text("⚠️ ကျေးဇူးပြု၍ ဂဏန်းပဲ ရိုက်ပေးပါ။")

async def leaderboard(update: Update, context: CallbackContext):
    if not user_scores:
        await update.message.reply_text("ခုထိတော့ ဘယ်သူမှ စံချိန်မတင်ရသေးဘူး။")
        return
    
    sorted_scores = sorted(user_scores.items(), key=lambda x: x[1])
    text = "🏆 **Leaderboard (အချက်အနည်းဆုံးနဲ့ နိုင်သူများ)** 🏆\n\n"
    for i, (name, score) in enumerate(sorted_scores[:10], 1):
        text += f"{i}. {name} - {score} ကြိမ်\n"
    await update.message.reply_text(text, parse_mode="Markdown")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("play", play))
    app.add_handler(CommandHandler("top", leaderboard))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, guess))
    app.run_polling()

if __name__ == '__main__':
    main()
