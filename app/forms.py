from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User


class ContactForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(message="Введіть своє ім'я!")]
                       )
    # email = StringField('Email',
    #                     validators=[DataRequired(message="Введіть свій email"),
    #                                 Email(message="Невірно введений email!")]
    #                     )
    message = TextAreaField('Message',
                            validators=[
                                DataRequired(),
                                Length(min=2, max=100,
                                       message="Текстове повідомлення повинне містити від 2 до 200 символів!")]
                            )
    submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
    username = StringField('Username',
        validators=[DataRequired(), Length(min=3, max=20, message="Username повинен бути від 3 до 20 символів")])
    # email = StringField('Email', validators=[DataRequired(), Email(message="Невірно введений email!")])

    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=8, message="Пароль повинен містити від 8 символів")])

    confirm_password = PasswordField('Підтвердіть пароль',
        validators=[DataRequired(), EqualTo('password', message="Паролі не співпадають")])

    submit = SubmitField("Зареєструватися")

    def validate_username(self, username):
        user = User.query.filter_by(user_login=username.data).first()
        if user:
            raise ValidationError('Такий юзернейм вже існує, виберіть інший')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])

    password = PasswordField('Пароль', validators=[DataRequired()])

    submit = SubmitField("Вхід")


class UserBookForm(FlaskForm):
    name_book = StringField('Назва книги', validators=[DataRequired(message="Введіть назву книги!")])

    name_author = StringField('Ім\'я автора', validators=[DataRequired(message="Введіть автора книги!")])

    surname_author = StringField('Прізвище автора', validators=[DataRequired(message="Введіть автора книги!")])

    price = IntegerField('Ціна', validators=[DataRequired(message="Введіть ціну книги!")])

    date_added = DateField('Дата покупки(YYYY-MM-DD)', validators=[DataRequired(message="Введіть дату покупки!")])

    submit = SubmitField("Додати")

class BookForm(FlaskForm):
    name_book = StringField('Назва книги', validators=[DataRequired(message="Введіть назву книги!")])

    name_author = StringField('Ім\'я автора', validators=[DataRequired(message="Введіть автора книги!")])

    surname_author = StringField('Прізвище автора', validators=[DataRequired(message="Введіть автора книги!")])

    description = TextAreaField('Опис', validators=[DataRequired(message="Введіть опис книги!")])

    page = IntegerField('Кількість сторінок', validators=[DataRequired(message="Введіть кількість сторінок!")])

    year = IntegerField('Рік')

    publisher = StringField('Видавництво', validators=[DataRequired(message="Введіть назву видавництва!")])

    category = StringField('Категорія', validators=[DataRequired(message="Введіть категорію книги!")])

    submit = SubmitField("Додати")

class UpdateForm(FlaskForm):
    data_readed = DateField('Дата прочитання(YYYY-MM-DD)', validators=[DataRequired(message="Введіть дату покупки!")])

    rating = IntegerField('Оцінка')

    rewiew = TextAreaField('Рецензія на книгу')

    submit = SubmitField("Додати")

