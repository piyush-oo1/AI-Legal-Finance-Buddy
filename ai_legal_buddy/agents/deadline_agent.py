import openai

class DeadlineAgent:
    MODEL = "gpt-4o"

    @staticmethod
    def get_deadlines(business_type):
        prompt = f"""
You are a legal compliance assistant. List upcoming compliance deadlines (filing, taxes, renewals, etc.) for a {business_type} business in India.

Format each deadline as:
- [Month Day] – [Deadline Description] ([Form Name, if any])

Return only the top 3 most relevant upcoming deadlines.
"""

        response = openai.chat.completions.create(
            model=DeadlineAgent.MODEL,
            messages=[
                {"role": "system", "content": "You are a legal assistant focused on business compliance in India."},
                {"role": "user", "content": prompt}
            ]
        )

        # Fix here: access `.content` directly instead of using dictionary-like syntax
        return response.choices[0].message.content.strip().split("\n")
