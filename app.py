from flask import Flask, redirect, url_for,Blueprint
from flask import render_template, flash
from datetime import timedelta
from flask import request, session


import mysql.connector
import requests

from pages.assignment_4.assignment_4 import assignment_4, interact_db

app = Flask(__name__)

app.register_blueprint(assignment_4)

app.secret_key = '123'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)


@app.route('/Contact')
def Contact_page():  # put application'ֶs code here
    return render_template('Contact.html')



@app.route('/')
def Home_page():  # put application's code here
    return render_template('NewHomePage.html')



@app.route('/Base')
def Base_page():
    return render_template('base.html')


if __name__ == '__main__':
    app.run(debug=True)


@app.route('/assignment3_1')
def ass3_1_page():  # put application's code here
    user_info = {'first_name': 'Lihi', 'last_name': 'Maor','BirthDay': '01.08.1996' ,'Gender': 'Female' }
    hobbies = ('Shopping', 'Sea','TV', 'Sport')
    Fav_music = {'singer': ["Travis Scott", "Natan Goshen", "Mergi", "Ravid Plotnik"],
                    'song': ["Wake up", "", "Koma28", "Kapara Sheli"]
                   }

    return render_template('assignment3_1.html',
                           user=user_info,
                           hobbies=hobbies,
                           Fav_music=Fav_music
                          )


users = {
    1:  {'user_Name': 'Din', 'user_Email': 'dino@gmail.com'},
    2: {'user_Name': 'Lihi', 'user_Email': 'lihimao@post.bgu.ac.il'},
    3: {'user_Name': 'Rona', 'user_Email':  'Rona@gmail.com'},
    4: {'user_Name': 'Tal', 'user_Email':  'Tal55@gmail.com'}
         }


@app.route('/assignment3_2', methods=['GET', 'POST'])
def LogIn_page():
    if request.method == 'POST':
        user_Name = request.form['user_Name']
        user_Email = request.form['user_Email']
        for user in users:
            if user_Name == users[user]["user_Name"]:
                return render_template('assignment3_2.html', massageHave="User Name already exist in the system")
            if user_Email == users[user]["user_Email"]:
                return render_template('assignment3_2.html', massageHave="User Email already exist in the system")

        users.update({list(users.keys())[-1]+1: {"user_Name": user_Name, "user_Email": user_Email}})

        session['user_Name'] = user_Name

        session['user_Email'] = user_Email

        session['logedin'] = True

    elif 'user_Name' in request.args:
        user_Name = request.args['user_Name']
        for user in users:
            if users[user]["user_Name"] == user_Name:
                user_Email = users[user]["user_Email"]
                return render_template('assignment3_2.html', user_Name=user_Name, user_Email=user_Email)
            elif user_Name == "":
                return render_template('assignment3_2.html', users=users)

        for user in users:
            if users[user]["user_Name"] != user_Name:
                return render_template('assignment3_2.html', massageNotHave="User not found in the system")

    return render_template('assignment3_2.html')


@app.route('/logOut')
def logOut():
    session['logedin'] = False
    session.clear()
    return redirect(url_for('LogIn_page'))


