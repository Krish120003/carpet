from PySide6.QtGui import QPixmap
from pathlib import Path
from db import Capture, conn
from datetime import datetime
import sys
import logging
import coloredlogs

coloredlogs.install()

logging.basicConfig()
logger = logging.getLogger("screenshot handler")
logger.setLevel(level=logging.INFO)

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

        capture = Capture.create(
            timestamp=current_time,
            filepath=image_path,
        )

        capture.save()

        logger.info(f"Saved screenshot to {image_path.absolute()}")

    return


def get_asset_path(basedir: Path) -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        print("running in a PyInstaller bundle")
        # check if on osx
        if sys.platform == "darwin":
            return basedir.parent / "Resources" / "assets"

    return basedir.parent / "assets"
