from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username',
        validators=[DataRequired(), Length(min=3, max=20, message="Username повинен бути від 3 до 20 символів")])
    email = StringField('Email', validators=[DataRequired(), Email(message="Невірно введений email!")])

    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=5, message="Пароль повинен містити від 5 символів")])

    confirm_password = PasswordField('Підтвердіть пароль',
        validators=[DataRequired(), EqualTo('password', message="Паролі не співпадають")])

    submit = SubmitField("Зареєструватися")


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message="Невірно введений email!")])

    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=5, message="Пароль повинен містити від 5 символів")])

    submit = SubmitField("Вхід")




class ContactForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(message="Введіть своє ім'я!")]
                       )
    email = StringField('Email',
                        validators=[DataRequired(message="Введіть свій email"),
                                    Email(message="Невірно введений email!")]
                        )
    message = TextAreaField('Message',
                            validators=[
                                DataRequired(),
                                Length(min=2, max=100,
                                       message="Текстове повідомлення повинне містити від 2 до 200 символів!")]
                            )
    submit = SubmitField('Submit')
