import os
from dotenv import load_dotenv

load_dotenv()  # se carga los datos del archivo .env
# el archivo .env solo funciona en desarrollo
# en produccion debe establecer esos datos en la variable de entorno del sistema
# la configuracion de eso dependerra que solucion que deploy utilizara

print([os.getenv("JWT_LOCATION_LOCATION"),])
class Setting(object):
    MYSQL_HOST = os.getenv("DATABASE_HOST")
    MYSQL_USER = os.getenv("DATABASE_USER")
    MYSQL_PASSWORD = os.getenv("DATABASE_PASSWORD")
    MYSQL_DB = os.getenv("DATABASE_DB")
    JWT_SECRET_KEY= os.getenv("JWT_SECRET_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY")
    UPLOAD_IMAGE = os.path.join(os.getcwd(), "static/img/upload")
    JWT_TOKEN_LOCATION = os.getenv("JWT_TOKEN_LOCATION")
