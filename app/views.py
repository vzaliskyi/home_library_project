# -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for, request, redirect, flash, session
from app import app, db, bcrypt
from app.forms import ContactForm, RegistrationForm, LoginForm
from app.models import User
from flask_login import login_user, current_user, logout_user
import json


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='LiBro')


@app.route("/about")
def about():
    return render_template('about.html', title='Про сторінку')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:#якщо користувач вже увійшов
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():#якщо валідація пройшла успішно
        user = User.query.filter_by(user_login=form.username.data).first()
        if user and bcrypt.check_password_hash(user.user_password, form.password.data):
            login_user(user)
            
            #переходимо на домашню сторінку
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:#якщо користувач вже увійшов
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():# якщо валідація пройшла успішно
        # flash(form.username.data + ' ' + form.email.data + ' ' + form.password.data)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # id
        id_ = db.session.query(User).order_by(User.id.desc()).first().id + 1

        # додаємо користувача до бд
        user = User(id=id_ ,user_login=form.username.data, user_password=hashed_password)
        db.session.add(user)
        db.session.commit()

        # flash('Account created succesfully', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


# @app.route("/contact", methods=['POST', 'GET'])
# def contact():
#     form = ContactForm()
#     session_name = session.get('name')
#     session_email = session.get('email')
#     print(f'contact-form is using by {session_name}')
#     # якщо користувач передає дані
#     if request.method == 'POST':
#         # і форма до того не була заповнена у поточній сесії (адже ім'я збережен в сесії відсутнє)
#         if session_name is None:
#             if form.validate_on_submit():
#                 # дістаємо дані із форм
#                 name = form.name.data
#                 email = form.email.data
#                 message = form.message.data
#                 # і записуємо ім'я та мейл у змінні сесії
#                 session['name'] = name
#                 session['email'] = email
#                 # зібрані дані із форми записуємо у json файл
#                 with open('data.json', 'a') as f:
#                     json.dump({'name': name, 'email': email, 'message': message}, f,
#                               indent=4, ensure_ascii=False)
#                 flash(f'Повідомлення від {name} було успішно надіслано', 'success')
#                 # виконуємо перенаправлення на сторінку 'контакт' із методом get
#                 return redirect(url_for('contact'))
#             else:
#                 flash('Деякі поля не пройшли валідацію, будь ласка, введіть дані ще раз', 'danger')
#         else:  # якщо форма до того ВЖЕ БУЛА заповнена у поточній сесії - то:
#             # значення полів ім'я та емейлу для проходження валідації беремо із змінних сесії
#             form.name.data = session_name
#             form.email.data = session_email
#             if form.validate_on_submit():
#                 # і нові дані зчитуємо лише з полля message
#                 message = form.message.data
#                 # зібрані дані із форми записуємо у json файл
#                 with open('data.json', 'a') as f:
#                     json.dump({'name': session_name, 'email': session_email, 'message': message}, f,
#                               indent=4, ensure_ascii=False)
#                 flash(f'Повідомлення від {form.name.data} було успішно надіслано', 'success')
#                 # виконуємо перенаправлення на сторінку 'контакт' із методом get
#                 return redirect(url_for('contact'))
#             else:
#                 flash('Деякі поля не пройшли валідацію, будь ласка, введіть дані ще раз', 'danger')
#     return render_template('contact.html', title='Контактна форма', form=form, session_name=session_name)
