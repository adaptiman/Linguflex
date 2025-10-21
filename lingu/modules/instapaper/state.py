from lingu import State


class InstapaperState(State):
    def __init__(self):
        super().__init__()
        #self.large_symbol = "🅸"
        self.large_symbol = "📰"
        self.is_connected = False
        self.connection_message = ""
        self.current_bookmark_title = ""
        self.current_bookmark_content = ""
        self.current_index = 0
        self.total_bookmarks = 0


state = InstapaperState()
