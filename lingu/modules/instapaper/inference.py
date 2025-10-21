"""
Instapaper Module

- provides voice-controlled access to Instapaper bookmarks
- allows reading, navigation, deletion, starring, and archiving of bookmarks

"""

from lingu import Populatable
from pydantic import Field
from .logic import logic


class ReadCurrentBookmarkTitle(Populatable):
    """
    Reads the title of the currently selected bookmark from Instapaper.
    """

    def on_populated(self):
        return logic.read_current_title()


class ReadCurrentBookmarkContent(Populatable):
    """
    Reads the full content/text of the currently selected bookmark from Instapaper.
    """

    def on_populated(self):
        return logic.read_current_article()


class NavigateToNextBookmark(Populatable):
    """
    Navigates to the next bookmark in the Instapaper collection.
    """

    def on_populated(self):
        return logic.navigate_next_bookmark()


class NavigateToPreviousBookmark(Populatable):
    """
    Navigates to the previous bookmark in the Instapaper collection.
    """

    def on_populated(self):
        return logic.navigate_previous_bookmark()


class NavigateToFirstBookmark(Populatable):
    """
    Navigates to the first bookmark in the Instapaper collection.
    """

    def on_populated(self):
        return logic.navigate_first_bookmark()


class NavigateToLastBookmark(Populatable):
    """
    Navigates to the last bookmark in the Instapaper collection.
    """

    def on_populated(self):
        return logic.navigate_last_bookmark()


class ListAllBookmarks(Populatable):
    """
    Lists all bookmarks in the Instapaper collection showing their titles.
    """

    def on_populated(self):
        return logic.list_bookmarks()


class DeleteCurrentBookmark(Populatable):
    """
    Deletes the currently selected bookmark from Instapaper.
    This action cannot be undone.
    """

    def on_populated(self):
        return logic.delete_current_bookmark()


class StarCurrentBookmark(Populatable):
    """
    Stars (favorites) the currently selected bookmark in Instapaper.
    """

    def on_populated(self):
        return logic.star_current_bookmark()


class ArchiveCurrentBookmark(Populatable):
    """
    Archives the currently selected bookmark in Instapaper.
    """

    def on_populated(self):
        return logic.archive_current_bookmark()


class AddNewBookmark(Populatable):
    """
    Adds a new bookmark to Instapaper using the provided URL.
    """
    url: str = Field(..., description="The URL to add as a bookmark to Instapaper")

    def on_populated(self):
        return logic.add_bookmark(self.url)


class CreateHighlight(Populatable):
    """
    Creates a highlight for the currently selected bookmark in Instapaper.
    """
    highlight_text: str = Field(..., description="The text to highlight in the current bookmark")

    def on_populated(self):
        return logic.create_highlight(self.highlight_text)
