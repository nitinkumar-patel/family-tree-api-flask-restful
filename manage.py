# set the path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from application import create_app


def run_app():
    app = create_app()
    manager = Manager(app)

    # Turn on debugger by default and reloader

    manager.add_command("runserver", Server(
        use_debugger=True,
        use_reloader=True,
        host=os.getenv('FLASK_APP_IP', '0.0.0.0'),
        port=int(os.getenv('FLASK_APP_PORT', 5000))
        )
    )
    manager.add_command('db', MigrateCommand)

    manager.run()


if __name__ == '__main__':
    run_app()
