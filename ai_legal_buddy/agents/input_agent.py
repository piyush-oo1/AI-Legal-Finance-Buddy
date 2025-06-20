class InputAgent:
    """
    Task: Validate and preprocess user inputs.
    """
    def __init__(self, doc_type, terms):
        self.doc_type = doc_type.strip()
        self.terms = terms.strip()

    def get_prompt_payload(self):
        return {
            "doc_type": self.doc_type,
            "terms": self.terms
        }
