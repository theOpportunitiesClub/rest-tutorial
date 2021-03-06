#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
#import RPi.GPIO as GPIO

app = Flask(__name__)

tasks = [
    {
        "id": 1,
        "title": "Buy groceries",
        "description": "Milk, Cheese, Pizza, Fruit, Tylenol",
        "done": False
        },
    {
        "id": 2,
        "title": "Learn Python",
        "Description": "Need to find a good Python tutorial on the Web",
        "done": False
        }
    ]

led_on = False

@app.route("/")
def index():
    return "Hello World from 3! \n\n"


#maybe, get the text file when using GET, re-write the whole text file w/ updated code when POST
@app.route("/gpio", methods=["GET"])
def control_gpio():
    data = "#This is python\nimport RPi.GPIO as GPIO\nimport time\n\nGPIO.setmode(GPIO.BOARD)\n"
    data = data + "GPIO.setup(7, GPIO.OUT)\nGPIO.output(7, True)\ntime.sleep(2)\nGPIO.output(7, False)"
    return data


@app.route("/todo/api/v1.0/tasks", methods=["GET"])
def get_tasks():
    return jsonify({"tasks": tasks})


@app.route("/todo/api/v1.0/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = [task for task in tasks if task["id"] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({"task": task[0]})


@app.route("/todo/api/v1.0/tasks", methods=["POST"])
def create_task():
        if not request.json or not "title" in request.json:
                abort(400)
        task = {
                "id": tasks[-1]["id"]+1,
                "title": request.json["title"],
                "description": request.json.get("description", ""),
                "done": False
                }
        tasks.append(task)
        return jsonify({"task":task}), 201


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
	app.run(debug = True)



































