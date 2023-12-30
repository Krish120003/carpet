from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtCore import QTimer, QObject, Slot


import sys
import os
from pathlib import Path

from utils import handle_screenshot
from viewer import Viewer

basedir = Path(os.path.dirname(__file__)).parent


class SystemApp(QObject):
    def __init__(self, app):
        super().__init__()
        self.app = app

        self.init_system_tray()

        self.screenshot_interval = 2000  # 2000 milliseconds = 2 seconds

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.capture_and_save_screenshot)
        self.timer.start(self.screenshot_interval)
        self.is_active = True

    def init_system_tray(self):
        icon = QIcon(str(basedir / "icon.png"))

        # Create the tray
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(icon)
        self.tray.setVisible(True)

        # Create the menu
        self.menu = QMenu()

        # for actions, we have
        # - view screenshots
        # - pause/resume screenshotting
        # - exit

        self.view_screenshots_item = QAction("View Screenshots")
        self.menu.addAction(self.view_screenshots_item)
        self.view_screenshots_item.triggered.connect(self.show_viewer)

        self.pause_item = QAction("Pause")
        self.menu.addAction(self.pause_item)
        self.pause_item.triggered.connect(self.toggle_screenshotting)

        # Add a Quit option to the menu.
        self.quit = QAction("Quit Carpet")
        self.quit.triggered.connect(self.app.quit)
        self.menu.addAction(self.quit)

        # Add the menu to the self.tray
        self.tray.setContextMenu(self.menu)

        self.tray.show()

    @Slot()
    def toggle_screenshotting(self):
        print("Pausing/Resuming")
        if self.is_active:
            self.timer.stop()
            self.pause_item.setText("Resume")
        else:
            self.timer.start(self.screenshot_interval)
            self.pause_item.setText("Pause")

        self.is_active = not self.is_active

    @Slot()
    def show_viewer(self):
        self.viewer = Viewer()
        self.viewer.show()

    def capture_and_save_screenshot(self):
        screen = QApplication.primaryScreen()
        screenshot = screen.grabWindow(0)  # Grab the entire screen
        handle_screenshot(screenshot)


if __name__ == "__main__":
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)

    system_app = SystemApp(app)

    sys.exit(app.exec())
