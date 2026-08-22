# 🍃 FoodRescue AI

**Turn your fridge into a feast with AI.**

FoodRescue AI looks at what you already have — from a photo, multiple photos, or even a voice note — and turns it into a real, cookable recipe. Built to cut everyday food waste by helping people cook with what's already in the fridge instead of buying more.

---

## ✨ Features

- **📷 Multiple ways to describe your fridge**
  - Take a live photo with your camera
  - Upload up to 5 photos at once
  - Or just speak out loud what you have — it gets transcribed and turned into an ingredient list

- **🧠 Smart ingredient recognition** — powered by Gemini Vision, combines results across all your photos into one clean list

- **✅ Full control before cooking** — review, edit, add, or remove any detected ingredient, and set quantities before generating a recipe

- **🍽️ Personalized recipe generation** — pick your servings, get 2 recipe options to choose from, each with prep time, servings, and step-by-step instructions

- **🎨 AI-generated dish photo** — see a preview of your finished meal before you start cooking

- **🌐 Multilingual** — UI supports English, Hindi, Bengali, Tamil, Telugu, Marathi, Gujarati, Kannada, Malayalam, Punjabi, and Urdu

- **🎬 Fully animated visuals** — the "How It Works" section uses lightweight CSS/HTML animations (a scanning camera, an orbiting AI core, a steaming dish) instead of static images, so no image assets are required for the walkthrough

---

## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | [Streamlit](https://streamlit.io/) |
| Backend | Flask  (any server exposing the endpoints below) |
| AI Vision & Text | Google Gemini (Vision + text generation) |
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
    └── (your Flask/FastAPI server exposing the endpoints below)
```

---

## 🔌 Backend API Contract

The frontend expects a backend running at `BACKEND_URL` (default `http://127.0.0.1:8000`) with these endpoints:

| Endpoint | Method | Purpose |
|---|---|---|
| `/analyze-fridge` | `POST` (multipart, field `images`, plus `language`) | Returns `{"ingredients": [...]}` detected across all uploaded photos |
| `/analyze-fridge-audio` | `POST` (multipart, field `audio`, plus `language`) | Transcribes the voice note and returns `{"ingredients": [...]}` |
| `/generate-recipe` | `POST` (JSON: `ingredients`, `servings`, `language`) | Returns `{"recipes": [ {recipe_name, prep_time, servings, steps}, ... ]}` (2 options) |
| `/generate-recipe-image` | `POST` (JSON: `recipe_name`) | Returns `{"image": "<base64-encoded PNG/JPEG>"}` |

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

### 3. (Optional) Set your backend URL

By default the app looks for the backend at `http://127.0.0.1:8000`. To point elsewhere:

```bash
# Windows (PowerShell)
$env:BACKEND_URL="http://127.0.0.1:5000"

# macOS / Linux
export BACKEND_URL="http://127.0.0.1:5000"
```

### 4. Run the backend

Start your Flask/FastAPI server (the one implementing the endpoints above) in a **separate terminal**:

```bash
python backend/app.py
```

### 5. Run the Streamlit app

```bash
streamlit run app.py
```

The app opens automatically at **http://localhost:8501**.

> ⚠️ If you see "Backend not reachable", it means step 4 wasn't started or is running on a different port than `BACKEND_URL` points to.

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
