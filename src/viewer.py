from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider
from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtGui import QPixmap
from db import conn, Capture
from utils import ocr


class Viewer(QWidget):
    closed = Signal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Carpet Viewer")
        self.resize(800, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # ok lets see how many images we hvae in the database
        min_id = Capture.select().order_by(Capture.cid).first()
        if min_id is None:
            min_id = 0
        else:
            min_id = min_id.cid

        max_id = Capture.select().order_by(Capture.cid.desc()).first()
        if max_id is None:
            max_id = 0
        else:
            max_id = max_id.cid

        self.current_id = max_id

        # slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(min_id)
        self.slider.setMaximum(max_id)

        self.slider.valueChanged.connect(self.update_image)

        self.layout.addWidget(self.slider)

        # image metadata
        self.image_metadata = QLabel()
        self.layout.addWidget(self.image_metadata)

        # image
        self.image_label = QLabel()
        self.image_label.setScaledContents(True)
        self.image_label.setFixedSize(800, 600)
        self.layout.addWidget(self.image_label)

        # ocr text
        # self.ocr_text = QLabel()
        # self.layout.addWidget(self.ocr_text)

        self.curr_img = None
        self.update_image()

    @Slot()
    def update_image(self):
        capture = Capture.get_by_id(self.slider.value())

        self.image_metadata.setText(
            f"ID: {capture.cid}\nTimestamp: {capture.timestamp}"
        )

        # delete previous image
        if self.curr_img is not None:
            del self.curr_img

        self.curr_img = QPixmap(capture.filepath)
        self.image_label.setPixmap(self.curr_img)

        # self.ocr_text.setText(capture.text)

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()
