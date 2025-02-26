import hashlib

def compute_hash(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()
