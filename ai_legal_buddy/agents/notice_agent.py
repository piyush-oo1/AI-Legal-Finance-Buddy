import openai

class NoticeAgent:
    MODEL = "gpt-4o"

    @staticmethod
    def generate_response(text, intent="neutral"):
        tone_instruction = {
            "conciliatory": "Write a cooperative and apologetic legal response",
            "defensive": "Write a firm and disputing legal response",
            "neutral": "Write a professional legal response requesting clarification"
        }.get(intent, "Write a professional legal response")

        prompt = f"""
You are a legal assistant. Based on the intent: '{intent}', and the following notice:

{text}

{tone_instruction}. Make the response formal, legally appropriate, and suitable to send to the opposing party.
"""
        response = openai.chat.completions.create(
            model=NoticeAgent.MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful legal assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()