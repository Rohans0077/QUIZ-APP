import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def load_quiz_data():
    """Load quiz data from a JSON file."""
    with open("quiz_data.json", "r") as file:
        return json.load(file)

@app.route("/")
def index():
    quiz_data = load_quiz_data()
    return render_template("index.html", quiz_data=quiz_data["quiz"])

@app.route("/check_answer", methods=["POST"])
def check_answer():
    data = request.get_json()
    question_id = data["question_id"]
    user_answer = data["user_answer"]
    quiz_data = load_quiz_data()

    # Find the question by ID
    question = next((q for q in quiz_data["quiz"]["questions"] if q["id"] == question_id), None)
    if question:
        is_correct = question["answer"] == user_answer
        return jsonify({"is_correct": is_correct, "correct_answer": question["answer"]})
    else:
        return jsonify({"error": "Invalid question ID"}), 400

if __name__ == "__main__":
    app.run(debug=True)
