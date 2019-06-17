import os
from apps import app, db
from flask_script import Manager,Server
from flask_migrate import Migrate, MigrateCommand

server = Server(host=app.config['HOST'], port=app.config['PORT'])
migrate = Migrate(app, db)


if __name__ == '__main__':
    app.run()