# 🍃 FoodRescue AI

**Turn your fridge into a feast with AI.**

🔗 **[Live Demo](https://foodrescue-ai-yerau4q22hpq7ck349hew2.streamlit.app/)**

FoodRescue AI looks at what you already have — from a photo, multiple photos, or even a voice note — and turns it into a real, cookable recipe. Built to cut everyday food waste by helping people cook with what's already in the fridge instead of buying more.

---

## ✨ Features

- **📷 Multiple ways to describe your fridge**
  - Take a live photo with your camera
  - Upload up to 5 photos at once
  - Or just speak out loud what you have — it gets transcribed and turned into an ingredient list

- **🧠 Smart ingredient recognition** — powered by Gemini Vision, combines results across all your photos into one clean list

- **✅ Full control before cooking** — review, edit, add, or remove any detected ingredient, and set quantities before generating a recipe

- **🍽️ Personalized recipe generation** — choose servings (1–10), get 2 recipe options to choose from, each with prep time, servings, and step-by-step instructions

- **🎨 AI-generated dish photo** — see a preview of your finished meal before you start cooking

- **🌐 Multilingual** — UI supports English, Hindi, Bengali, Tamil, Telugu, Marathi, Gujarati, Kannada, Malayalam, Punjabi, and Urdu

- **🎬 Fully animated visuals** — the "How It Works" section uses lightweight CSS/HTML animations (a scanning camera, an orbiting AI core, a steaming dish) instead of static images, so no image assets are required for the walkthrough

---

## 🧭 How to Use

1. **Pick your language** — use the language dropdown at the top to choose whichever of the 11 supported languages you're most comfortable with. The entire UI (including AI-generated recipes) switches to that language.

2. **Tell the app what's in your fridge** — in the "Get Started" card, choose one of three input methods:
   - **📷 Take a photo** — turn on your camera and snap up to 5 pictures of your fridge/shelves
   - **📁 Upload files** — upload up to 5 existing photos instead
   - **🎤 Describe by voice** — just say out loud what you have (e.g. *"I have eggs, half a block of cheese, some spinach, and leftover rice"*) and the app transcribes it

3. **Let AI detect the ingredients** — click **🔍 Analyze Ingredients**. Gemini Vision (or Gemini's audio understanding for voice notes) scans everything and builds a combined ingredient list.

4. **Review and edit the ingredient table** — an editable table appears where you can:
   - ✅ Toggle "Use?" to include or exclude an ingredient from the recipe
   - ✏️ Add a quantity next to any ingredient (optional)
   - ➕ Add ingredients the AI missed, or ❌ remove ones it got wrong

5. **Choose your servings** — set how many people you're cooking for, from **1 to 10**.

6. **Generate your recipe** — click **🍽️ Generate Recipes**. The app returns **2 different recipe options** built only from your selected ingredients (plus basic pantry staples like salt, oil, and spices).

7. **Pick one and cook** — select whichever recipe you like better. You'll get the full prep time, servings, an AI-generated photo of the finished dish, and clear step-by-step instructions to follow — turning what would've been food waste into a real meal. 🥦

---

## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | [Streamlit](https://streamlit.io/) |
| Backend | FastAPI , Python |
| AI Vision, Audio & Text | Google Gemini (Vision, audio transcription, and text generation) |
| Recipe dish images | [Pollinations.ai](https://pollinations.ai/) (free text-to-image API) |
| Data handling | `pandas` for the editable ingredients table |
| Styling | Custom CSS (dark theme, glassmorphism navbar, CSS keyframe animations) |

---

## 📁 Project Structure

```
foodrescue-ai/
├── frontend/
│   ├── app.py                  # Main Streamlit app
│   ├── image/                  # Logo & any static assets (optional)
│   │   └── foodrescue_icon_256.png
│   └── translations/           # One JSON file per supported language
│       ├── en.json
│       ├── hi.json
│       ├── bn.json
│       └── ...
└── backend/
    ├── main.py                 # Flask/FastAPI server (Gemini + Pollinations.ai calls)
    └── requirements.txt
```

---

## 🔌 Backend API Contract

The frontend expects a backend running at `BACKEND_URL` (default `http://127.0.0.1:8000`) with these endpoints:

| Endpoint | Method | Purpose |
|---|---|---|
| `/analyze-fridge` | `POST` (multipart, field `images`, plus `language`) | Returns `{"ingredients": [...]}` detected across all uploaded photos |
| `/analyze-fridge-audio` | `POST` (multipart, field `audio`, plus `language`) | Transcribes the voice note and returns `{"ingredients": [...]}` |
| `/generate-recipe` | `POST` (JSON: `ingredients`, `servings`, `language`) | Returns `{"recipes": [ {recipe_name, prep_time, servings, steps}, ... ]}` (2 options) |
| `/generate-recipe-image` | `POST` (JSON: `recipe_name`) | Returns `{"image": "<base64-encoded PNG/JPEG>"}` generated via Pollinations.ai |

> The frontend gracefully handles connection errors, timeouts, and malformed responses with user-facing error messages.

---

## 🚀 Getting Started

### 1. Clone / open the project

```bash
cd foodrescue-ai/frontend
```

### 2. Install dependencies

```bash
pip install streamlit pandas requests
```

Backend dependencies (in `backend/requirements.txt`) include `fastapi`/`flask`, `uvicorn`, `google-genai`, `python-dotenv`, `requests`, and `python-multipart`.

### 3. Set your Gemini API key (backend)

Create a `.env` file inside `backend/`:

```
GEMINI_API_KEY=your_key_here
```

Get a free key from [Google AI Studio](https://aistudio.google.com/apikey).

### 4. (Optional) Set your backend URL (frontend)

By default the app looks for the backend at `http://127.0.0.1:8000`. To point elsewhere:

```bash
# Windows (PowerShell)
$env:BACKEND_URL="http://127.0.0.1:5000"

# macOS / Linux
export BACKEND_URL="http://127.0.0.1:5000"
```

### 5. Run the backend

Start your Flask/FastAPI server in a **separate terminal**:

```bash
cd backend
uvicorn main:app --reload --port 8000
```

### 6. Run the Streamlit app

```bash
cd frontend
streamlit run app.py
```

The app opens automatically at **http://localhost:8501**.

> ⚠️ If you see "Backend not reachable", it means step 5 wasn't started or is running on a different port than `BACKEND_URL` points to.

---

## 🌐 Adding / Editing Translations

All UI text is pulled through a single helper:

```python
get_text("some_key", "Fallback English text")
```

- If `translations/<lang_code>.json` has `"some_key"`, that value is shown.
- If the key is **missing**, the English fallback text is shown instead — this is why partial translations look like "only some sections changed language."

To fully translate a language, its JSON file needs an entry for **every** key used via `get_text(...)` across `app.py` (hero text, "Why Choose" cards, "How It Works" steps, footer, etc. — not just the input panel).

**Tip:** grep the codebase for `get_text(` to generate a full list of keys and their English defaults, then translate that whole list into each `translations/<lang>.json` file.

---

## 🖌️ Customization

- **Colors / theme** — all CSS lives in one `st.markdown(...)` block near the top of `app.py`; the palette is cyan/blue (`#22d3ee`, `#3b82f6`) on a dark navy background.
- **Step visuals** — Steps 1–3 in "How It Works" are pure CSS/HTML animations (no image files needed):
  - Step 1: scanning camera with pulsing ingredient icons
  - Step 2: orbiting ingredient icons around a glowing "AI" core
  - Step 3: a plate with rising steam and floating info badges
- **Feature cards** — edit the `why_features` list to change the "Why Choose FoodRescue AI?" section.
- **Footer** — fully driven by `get_text(...)` calls, easy to re-brand or relink.

---

## ⚠️ Known Limitations

- **Gemini free-tier rate limits** — this project uses the **free tier** of the Google Gemini API, which has a **daily request quota**. Once that quota is used up for the day, ingredient detection and recipe generation will fail (you'll see an error from the backend) until the quota resets. For production or heavy usage, upgrade to a paid Gemini API plan.
- **Pollinations.ai image generation** — dish images are generated via Pollinations.ai's free API. Since it's a free/shared service, image generation can occasionally be slow or briefly unavailable during high demand.
- **Render free-tier cold starts** — if the backend is hosted on Render's free tier, it spins down after inactivity; the first request after idle time can take 30–50+ seconds to respond while the server wakes up.
- **Translation coverage** — a language only looks fully translated if its JSON file has every key used in the app; missing keys silently fall back to English (see "Adding / Editing Translations" above).

---

## 🛣️ Roadmap Ideas

- [ ] Save favorite recipes per user
- [ ] Nutrition breakdown per recipe
- [ ] Shopping list for missing ingredients
- [ ] Shareable recipe cards (image + steps as a downloadable PNG/PDF)

---

## 📄 License

Add your preferred license here (MIT, Apache 2.0, etc.).

---

*Built to make every ingredient count. Cook more, waste less.* 🥦
