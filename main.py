from flask import Flask, render_template, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
db = SQLAlchemy()
db.init_app(app)


class NewUser(FlaskForm):
    user_name = StringField('Name', validators=[DataRequired()])
    user_password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')


class CurrentUser(FlaskForm):
    user_name = StringField('Name', validators=[DataRequired()])
    user_password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

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

# # ADMIN DECORATOR
# # def admin_only(f):
# #     @wrapper(f)
# #     def decorated_function(*args, **kwargs):
# #         if user.id !=1:
# #             return abort(403)
# #         return f(*args, **kwargs)

# #     return decorated_function


@app.route("/")
def home():
    # TODO add functionality
    return render_template('index.html')


@app.route("/admin")
def admin_panel():
    return render_template('admin.html')


@app.route("/admin/products")
def admin_panel_products():
    return render_template('admin products.html')


@app.route("/admin/orders")
def admin_panel_orders():
    return render_template('admin orders.html')


@app.route("/admin/customers")
def admin_panel_customers():
    return render_template('admin customers.html')


@app.route("/login", methods=['POST', 'GET'])
def login():
    form = CurrentUser()
    # TODO check if log in user is in db
    if form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route("/register", methods=['POST', 'GET'])
def register():
    # TODO add new user to db
    form = NewUser()
    if form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route("/cart")
def cart():
    return render_template('cart.html')


if __name__ == "__main__":
    app.run(debug=True)
