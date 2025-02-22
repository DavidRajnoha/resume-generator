from typing import List

def load_applicant_data(paths: List[str]) -> List[str]:
    texts = []
    for path in paths:
        with open(path, "r") as file:
            texts.append(file.read())
    return texts
