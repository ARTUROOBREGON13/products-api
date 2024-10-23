import pytest
from app import create_app, db
from app.models import User, Product

@pytest.fixture
def app():
    app = create_app(True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context(): 
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_login(client):
    # Crear un usuario de prueba
    user = User(username='test')
    user.set_password('test')
    db.session.add(user)
    db.session.commit()

    # Intentar iniciar sesión con credenciales correctas
    response = client.post('/login', json={'username': 'test', 'password': 'test'})
    assert response.status_code == 200
    assert 'access_token' in response.json

    # Intentar iniciar sesión con credenciales incorrectas
    response = client.post('/login', json={'username': 'test', 'password': 'wrong'})
    assert response.status_code == 401

def test_create_product(client):
    # Crear un usuario de prueba y obtener un token JWT
    user = User(username='test')
    user.set_password('test')
    db.session.add(user)
    db.session.commit()
    
    # Crear un producto de prueba
    response = client.post('/login', json={'username': 'test', 'password': 'test'})
    access_token = response.json['access_token']

    # Crear un producto de prueba
    response = client.post('/products', json={'name': 'New Product', 'price': 9.99, 'quantity': 10},
                            headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 201

    # Intentar crear un producto con información incompleta
    response = client.post('/products', json={'name': 'New Product'},
                            headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 400

def test_get_products(client):
    # Crear un usuario de prueba y obtener un token JWT
    user = User(username='test')
    user.set_password('test')
    db.session.add(user)
    db.session.commit()
    
    # Crear un producto de prueba
    response = client.post('/login', json={'username': 'test', 'password': 'test'})
    access_token = response.json['access_token']
    
    # Crear varios productos de prueba
    products = [
        Product(name='Product 1', price=10.99, quantity=5),
        Product(name='Product 2', price=9.99, quantity=10),
        Product(name='Product 3', price=12.99, quantity=15)
    ]
    db.session.add_all(products)
    db.session.commit()

    # Intentar obtener la lista de productos
    response = client.get('/products', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert len(response.json['products']) == 3

def test_get_product(client):
    # Crear un usuario de prueba y obtener un token JWT
    user = User(username='test')
    user.set_password('test')
    db.session.add(user)
    db.session.commit()
    
    # Crear un producto de prueba
    response = client.post('/login', json={'username': 'test', 'password': 'test'})
    access_token = response.json['access_token']
    
    # Crear un producto de prueba
    product = Product(name='Test Product', price=10.99, quantity=5)
    db.session.add(product)
    db.session.commit()

    # Intentar obtener un producto por ID
    response = client.get(f'/products/{product.id}', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert response.json['name'] == 'Test Product'

def test_update_product(client):
    # Crear un usuario de prueba y obtener un token JWT
    user = User(username='test')
    user.set_password('test')
    db.session.add(user)
    db.session.commit()
    
    # Crear un producto de prueba
    response = client.post('/login', json={'username': 'test', 'password': 'test'})
    access_token = response.json['access_token']
    
    # Crear un producto de prueba
    product = Product(name='Test Product', price=10.99, quantity=5)
    db.session.add(product)
    db.session.commit()

    # Intentar actualizar un producto
    response = client.put(f'/products/{product.id}', json={'name': 'New Name', 'price': 9.99, 'quantity': 10}, 
                            headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200

def test_delete_product(client):
    # Crear un usuario de prueba y obtener un token JWT
    user = User(username='test')
    user.set_password('test')
    db.session.add(user)
    db.session.commit()
    # Crear un producto de prueba
    response = client.post('/login', json={'username': 'test', 'password': 'test'})
    access_token = response.json['access_token']
    
    # Crear un producto de prueba
    product = Product(name='Test Product', price=10.99, quantity=5)
    db.session.add(product)
    db.session.commit()

    # Intentar eliminar un producto
    response = client.delete(f'/products/{product.id}', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200

def test_products_pagination(client):
    # Crear un usuario de prueba y obtener un token JWT
    user = User(username='test')
    user.set_password('test')
    db.session.add(user)
    db.session.commit()

    response = client.post('/login', json={'username': 'test', 'password': 'test'})
    access_token = response.json['access_token']

    # Crear varios productos de prueba
    for i in range(15):
        product = Product(name=f'Product {i}', price=10.99, quantity=5)
        db.session.add(product)
    db.session.commit()

    # Intentar obtener la primera página de productos
    response = client.get('/products?page=1&limit=10', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert len(response.json['products']) == 10  # Debe devolver 10 productos en la primera página

    # Intentar obtener la segunda página de productos
    response = client.get('/products?page=2&limit=10', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert len(response.json['products']) == 5  # Debe devolver los productos restantes

def test_delete_non_existent_product(client):
    # Crear un usuario de prueba y obtener un token JWT
    user = User(username='test')
    user.set_password('test')
    db.session.add(user)
    db.session.commit()

    response = client.post('/login', json={'username': 'test', 'password': 'test'})
    access_token = response.json['access_token']

    # Intentar eliminar un producto que no existe
    response = client.delete(f'/products/9999', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 404
    assert 'Producto no encontrado' in response.json['msg']
    
def test_protected_routes_without_auth(client):
    # Intentar acceder a una ruta protegida sin autenticación
    response = client.get('/products')
    assert response.status_code == 401
    assert 'Missing Authorization Header' in response.json['msg']