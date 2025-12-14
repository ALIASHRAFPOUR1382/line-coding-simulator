# Telegram Bot for Tizhooshan Channel Management

A comprehensive Telegram bot for managing and interacting with users in a channel focused on Tizhooshan exam preparation. The bot provides user segmentation, welcome flow, weekly quiz system, and admin panel functionality.

## Features

- **Auto Welcome**: Personalized welcome messages for new channel members
- **User Segmentation**: Categorize users (6th grade student, 9th grade student, parents, teachers) via inline keyboard
- **Instant Gift Delivery**: Automatic gift link delivery after category selection
- **Weekly Quiz System**: Interactive quiz system with scoring and leaderboard
- **Winner Announcement**: Automatic announcement of top 3 quiz winners
- **Admin Panel**: Commands for quiz management and broadcast messaging

## Requirements

- Python 3.8+
- Telegram Bot Token (from @BotFather)
- Admin Telegram User IDs

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd robat
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:

Create a `.env` file in the project root with the following variables:
```
BOT_TOKEN=your_bot_token_here
ADMIN_IDS=123456789,987654321
CHANNEL_ID=@your_channel_username
WELCOME_GIFT_LINK=https://example.com/welcome-gift.pdf
DATABASE_PATH=bot.db
```

Configuration details:
- `BOT_TOKEN`: Your Telegram bot token from @BotFather
- `ADMIN_IDS`: Comma-separated list of admin Telegram user IDs
- `CHANNEL_ID`: Your channel username (with @) or numeric ID
- `WELCOME_GIFT_LINK`: URL for welcome gift PDF/download
- `DATABASE_PATH`: Path to SQLite database file (default: `bot.db`)

4. Initialize the database:
```bash
python -m bot.database.migrations
```

5. (Optional) Add sample quiz questions:
```bash
python scripts/add_sample_questions.py
```

6. Run the bot:
```bash
python -m bot.main
```

## Admin Commands

All admin commands must be sent in private chat with the bot:

- `/startquiz` - Start a new weekly quiz session and post announcement in channel
- `/endquiz` - End current quiz session and announce top 3 winners in channel
- `/broadcast <message>` - Send a message to all registered users
- `/adminhelp` - Show admin help message

## Project Structure

```
robat/
├── bot/
│   ├── main.py                 # Bot entry point
│   ├── config.py               # Configuration management
│   ├── database/               # Database models and operations
│   ├── handlers/               # Message and callback handlers
│   ├── keyboards/              # Inline and reply keyboards
│   ├── services/               # Business logic services
│   └── utils/                  # Utility functions and templates
├── .env.example                # Environment variables template
├── requirements.txt
└── README.md
```

## Database Schema

The bot uses SQLite database with the following tables:
- `users` - User information and categories
- `quiz_results` - Quiz scores and results
- `quiz_questions` - Quiz questions and answers
- `quiz_sessions` - Active quiz sessions
- `user_quiz_answers` - Individual user answers

## Features Overview

### User Onboarding
- Automatic welcome message when users join the channel
- Category selection (6th grade student, 9th grade student, parents, teachers)
- Instant gift delivery after category selection

### Quiz System
- Weekly quiz sessions managed by admins
- Interactive quiz with inline keyboard answers
- Automatic score calculation
- Top 3 winners announcement

### Admin Features
- Quiz session management
- Broadcast messaging to all users
- Admin-only command access

## License

This project is proprietary software.

