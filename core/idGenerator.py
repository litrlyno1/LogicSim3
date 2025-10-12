import uuid

def generateId(prefix : str) -> str:
    return f"{prefix}_{uuid.uuid4()}"