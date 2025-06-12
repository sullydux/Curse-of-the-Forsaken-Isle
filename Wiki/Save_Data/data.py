import json
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

def decode(target_number):
    target_number = str(target_number)
    with open("/Users/sullydux/Desktop/Save_Data/numbers.txt", "r") as num_file:
        numbers = [line.strip() for line in num_file]
    with open("/Users/sullydux/Desktop/Save_Data/letters.txt", "r") as let_file:
        letters = [line.strip() for line in let_file]
    if target_number in numbers:
        index = numbers.index(target_number)
        return letters[index]
    return None

def full_decode(save_data):
    num = 0
    value = ""
    while num + 3 <= len(save_data):
        letter = save_data[num:num+3]
        decoded = decode(letter)
        if decoded is not None:
            value += decoded
        num += 3
    return value

def find_values(val):
    values = ""
    collecting = False
    for char in val:
        if char == "❌":
            if collecting:
                return values
            collecting = True
            continue
        if collecting:
            values += char
    return values

@app.route("/analyze", methods=["POST"])
def analyze_save():
    save_data_encoded = request.json.get("code", "")
    print(save_data_encoded)

    # Run decode logic when data is received
    decoded = full_decode(save_data_encoded)
    Wiki_string = find_values(decoded)

    with open("/Users/sullydux/Desktop/Save_Data/data.json", "r") as file:
        data = json.load(file)

    data["desert"] = Wiki_string[0]
    data["tundra"] = Wiki_string[1]
    data["Boss dimension"] = Wiki_string[2]
    data["vill cave"] = Wiki_string[3]
    data["Lep"] = Wiki_string[4]
    data["vilage"] = Wiki_string[5]

    with open("/Users/sullydux/Desktop/Save_Data/data.json", "w") as file:
        json.dump(data, file, indent=2)

    # Return the updated unlock data to the frontend
    return jsonify({"status": "decoded and saved", "unlocked": data})

if __name__ == "__main__":
    app.run(debug=True)