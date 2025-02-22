def load_application_data(path: str) -> str:
    with open(path, "r") as file:
        return file.read()
