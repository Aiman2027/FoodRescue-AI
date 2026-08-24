# 🏗️ FoodRescue AI — System Architecture

This diagram shows how a request flows through FoodRescue AI, from the user's camera/upload/voice input all the way to a generated recipe with an AI dish photo.

```mermaid
flowchart TD
    subgraph Client["👤 User"]
        U[User opens Streamlit app]
    end

    subgraph Frontend["🖥️ Frontend — Streamlit Community Cloud"]
        LANG["Language selector<br/>(en, hi, bn, ta, te, mr, gu, kn, ml, pa, ur)"]
        INPUT{"Choose input method"}
        CAM["📷 Camera input<br/>(up to 5 photos)"]
        UPL["📁 File upload<br/>(up to 5 photos)"]
        VOI["🎤 Voice recorder<br/>(audio_input)"]
        TABLE["🧾 Editable ingredients table<br/>(pandas DataFrame + st.data_editor)"]
        SERV["🔢 Servings selector<br/>(1–10)"]
        OPTS["🍽️ Two recipe options<br/>(st.columns + st.container)"]
        RESULT["📋 Final recipe view<br/>steps + AI dish photo"]
    end

    subgraph Backend["⚙️ Backend API — FastAPI on Render"]
        EP1["POST /analyze-fridge"]
        EP2["POST /analyze-fridge-audio"]
        EP3["POST /generate-recipe"]
        EP4["POST /generate-recipe-image"]
    end

    subgraph AI["🤖 External AI Services"]
        GEMV["Gemini Vision<br/>(ingredient detection from photos)"]
        GEMA["Gemini Audio<br/>(voice transcription + extraction)"]
        GEMT["Gemini Text<br/>(recipe generation, multilingual)"]
        POLL["Pollinations.ai<br/>(text-to-image, dish photo)"]
    end

    U --> LANG --> INPUT
    INPUT --> CAM
    INPUT --> UPL
    INPUT --> VOI

    CAM --> EP1
    UPL --> EP1
    VOI --> EP2

    EP1 --> GEMV --> EP1
    EP2 --> GEMA --> EP2

    EP1 --> TABLE
    EP2 --> TABLE

    TABLE --> SERV --> EP3
    EP3 --> GEMT --> EP3
    EP3 --> OPTS --> EP4
    EP4 --> POLL --> EP4
    EP4 --> RESULT
```

---

## Component Overview

| Component | Responsibility |
|---|---|
| **Streamlit Frontend** | UI, session state, language switching, calling the backend API, rendering results |
| **FastAPI Backend** | Stateless API layer — receives images/audio/JSON, builds Gemini prompts, calls Gemini + Pollinations.ai, returns clean JSON |
| **Gemini Vision** | Detects ingredients from up to 5 fridge photos per request |
| **Gemini Audio** | Transcribes a voice note and extracts only the ingredient names |
| **Gemini Text** | Generates 2 complete recipes (name, prep time, servings, steps) in the selected language |
| **Pollinations.ai** | Free text-to-image API used to generate a preview photo of the finished dish |

## Deployment Topology

```mermaid
flowchart LR
    GH[("GitHub Repo<br/>main branch")]
    SC["Streamlit Community Cloud<br/>(frontend/app.py)"]
    RD["Render<br/>(backend/main.py, uvicorn)"]

    GH -- auto-deploy on push --> SC
    GH -- auto-deploy on push --> RD
    SC -- "BACKEND_URL (Streamlit Secrets)" --> RD
    RD -- "GEMINI_API_KEY (Render Environment)" --> GEM[Google Gemini API]
```

- **Frontend** and **backend** live in the *same* GitHub repo but are deployed as two separate services that talk to each other over HTTPS.
- The frontend never talks to Gemini or Pollinations.ai directly — all AI calls go through the backend, keeping the `GEMINI_API_KEY` server-side only.

