# Genjutsu Higgsfield AI

A private, local AI assistant with:
- no API key
- no cloud account
- no credits
- unlimited local use after model download
- runs fully on your machine through Ollama

## Features
- Local LLM inference using Ollama
- FastAPI backend
- Simple browser interface
- Offline-capable after setup
- No paid API dependency

## Requirements
- Python 3.10+
- Ollama installed and running
- A local model downloaded

## Install Ollama
Download and install from: https://ollama.com/

Then pull a model:

```bash
ollama pull llama3.1:8b
```

Alternative models:

```bash
ollama pull qwen2.5:7b
ollama pull mistral
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run the app

Start the backend:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Open the UI by serving the static page:

```bash
python -m http.server 8080
```

Then open:

```text
http://localhost:8080
```

## API

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Write a short poem about a local AI awakening"}'
```

## Notes
This project does not call any external paid API. It talks directly to your local Ollama server.
