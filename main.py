from flask import Flask, render_template, redirect, url_for, abort, flash
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from classes import NewUser, CurrentUser, AddProduct 

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
db = SQLAlchemy()
db.init_app(app)

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=False)

    orders = db.relationship('Orders', back_populates='product')


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255), nullable=False)
    user_password = db.Column(db.String(255), nullable=False)

    orders = db.relationship('Orders', back_populates='user')


class Orders(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_name_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                             nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'),
                           nullable=False)

    user = db.relationship('User', back_populates='orders')
    product = db.relationship('Product', back_populates='orders')


with app.app_context():
    db.create_all()


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
    products = db.session.query(Product).all()
    return render_template('index.html', products=products)


@app.route("/admin")
def admin():
    return render_template('admin.html')


@app.route("/admin/products", methods=["GET", "POST"])
def admin_panel_products():
    products = db.session.query(Product).all()
    form = AddProduct()
    if form.validate_on_submit():
        product = Product(
            name = form.name.data,
            price = form.price.data,
            stock = form.stock.data,
            description = form.description.data,
        )
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('admin_panel_products'))
    
    return render_template('admin-products.html', form=form, products=products)


@app.route("/admin/products/delete/<int:product_id>")
def delete_product(product_id):
    product_to_delete = db.get_or_404(Product, product_id)
    db.session.delete(product_to_delete)
    db.session.commit()
    return redirect(url_for('admin_panel_products'))


@app.route("/admin/orders")
def admin_panel_orders():
    return render_template('admin-orders.html')


@app.route("/admin/customers")
def admin_panel_customers():
    return render_template('admin-customers.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    form = CurrentUser()
    if form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = NewUser()
    if form.validate_on_submit():
        result = db.session.execute(db.select(User).where(User.user_name == form.user_name.data))
        user = result.scalar()
        if user:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))
        new_user = User(
            user_name = form.user_name.data,
        user_password = form.user_password.data,
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('register.html', form=form)


@app.route("/cart")
def cart():
    return render_template('cart.html')


if __name__ == "__main__":
    app.run(debug=True)
