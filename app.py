# Flask app with SQLAlchemy ORM & blueprints
from flask import Flask
from db import orm
from blueprints.user import user_bp
from blueprints.blog import blog_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/hobbies'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

orm.init_app(app)

# Register Blueprints
app.register_blueprint(user_bp)
app.register_blueprint(blog_bp)

if __name__ == '__main__':
    with app.app_context():
        orm.create_all()
    app.run(debug=True)
