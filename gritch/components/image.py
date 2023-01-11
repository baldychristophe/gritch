import io
from PIL import Image as pillow_image

from rich.console import RenderableType
from textual.widgets import Static

import requests

from rich_pixels import Pixels


class Image(Static):
    def __init__(
            self,
            image_url: str,
            size: tuple[int, int] = None,
            *,
            name=None,
            id=None,
            classes=None,
    ):
        super().__init__(name=name, id=id, classes=classes)
        self.image_url = image_url
        self.image_size = size

    def render(self) -> RenderableType:
        raw_request = requests.get(self.image_url)
        if raw_request.status_code != 200:
            return ""

        image_object = pillow_image.open(io.BytesIO(raw_request.content))
        if self.image_size:
            image_object.thumbnail(self.image_size)

        return Pixels.from_image(image_object)
