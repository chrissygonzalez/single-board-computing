import time
import random
import board
from adafruit_pyportal import PyPortal
from adafruit_display_shapes.circle import Circle

WIDTH = board.DISPLAY.width
HEIGHT = board.DISPLAY.height

SEARCH_URL = 'https://collectionapi.metmuseum.org/public/collection/v1/search?q=hasImages'
OBJECT_URL = "https://collectionapi.metmuseum.org/public/collection/v1/objects/"
image_count = 0
object_ids = []
object_id = 0

class MyPortal(PyPortal):
    def set_json_path(self, new_path):
        print('setting json_path')
        self.json_path = new_path
        print(self.json_path)

    def fetch_url(self, refresh_url=None, timeout=10, force_content_type=None):
        if refresh_url:
            self.url = refresh_url
        response = self.network.fetch(self.url, headers=self._headers, timeout=timeout)
        json = response.json()
        return json

    def fetch_image(self, json_data):
        try:
            filename, position = self.network.process_image(
                json_data, self.peripherals.sd_check()
            )
            if filename and position is not None:
                self.set_text('', 0)
                self.graphics.set_background(filename, position)
        except ValueError as error:
            print("Error displaying cached image. " + error.args[0])
            if self._default_bg is not None:
                self.graphics.set_background(self._default_bg)
        except KeyError as error:
            print("Error finding image data. '" + error.args[0] + "' not found.")
            self.set_background(self._default_bg)

BACKGROUND_FILE = "/met.bmp"

pyportal = MyPortal(default_bg=BACKGROUND_FILE,
                    image_json_path=['primaryImageSmall'],
                    image_resize=(320, 225),
                    image_position=(0, 0),
                    text_position = (15, HEIGHT - 9),
                    text_font ="/fonts/OpenSans-9.bdf",
                    text_color = 0xFFFFFF,
                    )

while image_count == 0:
    response = None
    try:
        print("retrieving url:", SEARCH_URL)
        response = pyportal.fetch_url(SEARCH_URL)
        image_count = response['total']
        object_ids = response['objectIDs']

    except (RuntimeError, KeyError, TypeError) as e:
        print("An error occured, retrying! -", e)


pyportal.set_json_path('title')
circle = Circle(WIDTH - 8, HEIGHT - 7, 5, fill=0)
pyportal.splash.append(circle)

while True:
    object_id = object_ids[random.randint(1, image_count)]

    try:
        circle.fill = 0xFF0000
        print("retrieving url:", (OBJECT_URL + str(object_id)))
        image_response = pyportal.fetch_url(OBJECT_URL + str(object_id))
        pyportal.fetch_image(image_response)
        pyportal.set_text(image_response['title'], 0)
        circle.fill = 0

    except (RuntimeError, KeyError, TypeError) as e:
        print("An error occured, retrying! -", e)

    stamp = time.monotonic()
    # wait 5 minutes before getting again
    while (time.monotonic() - stamp) < (5*60):
        # or, if they touch the screen, fetch immediately!
        if pyportal.touchscreen.touch_point:
            break
