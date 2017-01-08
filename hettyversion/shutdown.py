from flask import Blueprint, request

shutdown_blueprint = Blueprint('shutdown_blueprint', __name__)

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@shutdown_blueprint.route('/shutdown')
def shutdown():
	shutdown_server()
	return 'Server shutting down...'