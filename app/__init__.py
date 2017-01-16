from flask import Flask

def _initialize_blueprints(app):
    '''
    Register Flask blueprints
    '''
    from views.s3 import s3
    app.register_blueprint(s3, url_prefix='/api/v1/s3')

def create_app():
    '''
    Create an app by initializing components.
    '''
    app = Flask(__name__)

    _initialize_blueprints(app)

    # Do it!
    return app
