# -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for, request, redirect, flash, session
from app import app
from app.forms import ContactForm, RegistrationForm, LoginForm
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
    form = LoginForm()
    if form.validate_on_submit():#якщо реєстрація пройшла успішно
        # flash(f'Account created for {form.username.data}!', 'success')
        #переходимо на домашню сторінку
        return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():#якщо реєстрація пройшла успішно
        # flash(f'Account created for {form.username.data}!', 'success')
        #переходимо на домашню сторінку
        return redirect(url_for('home'))
    return render_template('register.html', form=form)



@app.route("/contact", methods=['POST', 'GET'])
def contact():
    form = ContactForm()
    session_name = session.get('name')
    session_email = session.get('email')
    print(f'contact-form is using by {session_name}')
    # якщо користувач передає дані
    if request.method == 'POST':
        # і форма до того не була заповнена у поточній сесії (адже ім'я збережен в сесії відсутнє)
        if session_name is None:
            if form.validate_on_submit():
                # дістаємо дані із форм
                name = form.name.data
                email = form.email.data
                message = form.message.data
                # і записуємо ім'я та мейл у змінні сесії
                session['name'] = name
                session['email'] = email
                # зібрані дані із форми записуємо у json файл
                with open('data.json', 'a') as f:
                    json.dump({'name': name, 'email': email, 'message': message}, f,
                              indent=4, ensure_ascii=False)
                flash(f'Повідомлення від {name} було успішно надіслано', 'success')
                # виконуємо перенаправлення на сторінку 'контакт' із методом get
                return redirect(url_for('contact'))
            else:
                flash('Деякі поля не пройшли валідацію, будь ласка, введіть дані ще раз', 'danger')
        else:  # якщо форма до того ВЖЕ БУЛА заповнена у поточній сесії - то:
            # значення полів ім'я та емейлу для проходження валідації беремо із змінних сесії
            form.name.data = session_name
            form.email.data = session_email
            if form.validate_on_submit():
                # і нові дані зчитуємо лише з полля message
                message = form.message.data
                # зібрані дані із форми записуємо у json файл
                with open('data.json', 'a') as f:
                    json.dump({'name': session_name, 'email': session_email, 'message': message}, f,
                              indent=4, ensure_ascii=False)
                flash(f'Повідомлення від {form.name.data} було успішно надіслано', 'success')
                # виконуємо перенаправлення на сторінку 'контакт' із методом get
                return redirect(url_for('contact'))
            else:
                flash('Деякі поля не пройшли валідацію, будь ласка, введіть дані ще раз', 'danger')
    return render_template('contact.html', title='Контактна форма', form=form, session_name=session_name)
