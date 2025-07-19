from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, RadioField, SubmitField, IntegerField, \
    TextAreaField
from wtforms.validators import Optional, DataRequired, length, equal_to, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired, FileSize
from wtforms.widgets import TextArea


class RegisterForm(FlaskForm):
    image = FileField("ატვირთეთ ფოტო", validators=[
        FileRequired(message="პროფილის ფოტო აუცილებელია"),
        FileAllowed(['jpg', 'png', 'jpeg', 'webp', 'svg'], 'მხოლოდ ფოტოები!'),
        FileSize(max_size=20 * 1024 * 1024, message="ფოტოების მაქსიმალური ზომაა 20mb")
                ])
    username = StringField('შეიყვანე სახელი', validators=[DataRequired()])
    password = PasswordField("შეიყვანე პაროლი", validators=[DataRequired(), length(min=8, max=20)])
    confirm_password = PasswordField("გაიმეორე პაროლი", validators=[DataRequired(), equal_to("password")])
    mobile_number =  IntegerField("შეიყვანეთ ნომერი", validators=[DataRequired()])
    register_button = SubmitField()

class LoginForm(FlaskForm):
    username = StringField('შეიყვანეთ სახელი')
    password = PasswordField("შეიყვანეთ  პაროლი")

    login_button = SubmitField("შესვლა")
    cancel_auth = SubmitField('გაუქმება')


class AuctionForm(FlaskForm):
    image = FileField("ატვირთეთ პროდუქტის ფოტო", validators=[
        FileRequired(message="პროდუქტის ფოტო აუცილებელია"),
        FileAllowed(['jpg', 'png', 'jpeg', 'webp', 'svg'], 'მხოლოდ ფოტოები!'),
        FileSize(max_size=20 * 1024 * 1024, message="ფოტოების მაქსიმალური ზომაა 20mb")
    ])
    product_name = StringField("პროდუქტის სახელი", validators=[DataRequired()])
    description = StringField("აღწერა", validators=[DataRequired()])
    price = IntegerField('საწყისი ფასი', validators=[DataRequired()])
    type = SelectField("ტიპი", choices=[
        ("", "აირჩიე ტიპი"),
        ("დამატენიანებელი", "დამატენიანებელი"),
        ("მზისგან დამცავი", "მზისგან დამცავი"),
        ("დასაბანი გელი", "დასაბანი გელი"),
        ("ექსფოლიატორი", "ექსფოლიატორი"),
        ("ტონერი", "ტონერი"),
        ("შრატი", "შრატი"),
        ("მასკა", "მასკა"),
        ("თვალის პაჩები", "თვალის პაჩები"),
        ("თვალის კრემი", "თვალის კრემი"),
        ("ბარიერის აღმდგენი", "ბარიერის აღმდგენი")
    ], validators=[DataRequired()])
    submit_auction = SubmitField('დაამატე აუქციონი')



class BrandForm(FlaskForm):
    name = StringField("შეიყვანეთ ბრენდის სახელი", validators=[DataRequired(), Length(max=50)])
    description =  TextAreaField("შეიყვანეთ ბრენდის აღწერა", validators=[DataRequired()])
    image = FileField("ატვირთეთ ბრენდის ფოტო", validators=[
        Optional(),
        FileAllowed(['jpg', 'png', 'jpeg', 'webp', 'svg'], 'მხოლოდ ფოტოები!'),
        FileSize(max_size=20 * 1024 * 1024, message="ფოტოების მაქსიმალური ზომაა 20mb")
    ])

    submit_brand =  SubmitField("დამატება")




class ProductForm(FlaskForm):
    image = FileField("ატვირთეთ პროდუქტის ფოტო", validators=[
        Optional(),
        FileAllowed(['jpg', 'png', 'jpeg', 'webp', 'svg'], 'მხოლოდ ფოტოები!'),
        FileSize(max_size=20 * 1024 * 1024, message="ფოტოების მაქსიმალური ზომაა 20mb")
    ])
    name = StringField("შეიყვანე პროდუქტის სახელი", validators=[DataRequired(), Length(max=50)])
    description = TextAreaField("შეიყვანეთ აღწერა", validators=[DataRequired()])
    price = IntegerField('შეიყვანეთ პროდუქტის ფასი', validators=[DataRequired()])
    type = SelectField(choices=[
        ("", "აირჩიე ტიპი"),
        ("დამატენიანებელი", "დამატენიანებელი"),
        ("მზისგან დამცავი", "მზისგან დამცავი"),
        ("დასაბანი გელი", "დასაბანი გელი"),
        ("ექსფოლიატორი", "ექსფოლიატორი"),
        ("ტონერი", "ტონერი"),
        ("შრატი", "შრატი"),
        ("მასკა", "მასკა"),
        ("თვალის პაჩები", "თვალის პაჩები"),
        ("თვალის კრემი", "თვალის კრემი"),
        ("ბარიერის აღმდგენი","ბარიერის აღმდგენი")

    ], validators=[DataRequired()])
    brand = SelectField("აირჩიე ბრენდი", choices=[], coerce=int, validators=[DataRequired()])
    stock = IntegerField("შეიყვანეთ მარაგი", validators=[DataRequired()])
    discount_price = IntegerField("შეიყვანეთ ფასდაკლებული ფასი", validators=[Optional()])
    submit_product = SubmitField('პროდუქტის დამატება')



