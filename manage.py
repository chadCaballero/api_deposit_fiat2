#por ver el shebang de anaconda

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from apps import app, db

migrate = Migrate(app, db)
manager = Manager(app)
server = Server(host=app.config['HOST'], port=app.config['PORT'])

manager.add_command("runserver", server)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
