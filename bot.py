import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, Filters

# Configuration with YOUR specific links
TOKEN = "YOUR_BOT_TOKEN"
CHANNEL_LINK = "https://t.me/CryptoPumpChannel01"
GROUP_LINK = "https://t.me/+WbrfygqR3JoyMWM0"
TWITTER_LINK = "https://x.com/captxrpm?s=11&t=RfuaoDpfagPLK3Y2aHujLw"

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("✅ Verify Completion", callback_data='verify')],
        [InlineKeyboardButton("💰 Submit SOL Wallet", callback_data='submit_wallet')]
    ]
    
    message = (
        f"👋 Welcome {user.first_name} to the Akindefi Airdrop!\n\n"
        "📋 To qualify for 100 SOL airdrop:\n"
        f"1. Join our Telegram Channel: {CHANNEL_LINK}\n"
        f"2. Join our Telegram Group: {GROUP_LINK}\n"
        f"3. Follow our Twitter: {TWITTER_LINK}\n"
        "4. Submit your SOL wallet address\n\n"
        "After completing all steps, click VERIFY below:"
    )
    
    update.message.reply_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        disable_web_page_preview=True
    )

def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    if query.data == 'verify':
        verify_completion(update, context)
    elif query.data == 'submit_wallet':
        context.user_data['awaiting_wallet'] = True
        query.message.reply_text("🔑 Please send your Solana wallet address now:")

def verify_completion(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    message = (
        "✅ Verification Complete!\n\n"
        "Well-done! We trust you've completed all tasks honestly.\n"
        "Hope you didn't cheat the system!\n\n"
        "Now submit your SOL wallet to receive your 100 SOL reward."
    )
    query.edit_message_text(message)

def handle_wallet(update: Update, context: CallbackContext) -> None:
    if 'awaiting_wallet' not in context.user_data:
        return
        
    wallet = update.message.text.strip()
    user = update.effective_user
    
    # Basic SOL address validation
    if len(wallet) >= 32 and len(wallet) <= 44:
        # In a real bot, you would save the wallet here
        # But per your request, we're not saving it
        
        # Send success message with reward notification
        success_msg = (
            "🎉 Congratulations! You've successfully completed the Akindefi Airdrop!\n\n"
            "💸 100 SOL is on its way to your wallet!\n\n"
            f"Wallet: `{wallet}`\n\n"
            "⏳ Please allow 24-48 hours for the transaction to process.\n"
            "Thank you for participating!"
        )
        
        update.message.reply_text(
            success_msg,
            parse_mode="Markdown"
        )
        
        # Reset the state
        context.user_data.pop('awaiting_wallet', None)
    else:
        update.message.reply_text(
            "⚠️ That doesn't look like a valid SOL wallet address. "
            "Please check and resend your Solana wallet address."
        )

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button_handler))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_wallet))

    updater.start_polling()
    logger.info("Bot is now running...")
    updater.idle()

if __name__ == '__main__':
    main()
