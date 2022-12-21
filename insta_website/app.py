import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

basedir = os.path.abspath(os.path.dirname(__file__))


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'db.sqlite'),
    )

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    print(f"It should be ok!")

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    from .auth_routes import auth as auth_blueprint
    from .main_routes import main as main_blueprint
    # blueprint for auth routes in our app
    app.register_blueprint(auth_blueprint)
    # blueprint for non-auth parts of app
    app.register_blueprint(main_blueprint)

    with app.app_context():
        db.create_all()

    return app


# if __name__ == "__main__":
#     app = create_app()
#     app.run(host='0.0.0.0', port=8000, debug=True)


