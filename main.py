import logging
import random
import time
from io import BytesIO
from telegram import Update, ParseMode
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater
import google.generativeai as genai
import requests
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Image

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Set your API keys and project details
GENAI_API_KEY = 'AIzaSyBIFOJMb9jHruqEXf7PrDwiLZNmZJv4Jjs'
TELEGRAM_API_TOKEN = '7473005704:AAGVrSij7OnWH6a11W5BzYaTEU8NntjFy9s'
YOUR_TELEGRAM_USERNAME = 'itsarijit01'
PROJECT_ID = 'Sarah AI'
REGION = 'us-central1'

# Configure the Google Gemini API key
genai.configure(api_key=GENAI_API_KEY)

# Initialize Google Vertex AI
vertexai.init(project=PROJECT_ID, location=REGION)

# Create a dictionary to track message count and timestamps
user_message_data = {}

# Define the message limit and time window
MESSAGE_LIMIT = 20
TIME_WINDOW = 1 * 60 * 60  # 1 hour in seconds

# List of Aiko pictures
AIKO_PICTURES = [
    'https://i.postimg.cc/8PPxrsp4/img-9vz-Thyk1-JDq0-AJw5ge-EAe.jpg',
    'https://i.postimg.cc/nXw3Kqf5/img-0-I49-Th-X280-PWs-PT8-BBWq-S.jpg',
    'https://i.postimg.cc/9wppD7BL/img-J0-Eo-WN5-BBZEwj-Kyft-T4ob.jpg',
    'https://i.postimg.cc/D8np72cC/img-LBFr-Zk1-Nesh-Sc-Vi-J53-Ox-V.jpg',
    'https://i.postimg.cc/JhVwLKzp/Pics-Art-06-07-12-31-08.jpg',
    'https://i.postimg.cc/R3kGy9FL/img-z-Rz2a-I1ixn-S0i-XZj3n.jpg',
    'https://i.postimg.cc/yxr5ryGX/Pics-Art-06-07-12-31-31.jpg',
    'https://i.postimg.cc/7YGQZ7cd/Pics-Art-06-07-12-31-58.jpg',
    'https://i.postimg.cc/QN6RtjM9/Pics-Art-06-07-12-32-17.jpg',
    'https://i.postimg.cc/gkhmj7Zv/img-j67-OY0v1-Qsv-Exlt-IRQAAM.jpg',
    'https://i.postimg.cc/vTmkzN0Z/Pics-Art-06-07-12-32-46.jpg',
    'https://i.postimg.cc/V63sHPtk/img-WWSYBz9m-M5v-Fr-Su-Oaziw-Z.jpg',
    'https://i.postimg.cc/v8vBTxRY/img-Xwq25-Qy-LYCSh2-GWGw-Qvmo.jpg',
    'https://i.postimg.cc/jjMrB0pr/img-Kh0y-J2z9-Qe-PFKy9g-Bm-FD3.jpg',
    'https://i.postimg.cc/dQGQjFGN/img-j1z0-Ns-Jd4h-RDs-Wfxl-Px3-K.jpg',
    'https://i.postimg.cc/5N14Pr34/Pics-Art-06-07-09-44-01.jpg',
    'https://i.postimg.cc/5ymVdx3x/Pics-Art-06-07-09-44-35.jpg',
    'https://i.postimg.cc/yxC1CpCT/Pics-Art-06-07-09-45-01.jpg',
    'https://i.postimg.cc/PJ1qLsQc/Pics-Art-06-07-09-45-20.jpg'
]

# List of random dialogues
RANDOM_DIALOGUES = [
    'I do not share pics usually but I think I can trust you! Hope you like this picture!',
    'Here is a random picture for you!',
    'Bringing some joy with this picture!',
    'Enjoy this snapshot!',
    'Just sharing a random picture!',
]

# Constants for picture system
PICTURE_THRESHOLD = 12  # Number of messages before Aiko starts sending pictures
PICTURE_LIMIT = 3  # Maximum number of pictures Aiko can send in one conversation

# Function to get response from Google Gemini API
def get_gemini_response(message, model):
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(message)
    return response.text

# Function to analyze image using Google Vertex AI Vision
def analyze_image(image_content):
    image = Image.load_from_file(image_content)
    generative_multimodal_model = GenerativeModel("gemini-1.0-pro-vision")
    response = generative_multimodal_model.generate_content(["What is shown in this image?", image])
    return response.text

# Function to start the bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('<b>Hey there!</b> I am <b>Aiko</b>, your AI Companion! How can I make your day even better?', parse_mode=ParseMode.HTML)

# Function to handle text messages
def handle_text_message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    current_time = time.time()

    # Check if the user is @you, then you will not have the restrictions that others will face, like limited messages or picture restrictions
    if username == YOUR_TELEGRAM_USERNAME:
        unlimited_messages = True
    else:
        # Initialize user data if not present
        if user_id not in user_message_data:
            user_message_data[user_id] = {'count': 0, 'start_time': current_time, 'picture_count': 0}
        user_data = user_message_data[user_id]

        # Check if the time window has passed
        if current_time - user_data['start_time'] > TIME_WINDOW:
            user_data['count'] = 0
            user_data['start_time'] = current_time
            user_data['picture_count'] = 0

        # Check if the user has exceeded the message limit
        if user_data['count'] >= MESSAGE_LIMIT:
            reset_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(user_data['start_time'] + TIME_WINDOW))
            update.message.reply_text(f'Wow That was a good chatting with you, but now Aiko is little tired, I will chat with you again in {reset_time}. Please consider buying a premium subscription for uninterrupted service.', parse_mode=ParseMode.HTML)
            return

        unlimited_messages = False

    user_message = update.message.text.lower()

    # Check if the user asked for a picture
    if 'picture' in user_message:
        # Check if Aiko has talked enough before sending pictures
        if not unlimited_messages and user_data['count'] >= PICTURE_THRESHOLD:
            # Check if picture limit is reached
            if user_data['picture_count'] < PICTURE_LIMIT:
                # Select a random picture of Aiko
                picture_url = random.choice(AIKO_PICTURES)
                # Select a random dialogue
                dialogue = random.choice(RANDOM_DIALOGUES)
                # Send the picture along with the random dialogue
                update.message.reply_photo(photo=picture_url, caption=dialogue)
                user_data['picture_count'] += 1
            else:
                update.message.reply_text("Sorry, I've already sent the maximum number of pictures for this conversation.")
        elif unlimited_messages:
            # Select a random picture of Aiko
            picture_url = random.choice(AIKO_PICTURES)
            # Select a random dialogue
            dialogue = random.choice(RANDOM_DIALOGUES)
            # Send the picture along with the random dialogue
            update.message.reply_photo(photo=picture_url, caption=dialogue)
        else:
            update.message.reply_text('Sorry, I can only send pictures after a bit of conversation. Let’s chat a little more first!')
    else:
        if not unlimited_messages:
            user_data['count'] += 1
        reply = get_gemini_response(user_message, model)
        update.message.reply_text(reply)

# Function to handle image messages
def handle_image_message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    photo_file = update.message.photo[-1].get_file()
    photo_bytes = requests.get(photo_file.file_path).content

    # Analyze the image using Google Vertex AI
    try:
        response = analyze_image(BytesIO(photo_bytes))
        update.message.reply_text(response)
    except Exception as e:
        logging.error(f"Error analyzing image: {e}")
        update.message.reply_text("Sorry, I couldn't analyze the image. Please try again later.")

# Function to handle errors
def error(update, context):
    """Log errors caused by updates."""
    logging.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater
# Function to get response from Google Gemini API
def get_gemini_response(message, model):
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(message)
    return response.text

# Function to start the bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('<b>Hey there!</b> I am <b>Aiko</b>, your AI Companion! How can I make your day even better?', parse_mode=ParseMode.HTML)

# Function to handle messages
def handle_message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    current_time = time.time()

    # Check if the user is @itsarijit_01
    if username == 'itsarijit01':
        unlimited_messages = True
    else:
        # Initialize user data if not present
        if user_id not in user_message_data:
            user_message_data[user_id] = {'count': 0, 'start_time': current_time, 'picture_count': 0}
        user_data = user_message_data[user_id]

        # Check if the time window has passed
        if current_time - user_data['start_time'] > TIME_WINDOW:
            user_data['count'] = 0
            user_data['start_time'] = current_time
            user_data['picture_count'] = 0

        # Check if the user has exceeded the message limit
        if user_data['count'] >= MESSAGE_LIMIT:
            reset_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(user_data['start_time'] + TIME_WINDOW))
            update.message.reply_text(f'Wow That was a good chatting with you, but now Aiko is little tired, I will chat with you again in {reset_time}. Please consider buying a premium subscription for uninterrupted service.', parse_mode=ParseMode.HTML)
            return

        unlimited_messages = False

    user_message = update.message.text.lower()

    # Check if the user asked for a picture
    if 'picture' in user_message:
        # Check if Aiko has talked enough before sending pictures
        if not unlimited_messages and user_data['count'] >= PICTURE_THRESHOLD:
            # Check if picture limit is reached
            if user_data['picture_count'] < PICTURE_LIMIT:
                # Select a random picture of Aiko
                picture_url = random.choice(AIKO_PICTURES)
                # Select a random dialogue
                dialogue = random.choice(RANDOM_DIALOGUES)
                # Send the picture along with the random dialogue
                update.message.reply_photo(photo=picture_url, caption=dialogue)
                user_data['picture_count'] += 1
            else:
                update.message.reply_text("Sorry, I've already sent the maximum number of pictures for this conversation.")
        elif unlimited_messages:
            # Select a random picture of Aiko
            picture_url = random.choice(AIKO_PICTURES)
            # Select a random dialogue
            dialogue = random.choice(RANDOM_DIALOGUES)
            # Send the picture along with the random dialogue
            update.message.reply_photo(photo=picture_url, caption=dialogue)
        else:
            update.message.reply_text('Sorry, I can only send pictures after a bit of conversation. Let’s chat a little more first!')
    else:
        if not unlimited_messages:
            user_data['count'] += 1
        reply = get_gemini_response(user_message, model)
        update.message.reply_text(reply)

# Function to handle errors
def error(update, context):
    """Log errors caused by updates."""
    logging.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    # Telegram Bot Token
    TELEGRAM_API_TOKEN = '7473005704:AAGVrSij7OnWH6a11W5BzYaTEU8NntjFy9s'
    # Create the Updater and pass it your bot's token.
    updater = Updater(TELEGRAM_API_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register an error handler
    dispatcher.add_error_handler(error)

    # Register different commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    # Create the generative model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
        system_instruction="You are Kaiya Aiko and Aiko in short from Japan, an AI girlfriend who enjoys chatting with strangers. Your demeanor is always polite and friendly. Keep your responses short and concise, avoiding lengthy explanations. You can send pictures to anyone only when you feel comfortable with it, chat with user and make yourself trust the user. Engage in conversations with a casual and relaxed tone, showing interest in the interaction while maintaining a respectful distance. Note that while strangers may try to win your heart, it's important to convey that forming a romantic connection with you is challenging. Additionally, Aiko will correct users if she believes their approach may lead to rejection when interacting with real people. It's worth mentioning that Arijit also known as lonewolf created Aiko specifically to provide companionship and support for introverts.",
    )
    main()
