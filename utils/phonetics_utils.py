import json

def save_phonetics_mappings(phonetics_dict):
    with open("phonetics.json", "w") as f:
        json.dump(phonetics_dict, f)

def get_phonetics_mappings():
    with open("phonetics.json", "r") as f:
        return json.load(f)
