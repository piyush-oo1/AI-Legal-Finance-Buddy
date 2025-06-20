# AI Legal Finance Buddy

AI Legal Finance Buddy is a Flask-based web application that leverages OpenAI's GPT models to assist users with legal document drafting, review, compliance tracking, and legal notice responses. It also supports document ingestion for vector-based retrieval and learning from user-uploaded samples.

## Features
- **Generate Legal Documents:** Create drafts for NDAs, Service Agreements, Lease Agreements, Employment Agreements, and more.
- **Review & Summarize:** Automated review and plain-language summary of generated drafts.
- **Respond to Legal Notices:** Generate formal, defensive, or conciliatory responses to legal notices.
- **Track Legal Deadlines:** Get compliance deadlines for different business types in India.
- **Document Ingestion:** Upload sample legal documents to improve future draft quality using vector search.
- **PDF Export:** Download generated drafts as styled, printable PDFs.

## Project Structure
```
.
├── app.py                  # Main Flask application
├── agents/                 # Modular AI agents for each task
│   ├── input_agent.py      # Validates and preprocesses user input
│   ├── generation_agent.py # Generates legal drafts using OpenAI
│   ├── review_agent.py     # Reviews drafts for clarity and tone
│   ├── formatting_agent.py # Converts drafts to styled PDF
│   ├── summary_agent.py    # Summarizes drafts in simple language
│   ├── vector_agent.py     # Handles vector DB for document retrieval
│   ├── notice_agent.py     # Generates responses to legal notices
│   └── deadline_agent.py   # Tracks compliance deadlines
├── templates/              # HTML templates for web UI
│   ├── home.html           # Home navigation
│   ├── index.html          # Main landing page
│   ├── generate.html       # Document generation form
│   ├── respond_notice.html # Notice response form
│   ├── track_deadlines.html# Deadline tracking form
│   ├── upload_sample_doc.html # Upload sample doc form
│   └── result.html         # Displays results and download links
├── static/
│   └── legal_draft.pdf     # Generated PDF drafts
├── uploads/                # User-uploaded sample documents
├── vector_db/              # Chroma vector DB for document retrieval
├── output/                 # (Reserved for future outputs)
└── venv/                   # Python virtual environment
```

## Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd ai_legal_buddy
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up environment variables:**
   - Create a `.env` file in the root directory with your OpenAI API key:
     ```env
     OPENAI_API_KEY=your_openai_api_key
     OPENAI_MODEL=gpt-4o-mini
     ```
5. **Run the application:**
   ```bash
   python app.py
   ```
   The app will be available at [http://localhost:5000](http://localhost:5000)

## Usage
- **Home:** Navigate to different features from the home page.
- **Generate Legal Document:** Fill in document type and terms to generate a draft, review, and summary. Download as PDF.
- **Respond to Notice:** Paste a legal notice and select the response tone to generate a reply.
- **Track Deadlines:** Select business type to view upcoming compliance deadlines.
- **Upload Sample Document:** Upload .pdf, .docx, or .txt files to improve document generation via vector search.

## Agents Overview
- **InputAgent:** Validates and structures user input for prompts.
- **GenerationAgent:** Uses OpenAI to draft legal documents.
- **ReviewAgent:** Reviews drafts for clarity, grammar, and professionalism.
- **FormattingAgent:** Converts markdown drafts to styled PDFs.
- **SummaryAgent:** Summarizes legal drafts in simple language.
- **VectorAgent:** Handles document ingestion and retrieval using Chroma vector DB.
- **NoticeAgent:** Crafts responses to legal notices based on user intent.
- **DeadlineAgent:** Provides compliance deadlines for Indian businesses.

## Requirements
- Python 3.8+
- Flask
- openai
- python-dotenv
- weasyprint
- markdown
- langchain, chromadb, pymupdf, docx2txt (for vector DB and document ingestion)

## Notes
- Uploaded documents are stored in the `uploads/` directory and ingested into the vector DB for future retrieval.
- Generated PDFs are saved in the `static/` directory.
- The app is designed for Indian legal compliance but can be extended for other jurisdictions.

## License
MIT License 