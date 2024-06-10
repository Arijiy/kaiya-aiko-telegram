# Aiko: Your AI Companion 🤖💬
Aiko is a friendly AI companion bot designed to provide companionship and support, especially for introverts. This bot is developed using Python, Telegram Bot API, and Google Gemini API for generating responses.

![Alt text](https://i.postimg.cc/XNm9PP9C/img-LBFr-Zk1-Nesh-Sc-Vi-J53-Ox-V.jpg)

## Features 🌟
- **Unlimited Messaging for Specific User**: The user with the username `@itsarijit_01` can send unlimited messages.
- **Message Limits**: Other users have a message limit of 20 messages every 5 hours.
- **Picture Sharing**: Aiko can share pictures after a conversation threshold.
- **Random Dialogues**: Aiko sends random dialogues along with pictures.

**You can test Aiko here: [CLICK HERE](https://t.me/aiko_kaiya_BOT)**

## Prerequisites 🛠️
- Python 3.7+
- Telegram Bot Token
- Google Gemini API Key

## Installation 💻
1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/aiko-bot.git
    cd aiko-bot
    ```
2. **Create a virtual environment and activate it**:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```   
3. **Set up environment variables**:
    Create a `.env` file in the root directory and add your API keys:
    ```env
    GEMINI_API_KEY=your_google_gemini_api_key
    TELEGRAM_BOT_API_KEY=your_telegram_bot_token
    ```
4. **Install the requirements packages**:
   - Install telegram 13 package
   ```pip install python-telegram-bot==13.14```
   - Install Google GenerativeAI package
   ```pip install google-generativeai```

## Usage 🚀
1. **Run the bot**:
    ```sh
    python bot.py
    ```
2. **Interact with the bot on Telegram**:
    - Use the `/start` command to initiate a conversation.
    - Send messages and interact with Aiko.
  
## Host The Bot 📡
1. Visit [PythonAnywhere](https://www.pythonanywhere.com/)
2. Create a account or sign-in to your account.
3. In your dashboard, go to ***files***.
4. There will be 7 files already from **pythonanywhere**, just write the name of your file ***main.py***, and click on the **NEW FILE** button.
5. The editor will open, paste the python code there, and click on ***OPEN DASH CONSOLE***, to open the terminal.
6. Install the [requires packages](##installation), through the terminal.
7. Click on the run button.
8. If you console shows, "**INFO_SHEDULER, STARTED**", well congrats your bot is now live or else there is an error while seting up your bot.

***PythonAnywhere is a free source for host you bot for test, for like a small community or members. If you have a large community, free is not for you cause your bot may become slow, so I will recommend buying one of there [tiers](https://www.pythonanywhere.com/user/synthwavestudios/account/).***
    
## Code Overview 📂
- **bot.py**: Main file containing the bot logic and handlers.
- **keep_alive.py**: Script to keep the bot running.

## Handlers 🛠️
- **start**: Greets the user and starts the conversation.
- **handle_message**: Handles user messages and checks for picture requests and message limits.

## Error Handling ⚠️
Logs errors and warnings for debugging purposes.

## License 📜
This project is licensed under the MIT License.

## Acknowledgements 🙏
- Developed by [Arijit (lonewolf)](https://github.com/Arijiy)
- Uses [Google Gemini API](https://cloud.google.com/gemini)
- Built with [Python Telegram Bot](https://python-telegram-bot.org)
