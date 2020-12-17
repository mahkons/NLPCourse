import re
import json


if __name__ == "__main__":
    with open("HW1.txt", 'r', encoding='utf-8', errors='ignore') as file:
        data = file.read()

    data = data.split("-------------------")[:-1]
    data = list(map(lambda text: text.replace('\n', ' '), data))
    data = list(map(lambda text: re.sub(r"^.*Abstract:", "", text), data))
    
    with open("text_1.txt", 'w', encoding='utf-8') as file:
        file.write(json.dumps(data))
