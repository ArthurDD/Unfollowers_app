import os
from flask import Flask
# from insta_website.project.models import db
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')

db.init_app(app)

from auth_routes import auth as auth_blueprint
from main_routes import main as main_blueprint
# blueprint for auth routes in our app
app.register_blueprint(auth_blueprint)
# blueprint for non-auth parts of app
app.register_blueprint(main_blueprint)

with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)


