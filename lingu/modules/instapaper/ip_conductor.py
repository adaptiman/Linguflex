"""A simple console application to interact with Instapaper bookmarks."""

import time
import netrc
import instapaper

# Global configuration
BOOKMARK_LIMIT = 25

def slow_print(text, delay=0.05):
    """Prints strings slowly to the console."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def read_title(i, current_index):
    """Reads the bookmark title."""
    try:
        marks = i.bookmarks(limit=BOOKMARK_LIMIT)
    except (AttributeError, ValueError, RuntimeError, OSError) as e:
        print(f"Error fetching bookmarks: {e}")
        return
    if marks:
        if 0 <= current_index < len(marks):
            m = marks[current_index]
            #slow_print(str(m.title))
            print(str(m.title))
        else:
            print("Current index is out of range.")
    else:
        print("No bookmarks found.")

def read_article(i, current_index):
    """Reads the content of the bookmark title."""
    try:
        marks = i.bookmarks(limit=BOOKMARK_LIMIT)
    except (AttributeError, ValueError, RuntimeError, OSError) as e:
        print(f"Error fetching bookmarks: {e}")
        return
    if marks:
        if 0 <= current_index < len(marks):
            m = marks[current_index]
            #slow_print(str(m.text))
            print(str(m.text))
        else:
            print("Current index is out of range.")
    else:
        print("No bookmarks found.")

def next_bookmark(i, current_index):
    """Navigates to the next bookmark."""
    marks = i.bookmarks(limit=BOOKMARK_LIMIT)
    if marks and current_index < len(marks) - 1:
        return current_index + 1
    print("Already at the last bookmark.")
    return current_index

def prev_bookmark(current_index):
    """Navigates to the previous bookmark."""
    if current_index > 0:
        return current_index - 1
    print("Already at the first bookmark.")
    return current_index

def first_bookmark(i):
    """Navigates to the first bookmark."""
    marks = i.bookmarks(limit=BOOKMARK_LIMIT)
    if marks:
        return 0
    print("No bookmarks found.")
    return 0

def last_bookmark(i):
    """Navigates to the last bookmark."""
    marks = i.bookmarks(limit=BOOKMARK_LIMIT)
    if marks:
        return len(marks) - 1
    print("No bookmarks found.")
    return 0

def show_bookmarks(i):
    """Displays a list of all bookmarks."""
    try:
        marks = i.bookmarks(limit=BOOKMARK_LIMIT)
    except (AttributeError, ValueError, RuntimeError, OSError) as e:
        print(f"Error fetching bookmarks: {e}")
        return
    for m in marks:
        print(f"{m.title}")

def delete_bookmark(i, current_index):
    """Deletes the currently selected bookmark."""
    marks = i.bookmarks(limit=BOOKMARK_LIMIT)
    if marks:
        if 0 <= current_index < len(marks):
            m = marks[current_index]
            confirmation = input(
                f"Are you sure you want to delete '{m.title}'? (y/N): "
            ).strip().lower()
            if confirmation == 'y' or confirmation == 'yes':
                m.delete()
                print(f"Bookmark '{m.title}' deleted.")
                return True
            else:
                print("Deletion cancelled.")
                return False
        else:
            print("Current index is out of range.")
            return False
    else:
        print("No bookmarks found.")
        return False

def star_bookmark(i, current_index):
    """Stars the currently selected bookmark."""
    marks = i.bookmarks(limit=BOOKMARK_LIMIT)
    if marks:
        if 0 <= current_index < len(marks):
            m = marks[current_index]
            try:
                m.star()
                print(f"Bookmark '{m.title}' starred.")
                return True
            except AttributeError as e:
                print(f"Error starring bookmark: {e}")
                return False
            except (ValueError, RuntimeError, OSError) as e:
                print(f"API error: {e}")
                return False
        else:
            print("Current index is out of range.")
            return False
    else:
        print("No bookmarks found.")
        return False

def add_bookmark(i):
    """Adds a new bookmark."""
    url = input('Enter URL to add: ').strip()
    try:
        # Uncomment and adjust if instapaper.Bookmark works as expected
        b = instapaper.Bookmark(i, {"url": url})
        b.save()
        print(f"Bookmark for {url} added.")
    except (AttributeError, ValueError, RuntimeError, OSError) as e:
        print(f"Error adding bookmark: {e}")

def create_highlight(i, current_index):
    """Creates a highlight for the currently selected bookmark."""
    try:
        marks = i.bookmarks(limit=BOOKMARK_LIMIT)
    except (AttributeError, ValueError, RuntimeError, OSError) as e:
        print(f"Error fetching bookmarks: {e}")
        return False

    if marks:
        if 0 <= current_index < len(marks):
            m = marks[current_index]
            print(f"Creating highlight for: {m.title}")
            print("Enter the text you want to highlight (press Enter twice to finish):")

            lines = []
            empty_line_count = 0
            while empty_line_count < 2:
                line = input()
                if line.strip() == "":
                    empty_line_count += 1
                else:
                    empty_line_count = 0
                lines.append(line)

            # Remove the last empty lines
            while lines and lines[-1].strip() == "":
                lines.pop()

            highlight_text = "\n".join(lines).strip()

            if highlight_text:
                try:
                    # Create the highlight using the instapaper create_highlight method
                    m.create_highlight(highlight_text)
                    print("Highlight created successfully!")
                    ellipsis = '...' if len(highlight_text) > 100 else ''
                    print(f"Highlighted text: {highlight_text[:100]}{ellipsis}")
                    return True
                except (AttributeError, ValueError, RuntimeError, OSError) as e:
                    print(f"Error creating highlight: {e}")
                    return False
            else:
                print("No text entered. Highlight cancelled.")
                return False
        else:
            print("Current index is out of range.")
            return False
    else:
        print("No bookmarks found.")
        return False

def archive_bookmark(i, current_index):
    """Archives the currently selected bookmark."""
    try:
        marks = i.bookmarks(limit=BOOKMARK_LIMIT)
    except (AttributeError, ValueError, RuntimeError, OSError) as e:
        print(f"Error fetching bookmarks: {e}")
        return False

    if marks:
        if 0 <= current_index < len(marks):
            m = marks[current_index]
            try:
                m.archive()
                print(f"Bookmark '{m.title}' archived successfully.")
                return True
            except (AttributeError, ValueError, RuntimeError, OSError) as e:
                print(f"Error archiving bookmark: {e}")
                return False
        else:
            print("Current index is out of range.")
            return False
    else:
        print("No bookmarks found.")
        return False

def main():
    """Main function to run the Instapaper console app."""
    # This is the login block where we authenticate with Instapaper
    # and create an Instapaper instance.
    secrets = netrc.netrc()
    login, _, password = secrets.authenticators('instapaper.com')
    consumerkey, _, consumersecret = secrets.authenticators('api.instapaper.com')
    i = instapaper.Instapaper(consumerkey, consumersecret)
    i.login(login, password)

    # Here begins the interactive console
    print("Welcome to the Instapaper Console App!")
    print("Type 'bookmarks' to list bookmarks, 'add' to add a bookmark, "
          "'delete' to delete current bookmark, 'star' to star current bookmark, "
          "'highlight' to create a highlight, 'archive' to archive current bookmark, "
          "or 'exit' to quit.")
    print("Navigation: 'title', 'next', 'prev', 'first', 'last', 'read'")
    current_index = 0

    # Display the current bookmark title at startup
    #print("\nCurrent bookmark:")
    read_title(i, current_index)

    while True:
        cmd = input('> ').strip().lower()
        if cmd == 'exit':
            print("Goodbye!")
            break
        elif cmd == 'bookmarks':
            show_bookmarks(i)
        elif cmd == 'add':
            add_bookmark(i)
        elif cmd == 'delete':
            delete_bookmark(i, current_index)
        elif cmd == 'star':
            star_bookmark(i, current_index)
        elif cmd == 'highlight':
            create_highlight(i, current_index)
        elif cmd == 'archive':
            archive_bookmark(i, current_index)
        elif cmd == 'title':
            read_title(i, current_index)
        elif cmd == 'next':
            current_index = next_bookmark(i, current_index)
            read_title(i, current_index)
        elif cmd == 'previous' or cmd == 'prev':
            current_index = prev_bookmark(current_index)
            read_title(i, current_index)
        elif cmd == 'first':
            current_index = first_bookmark(i)
            read_title(i, current_index)
        elif cmd == 'last':
            current_index = last_bookmark(i)
            read_title(i, current_index)
        elif cmd == 'read':
            read_article(i, current_index)
        else:
            print("Unknown command. Try 'bookmarks', 'add', 'delete', 'star', "
                  "'highlight', 'archive', 'title', 'next', 'prev', 'first', "
                  "'last', 'read', or 'exit'.")

if __name__ == "__main__":
    main()
