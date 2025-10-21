from lingu import Logic
from .handlers.instapaper_handler import InstapaperHandler


class InstapaperLogic(Logic):
    def __init__(self):
        super().__init__()
        self.handler = InstapaperHandler()
        
    def connect_to_instapaper(self):
        """Connect to Instapaper"""
        return self.handler.connect()
        
    def read_current_title(self):
        """Read the title of the current bookmark"""
        return self.handler.get_current_bookmark_title()
        
    def read_current_article(self):
        """Read the content of the current bookmark"""
        return self.handler.get_current_bookmark_content()
        
    def navigate_next_bookmark(self):
        """Navigate to the next bookmark"""
        return self.handler.navigate_next()
        
    def navigate_previous_bookmark(self):
        """Navigate to the previous bookmark"""
        return self.handler.navigate_previous()
        
    def navigate_first_bookmark(self):
        """Navigate to the first bookmark"""
        return self.handler.navigate_first()
        
    def navigate_last_bookmark(self):
        """Navigate to the last bookmark"""
        return self.handler.navigate_last()
        
    def list_bookmarks(self):
        """List all bookmarks"""
        return self.handler.list_all_bookmarks()
        
    def delete_current_bookmark(self):
        """Delete the current bookmark"""
        return self.handler.delete_current_bookmark()
        
    def star_current_bookmark(self):
        """Star the current bookmark"""
        return self.handler.star_current_bookmark()
        
    def archive_current_bookmark(self):
        """Archive the current bookmark"""
        return self.handler.archive_current_bookmark()
        
    def add_bookmark(self, url):
        """Add a new bookmark"""
        return self.handler.add_bookmark(url)
        
    def create_highlight(self, highlight_text):
        """Create a highlight for the current bookmark"""
        return self.handler.create_highlight(highlight_text)


logic = InstapaperLogic()
