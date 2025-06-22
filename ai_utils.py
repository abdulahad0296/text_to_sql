import google.genai as genai
from config import API_KEY


client = genai.Client(api_key=API_KEY)


#Loading gemini and get sql query as response

def get_response(question, prompt):
    full_prompt = f"{prompt[0]}\n\n{question}"
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",  # or "gemini-2.0-flash" if you want faster, cheaper responses
        contents=full_prompt
    )
    
    return response.text