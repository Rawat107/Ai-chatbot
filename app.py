from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from openai import OpenAI
import json
import os
from pymongo import MongoClient

load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='/static')

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client.chatbot
collection = db.logs

with open("models/model_prompts.json") as f:
    model_prompts = json.load(f)



def query_openai(prompt):
    try:
        completion = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7,
            top_p = 1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return completion.choices[0].message["content"]
    except Exception as e:
        return f"Error querying model: {e}"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get("input")
    model = data.get("model", "general")

    prompt = model_prompts[model].format(input=user_input)
    response = query_openai(prompt)

    save_to_db(user_input, model, response)

    return jsonify({"response": response})

def save_to_db(user_input, model, response):
    try:
        collection.insert_one({
            "input": user_input,
            "model": model,
            "response": response
        })
    except Exception as e:
        print(f"Error saving to DB: {e}")

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

