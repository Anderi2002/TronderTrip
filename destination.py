import urllib.request

class Destination:
    def __init__(self, name: str, image_url: str, tags: list[str]) -> None:
        if name.endswith("ene"):
            name = name[:-1]
        self.name = name
        self.image_url = image_url
        self.tags = tags

    @staticmethod
    def download_img(destination) -> None:
        urllib.request.urlretrieve(destination.image_url, f"images/{destination.name}.jpg")