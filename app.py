from flask import Flask
from db import orm
from flask_migrate import Migrate
from flask_caching import Cache


from dotenv import load_dotenv 
import os

load_dotenv()

app = Flask(__name__)
app.config['CACHE_TYPE'] = os.getenv('CACHE_TYPE')
app.config['CACHE_DEFAULT_TIMEOUT'] = os.getenv('CACHE_DEFAULT_TIMEOUT')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('MYSQL_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')

orm.init_app(app)
migrate = Migrate(app, orm)
cache = Cache(app)

from blueprints.user import user_bp
from blueprints.blog import blog_bp

# Register Blueprints
app.register_blueprint(user_bp)
app.register_blueprint(blog_bp)

if __name__ == '__main__':
    with app.app_context():
        orm.create_all()
    app.run(debug=True)
