from flask import Flask

# creates the Flask app and configs a secret key
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'key'

    # imports the created views and registers 
    # the blueprints to the app
    from .views import views
    app.register_blueprint(views, url_prefix='/')

    return app 
