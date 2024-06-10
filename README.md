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
3. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```
4. **Set up environment variables**:
    Create a `.env` file in the root directory and add your API keys:
    ```env
    GEMINI_API_KEY=your_google_gemini_api_key
    TELEGRAM_BOT_API_KEY=your_telegram_bot_token
    ```

## Usage 🚀
1. **Run the bot**:
    ```sh
    python bot.py
    ```
2. **Interact with the bot on Telegram**:
    - Use the `/start` command to initiate a conversation.
    - Send messages and interact with Aiko.
    
## Code Overview 📂
- **bot.py**: Main file containing the bot logic and handlers.
- **keep_alive.py**: Script to keep the bot running.
- **requirements.txt**: List of required Python packages.

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
