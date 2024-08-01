from ai71 import AI71

AI71_MODEL = "tiiuae/falcon-180B-chat"

def call_ai71(prompt,AI71_API_KEY):
    """Calls the AI71 API with a prompt"""
    client = AI71(AI71_API_KEY)
    response = client.chat.completions.create(model=AI71_MODEL, messages=prompt)
    return response