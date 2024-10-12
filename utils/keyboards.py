# INLINE KEYBOARDS 
# IMPORTANT
# ONE OF THE OPTIONAL PARAMETERS HAS TO BE SET!
# URL PARRAMTER AND CALLBACK_DATA CANNOT BOTH BE SET!
# IF URL IS NOT SET, CALLBACK_DATA PARRAM HAS TO BE SET! I.E IT CANNOT BE SET TO NONE!

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

# Inline Keyboards

# Start menu
main_menu = [[InlineKeyboardButton(
    '🔎 Flight Search', callback_data='start_flight_search'), InlineKeyboardButton('🔔 Flight Alerts', callback_data='get_flight_alerts')], [InlineKeyboardButton('🆘 Help', callback_data='help')]]
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

# verify/confirm delete all flight alert menu
verify_del_menu = [[InlineKeyboardButton('Yes', callback_data='del_all_FA')], [InlineKeyboardButton('No', callback_data='no_del')]]
verify_del_menu = InlineKeyboardMarkup(verify_del_menu)

# Admin Menu
admin_menu = [[InlineKeyboardButton("Set Run Interval", callback_data='admin-FTjob-set')],[InlineKeyboardButton('Set Flight Alert Limit', callback_data='admin-FTlimit-set')]]
admin_menu = InlineKeyboardMarkup(admin_menu)

def delete_all_menu(success=False):
    """
    Generates a InlineKeyboardMarkup for the delete all flight alert menu.

    Parameters
    ----------
    success : bool, optional
        Whether the deletion was successful or not. Defaults to False.

    Returns
    -------
    InlineKeyboardMarkup
        The delete all flight alert InlineKeyboardMarkup.
    """
    if success:
        menu = [[InlineKeyboardButton('✅ All flight alerts deleted', callback_data='#')], [
            InlineKeyboardButton('≡ Menu', callback_data='main_menu')]]
        menu = InlineKeyboardMarkup(menu)
        return menu
    else:
        menu = [[InlineKeyboardButton('❌ Delete all Flight Alerts', callback_data='verify_del')], [
            InlineKeyboardButton('≡ Menu', callback_data='main_menu')]]
        menu = InlineKeyboardMarkup(menu)
        return menu

def single_button(text: str, callback_data: str, url=None):
    """
    Generates a InlineKeyboardMarkup for a single button.

    Parameters
    ----------
    text : str
        The text on the button.
    callback_data : str
        The callback data for the button.
    url : str, optional
        The url to open when button is clicked. 
        If set, callback_data will be set to None. Defaults to None.

    Returns
    -------
    InlineKeyboardMarkup
        The single button InlineKeyboardMarkup.
    """
    if url != None:
        callback_data = None
    menu = [[InlineKeyboardButton(text, callback_data=callback_data)]]
    menu = InlineKeyboardMarkup(menu)
    return menu

def flight_result_menu(link, tracked=False, err=False):
    """
    Generates a InlineKeyboardMarkup for a flight result.

    Parameters
    ----------
    link : str
        The link to the flight result.
    tracked : bool, optional
        Whether the flight is being tracked. Defaults to False.
    err : bool, optional
        Whether there was an error with the flight search. Defaults to False.

    Returns
    -------
    InlineKeyboardMarkup
        The InlineKeyboardMarkup for the flight result.
    """
    if tracked:
        row1 = [InlineKeyboardButton(
            '✈️ Book Your Flight ✈️', url=link, callback_data=None)]
        row2 = [InlineKeyboardButton(
            '✅ Flight tracking activated', callback_data='#')]
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
    """
    Generates a InlineKeyboardMarkup for a flight alert.

    Parameters
    ----------
    link : str
        The link to the flight result.

    Returns
    -------
    InlineKeyboardMarkup
        The InlineKeyboardMarkup for the flight alert.
    """
    menu = [[InlineKeyboardButton('✈️ Book Your Flight ✈️', url=link, callback_data=None)], [
        InlineKeyboardButton('≡ Menu', callback_data="main_menu")]]
    menu = InlineKeyboardMarkup(menu)
    return menu

# REPLY KEYBOARDS

def airport_menu(airports: list):
    """
    Generates a ReplyKeyboardMarkup for a list of airports.

    Parameters
    ----------
    airports : list
        A list of airport names or codes.

    Returns
    -------
    ReplyKeyboardMarkup
        The ReplyKeyboardMarkup for the list of airports.
    """
    buttons = []
    for i in range(len(airports)):
        buttons.append([KeyboardButton(airports[i])])
    menu = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
    return menu

def adults_menu():
    """
    Generates a ReplyKeyboardMarkup for a list of adult numbers.

    Returns
    -------
    ReplyKeyboardMarkup
        The ReplyKeyboardMarkup for the list of adult numbers.
    """
    adults = ['1', '2', '3', '4']
    buttons = []
    for i in range(len(adults)):
        buttons.append([KeyboardButton(adults[i])])
    menu = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
    return menu

