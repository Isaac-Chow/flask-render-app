from flask import Flask
from flask_smorest import Api
from application.config import DevConfig
from application.models.shop import db
from application.routes import shop_blp as ShopBlueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevConfig)
    db.init_app(app)
    api = Api(app)

    api.register_blueprint(ShopBlueprint)

    with app.app_context():
        db.create_all()

    return app

app = create_app()