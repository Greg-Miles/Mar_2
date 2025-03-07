from settings import API_KEY
import os, base64
#pip install mistralai
from mistralai import Mistral


class TextRequest:

    def __init__(self, api_key: str):
        self.client = Mistral(api_key=api_key)


    def send(self, text: str, model: str) -> dict:

        chat_response = self.client.chat.complete(
            model=model,
            messages=[{
                "role": "user",
                "content": text
            }]
        )
        return {
            "response": chat_response.choices[0].message.content,
            "model": model
        }


class ImageRequest:

    def __init__(self, api_key: str):
        self.client = Mistral(api_key=api_key)

    def send(self, image_path: str, model: str) -> dict:
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
            base64_image = base64.b64encode(image_data).decode('utf-8')
            response = self.client.chat.complete(
                model=model,
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        },
                        {
                            "type": "text",
                            "text": "Опиши это изображение"
                        }
                    ]
                }]
            )
            return {
                "response": response.choices[0].message.content,
                "model": model
            }


class ChatFacade:
    def __init__(self, api_key: str):
        self.text_request = TextRequest(api_key)
        self.image_request = ImageRequest(api_key)
        self.history = []

    def select_mode(self)-> int:
        mode_str = input("""Выберите режим работы: 
                     1 - текст 
                     2 - изображение 
                    """)
        try:
            mode = int(mode_str)
            if mode not in [1, 2]:
                print("Некорректный ввод. Пожалуйста, введите 1 или 2.")
                return self.select_mode()
        except ValueError:
            print("Некорректный ввод. Пожалуйста, введите число.")
            return self.select_mode()
        return mode

    def select_model(self, mode: int) -> str:
        if mode == 1:
            model = 'mistral-small-latest'
        elif mode == 2:
            model = 'pixtral-12b'
        return model

    def load_image(self, image_path: str) -> str:
        if not os.path.exists(image_path):
            raise FileNotFoundError("Изображение не найдено")
        return image_path

    def ask_question(self, text: str, model: str, image_path: str = None)-> dict:

        if image_path:
            response = self.image_request.send(image_path, model)
        else:
            response = self.text_request.send(text, model)
        
        self.history.append((text, response))
        return response

    def get_history(self)-> list[tuple[str, dict]]:
        return self.history

    def clear_history(self)-> None:
        self.history = []

def main():
    chat = ChatFacade(API_KEY)
    while True:
        mode = chat.select_mode()
        model = chat.select_model(mode)
        
        if mode == 1:
            question = input("Введите ваш вопрос: ")
            response = chat.ask_question(question, model)
            print("Ответ:", response["response"])
        
        elif mode == 2:
            image_path = input("Введите путь к изображению: ")
            try:
                image_path = chat.load_image(image_path)
                response = chat.ask_question("", model, image_path)
                print("Описание изображения:", response["response"])
            except FileNotFoundError as e:
                print(e)
        
        continue_chat = input("Продолжить? (да/нет): ")
        if continue_chat.lower() != "да":
            break

if __name__ == "__main__":
    main()