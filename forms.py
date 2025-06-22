from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, RadioField, SubmitField, IntegerField
from wtforms.validators import Optional, DataRequired, length, equal_to
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
    birthdate =  DateField("შეიყვანეთ თარიღი", validators=[DataRequired()])
    mobile_number =  IntegerField("შეიყვანეთ ნომერი", validators=[DataRequired()])
    gender =  RadioField("აირჩიე სქესი", choices=["ქალი", "კაცი"], validators=[DataRequired()])
    country =  SelectField(choices=[
        ("", "აირჩიე ქვეყანა"),
        ("საქართველო", "საქართველო"),
        ("იაპონია", "იაპონია"),
        ("ამერიკა", "ამერიკა")
    ], validators=[DataRequired()])
    register_button = SubmitField()

class AuctionForm(FlaskForm):
    image = FileField("ატვირთეთ პროდუქტის ფოტო", validators=[
        FileRequired(message="პროდუქტის ფოტო აუცილებელია"),
        FileAllowed(['jpg', 'png', 'jpeg', 'webp', 'svg'], 'მხოლოდ ფოტოები!'),
        FileSize(max_size=20 * 1024 * 1024, message="ფოტოების მაქსიმალური ზომაა 20mb")
                ])
    product_name = StringField("შეიყვანე პროდუქტის სახელი", validators=[DataRequired()])
    description = StringField("შეიყვანეთ აღწერა", validators=[DataRequired()])
    type = SelectField(choices=[
        ("", "აირჩიე ტიპი"),
        ("moisturizer", "დამატენიანებელი"),
        ("spf", "მზისგან დამცავი"),
        ("cleanser", "სახის დასაბანი გელი")
    ], validators=[DataRequired()])
    submit_auction = SubmitField()


