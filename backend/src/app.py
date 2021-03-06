#src/app.py

from flask import Flask

from .config import app_config
from .models import db, bcrypt
from .models import UserModel, ReviewModel, NodeModel,AmenityModel,TourismModel,ShopModel

def create_app(env_name):
  """
  Create app
  """

  # app initiliazation
  app = Flask(__name__)

  app.config.from_object(app_config[env_name])

  # initializing bcrypt
  bcrypt.init_app(app)

  db.init_app(app)

  @app.route('/', methods=['GET'])
  def index():
    """
    example endpoint
    """
    return 'Welcome!'

  return app
