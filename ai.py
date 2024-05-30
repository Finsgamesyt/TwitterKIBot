import requests


class AIAPI:
    def __init__(self, base_url: str, model: str, lang: str):  # needed parameters for Url
        self.baseUrl = base_url
        self.model = model
        self.lang = lang

    # schreibt einen Tweet zu einem gegebenen Thema
    def prompt(self, text: str) -> str:
        headers = {
            "Content-Type": "application/json"  # Ausgabe erfolgt in json
        }
        data = {
            "model": self.model,
            "messages": [
                {  # Aufgabe:
                    "role": "system",
                    "content": f"Du bist ein {self.lang} Twitternutzer und schreibst einen Tweet  zum Thema des gegebenen Prompts. Antworte nur mit dem Tweet in {self.lang} ohne Anführungszeichen. Der Tweet darf nicht über 260 Zeichen enthalten."
                },
                {  # Prompt:
                    "role": "user",
                    "content": text
                }
            ]
        }
        # Request mit Inputs wird gepostet ( AI bekommt Input) (in Url Form)
        response = requests.post(f'{self.baseUrl}/v1/chat/completions', headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']  # gibt Antwort der KI zurück (string)
        else:
            return "error"

    def answer(self, *history: str) -> str:  # Funktion: antwortet auf einen Tweet, der gegeben wir
        headers = {
            "Content-Type": "application/json"
        }
        messages = [{"role": "user", "content": i} for i in history]
        messages.insert(0, {
            "role": "system",
            "content": f"Du bist ein {self.lang} Twitternutzer und beantwortest die vorherigen Tweets. Trage etwas neues zum Gespräch bei und antworte mit nur dem Tweet in {self.lang} ohne Anführungszeichen. Der Tweet darf nicht über 260 Zeichen enthalten."
        })
        data = {
            "model": self.model,
            "messages": messages
        }
        response = requests.post(f'{self.baseUrl}/v1/chat/completions', headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return "error"
