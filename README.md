# TELEGRAM BOT - Your Personal Flight Bot: Find the Cheapest Flights and Never Miss a Deal!

_This Telegram bot allows users to conveniently find the cheapest flights and receive price alerts for their desired routes._

## Table of Contents

- [About](#about)
- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## About

We all want the cheapest possible flight but getting cheap flights is no easy task.

This Telegram Bot uses Kiwi flight api to search flights and return the current cheapest flight for your desired routes and dates.

You can also save the flight result for the bot to track the flight price and the bot will notify you if the flight price has dropped.

## Features

- Live Flight Search (Oneway & Return Flight Search).
- Support for User input validation.
- Flight Tracking.
- KIWI API Support.
- Inline And Keyboard Markup support.

### Bot Commands

- `/start` - Initializes Bot welcome response.
- `/flight_alerts` - Show all saved flight alerts.
- `/reset` - Reset the flight search.

## Getting Started

1. Get your Telegram Bot token from [@BotFather](https://t.me/BotFather).

2. Create an account on [KIWI](https://partners.kiwi.com/) and get your flight search API KEY.

3. Configuration : edit the configuration by renaming the `.env.example file` and renaming it to `.env`, then edit the required env variables.

   | Env Variable      | Description                                              | Defaults               |
   | ----------------- | -------------------------------------------------------- | ---------------------- |
   | `BOT_USERNAME`    | Your Telegram Bot Username                               | None                   |
   | `BOT_TOKEN`       | Your Telegram Bot Token                                  | None                   |
   | `KIWI_API_KEY`    | Your KIWI API key                                        | None                   |
   | `DATABASE_PATH`   | Your database file path                                  | `database\database.db` |
   | `ADMINISTRATOR`   | Holds a list of telegram chat id's for admin rights      | []                     |
   | `FIRST_RUN_FS`    | Flight Search Job Schedule first run                     | `10800`                |
   | `JOB_INTERVAL_FS` | Flight search job schedule intervals                     | `10800`                |
   | `FT_LIMIT`        | Set limit on flight alerts - 0 = Unlimited Flight alerts | `0`                    |

### Database

This bot only supports a SQL database file. If you have an existing database file from previous use than edit your file path in your .env file.
The default path is database\database.db which will be created automatically on the first call on the DB instance.

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
