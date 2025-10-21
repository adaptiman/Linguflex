from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QTextEdit,
    QStackedWidget,
    QSizePolicy
)
from qfluentwidgets import (
    InfoBadge,
    InfoLevel,
    setTheme,
    Theme,
    TextEdit,
    SegmentedWidget,
    PushButton,
    LineEdit
)
from lingu import UI, Line, StretchLine
from PyQt6.QtCore import Qt, QUrl, pyqtSlot
from PyQt6.QtGui import QDesktopServices
from .logic import logic
from .state import state


class InstapaperUI(UI):
    def __init__(self):
        super().__init__()

        setTheme(Theme.DARK)

        # Header
        label = UI.headerlabel("📰 Instapaper Reader")
        self.header(label, nostyle=True)
        
        # Connection status
        self.connection_status = QLabel("Not connected")
        self.connection_status.setStyleSheet("color: orange;")
        
        # Current bookmark info
        self.current_title = QLabel("No bookmark selected")
        self.current_index = QLabel("Position: 0/0")
        
        # Navigation buttons
        nav_layout = QHBoxLayout()
        self.first_btn = PushButton("First")
        self.prev_btn = PushButton("Previous")
        self.next_btn = PushButton("Next")
        self.last_btn = PushButton("Last")
        
        nav_layout.addWidget(self.first_btn)
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addWidget(self.next_btn)
        nav_layout.addWidget(self.last_btn)
        
        # Action buttons
        action_layout = QHBoxLayout()
        self.read_title_btn = PushButton("Read Title")
        self.read_content_btn = PushButton("Read Content")
        self.list_btn = PushButton("List All")
        
        action_layout.addWidget(self.read_title_btn)
        action_layout.addWidget(self.read_content_btn)
        action_layout.addWidget(self.list_btn)
        
        # Management buttons
        mgmt_layout = QHBoxLayout()
        self.star_btn = PushButton("Star")
        self.delete_btn = PushButton("Delete")
        self.archive_btn = PushButton("Archive")
        
        mgmt_layout.addWidget(self.star_btn)
        mgmt_layout.addWidget(self.delete_btn)
        mgmt_layout.addWidget(self.archive_btn)
        
        # Add bookmark section
        add_layout = QHBoxLayout()
        self.url_input = LineEdit()
        self.url_input.setPlaceholderText("Enter URL to add...")
        self.add_btn = PushButton("Add Bookmark")
        
        add_layout.addWidget(self.url_input)
        add_layout.addWidget(self.add_btn)
        
        # Highlight section
        highlight_layout = QVBoxLayout()
        self.highlight_input = QTextEdit()
        self.highlight_input.setPlaceholderText("Enter text to highlight...")
        self.highlight_input.setMaximumHeight(100)
        self.highlight_btn = PushButton("Create Highlight")
        
        highlight_layout.addWidget(QLabel("Create Highlight:"))
        highlight_layout.addWidget(self.highlight_input)
        highlight_layout.addWidget(self.highlight_btn)
        
        # Status/output area
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setMaximumHeight(200)
        
        # Layout assembly
        self.addWidget(self.connection_status)
        self.addline()
        self.addWidget(self.current_title)
        self.addWidget(self.current_index)
        self.addline()
        self.addLayout(nav_layout)
        self.addline()
        self.addLayout(action_layout)
        self.addline()
        self.addLayout(mgmt_layout)
        self.addline()
        self.addLayout(add_layout)
        self.addline()
        self.addLayout(highlight_layout)
        self.addline()
        self.addWidget(QLabel("Output:"))
        self.addWidget(self.output_area)
        
        # Connect signals
        self.connect_signals()
        
        # Update UI with current state
        self.update_ui()
    
    def connect_signals(self):
        """Connect button signals to their respective handlers"""
        self.first_btn.clicked.connect(self.on_first_clicked)
        self.prev_btn.clicked.connect(self.on_prev_clicked)
        self.next_btn.clicked.connect(self.on_next_clicked)
        self.last_btn.clicked.connect(self.on_last_clicked)
        
        self.read_title_btn.clicked.connect(self.on_read_title_clicked)
        self.read_content_btn.clicked.connect(self.on_read_content_clicked)
        self.list_btn.clicked.connect(self.on_list_clicked)
        
        self.star_btn.clicked.connect(self.on_star_clicked)
        self.delete_btn.clicked.connect(self.on_delete_clicked)
        self.archive_btn.clicked.connect(self.on_archive_clicked)
        
        self.add_btn.clicked.connect(self.on_add_clicked)
        self.highlight_btn.clicked.connect(self.on_highlight_clicked)
    
    def update_ui(self):
        """Update UI elements with current state"""
        if state.is_connected:
            self.connection_status.setText("Connected to Instapaper")
            self.connection_status.setStyleSheet("color: green;")
        else:
            self.connection_status.setText("Not connected to Instapaper")
            self.connection_status.setStyleSheet("color: orange;")
        
        if state.current_bookmark_title:
            self.current_title.setText(f"Current: {state.current_bookmark_title}")
        else:
            self.current_title.setText("No bookmark selected")
        
        self.current_index.setText(f"Position: {state.current_index + 1}/{state.total_bookmarks}")
    
    def display_result(self, result):
        """Display operation result in the output area"""
        if isinstance(result, dict):
            if result.get("status") == "success":
                if "message" in result:
                    self.output_area.append(f"✓ {result['message']}")
                if "title" in result:
                    self.output_area.append(f"Title: {result['title']}")
                if "content" in result:
                    # Truncate long content for UI display
                    content = result['content']
                    if len(content) > 500:
                        content = content[:500] + "..."
                    self.output_area.append(f"Content: {content}")
                if "bookmarks" in result:
                    self.output_area.append("Bookmarks:")
                    for bookmark in result['bookmarks'][:10]:  # Show first 10
                        self.output_area.append(f"  {bookmark['index'] + 1}. {bookmark['title']}")
            else:
                self.output_area.append(f"✗ Error: {result.get('message', 'Unknown error')}")
        else:
            self.output_area.append(str(result))
        
        self.update_ui()
    
    @pyqtSlot()
    def on_first_clicked(self):
        result = logic.navigate_first_bookmark()
        self.display_result(result)
    
    @pyqtSlot()
    def on_prev_clicked(self):
        result = logic.navigate_previous_bookmark()
        self.display_result(result)
    
    @pyqtSlot()
    def on_next_clicked(self):
        result = logic.navigate_next_bookmark()
        self.display_result(result)
    
    @pyqtSlot()
    def on_last_clicked(self):
        result = logic.navigate_last_bookmark()
        self.display_result(result)
    
    @pyqtSlot()
    def on_read_title_clicked(self):
        result = logic.read_current_title()
        self.display_result(result)
    
    @pyqtSlot()
    def on_read_content_clicked(self):
        result = logic.read_current_article()
        self.display_result(result)
    
    @pyqtSlot()
    def on_list_clicked(self):
        result = logic.list_bookmarks()
        self.display_result(result)
    
    @pyqtSlot()
    def on_star_clicked(self):
        result = logic.star_current_bookmark()
        self.display_result(result)
    
    @pyqtSlot()
    def on_delete_clicked(self):
        result = logic.delete_current_bookmark()
        self.display_result(result)
    
    @pyqtSlot()
    def on_archive_clicked(self):
        result = logic.archive_current_bookmark()
        self.display_result(result)
    
    @pyqtSlot()
    def on_add_clicked(self):
        url = self.url_input.text().strip()
        if url:
            result = logic.add_bookmark(url)
            self.display_result(result)
            if result.get("status") == "success":
                self.url_input.clear()
        else:
            self.output_area.append("✗ Please enter a URL")
    
    @pyqtSlot()
    def on_highlight_clicked(self):
        highlight_text = self.highlight_input.toPlainText().strip()
        if highlight_text:
            result = logic.create_highlight(highlight_text)
            self.display_result(result)
            if result.get("status") == "success":
                self.highlight_input.clear()
        else:
            self.output_area.append("✗ Please enter text to highlight")
