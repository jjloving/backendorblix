from fastapi import FastAPI
from http.server import BaseHTTPRequestHandler
import os
import json
import asyncio
import requests
import datetime
from telebot.async_telebot import AsyncTeleBot
import firebase_admin
from firebase_admin import credentials, firebase, storage
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo


app = FastAPI()

@app.get("/")


#Initializw the bot
BOT_TOKEN = os.environ.get('8113117364:AAEBZZZQrXK2RfmvrKcNfntkvIsgnt-OrTw')
bot - AsyncTeleBot(BOT_TOKEN)

# firebase

firebase_config =json.loads(os.environ.get({"type": "service_account","project_id": "orblix-15f00","private_key_id": "bea8674faeeaf44749c4e5dfc69d10847ad72d31","private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDyrIZIyPG7DFP+\n7b1RTHnvfk3/0Ne9tyf578kawOJ+SJ6cMOYuqEZBebsu/6xQ4TBxwdRV/MPOvRp6\nm3JBzfKHLKr9E9yzCKyp0x61EEq6+m+W0M9MlUch/jqOzWWTAIs6f8JREUvX1B4s\neFW+gSgC/0Wkkr9+bi8EhVG/2nTWbqgNMrW75KeEDmktRnMaVpKc4tnqhVHZZROD\nkdgztyO4hevcdPy1AwNob8MCPiGU+Ao5FQNMzrKzAwp1kRSfB0TJOzRmCKWovUDQ\n/D5mcuWX5phqHzU7ZN+qGU8CRz0DQym4GJtotcBD6tp279tpIGvr5WBvKJHcSZ51\npsf8Og6nAgMBAAECggEAC4V8ZKVBsM8/h6ly5RK78U5uVphsPcId4ERtqFsDBdrd\nyO2baBiuKTql0+/olvhyC9yXf7Od+klJIgwSSySDgL5yqcxRHKDrTa7L1O3elm0A\nckkcpnap52fCEPiYe3e5pH/fUmj/UFJuUk8uRvqr0ySagltDQzXo/o5z2Kd/B5Um\nss9Btna416lXFSWDmQ8bKhBfk0rWuA+UtESfkPBhsu72ZZt++ACNsEFcOVaxmXly\nlpv26qPhIpGHXulbj9gSAIr+4abZuhOmMkrhrzDWSvJ2Om1jRIK5sN1ZnLYGiy72\ns3KBzhgClEuI+LAPfvGs/RFBXzmZPFTYJMfUsQ0zCQKBgQD9H7OzX99I5vuxCc/h\nfr+SoM5osZKkZOvtW6BbJvvYgF6KAURyV7vQvbOZ5w3uxK0bkQyA0PEAn4phTt88\nFixMN207OGLPHsrgHJVNQMmTG/AQyW4irsQ2M5Tm+GbnFXrTSRB0judXD+RIBAh0\nEm5sJ074tEUMVBxqPtF6mSyEbwKBgQD1bmzoIvfkcbLuPFfxNLAI0Le01tdxhoyV\n23uE5uOjeZc1YW5ILIcxSLMnMo+vKLwjWV+jI3pTTI6Xlxr0c1RXAy4o2ESZNWC6\nTrQJNOv3dtdKtj0BxgPpIwEYwtx9KDKQkZIGTXWppBNNhlwDlE40XPEJXJqBYf6D\nw6ZTR3/lSQKBgQCmNtoO0MbTnXHrSDEstslfpJ7F2s0bjHXsMD21fXzlJy5tWvWy\nS/A120wDpNjeUGIH9xCJyipnqVv6GAu47ip6he8Bcz5XGbZIwhw8VW3IXxEeRNdA\niRipKuf9X2JbHhzAf3sBvxEkd3gE3jka1zuRY6KU5/NrbBQYpFV0Nv8nmwKBgD/m\nUzaRPCdfLu32ChOD2z1AUkQkF424MUwnC97LWoNKegLs7hCef0hmnDZdZKl/GpS9\nhTftWcDsUsfHEL6KdG//JPp/bETTb+6x5Q/slm8kouMR1YprqsL9WSDAQzXWzGt1\nayZ27maPkHMDw1svNrlNZXhBgvyirehSfTB7kiH5AoGBAPoQ45r8A9Kzk2CBk8hu\nLYp9BKJd8CS2AFlXnyVtuNtqBHwrLFGGdmDsB+ojABeqcTw48BpmBPHcoOL+naCs\nu5TCrY+3lp0caQWuLV1agYr4BrcRrSS3MWNSHfxb8oSLAJOe4XYdS2ScmqYksL3c\n2NktC0qPOu4LoaqrpUWZbZfk\n-----END PRIVATE KEY-----\n","client_email": "firebase-adminsdk-il80v@orblix-15f00.iam.gserviceaccount.com","client_id": "102518934139618313626","auth_uri": "https://accounts.google.com/o/oauth2/auth","token_uri": "https://oauth2.googleapis.com/token","auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-il80v%40orblix-15f00.iam.gserviceaccount.com","universe_domain": "googleapis.com"}
))
cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred, {'storageBucket': 'orblix-15f00.appspot.com'})
db = firestore.client()
bucket = storage.bucket()


def generate_start_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Open Orblix App", web_app=WebAppInfo(url="https://orblix.netlify.app/")))
    return keyboard

@bot.message_handler(commands=['start'])
async def start(message):
    user_id = str(message.from_user.id)
    user_first_name = str(message.from_user.first_name)
    user_last_name = message.from_user.last_name
    user_username = message.from_user.user_name
    user_language_code = str(message.from_user.language_code)
    is_premium = message.from_user.is_premium
    text = message.text.split()
    welcome_message =(
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
            photos = await bot.get_user_profile_photos(user_id, limit=1)
            if photos.total_count > 0:
                file_id = photos.photos[0][-1].file_id
                file_info = await bot.get_file(file_id)
                file_path = file_info.file_path
                file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

                # Download the image
                response = requests.get(file_url)
                if response.status_code == 200:
                    # Upload to Firebase Storage
                    blob = bucket.blob(f"user_images/{user_id}.jpg")
                    blob.upload_from_string(response.content, content_type='image/jpeg')

                    # Generate the correct URL
                    user_image = blob.generate_signed_url(datetime.timedelta(days=365), method='GET')
                else:
                    user_image = None
            else:
                user_image = None

            user_data = {
                'userImage': user_image,
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
                        'userImage': user_image,
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


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        update_dict = json.loads(post_data.decode('utf-8'))

        asyncio.run(self.process_update(update_dict))

        self.send_response(200)
        self.end_headers()

    async def process_update(self, update_dict):
        update = types.Update.de_json(update_dict)
        await bot.process_new_updates([update])

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write("Bot is running".encode())
