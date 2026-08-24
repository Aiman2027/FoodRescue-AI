# 📐 FoodRescue AI — Technical Design Document

> See [`ARCHITECTURE.md`](./ARCHITECTURE.md) for the visual system diagram. This document explains the *why* and *how* behind it.

## 1. Overview

FoodRescue AI is a two-service application:

- **Frontend** — a Streamlit app (`frontend/app.py`) that owns the UI, session state, and language switching.
- **Backend** — a stateless FastAPI service (`backend/main.py`) that wraps the Google Gemini API (Vision, Audio, Text) and the Pollinations.ai image API behind four simple JSON endpoints.

The frontend never calls Gemini or Pollinations.ai directly — every AI call goes through the backend, so the `GEMINI_API_KEY` never leaves the server.

---

## 2. Data Flow

### 2.1 Ingredient detection (image path)

1. User selects **📷 Take a photo** or **📁 Upload files** and provides up to 5 images.
2. On clicking **Analyze Ingredients**, the frontend builds a `multipart/form-data` request containing all image bytes plus the current `language` code, and POSTs it to `/analyze-fridge`.
3. The backend loops over each image, sends it to `gemini-3.5-flash-lite` as an inline `Part.from_bytes(...)` alongside a structured prompt asking for a **JSON array of ingredient names only**, in the user's selected language.
4. Results from all images are merged and de-duplicated (case-insensitive) server-side.
5. The backend returns `{"ingredients": [...], "language": "..."}`.
6. The frontend stores this in `st.session_state.detected_ingredients` and builds a fresh `pandas.DataFrame` for the editable table.

### 2.2 Ingredient detection (voice path)

1. User selects **🎤 Describe by voice** and records a note via `st.audio_input`.
2. The frontend POSTs the raw audio bytes to `/analyze-fridge-audio`.
3. The backend sends the audio directly to Gemini with a prompt asking it to **transcribe first, then extract only ingredient names** (stripping quantities/units), returning a strict JSON object: `{"transcript": "...", "ingredients": [...]}`.
4. If Gemini's response isn't valid JSON (rare), the backend falls back to a naive comma/newline split of the raw text so the app never hard-crashes on a parsing failure.

### 2.3 Recipe generation

1. Once the user finalizes the ingredient table (toggling "Use?", editing quantities, adding/removing rows) and picks **servings (1–10)**, clicking **Generate Recipes** POSTs `{ingredients, servings, language}` (JSON) to `/generate-recipe`.
2. The backend prompts Gemini to return **exactly two** complete recipes as a JSON array, each with `recipe_name`, `prep_time`, `servings`, and a `steps` array — with an explicit instruction that **every string value**, not just some, must be in the target language.
3. The frontend renders both options side-by-side (`st.columns`) with `st.metric` KPIs for prep time/servings and a 3-step preview; the user picks one via **✅ Make This Recipe**.

### 2.4 Dish image generation

1. Once a recipe is selected, the frontend POSTs `{"recipe_name": "..."}` to `/generate-recipe-image`.
2. The backend builds a photography-style prompt and calls Pollinations.ai's free image endpoint (`image.pollinations.ai/prompt/<encoded-prompt>`), then re-encodes the returned image bytes as base64.
3. The frontend decodes and renders the image inside a fixed-size, rounded card (`object-fit: cover`) so every dish photo looks consistent regardless of the image's native aspect ratio.

---

## 3. API Integration Strategy

| Concern | Approach |
|---|---|
| **Statelessness** | The backend holds no session state — every request is self-contained. All session state (uploaded images, ingredient edits, chosen recipe) lives in `st.session_state` on the frontend. |
| **Timeouts** | Image/audio analysis: 120s timeout. Recipe + image generation: 180s timeout — generous enough for cold-start latency on Render's free tier. |
| **Error handling** | Every backend call is wrapped in `try/except` on the frontend for `ConnectionError`, `Timeout`, and generic exceptions, each surfaced as a translated, user-facing `st.error()` rather than a raw traceback. |
| **CORS** | The backend allows all origins (`allow_origins=["*"]`) since it's a public API consumed only by the Streamlit frontend, with no cookie-based auth to protect. |
| **Secrets** | `GEMINI_API_KEY` lives only in Render's Environment Variables (never committed). `BACKEND_URL` lives in Streamlit Cloud's Secrets, pointing the frontend at the deployed backend instead of `localhost`. |
| **Prompt engineering** | Every prompt is an f-string built dynamically from the request (language name, ingredient list, servings count), with explicit output-format constraints ("Return ONLY a JSON array", "no markdown", "no explanations") so responses can be parsed deterministically. |

---

## 4. Logic Modules

### Frontend (`frontend/app.py`)
- **Translation layer** — a single `get_text(key, default)` helper backed by per-language JSON files in `frontend/translation/`; any missing key silently falls back to English.
- **Input capture module** — three mutually exclusive input modes (camera / upload / voice), each managing its own `st.session_state` keys (`camera_images`, `confirmed_uploads`, `fridge_audio`).
- **Ingredient review module** — a `pandas.DataFrame`-backed `st.data_editor` with a checkbox column ("Include in Recipe"), letting users correct AI mistakes before generation.
- **Recipe module** — handles the two-option selection flow and the final recipe view, including lazy image generation (only fetched once, cached in `st.session_state.recipe_image`).
- **Presentation layer** — pure CSS/HTML animations (`ai-orbit-wrap`, `snap-wrap`, `dish-wrap`) used in the "How It Works" walkthrough instead of static images, keeping the repo asset-light.

### Backend (`backend/main.py`)
- **Vision module** (`/analyze-fridge`) — per-image Gemini calls + ingredient de-duplication.
- **Audio module** (`/analyze-fridge-audio`) — transcription + extraction with a JSON-parsing fallback.
- **Recipe module** (`/generate-recipe`) — dual-recipe generation with strict language enforcement.
- **Image module** (`/generate-recipe-image`) — Pollinations.ai proxy + base64 encoding.

---

## 5. Known Constraints

- Gemini's **free-tier daily quota** can be exhausted under heavy testing, after which all AI endpoints return an error until the quota resets.
- Render's **free-tier cold starts** add 30–50s latency to the first request after a period of inactivity.
- See the main [`README.md`](./README.md) "Known Limitations" section for the full list.

