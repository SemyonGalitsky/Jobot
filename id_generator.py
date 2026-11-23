import uuid


class IdGenerator:
    @staticmethod
    def generate_id():
        return str(uuid.uuid4())[:8]