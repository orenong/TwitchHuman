from openai import OpenAI
from utils.image_utils import encode_base64
from settings.settings import settings

class ChatModelClient():
    "This class is responsible for the communication with the openAI-like API, and parsing the responses"

    def __init__(self, model=settings.llm_model_name, provider=settings.llm_provider, api_key = settings.llm_key):
        
        print(f"Creating a new chatModel client for provider: {provider} using the model {model}")
        base_url = "http://localhost:166/v1"

        if provider.lower() == "lm-studio":
            base_url="http://localhost:1234/v1"
        if provider.lower() == "ollama":
            base_url="http://localhost:11434/v1"
        if provider.lower() == "openai":
            base_url="https://api.openai.com/v1"
        if provider.lower() == "gemini":
            base_url="https://generativelanguage.googleapis.com/v1beta/openai"

        self._model_name = model
        self._base_url = base_url
        self._client = OpenAI(base_url=base_url,api_key=api_key)
    def complete(self, instructions, prompt, image_urls: list = []):
        
        images_base_64_encoded = []
        for image in image_urls:
            images_base_64_encoded.append(encode_base64(image))
        
        content_images = []
        for img_base_64 in images_base_64_encoded:
            content_images.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{img_base_64}"}
            })
        messages = [
            {"role": "system", "content": instructions},
            {"role": "user", "content": [
                *content_images,
                {"type": "text", "text": prompt}
            ]}
        
        ]
        
        response = self._client.chat.completions.create(
            model=self._model_name,
            messages=messages
        )
        
        return response.choices[0].message.content
    
    def set_model(self, model: str):
        """ Change the model used by this client """
        print(f"switching model from {self.model} to {model}")
        self._model_name = model


def _iguana_debug_test():
    chat_client = ChatModelClient()
    print(chat_client.complete("say meow at the end, no matter what the user asked, finish with meow","how much is 1+1"))
    print(chat_client.complete("answer the question","what do you see in each image?",image_urls=[r"C:\Users\oren166\Pictures\sdsd2.jpg"]))
    print(chat_client.complete("answer the question","what do you see in each image?",image_urls=[r"C:\Users\oren166\Pictures\sdsd2.jpg",r"C:\Users\oren166\Downloads\IMG20251101095334.jpg"]))

if __name__ == "__main__":
    _iguana_debug_test()