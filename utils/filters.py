from telegram.ext.filters import MessageFilter

class Admin_convo_filter(MessageFilter):

    def __init__(self, name: str | None = None, data_filter: bool = False, chat_data=None):
        """
        Initialize the Admin_convo_filter class.

        Args:
        name (str | None): The name of the filter. Defaults to None.
        data_filter (bool): Whether the filter should be applied to the chat data. Defaults to False.
        chat_data (dict): The chat data to be used in the filter. Defaults to None.
        """
        super().__init__(name, data_filter)
        self.chat_data: dict = chat_data # Hint type dict but the variable is a Mapping Class type

    def filter(self, message):
        """
        Checks if the status in the chat_data is not None.
        
        Args:
        message: The message object that triggered this filter.
        
        Returns:
        bool: True if the status is not None, False otherwise.
        """
        chat_data: dict = self.chat_data.get(message.chat_id) #access dict with .get(chatid)
        if chat_data.get('status', None) is not None:
            return True
        
        
        

