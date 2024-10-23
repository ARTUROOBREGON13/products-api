from flask import Flask
from flask_caching.backends.simplecache import SimpleCache
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .config import Config
from flask_swagger_ui import get_swaggerui_blueprint
import json, os

# Inicializa las extensiones
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def populate_users():
    from app.models import User
    if User.query.count() == 0:
        user1 = User(username='user1')
        user1.set_password('password1')
        user2 = User(username='user2')
        user2.set_password('password2')

        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        
def populate_products(app):
    from app.models import Product
    if Product.query.count() == 0:
        json_file_path = os.path.join(app.static_folder, 'products.json')
        with open(json_file_path) as f:
            products_data = json.load(f)
        
        for item in products_data:
            product = Product(
                name="{} {}".format(item['name'], item['color']),
                price=item['price'],
                quantity=item['quantity']
            )
            db.session.add(product)
        
        db.session.commit()
        print("Products populated.")

def create_app(test=False):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
        Config.MYSQL_USER, Config.MYSQL_PASSWORD, Config.MYSQL_HOST, Config.MYSQL_PORT, Config.MYSQL_DB)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET
    app.config['DEBUG'] = Config.DEBUG
    app.config['TESTING'] = test
    cache = SimpleCache()

    # Inicializa las extensiones con la app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Configura Swagger
    SWAGGER_URL = Config.SWAGGER_URL
    API_URL = '/static/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "Products API"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # Importa modelos y rutas después de inicializar la app
    from .models import Product, User
    from .routes import api
    app.register_blueprint(api)
    
    if not test:
        with app.app_context():
            db.create_all()
            populate_users()
            populate_products(app)
    return app