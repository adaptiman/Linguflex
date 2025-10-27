from lingu import State
from typing import List, Dict, Any


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
        self.bookmarks_data: List[Dict[str, Any]] = []  # Store bookmark metadata
        self.last_refresh_time = None
        
    def get_current_bookmark_info(self) -> Dict[str, Any]:
        """Get formatted info about current bookmark"""
        return {
            "title": self.current_bookmark_title,
            "content": self.current_bookmark_content,
            "index": self.current_index + 1,  # 1-based for display
            "total": self.total_bookmarks,
            "connected": self.is_connected
        }


state = InstapaperState()
