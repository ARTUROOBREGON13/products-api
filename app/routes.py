from flask import abort, Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from . import db
from .models import Product, User
from flask_caching import Cache
from werkzeug.exceptions import HTTPException

cache = Cache()
api = Blueprint('v1', __name__)

def get_or_404(model, id):
    instance = db.session.get(model, id)
    if instance is None:
        abort(404)
    return instance

@api.route('/login', methods=['POST'])
def login():
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        if not username or not password:
            return jsonify({"msg": "Falta username o password"}), 400
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({"msg": "Bad username or password"}), 401
    except Exception as e:
        return jsonify({"msg": "Error al iniciar sesión"}), 500

@cache.cached(timeout=60)
@api.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    try:
        data = request.json
        if not data or not data.get('name') or not data.get('price') or not data.get('quantity'):
            return jsonify({"msg": "Falta información del producto"}), 400
        new_product = Product(name=data['name'], price=data['price'], quantity=data['quantity'])
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'message': 'Producto creado'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Error al crear producto"}), 500

@api.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        products = Product.query.paginate(page=page, per_page=limit, error_out=True, count=True)
        return jsonify({
            'products': [{'id': p.id, 'name': p.name, 'price': p.price, 'quantity': p.quantity} for p in products.items],
            'total': products.total,
            'page': products.page,
            'pages': products.pages
        })
    except Exception as e:
        return jsonify({"msg": "Error al obtener productos"}), 500

@api.route('/products/<int:id>', methods=['GET'])
@jwt_required()
def get_product(id):
    try:
        product = get_or_404(Product, id)
        return jsonify({'id': product.id, 'name': product.name, 'price': product.price, 'quantity': product.quantity})
    except Exception as e:
        if isinstance(e, HTTPException) and e.code == 404:
            return jsonify({"msg": "Producto no encontrado"}), e.code
        return jsonify({"msg": "Error al obtener producto"}), 500

@api.route('/products/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    try:
        product = get_or_404(Product, id)
        data = request.json
        if not data or not data.get('name') or not data.get('price') or not data.get('quantity'):
            return jsonify({"msg": "Falta información del producto"}), 400
        product.name = data['name']
        product.price = data['price']
        product.quantity = data['quantity']
        db.session.commit()
        return jsonify({'message': 'Producto actualizado'})
    except Exception as e:
        db.session.rollback()
        if isinstance(e, HTTPException) and e.code == 404:
            return jsonify({"msg": "Producto no encontrado"}), e.code
        return jsonify({"msg": "Error al actualizar producto"}), 500

@api.route('/products/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    try:
        product = get_or_404(Product, id)
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Producto eliminado'})
    except Exception as e:
        db.session.rollback()
        if isinstance(e, HTTPException) and e.code == 404:
            return jsonify({"msg": "Producto no encontrado"}), e.code
        return jsonify({"msg": "Error al eliminar producto"}), 500