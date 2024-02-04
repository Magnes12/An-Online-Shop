from flask import Flask, render_template, redirect, url_for
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


@app.route("/register", methods=['POST', 'GET'])
def register():
    form = NewUser()
    if form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
