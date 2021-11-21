import os

from flask import Flask
from flask.templating import render_template

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'quizoo.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import db
    from . import user

    db.init_app(app)
    app.register_blueprint(user.bp)

    from datetime import datetime

    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}

    @app.route('/')
    def main():
        return render_template('base.html')

    return app
