from flask import Flask

from flask_login import LoginManager
import os
import cloudinary
import cloudinary.uploader
from .routes import api_blue as api_blueprint
from .extension import db, bcrypt, jwt, mail
from flask_cors import CORS



def create_app():
  app = Flask(__name__)
  CORS(app)
  

  app.config['SECRET_KEY'] = '2d8926762ccbac889d55b32635333a91'
  app.config['JWT_SECRET_KEY'] = '2d8926762ccbac889d55b326334567'  



  cloudinary.config(  
    cloud_name = "duyoxldib", 
    api_key = "778871683257166", 
    api_secret = "NM2WHVuvMytyfnVziuzRScXrrNk" 
  )

  DB_PATH = os.environ.get('SQLITE_DB_PATH', 'sqlite:///mydatabase.db')  # Default SQLite path
  app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH
  app.config['SECRET_KEY'] = '1e04deb868b1640f313bbb8c680f3d49'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
  app.config['MAIL_PORT'] = 587
  app.config['MAIL_USE_TLS'] = True
  app.config['MAIL_USERNAME'] = "kingsleydike318@gmail.com"
  app.config['MAIL_PASSWORD'] = 'byyhvorltumsxffq'

  db.init_app(app)
  bcrypt.init_app(app)
  jwt.init_app(app)
  mail.init_app(app)
  CORS(app, supports_credentials=True)
  
  app.register_blueprint(api_blueprint, 
                         url_prefix='/api')


  
  return app