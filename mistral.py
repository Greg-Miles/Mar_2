from settings import API_KEY
import os
#pip install mistralai
from mistralai import Mistral

class TextRequest:

    def __init__(self):
        pass

    def send(self, text: str, model: str) -> dict:
        pass


class ImageRequest:

    def __init__(self):
        pass

    def send(self, image_path: str, model: str) -> dict:
        pass

class ChatFacade:
    def __init__(self):
        self.text_request = TextRequest()
        self.image_request = ImageRequest()

    def select_mode(self)-> int:
        pass

    def select_model(self, mode: int) -> str:
        pass

    def load_image(self, image_path: str) -> str:
        pass

    def ask_question(self, text: str, model: str, image_path: str = None)-> dict:
        pass

    def get_history(self)-> list[tuple[str, dict]]:
        pass

    def clear_history(self)-> None:
        pass