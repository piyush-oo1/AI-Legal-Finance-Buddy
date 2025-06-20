import os
from flask import Flask, request, render_template
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Import agents
from agents.input_agent import InputAgent
from agents.generation_agent import GenerationAgent
from agents.review_agent import ReviewAgent
from agents.formatting_agent import FormattingAgent
from agents.summary_agent import SummaryAgent
from agents.vector_agent import VectorAgent
from agents.notice_agent import NoticeAgent
from agents.deadline_agent import DeadlineAgent

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/generate_form")
def generate_form():
    return render_template("generate.html")

@app.route("/respond_form")
def respond_form():
    return render_template("respond_notice.html")

@app.route("/track_form")
def track_form():
    return render_template("track_deadlines.html")

@app.route("/upload_form")
def upload_form():
    return render_template("upload_sample_doc.html")

# @app.route('/', methods=['GET'])
# def index():
#     return render_template('index.html', result=None)

@app.route('/upload_sample_doc', methods=['POST'])
def upload_sample():
    file = request.files['file']
    doc_type = request.form['doc_type']
    if file and doc_type:
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        path = os.path.join(upload_dir, file.filename)
        file.save(path)
        VectorAgent.ingest_document(path, doc_type)
        return render_template("upload_sample_doc.html", filename=file.filename)
    return "Missing file or doc_type."

@app.route('/generate', methods=['POST'])
def generate():
    input_agent = InputAgent(
        doc_type=request.form['doc_type'],
        terms=request.form['terms']
    )
    payload = input_agent.get_prompt_payload()

    model_override = request.form.get('model', '').strip()
    model = model_override if model_override else DEFAULT_MODEL
    GenerationAgent.MODEL = model
    ReviewAgent.MODEL = model

    # Check vector DB first
    existing = VectorAgent.search_existing(payload['doc_type'], payload['terms'])
    if existing:
        draft = existing['draft']
        feedback = existing.get('feedback', '')
        summary = existing.get('summary', '')
        pdf_url = existing.get('pdf_url', '')
        result = f"{draft}\n\n---\n\n**Review & Suggestion:**\n{feedback}\n\n---\n\n**Summary:**\n{summary}"
        return render_template('result.html', result=result, pdf_url=pdf_url)

    draft = GenerationAgent.generate_draft(
        payload['doc_type'], payload['terms']
    )
    feedback = ReviewAgent.review_draft(draft)
    summary = SummaryAgent.summarize_draft(draft)
    result = f"{draft}\n\n---\n\n**Review & Suggestion:**\n{feedback}\n\n---\n\n**Summary:**\n{summary}"

    pdf_path = FormattingAgent.generate_pdf(result)
    VectorAgent.store_document(payload['doc_type'], payload['terms'], draft, summary, feedback, pdf_path)

    return render_template('result.html', result=result, pdf_url="/static/legal_draft.pdf")


@app.route('/respond_notice', methods=['POST'])
def respond_notice():
    notice_text = request.form['notice_text']
    intent = request.form.get('intent', 'neutral')
    response = NoticeAgent.generate_response(notice_text, intent)
    return render_template('result.html', result=response, pdf_url=None)

@app.route('/track_deadlines', methods=['POST'])
def track_deadlines():
    business_type = request.form['business_type']
    deadlines = DeadlineAgent.get_deadlines(business_type)
    formatted = f"Upcoming deadlines for {business_type}:\n\n" + "\n".join(deadlines)
    return render_template('result.html', result=formatted, pdf_url=None)


if __name__ == '__main__':
    app.run(debug=True, port=5000)