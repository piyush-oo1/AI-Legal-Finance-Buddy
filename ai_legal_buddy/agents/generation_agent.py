import os
import openai

class GenerationAgent:
    SYSTEM_MESSAGE = "You are a helpful AI Legal Assistant."
    MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    @staticmethod
    def generate_draft(doc_type, terms):
        prompt = (
            f"Document type: {doc_type}\n"
            f"Key parties & terms: {terms}\n"
            f"Produce a clear, concise, professional {doc_type} draft."
        )
        response = openai.chat.completions.create(
            model=GenerationAgent.MODEL,
            messages=[
                {"role": "system", "content": GenerationAgent.SYSTEM_MESSAGE},
                {"role": "user", "content": prompt},
            ],
            max_tokens=800,
            temperature=0.2,
        )
        return response.choices[0].message.content.strip()