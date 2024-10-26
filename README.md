# TELEGRAM BOT - Your Personal Flight Bot: Find the Cheapest Flights and Never Miss a Deal!

_This Telegram bot allows users to conveniently find the cheapest flights and receive price alerts for their desired routes._

Try out the [Flight Spotter Bot](https://t.me/FlightSpotter_Bot) on Telegram. 

## Table of Contents

- [About](#about)
- [Features](#features)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [License](#license)


## About

We all love finding cheap flights, but it can often feel like a challenge. That’s where this Telegram Bot comes in!

Powered by the Kiwi flight API, this bot makes it easy to search for the best deals on flights for your chosen routes and dates. Once you find a flight, you can even save it for price tracking. The bot will notify you if the price drops, so you’ll never miss out on a great deal!

## Features

- Live Flight Search (Oneway,Return and Multi-City Flight Search).
- Support for User input validation.
- Flight Tracking.
- KIWI API Support.
- Inline And Keyboard Markup support.
- Admin Panel.
- Price Alerts.

### Bot Commands

- `/start` - Initializes Bot welcome response.
- `/flight_alerts` - Show all saved flight alerts.
- `/menu` - Navigate to Main Menu.
- `/reset` - Reset the flight search.
- `/help` - Show Help.
- `/admin` - Navigate to Admin Dashboard.

## Getting Started

1. Get your Telegram Bot token from [@BotFather](https://t.me/BotFather).

2. Create an account on [KIWI](https://partners.kiwi.com/) and get your flight search API KEY.

3. Configuration : edit the configuration by renaming the `.env.example file` and renaming it to `.env`, then edit the required env variables.

   | Env Variable      | Description                                              | Defaults               |
   | ----------------- | -------------------------------------------------------- | ---------------------- |
   | `BOT_TOKEN`       | Your Telegram Bot Token                                  | None                   |
   | `KIWI_API_KEY_STD`| Your KIWI API key for Oneway and Return flight search    | None                   |
   | `KIWI_API_KEY_MULTICITY `| Your KIWI API key for Multicity flight search      | None                   |
   | `DATABASE_PATH`   | Your database file path                                  | `database\database.db` |
   | `ADMINISTRATOR`   | Holds a list of telegram chat id's for admin rights      | [Integer]                     |


### Database

This bot is compatible only with a SQL database file. If you have an existing database from prior use, make sure to update the file path in your .env file. The default path is database/database.db, which will be automatically created upon the first call to the database instance.

## Installation

### From Source

1. Create a virtual environment:

```shell
python -m venv venv
```

2. Activate the virtual environment:

```shell
# For Linux or macOS:
source venv/bin/activate

# For Windows:
venv\Scripts\activate
```

3. Install the dependencies using `requirements.txt` file:

```shell
pip install -r requirements.txt
```

4. Use the following command to start the bot:

```shell
python bot.py
```

### Manual Docker Build

1. Build Docker Image with Environment Variables:

   _Replace your-image-name:your-tag with your desired image and tag._

   ```shell
   docker build --build-arg ENV_FILE=.env -t your-image-name:your-tag
   ```

2. Run Docker Container
   ```shell
   docker run -d -p 8080:80 --env-file .env your-image-name:your-tag
   ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
