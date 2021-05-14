# -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for, request, redirect, flash, session
from app import app, db, bcrypt
from app.forms import ContactForm, RegistrationForm, LoginForm, BookForm, UserBookForm
from app.models import User, User_books, Books, Publishers, autor_has_books, Authors, Categories
from flask_login import login_user, current_user, logout_user, login_required
# import datetime
import json



@app.route("/")
@app.route("/home")
def home():
    books = []#якщо користувач не авторизований, щоб не вибивало помилку
    if current_user.is_authenticated:
        books = db.session.query(User, User_books, Books, Publishers, autor_has_books, Authors#об'єднюємо таблиці
            ).filter(
                User_books.user_id==current_user.id
            ).filter(
                User.id==current_user.id
            ).filter(
                Books.book_id==User_books.book_id
            ).filter(
                Publishers.publishers_id==Books.publisher_id
            ).filter(
                Books.book_id==autor_has_books.columns.book_id
            ).filter(
                Authors.author_id==autor_has_books.columns.book_id
            ).all()
    return render_template('home.html', title='LiBro', books=books)


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

@app.route("/book/<int:user_book_id>")
@login_required
def book(user_book_id):
    book = db.session.query(User, User_books, Books, Publishers, autor_has_books, Authors#об'єднюємо таблиці
            ).filter(
                User_books.user_book_id==user_book_id
            ).filter(
                User_books.user_id==current_user.id
            ).filter(
                User.id==current_user.id
            ).filter(
                Books.book_id==User_books.book_id
            ).filter(
                Publishers.publishers_id==Books.publisher_id
            ).filter(
                Books.book_id==autor_has_books.columns.book_id
            ).filter(
                Authors.author_id==autor_has_books.columns.book_id
            ).first()
    return render_template('book.html', book=book)

@app.route("/book/add", methods=['GET', 'POST'])
@login_required
def add_book():
    form = UserBookForm()
    if form.validate_on_submit():
        author_name = db.session.query(Authors).filter(Authors.first_name==form.name_author.data).all()#отримуємо всіх авторів з таким ім'ям
        author_surname = db.session.query(Authors).filter(Authors.second_name==form.surname_author.data).all()#отримуємо всіх авторів з таким прізвищем
        author = list(set(author_name).intersection(author_surname))#отримуємо автора з таким ім'ям і прізвищем

        if author:
            author_id = author[0].author_id
        else:
            # author_id = db.session.query(Authors).order_by(Authors.author_id.desc()).first().author_id + 1
            # author = Authors(author_id=author_id, first_name=form.name_author.data, second_name=form.surname_author.data)
            # db.session.add(author)
            return redirect(url_for('new_book'))


        book = db.session.query(Books, autor_has_books, Authors
            ).filter(
                Books.book_name==form.name_book.data
            ).filter(
                Books.book_id==autor_has_books.columns.book_id
            ).filter(
                author_id==autor_has_books.columns.book_id
            ).first()

        if book:#якщо така книга існує
            book_id = book.Books.book_id
        else:
            return render_template('new_book.html', title='New Book', legend='New Book')

        user_book_id = db.session.query(User_books).order_by(User_books.user_book_id.desc()).first().user_book_id + 1
        user_book = User_books(user_book_id=user_book_id, price=form.price.data,
            data_added=form.date_added.data, user_id=current_user.id, book_id=book_id)

        db.session.add(user_book)
        # db.session.add(user_book)

        db.session.commit()
        return redirect(url_for('home'))

    return render_template('add_book.html', title='Add Book',
                           form=form, legend='Add Book')


@app.route("/book/new", methods=['GET', 'POST'])
@login_required
def new_book():
    form = BookForm()
    if form.validate_on_submit():

        publisher = db.session.query(Publishers).filter(Publishers.publishes_name==form.publisher.data).first()
        if publisher:#якщо таке видавництво є в базі даних
            publisher_id = publisher.publishers_id
        else:#якщо його немає
            publisher_id = db.session.query(Publishers).order_by(Publishers.publishers_id.desc()).first().publishers_id + 1
            publisher = Publishers(publishers_id=publisher_id, publishes_name=form.publisher.data)
            db.session.add(publisher)
            # db.session.commit()


        category = db.session.query(Categories).filter(Categories.category_name==form.category.data).first()
        if category:
            category_id = category.category_id
        else:
            category_id = db.session.query(Categories).order_by(Categories.category_id.desc()).first().category_id + 1
            category = Categories(category_id=category_id, category_name=form.category.data)
            db.session.add(category)
            # db.session.commit()
        

        author_name = db.session.query(Authors).filter(Authors.first_name==form.name_author.data).all()#отримуємо всіх авторів з таким ім'ям
        author_surname = db.session.query(Authors).filter(Authors.second_name==form.surname_author.data).all()#отримуємо всіх авторів з таким прізвищем
        author = list(set(author_name).intersection(author_surname))#отримуємо автора з таким ім'ям і прізвищем

        if author:
            author_id = author[0].author_id
        else:
            author_id = db.session.query(Authors).order_by(Authors.author_id.desc()).first().author_id + 1
            author = Authors(author_id=author_id, first_name=form.name_author.data, second_name=form.surname_author.data)
            db.session.add(author)
            # db.session.commit()

        # date_add = form.data_added.data.split('.')



        book_id = db.session.query(Books).order_by(Books.book_id.desc()).first().book_id + 1
        book = Books(book_id=book_id, book_name=form.name_book.data, description=form.description.data, page=form.page.data,
         year=form.year.data, publisher_id=publisher_id, categories_id=category_id)





        db.session.add(book)
        # db.session.add(user_book)

        db.session.commit()

        ins = autor_has_books.insert().values(book_id=book_id, author_id=author_id)
        db.engine.execute(ins)
        # flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('new_book.html', title='New Book',
                           form=form, legend='New Book')


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
