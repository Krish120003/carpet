from PySide6.QtGui import QPixmap
from pathlib import Path
from db import Capture, conn
from datetime import datetime

import logging
import coloredlogs

coloredlogs.install()

logging.basicConfig()
logger = logging.getLogger("screenshot handler")
logger.setLevel(level=logging.INFO)


def handle_screenshot(image: QPixmap) -> None:
    current_time = datetime.now()

    image_path = Path("data") / f"screenshot_{current_time}.jpeg"

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
