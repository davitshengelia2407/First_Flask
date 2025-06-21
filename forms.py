from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, RadioField, SubmitField, IntegerField
from wtforms.validators import Optional, DataRequired, length, equal_to
from flask_wtf.file import FileField, FileAllowed, FileRequired, FileSize


class RegisterForm(FlaskForm):
    image = FileField("ატვირთეთ ფოტო", validators=[ FileRequired(message="profile image is required"),
                      FileAllowed(['jpg', 'png', 'jpeg', 'webp', 'svg'], 'Images only!'),
                      FileSize(max_size=20 * 1024 * 1024, message="Image must be less than 20MB")
                                                    ])
    username = StringField('შეიყვანე სახელი', validators=[DataRequired()])
    password = PasswordField("შეიყვანე პაროლი", validators=[DataRequired(), length(min=8, max=20)])
    confirm_password = PasswordField("გაიმეორე პაროლი", validators=[DataRequired(), equal_to("password")])
    birthdate =  DateField("შეიყვანეთ თარიღი", validators=[DataRequired()])
    mobile_number =  IntegerField("შეიყვანეთ ნომერი", validators=[DataRequired()])
    gender =  RadioField("აირჩიე სქესი", choices=["ქალი", "კაცი"], validators=[DataRequired()])
    country =  SelectField(choices=[
        ("", "აირჩიე ქვეყანა"),  # 👈 this empty string is key
        ("საქართველო", "საქართველო"),
        ("იაპონია", "იაპონია"),
        ("ამერიკა", "ამერიკა")
    ], validators=[DataRequired()])

    register_button = SubmitField()

