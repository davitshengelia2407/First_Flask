from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, IntegerField, TextAreaField, ValidationError, \
    FloatField
from wtforms.validators import Optional, DataRequired, length, equal_to, Length, Regexp
from flask_wtf.file import FileField, FileAllowed, FileRequired, FileSize


class RegisterForm(FlaskForm):
    image = FileField("ატვირთეთ ფოტო", validators=[
        FileRequired(message="პროფილის ფოტო აუცილებელია"),
        FileAllowed(['jpg', 'png', 'jpeg', 'webp', 'svg'], 'მხოლოდ ფოტოები!'),
        FileSize(max_size=20 * 1024 * 1024, message="ფოტოების მაქსიმალური ზომაა 20mb")
                ])
    username = StringField('შეიყვანე სახელი', validators=[DataRequired()])
    password = PasswordField("შეიყვანე პაროლი", validators=[DataRequired(), length(min=8, max=20)])
    confirm_password = PasswordField("გაიმეორე პაროლი", validators=[DataRequired(), equal_to("password")])
    mobile_number =  StringField("შეიყვანეთ ნომერი", validators=[DataRequired(), length(min=9, max=15)])
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
    price = FloatField('საწყისი ფასი', validators=[DataRequired()])
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
    name = StringField("შეიყვანეთ ბრენდის სახელი", validators=[DataRequired(), Length(max=100)])
    description =  TextAreaField("შეიყვანეთ ბრენდის აღწერა", validators=[DataRequired()])
    image = FileField("ატვირთეთ ბრენდის ფოტო", validators=[
        Optional(),
        FileAllowed(['jpg', 'png', 'jpeg', 'webp', 'svg'], 'მხოლოდ ფოტოები!'),
        FileSize(max_size=20 * 1024 * 1024, message="ფოტოების მაქსიმალური ზომაა 20mb")
    ])

    submit_brand =  SubmitField("დამატება")




from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, TextAreaField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Optional, NumberRange, Length
from flask_wtf.file import FileAllowed, FileSize

class ProductForm(FlaskForm):
    image = FileField("ატვირთეთ პროდუქტის ფოტო", validators=[
        Optional(),
        FileAllowed(['jpg', 'png', 'jpeg', 'webp', 'svg'], 'მხოლოდ ფოტოები!'),
        FileSize(max_size=20 * 1024 * 1024, message="ფოტოების მაქსიმალური ზომაა 20mb")
    ])
    name = StringField("შეიყვანე პროდუქტის სახელი", validators=[DataRequired(), Length(max=50)])
    description = TextAreaField("შეიყვანეთ აღწერა", validators=[DataRequired()])
    price = FloatField('შეიყვანეთ პროდუქტის ფასი', validators=[DataRequired(), NumberRange(min=0, message="ფასი ვერ იქნება უარყოფითი")])
    discount_price = FloatField("შეიყვანეთ ფასდაკლებული ფასი", validators=[Optional(), NumberRange(min=0, message="ფასდაკლება ვერ იქნება უარყოფითი")])
    stock = IntegerField("შეიყვანეთ მარაგი", validators=[DataRequired(), NumberRange(min=0, message="მარაგი ვერ იქნება უარყოფითი")])
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
    submit_product = SubmitField('პროდუქტის დამატება')




class CardAuthorizationForm(FlaskForm):
    card_number = StringField('Card Number', validators=[
        DataRequired(),
        Regexp(r'^\d{15,16}$', message="Card number must be 15 or 16 digits")
    ])

    expiry = StringField('Expiry Date (MM/YY)', validators=[
        DataRequired(),
        Regexp(r'^(0[1-9]|1[0-2])\/\d{2}$', message="Use MM/YY format")
    ])

    cvv = StringField('CVV (CCV)', validators=[
        DataRequired(),
        Regexp(r'^\d{3,4}$', message="CVV must be 3 or 4 digits")
    ])

    submit = SubmitField('Authorize Payment')

    def validate(self, **kwargs):  # ✅ accepts extra_validators
        rv = super().validate(**kwargs)
        if not rv:
            return False

        card_number = self.card_number.data
        cvv = self.cvv.data

        if card_number.startswith(('34', '37')):  # AmEx
            if len(card_number) != 15:
                self.card_number.errors.append("AmEx cards must have 15 digits.")
                return False
            if len(cvv) != 4:
                self.cvv.errors.append("AmEx CVV must be 4 digits.")
                return False
        else:
            if len(card_number) != 16:
                self.card_number.errors.append("Card number must be 16 digits.")
                return False
            if len(cvv) != 3:
                self.cvv.errors.append("CVV must be 3 digits.")
                return False

        return True




class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Ძველი პაროლი", validators=[DataRequired()])
    new_password = PasswordField("ახალი პაროლი", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField("Დადასტურება", validators=[DataRequired()])





