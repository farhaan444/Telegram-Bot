from telegram.ext.filters import MessageFilter

class Admin_convo_filter(MessageFilter):

    def __init__(self, name: str | None = None, data_filter: bool = False, chat_data=None):
        super().__init__(name, data_filter)
        self.chat_data: dict = chat_data # Hint type dict but the variable is a Mapping Class type

    def filter(self, message):
        chat_data: dict = self.chat_data.get(message.chat_id) #access dict with .get(chatid)
        if chat_data.get('status', None) is not None:
            return True
        
        
        

