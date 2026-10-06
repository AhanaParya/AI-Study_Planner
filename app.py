from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Ollama local API
OLLAMA_URL = "http://localhost:11434/api/generate"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate-plan", methods=["POST"])
def generate_plan():

    data = request.get_json()

    subjects = data.get("subjects")
    exam_date = data.get("exam_date")
    hours = data.get("hours")

    if not subjects or not exam_date or not hours:
        return jsonify({
            "error": "Please fill all the fields."
        }), 400

    prompt = f"""
You are an expert AI study planner.

Create a personalized study timetable for a college student.

Subjects:
{subjects}

Exam date:
{exam_date}

Available study hours per day:
{hours}

Create a realistic timetable.

Requirements:

1. Divide the study time between the subjects.
2. Give more time to difficult subjects.
3. Include short breaks.
4. Include revision sessions.
5. Include practice/problem-solving sessions.
6. Include final revision before the exam.
7. Never exceed the available study hours per day.
8. Make the schedule realistic for a college student.

For each day provide:

- Time
- Subject
- Activity
- Duration

At the end, give 5 useful study tips.

Keep the answer clear and easy to understand.
"""

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False
            }
        )

        if response.status_code != 200:
            return jsonify({
                "error": "Ollama returned an error."
            }), 500

        result = response.json()

        plan = result.get("response", "")

        return jsonify({
            "plan": plan
        })

    except requests.exceptions.ConnectionError:

        return jsonify({
            "error": "Cannot connect to Ollama. Make sure Ollama is running."
        }), 500

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)