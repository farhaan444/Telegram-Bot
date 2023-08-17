from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

# INLINE KEYBOARDS

# Start menu
main_menu = [[InlineKeyboardButton(
    '🔎 Flight Search', callback_data='start_flight_search'), InlineKeyboardButton('🔔 Flight Alerts', callback_data='#')]]
main_menu = InlineKeyboardMarkup(main_menu)

# flght route menu
# One way or Return (no support for multicity)
direction_type = [[InlineKeyboardButton(
    '➡️ One Way', callback_data='oneway'), InlineKeyboardButton('↩️ Return', callback_data='return')]]
direction_type = InlineKeyboardMarkup(direction_type)


def flight_result_menu(link):
    """This function takes a url arg and constructs a inline keyboard button that when clicked will open externaly.
    It will also add a tracking button. Callback_data = None for the link button"""
    button = [[InlineKeyboardButton(
        '✈️ Book Your Flight ✈️', url=link, callback_data=None)], [InlineKeyboardButton('≡ Menu', callback_data="main_menu")]]
    menu = InlineKeyboardMarkup(button)
    return menu


# REPLY KEYBOARDS


def airport_menu(airports: list):
    """This function builds a reply keyboard for available airports"""
    buttons = []
    for i in range(len(airports)):
        buttons.append([KeyboardButton(airports[i])])
    menu = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
    return menu


def adults_menu():
    """This function will build and return a reply keyboard for possible number of adults to travel."""
    adults = ['1', '2', '3', '4']
    buttons = []
    for i in range(len(adults)):
        buttons.append([KeyboardButton(adults[i])])
    menu = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
    return menu
