## MCQ Generator (LangChain + OpenAI + Streamlit)

Generate multiple-choice questions (MCQs) from PDF or text files using LangChain and OpenAI, with an easy-to-use Streamlit UI. The app creates a quiz and a short expert-style review of the quiz complexity.

### Features
- Generate MCQs from uploaded `.pdf` or `.txt` files
- Configure number of questions, subject, and tone/complexity
- View results in a table with choices and correct answers
- Get an automatic short review of quiz complexity and fit for the audience

### Tech Stack
- Python 3.11+
- Streamlit for UI
- LangChain (+ `langchain_community`, `langchain_openai`)
- OpenAI Chat Models
- PyPDF2 for PDF text extraction
- dotenv for environment variable management

---

## Project Structure
```text
src/
  McqGenerator/
    mcqgenerator.py   # Prompt templates and generation/evaluation chains
    utils.py          # PDF/text reading and quiz table parsing helpers
    logger.py         # Logging utilities
StreamlitApp.py        # Streamlit UI
requirements.txt       # Dependencies
setup.py               # Editable install (-e .)
Response.json          # Example response schema used as a guide for the LLM
```

Note: `StreamlitApp.py` currently loads `Response.json` from an absolute path. See the Configuration section below to fix or change this.

---

## Prerequisites
- Python 3.11 (recommended)
- An OpenAI API key with access to chat models

---

## Setup
### 1) Clone and create a virtual environment
```bash
git clone <your-repo-url>
cd "Mcq Generator"
python -m venv env
# Windows PowerShell
env\Scripts\Activate.ps1
```

### 2) Install dependencies
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

This project uses `-e .` (editable install) which relies on `setup.py`.

### 3) Configure environment variables
Create a `.env` file at the project root with your OpenAI key:
```bash
echo OPENAI_API_KEY=sk-your-key-here > .env
```

Alternatively, set it in your shell/session environment.

### 4) Ensure `Response.json` is available
`StreamlitApp.py` expects `Response.json` (a schema guiding the model output). Place it at the project root (same folder as `StreamlitApp.py`). Then update the app to use a relative path (recommended). Example change:

```python
# In StreamlitApp.py
with open("Response.json", "r") as file:
    responce = json.load(file)
```

If you prefer, keep an absolute path, but ensure it matches your machine.

---

## Run the App
```bash
streamlit run StreamlitApp.py
```

Then open the URL shown in the terminal (usually http://localhost:8501).

---

## Usage
1. Upload a `.pdf` or `.txt` file
2. Set number of questions
3. Provide a subject (e.g., Physics, History)
4. Set a tone/complexity (e.g., Simple, Intermediate)
5. Click "Generate MCQs"

You will see a table with MCQs, choices, and the correct answer. A short review will be displayed below.

---

## How It Works
- `src/McqGenerator/mcqgenerator.py` defines two prompts and two chains:
  - quiz generation chain creates MCQs in a JSON-like format
  - review chain evaluates complexity and provides a brief summary
- `src/McqGenerator/utils.py` reads PDFs/text and converts the quiz JSON into a tabular structure for display.
- `StreamlitApp.py` wires the UI, file handling, chain execution, and result rendering.

Default model: `gpt-3.5-turbo` (configurable in `mcqgenerator.py`).

---

## Architecture

```mermaid
flowchart TD
    U[User] -->|Upload PDF/TXT, set params| S[StreamlitApp.py UI]
    S -->|read_file| UTL[utils.read_file]
    UTL -->|extracted text| S
    S -->|prompt vars + Response.json| G[generate_evaluate_chain]
    G -->|Quiz JSON| S
    G -->|Review text| S
    S -->|parse| T[utils.get_table_data]
    T -->|table data (DataFrame)| S
    S -->|Table + Review| UI[Rendered UI]

    subgraph LLM
      G --- OAI[OpenAI ChatOpenAI (gpt-3.5-turbo)]
    end
```

---

## Configuration Tips
- Model: change `model="gpt-3.5-turbo"` in `mcqgenerator.py` to use a different OpenAI model.
- Temperature: adjust `temperature=0.5` to control creativity.
- Absolute path in `StreamlitApp.py`: replace with a relative path to `Response.json` as shown above.

---

## Troubleshooting
- OpenAI quota errors: "quota exceeded" indicates billing/plan issues or exhausted credits.
- No readable text from PDF: try another PDF or pre-process/scanned PDFs with OCR.
- Table not showing: raw quiz is displayed if parsing fails. Ensure the model adheres to the `Response.json` structure.
- Import errors for LangChain/OpenAI: ensure both `langchain_community` and `langchain_openai` are installed (already included in `requirements.txt`).

---

## Development
```bash
# Lint/type-check as desired (not configured by default)
pip list
python test.py  # if you add tests/util checks here
```

Project is packaged with `setup.py` to support `-e .` during development.

---

## Security
- Never commit your `.env` or API keys
- Scope your OpenAI key and rotate if exposed

---

## License
Add your preferred license. If omitted, all rights are reserved by default.

---

## Acknowledgements
- LangChain team and community packages
- OpenAI for chat models
- Streamlit for rapid UI
