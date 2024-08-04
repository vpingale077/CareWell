from ai71 import AI71

AI71_MODEL = "tiiuae/falcon-40b-instruct"

def call_ai71(prompt,AI71_API_KEY):
    """Calls the AI71 API with a prompt"""
    client = AI71(AI71_API_KEY)
    print("call_ai71",prompt)
    response = client.chat.completions.create(model=AI71_MODEL, messages=prompt)
    return response