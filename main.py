from flask import Flask, render_template, redirect, url_for, abort, flash
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from forms import NewUser, CurrentUser, AddProduct
from functools import wraps

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
db = SQLAlchemy()
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=False)

    carts = db.relationship('Cart', back_populates='product')


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    carts = db.relationship('Cart', back_populates='user')
    orders = db.relationship('Order', back_populates='user')


class Cart(db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True)
    user_name_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                             nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'),
                           nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    user = db.relationship('User', back_populates='carts')
    product = db.relationship('Product', back_populates='carts')
    orders = db.relationship('Order', back_populates='cart')


class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'),
                        nullable=False)
    price = db.Column(db.Float, nullable=False)

    user = db.relationship('User', back_populates='orders')
    cart = db.relationship('Cart', back_populates='orders')


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def home():
    products = db.session.query(Product).all()
    return render_template('index.html', products=products,
                           current_user=current_user)


@app.route("/admin")
@admin_only
def admin():
    return render_template('admin.html')


@app.route("/admin/products", methods=["GET", "POST"])
@admin_only
def admin_panel_products():
    products = db.session.query(Product).all()
    form = AddProduct()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            price=form.price.data,
            stock=form.stock.data,
            description=form.description.data,
        )
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('admin_panel_products'))

    return render_template('admin-products.html', form=form, products=products)


@app.route("/admin/products/delete/<int:product_id>")
@admin_only
def delete_product(product_id):
    product_to_delete = db.get_or_404(Product, product_id)
    db.session.delete(product_to_delete)
    db.session.commit()
    return redirect(url_for('admin_panel_products'))


@app.route("/admin/orders")
@admin_only
def admin_panel_orders():
    orders = db.session.query(Order).all()
    return render_template('admin-orders.html', orders=orders)


@app.route("/admin/customers")
@admin_only
def admin_panel_customers():
    customers = db.session.query(User).all()
    return render_template('admin-customers.html', customers=customers)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = NewUser()
    if form.validate_on_submit():
        result = db.session.execute(db.select(User).where(User.username == form.user_name.data))
        user = result.scalar()
        if user:
            flash("You've already signed up with that name, log in instead!")
            return redirect(url_for('login'))

        hash_password = generate_password_hash(
            form.user_password.data,
            method='pbkdf2:sha256',
            salt_length=8,
        )
        new_user = User(
            username=form.user_name.data,
            password=hash_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))

    return render_template('register.html', form=form,
                           current_user=current_user)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = CurrentUser()
    if form.validate_on_submit():
        password = form.user_password.data
        result = db.session.execute(db.select(User).where(User.username == form.user_name.data))
        user = result.scalar()

        if not user:
            flash("That user name does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))

    return render_template('login.html', form=form, current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/add_to_cart/<int:product_id>")
@login_required
def add_to_cart(product_id):
    if current_user.is_authenticated:
        cart_item = Cart.query.filter_by(user_name_id=current_user.id,
                                         product_id=product_id).first()
        if cart_item:
            cart_item.quantity += 1
            db.session.commit()
            flash("Quantity updated in the cart!")
        else:
            product = db.session.query(Product).get(product_id)
            if product:
                cart_item = Cart(
                    user_name_id=current_user.id,
                    product_id=product.id,
                )
                db.session.add(cart_item)
                db.session.commit()
                flash("Product added to cart!")
            else:
                flash("Product not found!")
    else:
        flash("Please log in to add products to your cart.")
    return redirect(url_for('cart'))


@app.route("/cart")
def cart():
    cart_items = Cart.query.filter_by(user_name_id=current_user.id).all()
    product_names = {}
    for item in cart_items:
        product = Product.query.get(item.product_id)
        product_names[item.product_id] = {'name': product.name,
                                          'price': product.price}
    return render_template('cart.html', cart_items=cart_items,
                           product_names=product_names)


@app.route("/cart/payment/<int:cart_id>")
@login_required
def payment(cart_id):
    if current_user.is_authenticated:
        cart_item = Cart.query.filter_by(user_name_id=current_user.id,
                                         id=cart_id).first()
        product_item = Product.query.filter_by(id=cart_item.product_id).first()

        if cart_item:
            price_all = cart_item.quantity * product_item.price
            order = Order(
                user_id=current_user.id,
                cart_id=cart_item.id,
                price=price_all,
            )
            db.session.add(order)
            db.session.commit()
            flash("Order set!")
            return redirect(url_for('home'))

    flash("Error processing payment. Please check your cart.")
    return redirect(url_for('cart'))


if __name__ == "__main__":
    app.run(debug=True,
            port=5000)
