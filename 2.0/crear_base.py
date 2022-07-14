import MySQLdb
from dotenv import load_dotenv
import os

load_dotenv()

try:
    c = MySQLdb.connect(
                os.getenv("DATABASE_HOST"),
                os.getenv("DATABASE_USER"),
                os.getenv("DATABASE_PASSWORD"),
                os.getenv("DATABASE_DB")
            )
    cursor = c.cursor()
    cursor.execute(f"drop table if exists shoppingcar;")
    cursor.execute(f"drop table if exists product;")
    cursor.execute(f"drop table if exists user;")

    cursor.execute("""create table user(
        id int auto_increment,
        name varchar(200) not null,
        lastname varchar(200) not null,
        email varchar(200) not null,
        password varchar(300) not null,
        phonenumber int not null,
        primary key(id));""")

    cursor.execute("""create table product(
        id int auto_increment,
        description varchar(200) not null,
        price float not null,
        stock int not null,
        image varchar(200) not null,
        user_id int not null,
        primary key(id),
        foreign key(user_id) references user(id) on delete cascade
    );""")

    cursor.execute("""create table shoppingcar(
        user_id int not null,
        product_id int not null,
        foreign key(user_id) references user(id) on delete cascade,
        foreign key(product_id) references product(id) on delete cascade
    );""")

    print("Se han creado las tablas.")
    c.close()
except Exception as e:
    print(e)
