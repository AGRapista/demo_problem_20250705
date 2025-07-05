from flask import Flask, request, jsonify
import re, random

app = Flask(__name__)

# Note: Assuming retrieval and update of letter object is case insensitive
letters = [
    {"letter": "A", "value": 1, "strokes": 2, "vowel": True},
    {"letter": "B", "value": 2, "strokes": 1, "vowel": False}
]

# Functions
def check_credentials(username, password):
    password_valid = username[::-1] == password

    if len(username) < 4:
        username_valid = False

    username = username.lower()
    username_valid = bool(re.search(r'a.*b.*c', username))

    return password_valid and username_valid

def is_valid_letter_obj(data):
    required_keys = ['letter', 'value', 'strokes', 'vowel']
    if not all(key in data for key in required_keys):
        return False

    # Validate letter
    if not isinstance(data['letter'], str) or not data['letter'].strip():
        return False

    # Validate value
    if not isinstance(data['value'], int):
        return False

    # Validate strokes
    if not isinstance(data['strokes'], int) or data['strokes'] == data['value']:
        return False

    # Validate vowel
    if not isinstance(data['vowel'], bool):
        return False

    return True, 0 # Valid 

def shuffle_list(data):
    for item in data:
        index = data.index(item)
        random_index = random.randint(0, len(data) - 1)
        data[index], data[random_index] = data[random_index], data[index]
    return data


# APIs

# Login
# POST /api/login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    try:
        username = data['username']
        password = data['password']
    except:
        return jsonify({"error": "Invalid format or request not suitable"})

    if check_credentials(username, password):
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Login failed"})


# List letters
# GET /api/letters
@app.route('/api/letters', methods=['GET'])
def get_letters():
    letters_sorted = sorted(letters, key=lambda x: x['value'])
    letter_names = [item["letter"] for item in letters_sorted]
    output = {"letters" : letter_names}
    return jsonify(output), 200


# Add letter
# POST /api/letter/add
@app.route('/api/letter/add', methods=['POST'])
def add_letter():
    data = request.get_json()
    data_is_valid = is_valid_letter_obj(data)
    if not data_is_valid:
        return jsonify({"status" : 1})
    if data in letters:
        return jsonify({"status" : 1})
    letters.append(data)
    return jsonify({"status" : 0})


# Get letter
# GET /api/letter/<letter:str>
@app.route('/api/letter/<string:letter>', methods=['GET'])
def get_letter(letter):
    for item in letters:
        if letter == item["letter"]: 
            return jsonify(item)
    return jsonify({"message"})


# Shuffle letters
# GET /api/letter/shuffle
@app.route('/api/letter/shuffle', methods=['GET'])
def get_shuffled_letters():
    letter_list = [item["letter"] for item in letters]
    cleaned_list = list(set(shuffle_list(letter_list)))
    return shuffle_list(cleaned_list)


# Filter letters
# GET /api/letter/filter/<val:int>
@app.route('/api/filter/<int:value>', methods=['GET'])
def get_filtered_letters(value):
    letter_list = [item["letter"] for item in letters if item["value"] <= value]
    return jsonify({"letters" : letter_list})

if __name__ == '__main__':
    app.run(debug=True)