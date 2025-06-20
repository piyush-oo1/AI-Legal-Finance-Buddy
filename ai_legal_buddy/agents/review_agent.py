import os
import openai

class ReviewAgent:
    """
    Task: Review the generated draft for clarity and suggest improvements.
    """
    MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    @staticmethod
    def review_draft(draft):
        review_prompt = (
            "Review the following legal document for clarity, grammar, and professional tone. "
            "Provide concise feedback and suggest one improvement.\n\n" + draft
        )
        response = openai.chat.completions.create(
            model=ReviewAgent.MODEL,
            messages=[
                {"role": "system", "content": "You are an expert legal editor."},
                {"role": "user", "content": review_prompt},
            ],
            max_tokens=200,
            temperature=0.1,
        )
        return response.choices[0].message.content.strip()