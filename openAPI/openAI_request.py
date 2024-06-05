from openai import OpenAI
from variables import LLM_serverURL, LLM_token

# Completion API
class getCompletion:
    def __init__ (self,  MODEL: str, API_NAME: str = "v1"):
        self.url = LLM_serverURL + API_NAME
        self.key = LLM_token
        self.model = MODEL

    def answer(self, USR_MSG: str, SYS_MSG: str = "_", FLL_MSG = {""}):
        client = OpenAI(base_url = self.url, api_key = self.key)
        if FLL_MSG != {""}:
            userMessage = FLL_MSG
        else:
            userMessage = [{"role": "user", "content": USR_MSG}]
            if SYS_MSG != "_":
                userMessage = [{"role": "system", "content": SYS_MSG}, + {"role": "user", "content": USR_MSG}]
        completion = client.chat.completions.create(
            model = self.model,
            messages=
               userMessage
            ,
            temperature=0,
        )
        return completion.choices[0].message