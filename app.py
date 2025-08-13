from flask import Flask
from db import orm
from blueprints.user import user_bp
from blueprints.blog import blog_bp
from dotenv import load_dotenv 
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('MYSQL_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

orm.init_app(app)

# Register Blueprints
app.register_blueprint(user_bp)
app.register_blueprint(blog_bp)

if __name__ == '__main__':
    with app.app_context():
        orm.create_all()
    app.run(debug=True)
