from PySide6.QtGui import QPixmap
from pathlib import Path
from db import Capture, conn
from datetime import datetime
import sys
import logging
import coloredlogs

from ocrmac import ocrmac

coloredlogs.install()

logging.basicConfig()
logger = logging.getLogger("screenshot handler")
logger.setLevel(level=logging.DEBUG)

app_basedir = Path(__file__).parent


def handle_screenshot(image: QPixmap) -> None:
    current_time = datetime.now()

    image_path = app_basedir / Path("data") / f"screenshot_{current_time}.jpeg"

    if not image_path.parent.exists():
        image_path.parent.mkdir()

    # create a capture
    with conn.atomic():
        # save the image
        image.save(str(image_path), format="jpeg", quality=30)

        # get the ocr text
        text = ocr(str(image_path))
        # text = ""

        capture = Capture.create(
            timestamp=current_time,
            filepath=image_path,
            text=text,
        )

        capture.save()

        logger.info(f"Saved screenshot to {image_path.absolute()}")

    return


def get_asset_path(basedir: Path) -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        logger.info("running in a PyInstaller bundle")
        # check if on osx
        if sys.platform == "darwin":
            return basedir.parent / "Resources" / "assets"

    return basedir.parent / "assets"


def ocr(img: str) -> str:
    t1 = datetime.now()
    annotations = ocrmac.OCR(img, recognition_level="fast").recognize()
    t2 = datetime.now()

    # filter to every annotation with a confidence of 0.8 or higher
    annotations = [a[0] for a in annotations if a[1] >= 0.8]

    logger.info(f"OCR completed for image {img}")
    logger.debug(f"OCR results: {annotations}")
    logger.info(f"OCR took {(t2 - t1).total_seconds()} seconds")

    return "\n".join(annotations)
