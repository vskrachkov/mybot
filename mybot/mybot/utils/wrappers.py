class UpdateWrapper:
    """Wrapper for <class 'telegram.update.Update'>.
    Class that wraps the objects and provide additional methods
    to them or override existing ones. Helper methods prevents
    you from using multiple dots in your code.

    Be free to inherit from this class and extend existing functionality.
    """
    def __init__(self, update):
        self._origin = update

    def __getattr__(self, item):
        cls = self.__class__

        if hasattr(cls, item):
            # returns attr of the wrapper
            return getattr(self, item)

        # else returns attr of the origin object
        return getattr(self._origin, item)

    @property
    def chat_id(self):
        """Returns id of the chart in which message was sent."""
        return self.message.chat_id

    def get_msg_text(self):
        """Returns text of the user message."""
        return self.message.text

    def get_msg_date(self):
        """Returns date when the user message was sent."""
        return self.message.date

    def get_username(self):
        """Returns 'username' of the user whom sent the message."""
        return self.message.chat.username

    def get_full_name(self):
        """Returns 'full_name' of the user whom sent the message."""
        return f'{self.message.chat.first_name} ' \
               f'{self.message.chat.last_name}'

    def get_photos(self):
        """Returns list of the photos pinned to the message."""
        return self.message.photo

    def get_stickers(self):
        """Returns list of the stickers that was sent by user."""
        return self.message.sticker

    def get_video(self):
        """Returns the video that pinned to the message."""
        return self.message.video