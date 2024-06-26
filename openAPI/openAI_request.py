from openai import OpenAI
from variables import LLM_serverURL, LLM_token, LLM_name

# Completion API
class getCompletion:
    def __init__ (self, API_NAME: str = "v1"):
        self.url = LLM_serverURL + API_NAME
        self.key = LLM_token
        self.model = LLM_name

    def answer(self, USR_MSG: str, FLL_MSG = {""}):
        client = OpenAI(base_url = self.url, api_key = self.key)
        if FLL_MSG != {""}:
            userMessage = FLL_MSG
        else:
            userMessage = [{"role": "user", "content": USR_MSG}]
        completion = client.chat.completions.create(
            model = self.model,
            messages = userMessage,
            temperature=0.7,
        )
        return completion.choices[0].message