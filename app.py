from flask import Flask,jsonify
from flask import abort
from flask import make_response
from flask import request
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)

tasks = [
	{
		'id':1,
		'title':'buy groceries',
		'descrip': 'mike, cheese, fruit',
		'done': False
	},
	{
	'id':2,
	'title':'learn python',
	'descrip':'need to find tutorial',
	'done':False
	}


]

@app.route('/')
def index():
	return "Hello World"

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
@auth.login_required
def get_task():
	return jsonify({'tasks':tasks})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task_single(task_id):
	task = list(filter(lambda t: t['id'] == task_id, tasks))
	if len(task) == 0:
		abort(404)
	return jsonify({'task': task[0]})

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
	if not request.json or not 'title' in request.json:
		abort(400)

	task = {
		'id': tasks[-1]['id'] + 1,
		'title': request.json['title'],
		'descrip': request.json.get('descrip', ''),
		'done': False 
	}

	tasks.append(task)
	return jsonify({'task':task}), 201

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = list(filter(lambda t: t['id'] == task_id, tasks))
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    if 'descrip' in request.json and type(request.json['descrip']) != str:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['descrip'] = request.json.get('descrip', task[0]['descrip'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = list(filter(lambda t: t['id'] == task_id, tasks))
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

@auth.get_password
def get_password(username):
	if username == 'ok':
		return 'python'
	return None

@auth.error_handler
def unauthorized():
	return make_response(jsonify({'error': 'unauthorized access'}), 401)




if __name__ == '__main__':
	app.run(debug=True)