# Installation Guide - Gemini API Setup

## Step 1: Install Google Gemini SDK

Run ONE of these commands:

### Option A: Using project venv (if it exists in parent directory)
```bash
cd D:\Ammi-s-Assitant
venv\Scripts\pip install google-genai python-dotenv
```

### Option B: Using global pip
```bash
pip install google-genai python-dotenv
```

### Option C: Using requirements file
```bash
pip install -r backend/requirements_gemini.txt
```

## Step 2: Verify Installation

```bash
python -c "from google import genai; print('Gemini SDK installed!')"
```

## Step 3: Test Agent

```bash
cd backend
python test_agent.py
```

## Troubleshooting

If you get "ModuleNotFoundError":
1. Check which Python is running: `which python` or `where python`
2. Install to that specific Python: `path/to/python.exe -m pip install google-genai`
3. Or activate venv first: `venv\Scripts\activate` then install

## What's Changed

- **API**: Switched from OpenAI to Google Gemini
- **SDK**: Using `google-genai` (official Python SDK)
- **Model**: `gemini-2.0-flash-exp` (latest, fast, creative)
- **Key**: Already configured in `.env`
- **Function Calling**: Automatic (Gemini handles execution)

## Benefits of Gemini

✅ **Free tier**: More generous than OpenAI
✅ **Automatic function calling**: Simpler code
✅ **Latest features**: Gemini 2.0 is cutting-edge
✅ **Fast**: Flash variant is optimized for speed
✅ **AI Recipe Generation**: New `generate_new_recipe` tool!
