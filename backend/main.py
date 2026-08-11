from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)
CORS(app)


@app.route("/")
def health_check():
    return jsonify({"status": "ok", "message": "FoodRescue AI backend running"})

@app.route("/analyze-fridge", methods=["POST"])
def analyze_fridge():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image_file = request.files["image"]
    image_bytes = image_file.read()

    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = """
    Look at this fridge/ingredients photo. List only the food items you can 
    clearly identify. Return ONLY a comma-separated list of ingredient names, 
    nothing else. Example: eggs, milk, tomatoes, cheese
    """

    response = model.generate_content([
        prompt,
        {"mime_type": "image/jpeg", "data": image_bytes}
    ])

    ingredients_text = response.text.strip()
    ingredients_list = [item.strip() for item in ingredients_text.split(",")]

    return jsonify({"ingredients": ingredients_list})

if __name__ == "__main__":
    app.run(debug=True, port=5000)