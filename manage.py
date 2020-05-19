__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
manage.py
- provides a command line utility for interacting with the
  application to perform interactive debugging and setup
"""

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from application.main import create_app
from application.db import db
from application.models.state_collection import StateCollection, StateCollectionUserPermission
from application.models.state_item import StateItem, StateItemUserPermission
from application.models.user import User


app = create_app()

migrate = Migrate(app, db)
manager = Manager(app)

# provide a migration utility command
manager.add_command('db', MigrateCommand)

# enable python shell with application context


@manager.shell
def shell_ctx():
    return dict(app=app,
                db=db,
                StateCollection=StateCollection, StateCollectionUserPermission=StateCollectionUserPermission,
                StateItem=StateItem, StateItemUserPermission=StateItemUserPermission,
                User=User)


if __name__ == '__main__':
    manager.run()
