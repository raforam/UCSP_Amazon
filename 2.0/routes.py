import uuid
import os
import base64

from flask import render_template, jsonify, request, redirect, url_for
from flask_jwt_extended import JWTManager,create_access_token, jwt_required, get_jwt_identity, set_access_cookies, unset_jwt_cookies

from app import app
from models import Person, Product

jwt = JWTManager(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    if request.get_json():
        email = request.get_json().get("email")
        password = request.get_json().get("password")
        if email and password:
            person = Person.getByEmail(email)
            if person:
                if person.is_correct_password(password):
                    access_token = create_access_token(identity=person.id)
                    response = jsonify(status=200,
                                    message="acces correct")
                    set_access_cookies(response, access_token)
                    return response
                return jsonify(status=404,message="password incorrecta")
            return jsonify(status=404,
                            message="email o password incorrectos")
        return jsonify(status=400,message="Faltan Datos")
    return jsonify(status=400,
                        message="Faltan datos")

@app.route("/signup")
def sign_up():
    return render_template("signup.html")

@app.route("/signup_action", methods=["POST"])
def signup_action():
    if request.get_json():
        name = request.get_json().get("name")
        lastname = request.get_json().get("lastname")
        email = request.get_json().get("email")
        password = request.get_json().get("password")
        phonenumber = request.get_json().get("phonenumber")

        if name and lastname and email and password:
            person = Person.getByEmail(email)
            if not person:
                person = Person(name, lastname, email, password, phonenumber)
                person.save()
                return jsonify(status=200,
                    message="Se ha registrado al Usuario con exito")
            return jsonify(status=400,
                message="Ya existe un usuario con ese correo")
        return jsonify(status=400,message="Faltan Datos")
    return jsonify(status=400,
            message = "Faltan Datos")

@app.route("/sale")
def sale():
    return render_template("sale.html")

@app.route("/getmyproducts", methods=["GET"])
@jwt_required()
def get_my_products():
    id = get_jwt_identity()
    products = Product.get_by_user_id(id)
    return jsonify(status=200, 
            products=[ {"id":product.id, "description":product.description ,"price": product.price,  "stock":product.stock,  "image":product.image} for product in products])

@app.route("/getproductstosale", methods=["GET"])
@jwt_required()
def get_products_to_sale():
   id = get_jwt_identity()
   products = Product.get_by_id(id)
   return jsonify(status=200, 
            products=[ {"id":product.id, "description":product.description ,"price": product.price,  "stock":product.stock,  "image":product.image} for product in products])

@app.route("/buy")
def buy():
    return render_template("buy.html")

@app.route("/register_product", methods=["POST"])
@jwt_required()
def register_product():
    """registra los productos a vender"""
    if request.form and request.files:
        description = request.form.get("description")
        price = request.form.get("price")
        stock = request.form.get("stock")
        image = request.files.get("image")
        if description and price and stock and image:
            # here current user
            if image.filename.endswith(".jpg") or image.filename.endswith(".png"):
                imagename = str(uuid.uuid4()) + image.filename[-4:]
                product = Product(description, price, stock, imagename, get_jwt_identity())
                path_resulting = os.path.join(app.config["UPLOAD_IMAGE"], imagename)
                image.save(path_resulting)
                product.save()
                return jsonify(status=200, message="Producto ha sido registrado")
            return jsonify(status=404, message="Formato de imagen no permitida")
        return jsonify(status=400,message="Faltan Datos")
    return jsonify(status=400,message="Faltan Datos")


@app.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    response = jsonify(status=200, message="logout successfully")
    unset_jwt_cookies(response)
    return response


@app.route("/shoppingcar")
def shopppingcar():
    return render_template("shoppingcar.html")

@app.route("/getmyshoppingcar", methods=["GET"])
@jwt_required()
def get_my_shopping_car():
    id = get_jwt_identity()
    user = Person.get_by_id(id)
    return jsonify(status=200,
            products=[ {"id":product.id, "description":product.description ,"price": product.price,  "stock":product.stock,  "image":product.image} for product in user.shopping_car])


@app.route("/addtocar", methods=["POST"])
@jwt_required()
def add_to_car():
    if request.get_json():
        id = request.get_json().get("id")
        if id:
            product = Product.get_by_id(id)
            if product:
                user = Person.get_by_id(get_jwt_identity())
                user.add_to_car(id)
                return jsonify(status=200, message="El producto se agrego a su carrito de Compras")
            return jsonify(status=404, message="Ocurrio un problema. Intentelo de nuevo")
        return jsonify(status=400, message="Faltan datos")
    return jsonify(status=400, message="Faltan datos")

@app.route("/delete_item_car", methods=["DELETE"])
@jwt_required()
def delete_item_car():
    if request.get_json():
        id = request.get_json().get("id")
        if id:
            user = Person.get_by_id(get_jwt_identity())
            user.delete_product_from_car(id)
            return jsonify(status=200, message="El producto ha sido eliminado de su carrito de compra")
        return jsonify(status=400, message="Faltan datos")
    return jsonify(status=400, message="Faltan datos")
