import cloudinary
from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "732$@#%#$&&^dhfjdfgf@#$#^%^^%&"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/stumansys?charset=utf8mb4" \
                                        % quote('Byt.123456')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True


db = SQLAlchemy(app)
login = LoginManager(app)

cloudinary.config(cloud_name='ddpchchrn', api_key='354796781585766', api_secret='jfNB0Bm2xSRc04s_kLGpnS-o5Wk')
