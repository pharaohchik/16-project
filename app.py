from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="templates")

app.secret_key = '1F7VkTpXpSB09P6UskV9Kq$23QWD9FG440'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///miniBoBR.db'
db = SQLAlchemy(app)


class Visitors(db.Model):
    __tableName__ = 'Visitors'
    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    name_p = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(30), nullable=True)
    arrival = db.Column(db.Integer, nullable=False)
    leaving = db.Column(db.Integer, nullable=False)

    def __init__(self, surname, name, name_p, phone, email, arrival, leaving):
        self.surname = surname
        self.name = name
        self.name_p = name_p
        self.phone = phone
        self.email = email
        self.arrival = arrival
        self.leaving = leaving


@app.route('/')
def registration():
    return render_template('registrationn.html')


class Hotel_room(db.Model):
    __tableName__ = 'Hotel_room'
    id = db.Column(db.Integer, primary_key=True)
    room_type = db.Column(db.String(8), nullable=False)
    visitors_amount = db.Column(db.Integer, nullable=False)
    square = db.Column(db.Integer, nullable=False)
    bathtub = db.Column(db.Integer, nullable=False)
    balcony = db.Column(db.Integer, nullable=False)
    free_rooms = db.Column(db.Integer, nullable=False)

    def __init__(self, room_type, visitors_amount, square, bathtub, balcony, free_rooms):
        self.room_type = room_type
        self.visitors_amount = visitors_amount
        self.square = square
        self.bathtub = bathtub
        self.balcony = balcony
        self.free_rooms = free_rooms


@app.route('/reg', methods=['POST'])
def reg():
    name = request.form['name']
    surname = request.form['surname']
    name_p = request.form['name_p']
    phone = request.form['phone']
    email = request.form['email']
    arrival = request.form['arrival']
    leaving = request.form['leaving']
    user = Visitors(surname, name, name_p, phone, email, arrival, leaving)
    db.session.add(user)
    db.session.flush()
    db.session.commit()
    return redirect('/book')


@app.route('/book')
def book():
    return render_template('book.html')


@app.route('/verification')
def verification():
    return render_template('verification.html')


@app.route('/check', methods=['POST'])
def check():
    surname = request.form.get('surname')
    phone = request.form.get('phone')
    for user in Visitors.query.all():
        if (user.surname == surname) and (user.phone == phone):
            return redirect('/lox')
    return redirect('/congratulation')


@app.route('/lox')
def lox():
    return render_template("lox.html")


@app.route('/congratulation')
def congratulation():
    return render_template('congratulation.html')


@app.route('/hotel_room_list')
def room_list():
    a =[]
    for room in Hotel_room.query.all():
        print(room.room_type, room.visitors_amount, room.square, room.bathtub, room.balcony, room.free_rooms)
        a.append([room.room_type, room.visitors_amount, room.square, room.bathtub, room.balcony, room.free_rooms])
    return str(a)


if __name__ == '__main__':
    app.run(debug=True)