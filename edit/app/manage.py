import sys
if sys.platform.startswith('win'):
    sys.path.append('D:\ABC\edit')
else:
    sys.path.append('/home/hui/python_workspace/blog/edit')
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

from app.extension import db
from app import create_app


app = create_app()

manage = Manager(app)
migrate = Migrate(app,db)
manage.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manage.run()