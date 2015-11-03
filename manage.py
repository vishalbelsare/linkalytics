# manage.py

from flask.ext.script import Manager, Server

try:
    from app import app
except ImportError:
    from src import app


server  = Server(host="0.0.0.0", port=8080)
manager = Manager(app)

manager.add_command('runserver', server)

if __name__ == "__main__":
    manager.run()
