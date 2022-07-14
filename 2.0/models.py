from flask_mysqldb import MySQL
from passlib.hash import pbkdf2_sha256

from app import app

mysql = MySQL(app)

class Person:
    def __init__(self, name, lastname, email, password, phonenumber, id=None):
        self.__id = id
        self.__name = name
        self.__lastname = lastname
        self.__email = email
        self.__phonenumber = phonenumber
        self.__password = password
        self.__shopping_car = None

    def get_id(self):
        return self.__id
   
    @property
    def id(self):
        return self.__id

    def is_correct_password(self, password):
        return pbkdf2_sha256.verify(password, self.__password)

    def set_password_encrypt(self):
        self.__password = pbkdf2_sha256.hash(self.__password)

    def save(self):
        self.set_password_encrypt()
        cursor = mysql.connection.cursor()
        cursor.execute("insert into user(name, lastname, email, password, phonenumber) values(%s, %s, %s, %s, %s)", (self.__name, self.__lastname, self.__email, self.__password, self.__phonenumber))
        mysql.connection.commit()

    def delete(self):
        """delete from database"""
        pass

    def edit(self):
        """edit fromd atabase"""
        pass

    def read(self):
        """read an object"""
        pass
    
    @property
    def shopping_car(self):
        cursor = mysql.connection.cursor()
        cursor.execute("""select product.description, product.price, product.stock, product.image, product.user_id, product.id from product
                inner join shoppingcar on shoppingcar.product_id = product.id
                and shoppingcar.user_id=%s""", (self.__id, ))
        datas = cursor.fetchall()
        if datas:
            return [Product(data[0], data[1], data[2], data[3], data[4], data[5]) for data in datas] 
        return []

    def delete_product_from_car(self, id):
        print(id, self.__id, sep="---")
        cursor = mysql.connection.cursor()
        cursor.execute("delete from shoppingcar where product_id=%s and user_id=%s", (id, self.__id))
        mysql.connection.commit()
    
    def add_to_car(self, id):
        cursor = mysql.connection.cursor()
        cursor.execute("insert into shoppingcar(user_id, product_id) values(%s, %s)", (self.__id, id))
        mysql.connection.commit()

    @staticmethod
    def getByEmail(email):
        cursor = mysql.connection.cursor()
        cursor.execute("select id, name, lastname, email, password, phonenumber from user where email = %s", (email,))
        data = cursor.fetchone()
        if data:
            return Person(data[1],data[2], data[3], data[4], data[5], data[0])
        return None

    @staticmethod
    def get_by_id(id):
        cursor = mysql.connection.cursor()
        cursor.execute("select id, name, lastname, email, password, phonenumber from user where id = %s", (id,))
        data = cursor.fetchone()
        if data:
            return Person(data[1],data[2], data[3], data[4], data[5], data[0])
        return None


class Product:

    def __init__(self, description, price, stock, image, user_id, id=None):
        self.__id = id
        self.__description = description
        self.__price = price
        self.__user_id = user_id
        self.__stock = stock
        self.__image = image

    def save(self):
        """save in database"""
        cursor = mysql.connection.cursor()
        cursor.execute("insert into product(description, price, stock, image, user_id) values(%s, %s, %s, %s, %s)", (self.__description, self.__price, self.__stock, self.__image, self.__user_id))
        mysql.connection.commit()
    
    @property
    def id(self):
        return self.__id

    @property
    def description(self):
        return self.__description

    @property
    def price(self):
        return self.__price

    @property
    def user_id(self):
        return self.__user_id

    @property
    def stock(self):
        return self.__stock

    @property
    def image(self):
        return self.__image

    @staticmethod
    def get_by_user_id(id):
        cursor = mysql.connection.cursor()
        cursor.execute("select description, price, stock, image, user_id, id from product where user_id=%s", (id,))
        datas = cursor.fetchall()
        if datas:
            return [Product(data[0], data[1], data[2], data[3], data[4], data[5]) for data in datas]
        return []

    @staticmethod
    def get_by_id(id):
        cursor = mysql.connection.cursor()
        cursor.execute("select description, price, stock, image, user_id, id from product where user_id!=%s", (id,))
        datas = cursor.fetchall()
        if datas:
            return [Product(data[0], data[1], data[2], data[3], data[4], data[5]) for data in datas]
        return []

        self.__user_id = user_id
        self.__product_id = product_id


