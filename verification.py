import json
from aws import get_all_shelters

with open("santa_clara_shelters.json", "r") as file:
    verified_shelters = set(json.load(file)["shelters"])


shelters_from_db = get_all_shelters()

for s in shelters_from_db:
    s["verif"] = s["name"] in verified_shelters
