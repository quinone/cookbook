import os

from flask_migrate import Migrate

from app import create_app, db
from app.model import User, Role, Recipe

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db, render_as_batch=True)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Recipe=Recipe)


