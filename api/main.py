from fastapi import FastAPI, Request
import asyncio
from telebot.async_telebot import AsyncTeleBot
import firebase_admin
from firebase_admin import credentials, firestore
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

app = FastAPI()

# Initialize the bot
BOT_TOKEN = '8113117364:AAEBZZZQrXK2RfmvrKcNfntkvIsgnt-OrTw'
bot = AsyncTeleBot(BOT_TOKEN)

# Firebase configuration
firebase_service_account = {
    "type": "service_account",
    "project_id": "orblix-15f00",
    "private_key_id": "bea8674faeeaf44749c4e5dfc69d10847ad72d31",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADAN...",
    "client_email": "firebase-adminsdk-il80v@orblix-15f00.iam.gserviceaccount.com",
    "client_id": "102518934139618313626",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-il80v@orblix-15f00.iam.gserviceaccount.com"
}
cred = credentials.Certificate(firebase_service_account)
firebase_admin.initialize_app(cred)
db = firestore.client()

def generate_start_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Open Orblix App", web_app=WebAppInfo(url="https://orblix.netlify.app/")))
    return keyboard

@bot.message_handler(commands=['start'])
async def start(message):
    user_id = str(message.from_user.id)
    user_first_name = str(message.from_user.first_name)
    user_last_name = message.from_user.last_name
    user_username = message.from_user.username
    user_language_code = str(message.from_user.language_code)
    is_premium = message.from_user.is_premium
    text = message.text.split()
    welcome_message = (
        f"Hi, {user_first_name}!👋\n\n"
        f"Welcome to Orblix!\n\n"
        f"Here you can earn tokens by mining them!\n\n"
        f"Airdrop date coming soon!\n\n"
        f"Invite friends to earn more tokens, and level up fast!\n\n"
    )

    try:
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()
        
        if not user_doc.exists:
            user_data = {
                'firstName': user_first_name,
                'lastName': user_last_name,
                'username': user_username,
                'languageCode': user_language_code,
                'isPremium': is_premium,
                'referrals': {},
                'balance': 0,
                'mineRate': 0.001,
                'isMining': False,
                'miningStartedTime': None,
                'daily': {
                    'claimedTime': None,
                    'claimedDay': 0,
                },
                'links': None,
            }
            
            if len(text) > 1 and text[1].startswith('ref_'):
                referrer_id = text[1][4:]
                referrer_ref = db.collection('users').document(referrer_id)
                referrer_doc = referrer_ref.get()

                if referrer_doc.exists:
                    user_data['referredBy'] = referrer_id

                    referrer_data = referrer_doc.to_dict()

                    bonus_amount = 500 if is_premium else 300

                    current_balance = referrer_data.get('balance', 0)
                    new_balance = current_balance + bonus_amount

                    referrals = referrer_data.get('referrals', {})
                    if referrals is None:
                        referrals = {}
                    referrals[user_id] = {
                        'addedValue': bonus_amount,
                        'firstName': user_first_name,
                        'lastName': user_last_name,
                    }

                    referrer_ref.update({
                        'balance': new_balance,
                        'referrals': referrals
                    })
                else:
                    user_data['referredBy'] = None
            else:
                user_data['referredBy'] = None
            
            user_ref.set(user_data)
        
        keyboard = generate_start_keyboard()
        await bot.reply_to(message, welcome_message, reply_markup=keyboard)
    except Exception as e:
        error_message = "Error. Please try again!"
        await bot.reply_to(message, error_message)
        print(f"Error: {str(e)}")

@app.post('/')
async def process_update(request: Request):
    update_dict = await request.json()
    update = types.Update.de_json(update_dict)
    asyncio.create_task(bot.process_new_updates([update]))
    return {'status': 'ok'}

@app.get('/')
async def root():
    return {"message": "Bot is running"}
