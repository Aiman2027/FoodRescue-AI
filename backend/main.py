import os
import json
import base64
import mimetypes
import requests
from urllib.parse import quote


from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from google import genai
from google.genai import types




load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing in .env")

client = genai.Client(api_key=GEMINI_API_KEY)


GEMINI_MODEL = "gemini-3.5-flash-lite"




app = FastAPI(
    title="FoodRescue AI API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "bn": "Bengali",
    "ta": "Tamil",
    "te": "Telugu",
    "mr": "Marathi",
    "gu": "Gujarati",
    "kn": "Kannada",
    "ml": "Malayalam",
    "pa": "Punjabi",
    "ur": "Urdu",
}


def get_language_name(language_code: str) -> str:
    return SUPPORTED_LANGUAGES.get(language_code, "English")


def clean_ingredient_list(text: str):
    text = (text or "").strip()

    text = (
        text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:
        data = json.loads(text)

        if isinstance(data, list):
            return [
                str(item).strip()
                for item in data
                if str(item).strip()
            ]
    except Exception:
        pass

    
    text = text.replace("\n", ",")

    ingredients = [
        item.strip()
        for item in text.split(",")
        if item.strip()
    ]

    return ingredients


def clean_json_text(text: str):
    text = (text or "").strip()
    return (
        text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )



@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "FoodRescue AI backend running",
        "framework": "FastAPI",
        "ai": "Gemini 2.5 Flash"
    }




@app.post("/analyze-fridge")
async def analyze_fridge(
    images: list[UploadFile] = File(...),
    language: str = Form("en")
):
    if not images:
        return JSONResponse(
            status_code=400,
            content={"error": "No images provided"}
        )

    if len(images) > 5:
        images = images[:5]

    language_name = get_language_name(language)
    all_ingredients = []

    for image_file in images:
        try:
            image_bytes = await image_file.read()

            if not image_bytes:
                continue

            mime_type = (
                image_file.content_type
                or mimetypes.guess_type(image_file.filename or "")[0]
                or "image/jpeg"
            )

            prompt = f"""
You are FoodRescue AI.

Analyze this fridge/kitchen image carefully.

Identify visible:
- food items
- ingredients
- vegetables
- fruits
- dairy
- grains
- packaged food
- leftovers
- sauces
- cooking ingredients

Do not invent items that are not reasonably visible.

Return ONLY a JSON array of ingredient names.

Example:
["eggs", "milk", "tomatoes", "cheese"]

The ingredient names should be written in {language_name}.

Do not include quantities.
Do not include explanations.
Do not use markdown.
"""

            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=[
                    types.Part.from_bytes(
                        data=image_bytes,
                        mime_type=mime_type
                    ),
                    prompt
                ],
                config=types.GenerateContentConfig(
                    temperature=0.1
                )
            )

            ingredients_text = response.text or ""

            ingredients = clean_ingredient_list(ingredients_text)
            all_ingredients.extend(ingredients)

        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={
                    "error": f"Failed to analyze image: {str(e)}"
                }
            )

    
    unique_ingredients = []
    seen = set()

    for item in all_ingredients:
        normalized = item.strip().lower()

        if normalized and normalized not in seen:
            seen.add(normalized)
            unique_ingredients.append(item.strip())

    return {
        "ingredients": unique_ingredients,
        "language": language
    }




@app.post("/analyze-fridge-audio")
async def analyze_fridge_audio(
    audio: UploadFile = File(...),
    language: str = Form("en")
):
    language_name = get_language_name(language)

    try:
        audio_bytes = await audio.read()

        if not audio_bytes:
            return JSONResponse(
                status_code=400,
                content={"error": "Empty audio file"}
            )

        mime_type = (
            audio.content_type
            or mimetypes.guess_type(audio.filename or "")[0]
            or "audio/wav"
        )

        prompt = f"""
You are FoodRescue AI.

Listen to the user's audio.

First, understand/transcribe what the user says.
Then extract ONLY the food ingredients mentioned by the user.

Remove:
- quantities
- measurements
- unnecessary descriptions

For example:

"half a block of cheese and two tomatoes"

should become:

["cheese", "tomatoes"]

Return ONLY valid JSON in this exact structure:

{{
  "transcript": "what the user said",
  "ingredients": ["ingredient 1", "ingredient 2"]
}}

Write ingredient names in {language_name}.
Do not explain anything.
Do not use markdown.
"""

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[
                types.Part.from_bytes(
                    data=audio_bytes,
                    mime_type=mime_type
                ),
                prompt
            ],
            config=types.GenerateContentConfig(
                temperature=0.1
            )
        )

        result_text = clean_json_text(response.text or "")

        try:
            result = json.loads(result_text)
        except json.JSONDecodeError:
            result = {
                "transcript": response.text or "",
                "ingredients": clean_ingredient_list(response.text or "")
            }

        ingredients = result.get("ingredients", [])
        if not isinstance(ingredients, list):
            ingredients = clean_ingredient_list(str(ingredients))

        return {
            "ingredients": ingredients,
            "transcript": result.get("transcript", ""),
            "language": language
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": f"Failed to analyze audio: {str(e)}"
            }
        )




@app.post("/generate-recipe")
async def generate_recipe(data: dict):
    if not data or "ingredients" not in data:
        return JSONResponse(
            status_code=400,
            content={"error": "No ingredients provided"}
        )

    ingredients = data.get("ingredients", [])
    servings = data.get("servings", 2)
    language = data.get("language", "en")

    language_name = get_language_name(language)

   

    try:
        servings = int(servings)
    except Exception:
        servings = 2

    if servings < 1:
        servings = 1

    if servings > 10:
        servings = 10

    if not ingredients:
        return JSONResponse(
            status_code=400,
            content={"error": "At least one ingredient is required"}
        )

    ingredients_text = ", ".join(
        str(item).strip()
        for item in ingredients
    )

    prompt = f"""
You are a professional chef and food-waste reduction assistant.

Available ingredients:

{ingredients_text}

Create EXACTLY TWO different practical recipes.

Important rules:

1. Use the available ingredients as the main ingredients.
2. You may use common pantry staples:
   salt, pepper, oil, water and basic spices.
3. Do not require expensive or unusual ingredients.
4. Recipes should be realistic.
5. Recipes should serve exactly {servings} people.
6. CRITICAL LANGUAGE RULE: The ENTIRE response — including
   "recipe_name", "prep_time", "servings", and EVERY single
   step inside "steps" — MUST be written completely in
   {language_name} language and script. Do not mix English
   words. Do not translate only some fields and leave others
   in English. ALL text values in the JSON must be in
   {language_name}.
7. Return ONLY valid JSON.
8. No markdown.
9. No explanation outside JSON.

Return exactly this structure (translate all string VALUES
into {language_name}, keep the JSON keys in English exactly
as shown):

[
  {{
    "recipe_name": "Recipe name in {language_name}",
    "prep_time": "20 mins (in {language_name})",
    "servings": "{servings} people (in {language_name})",
    "steps": [
      "Step 1 in {language_name}",
      "Step 2 in {language_name}",
      "Step 3 in {language_name}",
      "Step 4 in {language_name}"
    ]
  }},
  {{
    "recipe_name": "Second recipe in {language_name}",
    "prep_time": "25 mins (in {language_name})",
    "servings": "{servings} people (in {language_name})",
    "steps": [
      "Step 1 in {language_name}",
      "Step 2 in {language_name}",
      "Step 3 in {language_name}",
      "Step 4 in {language_name}"
    ]
  }}
]
"""

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7
            )
        )

        recipe_text = clean_json_text(response.text or "")
        recipes_json = json.loads(recipe_text)

        if isinstance(recipes_json, dict):
            recipes_json = [recipes_json]

        return {
            "recipes": recipes_json,
            "language": language
        }

    except json.JSONDecodeError:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Could not parse recipe",
                "raw": recipe_text
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": f"Recipe generation failed: {str(e)}"
            }
        )


@app.post("/generate-recipe-image")
async def generate_recipe_image(data: dict):
    if not data or "recipe_name" not in data:
        return JSONResponse(
            status_code=400,
            content={"error": "No recipe name provided"}
        )

    recipe_name = data.get("recipe_name", "Food")

    prompt = (
        f"A high-quality, appetizing professional food photography "
        f"shot of {recipe_name}, plated beautifully, natural lighting, "
        f"restaurant-style presentation"
    )

    try:
        encoded_prompt = quote(prompt)
        image_url = (
            f"https://image.pollinations.ai/prompt/{encoded_prompt}"
            f"?width=1024&height=1024&nologo=true"
        )

        response = requests.get(image_url, timeout=60)

        if response.status_code != 200:
            return JSONResponse(
                status_code=500,
                content={"error": f"Image generation failed: {response.status_code}"}
            )

        image_base64 = base64.b64encode(response.content).decode("utf-8")

        return {"image": image_base64}

    except requests.exceptions.Timeout:
        return JSONResponse(
            status_code=500,
            content={"error": "Image generation timed out. Please try again."}
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Image generation failed: {str(e)}"}
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
