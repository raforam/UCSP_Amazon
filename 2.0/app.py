from flask import Flask
from settings import Setting


app = Flask(__name__)
app.config.from_object(Setting)


