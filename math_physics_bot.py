import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from sympy import sympify, solve, Eq, Symbol

# Enable logging for debugging:
logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Hi! I am your Math & Physics bot 🤖. Send me an equation or a physics problem!'
    )

async def solve_equation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    try:
        # Attempt to parse and solve as algebraic equation
        if '=' in text:
            lhs, rhs = text.split('=')
            eq = Eq(sympify(lhs), sympify(rhs))
            x = Symbol('x')
            solution = solve(eq, x)
            await update.message.reply_text(f"Solution: {solution}")
        else:
            # If not an equation, just evaluate
            result = sympify(text)
            await update.message.reply_text(f"Result: {result}")
    except Exception as e:
        await update.message.reply_text("Sorry, I couldn't solve this. Make sure the equation is valid.")

def main():
    TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, solve_equation))

    app.run_polling()

if __name__ == "__main__":
    main()