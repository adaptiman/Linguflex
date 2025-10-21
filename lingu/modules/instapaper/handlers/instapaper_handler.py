"""
Instapaper Handler

Business logic for interacting with Instapaper bookmarks.
Independent of Linguflex for standalone testing.
"""

import netrc
from typing import List, Dict, Optional, Tuple

# Try to import required dependencies
try:
    import instapaper
    INSTAPAPER_AVAILABLE = True
except ImportError:
    INSTAPAPER_AVAILABLE = False
    print("Warning: 'instapaper' module not found. Install with: pip install instapaper")

# Try to import lingu config, fallback to default if not available
try:
    from lingu import cfg
    LINGU_AVAILABLE = True
except ImportError:
    LINGU_AVAILABLE = False
    # Fallback configuration function
    def cfg(module: str, key: str, default=None):
        # When running standalone, just return the default value
        return default


class InstapaperHandler:
    """Handler for Instapaper operations"""
    
    def __init__(self, bookmark_limit: Optional[int] = None):
        self.bookmark_limit = bookmark_limit or cfg("instapaper", "bookmark_limit", default=25)
        self.instapaper_client = None
        self.current_index = 0
        
    def connect(self) -> Dict[str, str]:
        """
        Connect to Instapaper using credentials from .netrc
        
        Returns:
            Dict containing connection status and message
        """
        try:
            secrets = netrc.netrc()
            login, _, password = secrets.authenticators('instapaper.com')
            consumerkey, _, consumersecret = secrets.authenticators('api.instapaper.com')
            
            self.instapaper_client = instapaper.Instapaper(consumerkey, consumersecret)
            self.instapaper_client.login(login, password)
            
            return {
                "status": "success",
                "message": "Successfully connected to Instapaper"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to connect to Instapaper: {str(e)}"
            }
    
    def get_bookmarks(self) -> Tuple[Optional[List], Dict[str, str]]:
        """
        Retrieve bookmarks from Instapaper
        
        Returns:
            Tuple of (bookmarks list, status dict)
        """
        if not self.instapaper_client:
            return None, {"status": "error", "message": "Not connected to Instapaper"}
            
        try:
            marks = self.instapaper_client.bookmarks(limit=self.bookmark_limit)
            return marks, {"status": "success", "message": f"Retrieved {len(marks) if marks else 0} bookmarks"}
        except Exception as e:
            return None, {"status": "error", "message": f"Error fetching bookmarks: {str(e)}"}
    
    def get_current_bookmark_title(self) -> Dict[str, str]:
        """Get the title of the current bookmark"""
        marks, status = self.get_bookmarks()
        if status["status"] == "error":
            return status
            
        if marks and 0 <= self.current_index < len(marks):
            return {
                "status": "success",
                "title": marks[self.current_index].title,
                "index": str(self.current_index),
                "total": str(len(marks))
            }
        return {"status": "error", "message": "Current index is out of range"}
    
    def get_current_bookmark_content(self) -> Dict[str, str]:
        """Get the content/text of the current bookmark"""
        marks, status = self.get_bookmarks()
        if status["status"] == "error":
            return status
            
        if marks and 0 <= self.current_index < len(marks):
            return {
                "status": "success",
                "content": marks[self.current_index].text or "No content available",
                "title": marks[self.current_index].title,
                "index": str(self.current_index)
            }
        return {"status": "error", "message": "Current index is out of range"}
    
    def navigate_next(self) -> Dict[str, str]:
        """Navigate to the next bookmark"""
        marks, status = self.get_bookmarks()
        if status["status"] == "error":
            return status
            
        if marks and self.current_index < len(marks) - 1:
            self.current_index += 1
            return {
                "status": "success",
                "message": f"Moved to bookmark {self.current_index + 1} of {len(marks)}",
                "index": str(self.current_index),
                "title": marks[self.current_index].title
            }
        return {"status": "error", "message": "Already at the last bookmark"}
    
    def navigate_previous(self) -> Dict[str, str]:
        """Navigate to the previous bookmark"""
        marks, status = self.get_bookmarks()
        if status["status"] == "error":
            return status
            
        if self.current_index > 0:
            self.current_index -= 1
            return {
                "status": "success", 
                "message": f"Moved to bookmark {self.current_index + 1} of {len(marks)}",
                "index": str(self.current_index),
                "title": marks[self.current_index].title
            }
        return {"status": "error", "message": "Already at the first bookmark"}
    
    def navigate_first(self) -> Dict[str, str]:
        """Navigate to the first bookmark"""
        marks, status = self.get_bookmarks()
        if status["status"] == "error":
            return status
            
        if marks:
            self.current_index = 0
            return {
                "status": "success",
                "message": f"Moved to first bookmark",
                "index": "0",
                "title": marks[0].title
            }
        return {"status": "error", "message": "No bookmarks found"}
    
    def navigate_last(self) -> Dict[str, str]:
        """Navigate to the last bookmark"""
        marks, status = self.get_bookmarks()
        if status["status"] == "error":
            return status
            
        if marks:
            self.current_index = len(marks) - 1
            return {
                "status": "success",
                "message": f"Moved to last bookmark",
                "index": str(self.current_index),
                "title": marks[self.current_index].title
            }
        return {"status": "error", "message": "No bookmarks found"}
    
    def list_all_bookmarks(self) -> Dict[str, any]:
        """Get a list of all bookmark titles"""
        marks, status = self.get_bookmarks()
        if status["status"] == "error":
            return status
            
        if marks:
            bookmark_list = [{"index": i, "title": mark.title} for i, mark in enumerate(marks)]
            return {
                "status": "success",
                "bookmarks": bookmark_list,
                "count": len(marks)
            }
        return {"status": "error", "message": "No bookmarks found"}
    
    def delete_current_bookmark(self) -> Dict[str, str]:
        """Delete the currently selected bookmark"""
        marks, status = self.get_bookmarks()
        if status["status"] == "error":
            return status
            
        if marks and 0 <= self.current_index < len(marks):
            try:
                bookmark = marks[self.current_index]
                title = bookmark.title
                bookmark.delete()
                
                # Adjust current index if necessary
                if self.current_index >= len(marks) - 1:
                    self.current_index = max(0, len(marks) - 2)
                
                return {
                    "status": "success",
                    "message": f"Bookmark '{title}' deleted successfully"
                }
            except Exception as e:
                return {"status": "error", "message": f"Error deleting bookmark: {str(e)}"}
        return {"status": "error", "message": "Current index is out of range"}
    
    def star_current_bookmark(self) -> Dict[str, str]:
        """Star the currently selected bookmark"""
        marks, status = self.get_bookmarks()
        if status["status"] == "error":
            return status
            
        if marks and 0 <= self.current_index < len(marks):
            try:
                bookmark = marks[self.current_index]
                bookmark.star()
                return {
                    "status": "success",
                    "message": f"Bookmark '{bookmark.title}' starred successfully"
                }
            except Exception as e:
                return {"status": "error", "message": f"Error starring bookmark: {str(e)}"}
        return {"status": "error", "message": "Current index is out of range"}
    
    def archive_current_bookmark(self) -> Dict[str, str]:
        """Archive the currently selected bookmark"""
        marks, status = self.get_bookmarks()
        if status["status"] == "error":
            return status
            
        if marks and 0 <= self.current_index < len(marks):
            try:
                bookmark = marks[self.current_index]
                bookmark.archive()
                
                # Adjust current index if necessary
                if self.current_index >= len(marks) - 1:
                    self.current_index = max(0, len(marks) - 2)
                
                return {
                    "status": "success",
                    "message": f"Bookmark '{bookmark.title}' archived successfully"
                }
            except Exception as e:
                return {"status": "error", "message": f"Error archiving bookmark: {str(e)}"}
        return {"status": "error", "message": "Current index is out of range"}
    
    def add_bookmark(self, url: str) -> Dict[str, str]:
        """Add a new bookmark"""
        if not self.instapaper_client:
            return {"status": "error", "message": "Not connected to Instapaper"}
            
        if not url or not url.strip():
            return {"status": "error", "message": "URL is required"}
            
        try:
            bookmark = instapaper.Bookmark(self.instapaper_client, {"url": url.strip()})
            bookmark.save()
            return {
                "status": "success",
                "message": f"Bookmark for {url} added successfully"
            }
        except Exception as e:
            return {"status": "error", "message": f"Error adding bookmark: {str(e)}"}
    
    def create_highlight(self, highlight_text: str) -> Dict[str, str]:
        """Create a highlight for the current bookmark"""
        if not highlight_text or not highlight_text.strip():
            return {"status": "error", "message": "Highlight text is required"}
            
        marks, status = self.get_bookmarks()
        if status["status"] == "error":
            return status
            
        if marks and 0 <= self.current_index < len(marks):
            try:
                bookmark = marks[self.current_index]
                bookmark.create_highlight(highlight_text.strip())
                return {
                    "status": "success",
                    "message": f"Highlight created successfully for '{bookmark.title}'"
                }
            except Exception as e:
                return {"status": "error", "message": f"Error creating highlight: {str(e)}"}
        return {"status": "error", "message": "Current index is out of range"}
    
    def get_current_index(self) -> int:
        """Get the current bookmark index"""
        return self.current_index
    
    def set_current_index(self, index: int) -> Dict[str, str]:
        """Set the current bookmark index"""
        marks, status = self.get_bookmarks()
        if status["status"] == "error":
            return status
            
        if marks and 0 <= index < len(marks):
            self.current_index = index
            return {
                "status": "success",
                "message": f"Current index set to {index}",
                "title": marks[index].title
            }
        return {"status": "error", "message": f"Index {index} is out of range"}


# Main execution loop
if __name__ == "__main__":
    print("=== Instapaper Handler Test ===")
    
    # Check if required dependencies are available
    if not INSTAPAPER_AVAILABLE:
        print("✗ Cannot run test: 'instapaper' module not found")
        print("  Install with: pip install instapaper")
        exit(1)
    
    # Create handler instance
    handler = InstapaperHandler()
    
    # Test connection
    print("\n1. Testing connection...")
    connection_result = handler.connect()
    if connection_result["status"] == "success":
        print(f"✓ Connection successful: {connection_result['message']}")
    else:
        print(f"✗ Connection failed: {connection_result['message']}")
        exit(1)
    
    # Test getting bookmarks
    print("\n2. Testing bookmark retrieval...")
    bookmarks, bookmark_result = handler.get_bookmarks()
    if bookmark_result["status"] == "success":
        print(f"✓ Bookmark retrieval successful: {bookmark_result['message']}")
        if bookmarks:
            print(f"  First bookmark title: '{bookmarks[0].title}'")
    else:
        print(f"✗ Bookmark retrieval failed: {bookmark_result['message']}")
    
    print("\n=== Test Complete ===")