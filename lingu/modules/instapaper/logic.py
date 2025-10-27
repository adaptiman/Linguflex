from lingu import Logic, cfg, log, repeat
from .handlers.instapaper_handler import InstapaperHandler
from .state import state

# Get credentials via cfg
instapaper_username = cfg("instapaper", "username", env_key="INSTAPAPER_USERNAME")
instapaper_password = cfg("instapaper", "password", env_key="INSTAPAPER_PASSWORD")
instapaper_api_key = cfg("instapaper", "API_KEY", env_key="INSTAPAPER_API_KEY")
instapaper_api_secret = cfg("instapaper", "API_SECRET", env_key="INSTAPAPER_API_SECRET")

no_credentials_msg = \
    "Can't perform that action, Instapaper credentials are needed."


class InstapaperLogic(Logic):
    def init(self):
        # Check if all required credentials are available
        if not all([instapaper_username, instapaper_password, instapaper_api_key, instapaper_api_secret]):
            missing = []
            if not instapaper_username: missing.append("INSTAPAPER_USERNAME")
            if not instapaper_password: missing.append("INSTAPAPER_PASSWORD")
            if not instapaper_api_key: missing.append("INSTAPAPER_API_KEY")
            if not instapaper_api_secret: missing.append("INSTAPAPER_API_SECRET")
            
            log.err(
                f"[instapaper] Missing required environment variables: {', '.join(missing)}.\n"
                "  Set these environment variables or add them to 'settings.yaml'."
            )
            state.set_disabled(True)
            state.connection_message = f"Missing credentials: {', '.join(missing)}"
            self.ready()
            return

        # Try to connect to Instapaper
        connection_result = self.handler.connect()
        if connection_result["status"] == "success":
            log.inf("[instapaper] Successfully connected to Instapaper")
            state.is_connected = True
            state.connection_message = connection_result["message"]
            
            # Load initial bookmarks
            self.refresh_bookmarks()
        else:
            log.err(f"[instapaper] Connection failed: {connection_result['message']}")
            state.set_disabled(True)
            state.is_connected = False
            state.connection_message = connection_result["message"]
        
        self.ready()

    def __init__(self):
        super().__init__()
        self.handler = InstapaperHandler()
        self.bookmarks = []

    def refresh_bookmarks(self):
        """Refresh bookmarks from Instapaper and update state"""
        if not state.is_connected:
            return
            
        bookmarks, result = self.handler.get_bookmarks()
        if result["status"] == "success" and bookmarks:
            self.bookmarks = bookmarks
            state.total_bookmarks = len(bookmarks)
            # Update current bookmark info if we have bookmarks
            if bookmarks and state.current_index < len(bookmarks):
                current_bookmark = bookmarks[state.current_index]
                state.current_bookmark_title = current_bookmark.title
                state.current_bookmark_content = getattr(current_bookmark, 'text', '') or "Content not available"
            log.inf(f"[instapaper] Refreshed {len(bookmarks)} bookmarks")
        else:
            log.err(f"[instapaper] Failed to refresh bookmarks: {result.get('message', 'Unknown error')}")

    @repeat(60 * 30)  # Refresh bookmarks every 30 minutes
    def repeat_refresh_bookmarks(self):
        if state.is_disabled or not state.is_connected:
            return
        self.refresh_bookmarks()
        
    def connect_to_instapaper(self):
        """Connect to Instapaper"""
        if not all([instapaper_username, instapaper_password, instapaper_api_key, instapaper_api_secret]):
            return no_credentials_msg
        return self.handler.connect()
        
    def read_current_title(self):
        """Read the title of the current bookmark"""
        if not state.is_connected:
            return no_credentials_msg
        result = self.handler.get_current_bookmark_title()
        if result.get("status") == "success":
            state.current_bookmark_title = result.get("title", "")
        return result
        
    def read_current_article(self):
        """Read the content of the current bookmark"""
        if not state.is_connected:
            return no_credentials_msg
        result = self.handler.get_current_bookmark_content()
        if result.get("status") == "success":
            state.current_bookmark_content = result.get("content", "")
        return result
        
    def navigate_next_bookmark(self):
        """Navigate to the next bookmark"""
        if not state.is_connected:
            return no_credentials_msg
        result = self.handler.navigate_next()
        if result.get("status") == "success":
            state.current_index = self.handler.get_current_index()
            self._update_current_bookmark_state()
        return result
        
    def navigate_previous_bookmark(self):
        """Navigate to the previous bookmark"""
        if not state.is_connected:
            return no_credentials_msg
        result = self.handler.navigate_previous()
        if result.get("status") == "success":
            state.current_index = self.handler.get_current_index()
            self._update_current_bookmark_state()
        return result
        
    def navigate_first_bookmark(self):
        """Navigate to the first bookmark"""
        if not state.is_connected:
            return no_credentials_msg
        result = self.handler.navigate_first()
        if result.get("status") == "success":
            state.current_index = 0
            self._update_current_bookmark_state()
        return result
        
    def navigate_last_bookmark(self):
        """Navigate to the last bookmark"""
        if not state.is_connected:
            return no_credentials_msg
        result = self.handler.navigate_last()
        if result.get("status") == "success":
            state.current_index = state.total_bookmarks - 1
            self._update_current_bookmark_state()
        return result

    def _update_current_bookmark_state(self):
        """Update state with current bookmark information"""
        if self.bookmarks and 0 <= state.current_index < len(self.bookmarks):
            current_bookmark = self.bookmarks[state.current_index]
            state.current_bookmark_title = current_bookmark.title
            state.current_bookmark_content = getattr(current_bookmark, 'text', '') or "Content not available"

    def list_bookmarks(self):
        """List all bookmarks"""
        if not state.is_connected:
            return no_credentials_msg
        return self.handler.list_all_bookmarks()
        
    def delete_current_bookmark(self):
        """Delete the current bookmark"""
        if not state.is_connected:
            return no_credentials_msg
        result = self.handler.delete_current_bookmark()
        if result.get("status") == "success":
            # Refresh bookmarks after deletion
            self.refresh_bookmarks()
        return result
        
    def star_current_bookmark(self):
        """Star the current bookmark"""
        if not state.is_connected:
            return no_credentials_msg
        return self.handler.star_current_bookmark()
        
    def archive_current_bookmark(self):
        """Archive the current bookmark"""
        if not state.is_connected:
            return no_credentials_msg
        result = self.handler.archive_current_bookmark()
        if result.get("status") == "success":
            # Refresh bookmarks after archiving
            self.refresh_bookmarks()
        return result
        
    def add_bookmark(self, url):
        """Add a new bookmark"""
        if not state.is_connected:
            return no_credentials_msg
        result = self.handler.add_bookmark(url)
        if result.get("status") == "success":
            # Refresh bookmarks after adding
            self.refresh_bookmarks()
        return result
        
    def create_highlight(self, highlight_text):
        """Create a highlight for the current bookmark"""
        if not state.is_connected:
            return no_credentials_msg
        return self.handler.create_highlight(highlight_text)


logic = InstapaperLogic()
