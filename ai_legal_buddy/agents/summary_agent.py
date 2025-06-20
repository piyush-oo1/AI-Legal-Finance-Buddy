import os
import openai

class SummaryAgent:
    MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    @staticmethod
    def summarize_draft(draft_text):
        prompt = (
            "Summarize the following legal contract in very simple language, like you're explaining it to a 5-year-old. "
            "Only focus on who is involved, what each person agrees to do, for how long, and any important rules.\n\n"
            + draft_text
        )
        response = openai.chat.completions.create(
            model=SummaryAgent.MODEL,
            messages=[
                {"role": "system", "content": "You simplify legal contracts for beginners."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=300,
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()