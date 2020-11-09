from json import loads

# load makes and models from json file
def load_makes(website: str, _MAKES_JSON: str) -> dict:
    with open(_MAKES_JSON, "r", encoding="utf-8", newline="") as mjson:
        data = mjson.read()
        makes_dict = loads(data)
        makes_dict = makes_dict[website]
    return makes_dict
