class SignatureDatabase:

    def __init__(self):
        self.signatures = set()

    def add_signature(self, signature: str):
        self.signatures.add(signature)

    def check_signature(self, signature: str) -> bool:
        return signature in self.signatures
