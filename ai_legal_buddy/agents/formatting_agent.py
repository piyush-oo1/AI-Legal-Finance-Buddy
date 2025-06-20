import os
from markdown import markdown
from weasyprint import HTML

class FormattingAgent:
    """
    Task: Convert markdown-style legal content into a styled, printable A4 PDF.
    """
    @staticmethod
    def generate_pdf(document_text, output_path="static/legal_draft.pdf"):
        # Convert markdown to HTML
        html_body = markdown(document_text)

        # Full A4 page template
        html_template = f"""
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                @page {{ size: A4; margin: 2cm; }}
                body {{ font-family: 'Georgia', serif; font-size: 12pt; color: #333; line-height: 1.6; }}
                h1, h2, h3 {{ color: #222; }}
                h1 {{ font-size: 18pt; margin-top: 24px; }}
                h2 {{ font-size: 14pt; margin-top: 18px; }}
                h3 {{ font-size: 12pt; margin-top: 14px; }}
                p, ul, ol {{ margin: 10px 0; }}
                ul, ol {{ padding-left: 20px; }}
                strong {{ font-weight: bold; }}
                em {{ font-style: italic; }}
                code, pre {{ background-color: #f4f4f4; padding: 4px; border-radius: 4px; }}
            </style>
        </head>
        <body>
            {html_body}
        </body>
        </html>
        """

        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Generate PDF
        HTML(string=html_template).write_pdf(output_path)
        return output_path
