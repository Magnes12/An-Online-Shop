from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy()
db.init_app(app)


# class Product(db.Model):
#     __tablename__ = 'products'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255), nullable=False)
#     price = db.Column(db.Float, nullable=False)
#     stock = db.Column(db.Integer, nullable=False)
#     description = db.Column(db.String(255), nullable=False)

#     orders = db.relationship('Orders', back_populates='product')


# class User(db.Model):
#     __tablename__ = 'users'

#     id = db.Column(db.Integer, primary_key=True)
#     user_name = db.Column(db.String(255), nullable=False)
#     user_password = db.Column(db.String(255), nullable=False)

#     orders = db.relationship('Orders', back_populates='user')


# class Orders(db.Model):
#     __tablename__ = 'orders'

#     id = db.Column(db.Integer, primary_key=True)
#     user_name_id = db.Column(db.Integer, db.ForeignKey('users.id'),
#                              nullable=False)
#     product_id = db.Column(db.Integer, db.ForeignKey('products.id'),
#                            nullable=False)

#     user = db.relationship('User', back_populates='orders')
#     product = db.relationship('Product', back_populates='orders')


# with app.app_context():
#     db.create_all()


@app.route("/")
def home():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
