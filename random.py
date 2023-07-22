import sys
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QTabWidget, QTabBar, QMessageBox, QMenu, QAction, QComboBox
from PyQt5.QtGui import QIcon, QPixmap, QColor
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile

class TabWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.webview = QWebEngineView()
        self.setCentralWidget(self.webview)

    def closeEvent(self, event):
        # Stop the video from playing
        self.webview.page().runJavaScript("document.querySelector('video').pause();")
        event.accept()

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nikicha Search")
        self.setGeometry(100, 100, 800, 600)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Apply black background and green text color to the whole window
        self.setStyleSheet("background-color: black; color: green;")

        # Top layout for settings menu, sign-in button, and new tab button
        top_layout = QHBoxLayout()

        # Settings menu
        settings_menu = QMenu()
        settings_button = QPushButton("⚙")  # Gear icon symbol
        settings_button.setStyleSheet("background-color: none; border: none;")
        settings_button.setMenu(settings_menu)
        top_layout.addWidget(settings_button)

        # Sign-in button
        sign_in_button = QPushButton("Sign In")
        sign_in_button.clicked.connect(self.sign_in_with_google)
        top_layout.addWidget(sign_in_button)

        # New tab button
        new_tab_button = QPushButton("+")
        new_tab_button.clicked.connect(self.add_new_tab)
        top_layout.addWidget(new_tab_button)

        layout.addLayout(top_layout)

        # Nikicha Search label
        label = QLabel("Nikicha Search", alignment=Qt.AlignCenter, objectName="title_label")
        layout.addWidget(label)

        # Address bar and Go button
        self.address_bar = QLineEdit()
        layout.addWidget(self.address_bar)
        self.address_bar.setAlignment(Qt.AlignCenter)

        self.go_button = QPushButton("Go")
        self.go_button.clicked.connect(self.load_url)
        layout.addWidget(self.go_button)

        # Tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # Add an initial tab
        self.add_new_tab()

        # Settings tab
        self.settings_tab = QWidget()

        # Settings content
        settings_label = QLabel("Settings", objectName="settings_label")
        settings_layout = QVBoxLayout(self.settings_tab)
        settings_layout.addWidget(settings_label)

        # Language selection
        language_label = QLabel("Language:")
        settings_layout.addWidget(language_label)

        self.language_combo = QComboBox()
        self.language_combo.addItem("English")
        settings_layout.addWidget(self.language_combo)

        # Add settings menu action
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings)
        settings_menu.addAction(settings_action)

    def load_url(self):
        url = self.address_bar.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        self.tab_widget.currentWidget().webview.load(QUrl(url))

    def sign_in_with_google(self):
        profile = QWebEngineProfile.defaultProfile()
        webview = QWebEngineView()
        webview.setPage(profile)

        # Load the Google sign-in page
        webview.load(QUrl("https://accounts.google.com"))

        # Create a new tab and add it to the tab widget
        tab_window = TabWindow()
        tab_window.webview = webview

        if self.tab_widget.count() == 1 and isinstance(self.tab_widget.widget(0), QLabel):
            self.tab_widget.removeTab(0)

        self.tab_widget.addTab(tab_window, "Google Sign-In")

        # Add close button to the tab
        tab_bar = self.tab_widget.tabBar()
        close_button = QPushButton('✕')  # Close button with '✕' symbol
        close_button.setStyleSheet("background-color: none; border: none;")
        close_button.clicked.connect(lambda: self.close_tab(tab_window))
        tab_bar.setTabButton(self.tab_widget.indexOf(tab_window), QTabBar.RightSide, close_button)

    def add_new_tab(self):
        # Create a new tab and add it to the tab widget
        tab_window = TabWindow()
        tab_window.webview.load(QUrl("https://www.google.com/"))  # Replace with your desired home page URL

        if self.tab_widget.count() == 1 and isinstance(self.tab_widget.widget(0), QLabel):
            self.tab_widget.removeTab(0)

        self.tab_widget.addTab(tab_window, "New Tab")

        # Add close button to the tab
        tab_bar = self.tab_widget.tabBar()
        close_button = QPushButton('✕')  # Close button with '✕' symbol
        close_button.setStyleSheet("background-color: none; border: none;")
        close_button.clicked.connect(lambda: self.close_tab(tab_window))
        tab_bar.setTabButton(self.tab_widget.indexOf(tab_window), QTabBar.RightSide, close_button)

    def close_tab(self, tab_window):
        index = self.tab_widget.indexOf(tab_window)
        self.tab_widget.removeTab(index)
        tab_window.close()
        if self.tab_widget.count() == 0:
            label = QLabel("No Google Tabs Opened", alignment=Qt.AlignCenter, objectName="empty_tabs_label")
            self.tab_widget.addTab(label, "Empty")

    def open_settings(self):
        if self.tab_widget.indexOf(self.settings_tab) == -1:
            self.tab_widget.addTab(self.settings_tab, "Settings")
            self.tab_widget.setCurrentWidget(self.settings_tab)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    browser = BrowserWindow()
    browser.show()
    sys.exit(app.exec_())
