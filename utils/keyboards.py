from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

# INLINE KEYBOARDS
# IMPORTANT
# ONE OF THE OPTIONAL PARAMETERS HAS TO BE SET!
# URL PARRAMTER AND CALLBACK_DATA CANNOT BOTH BE SET!
# IF URL IS NOT SET, CALLBACK_DATA PARRAM HAS TO BE SET! I.E IT CANNOT BE SET TO NONE!

# Start menu
main_menu = [[InlineKeyboardButton(
    '🔎 Flight Search', callback_data='start_flight_search'), InlineKeyboardButton('🔔 Flight Alerts', callback_data='get_flight_alerts')]]
main_menu = InlineKeyboardMarkup(main_menu)

# flght route menu
# One way, Return or multicity
flight_type_menu = [[InlineKeyboardButton(
    '➡️ One Way', callback_data='oneway'), InlineKeyboardButton('↩️ Return', callback_data='return')], [InlineKeyboardButton('🔄️ Multi-City', callback_data='multi-city')]]
flight_type_menu = InlineKeyboardMarkup(flight_type_menu)

# Single Button - Redidirect to start Main Menu
main_menu_redirect = [[InlineKeyboardButton(
    '≡ Menu', callback_data='main_menu')]]
main_menu_redirect = InlineKeyboardMarkup(main_menu_redirect)

# Multi-City Menu
multicity_menu = [[InlineKeyboardButton(
    '➕ Add Flight', callback_data='add_flight'), InlineKeyboardButton('🔎 Get Result', callback_data='multicity_result')]]
multicity_menu = InlineKeyboardMarkup(multicity_menu)


def delete_all_menu(success=False):
    """This function takes one argument: Success:Bool
    The function will create a inline keyboard with two buttons
    if True button1 = all flights deleted else button1 == Delete all flights.
    button2 = Menu button redirect to main menu"""
    if success:
        menu = [[InlineKeyboardButton('✅ All flight alerts deleted', callback_data='#')], [
            InlineKeyboardButton('≡ Menu', callback_data='main_menu')]]
        menu = InlineKeyboardMarkup(menu)
        return menu
    else:
        menu = [[InlineKeyboardButton('❌ Delete all Flight Alerts', callback_data='del_all_FA')], [
            InlineKeyboardButton('≡ Menu', callback_data='main_menu')]]
        menu = InlineKeyboardMarkup(menu)
        return menu


def single_button(text: str, callback_data: str, url=None):
    """This function takes two arguments, text, callback_data and url.
    This is used to build a single button inline keyboard button.
    callback_data and url both cannot be none"""
    if url != None:
        callback_data = None
    menu = [[InlineKeyboardButton(text, callback_data=callback_data)]]
    menu = InlineKeyboardMarkup(menu)
    return menu


def flight_result_menu(link, tracked=False, err=False):
    """This function takes a url arg and constructs a inline keyboard button that when clicked will open externaly.
    It will also add a tracking button. Callback_data = None for the link button
    tracked arg set to true to replace track Price to Flight tracked -- Default False"""

    if tracked:
        row1 = [InlineKeyboardButton(
            '✈️ Book Your Flight ✈️', url=link, callback_data=None)]
        row2 = [InlineKeyboardButton(
            '✅ Flight tracking created', callback_data='#')]
        row3 = [InlineKeyboardButton('🔎 New Flight Search', callback_data='start_flight_search'),
                InlineKeyboardButton('≡ Menu', callback_data="main_menu")]
        button = [row1, row2, row3]
        menu = InlineKeyboardMarkup(button)
        return menu
    elif err:
        link = None
        row1 = [InlineKeyboardButton(
            '✈️ Book Your Flight ✈️', url=link, callback_data='#')]
        row2 = [InlineKeyboardButton(
            '❌ Error! Flight Search Expired', callback_data='#')]
        row3 = [InlineKeyboardButton('🔎 New Flight Search', callback_data='start_flight_search'),
                InlineKeyboardButton('≡ Menu', callback_data="main_menu")]
        button = [row1, row2, row3]
        menu = InlineKeyboardMarkup(button)
        return menu
    else:
        row1 = [InlineKeyboardButton(
            '✈️ Book Your Flight ✈️', url=link, callback_data=None)]
        row2 = [InlineKeyboardButton(
            '🔔 Track Price', callback_data='track_flight')]
        row3 = [InlineKeyboardButton('🔎 New Flight Search', callback_data='start_flight_search'),
                InlineKeyboardButton('≡ Menu', callback_data="main_menu")]
        button = [row1, row2, row3]
        menu = InlineKeyboardMarkup(button)
        return menu


def flight_alert_menu(link):
    """This function builds an inline keyboard
    The function takes one argument: a url link must be parsed through
    Two buttons are created, butt1= book flight, butt2= main menu redirect to main menu"""
    menu = [[InlineKeyboardButton('✈️ Book Your Flight ✈️', url=link, callback_data=None)], [
        InlineKeyboardButton('≡ Menu', callback_data="main_menu")]]
    menu = InlineKeyboardMarkup(menu)
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
