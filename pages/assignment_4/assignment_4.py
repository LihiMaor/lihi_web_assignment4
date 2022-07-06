from flask import render_template, Blueprint, request
from flask import redirect,jsonify, url_for,session
import requests
import app
import mysql.connector
from flask import flash
from datetime import timedelta




assignment_4 = Blueprint('assignment_4', __name__,
                         static_folder='static',
                         static_url_path='/assignment_4',
                         template_folder='templates')


@assignment_4.route('/assignment4')
def assignment4_Page():
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    return render_template('assignment4.html', users=users_list)



# ------------- DATABASE CONNECTION --------------- #

def interact_db(query, query_type: str):
    return_value = False
    connection = mysql.connector.connect(host='localhost',
                                         user='root',
                                         passwd='root',
                                         database='webcourse')
    cursor = connection.cursor(named_tuple=True)
    cursor.execute(query)


    if query_type == 'commit':
        # Use for INSERT, UPDATE, DELETE statements.
        # Returns: The number of rows affected by the query (a non-negative int).
        connection.commit()
        return_value = True

    if query_type == 'fetch':
        # Use for SELECT statement.
        # Returns: False if the query failed, or the result of the query if it succeeded.
        query_result = cursor.fetchall()
        return_value = query_result

    connection.close()
    cursor.close()
    return return_value


# -------------------- IfUserInList--------------------- #

def IfUserInList(idnum):
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    for user in users_list:
        if idnum == user.id:
            return True
    return False





# -------------------- INSERT --------------------- #
@assignment_4.route('/insert_user', methods=['POST'])
def insert_user_func():
    Id = request.form['id']
    name = request.form['user_Name']
    email = request.form['user_Email']
    if IfUserInList(Id):
        flash("There is already a registered user with the ID you entered",'success')
        return redirect('/assignment4')
    query = "INSERT INTO users(id ,user_Name, user_Email) VALUES ('%s','%s', '%s')" % (Id ,name, email)
    interact_db(query=query, query_type='commit')
    flash("the user added successfully", 'success')
    return redirect('/assignment4')


# -------------------- DELETE --------------------- #

@assignment_4.route('/delete_user', methods=['POST'])
def delete_user_func():
    user_id = request.form['id']
    if not IfUserInList(user_id):
        flash("There is no user with the ID you entered",'error')
        return redirect('/assignment4')
    query = "DELETE FROM users WHERE id='%s';" % user_id
    interact_db(query, query_type='commit')
    flash("the user deleted successfully",'success')
    return redirect('/assignment4')





# -------------------- UPDATE --------------------- #

@assignment_4.route('/update_user', methods=['POST'])
def update_user_func():
    id = request.form['id']
    if not IfUserInList(id):
        flash("There is no user with the ID you entered", 'error')
        return redirect('/assignment4')

    if request.form['user_Name'] != '':
        name = request.form['user_Name']
        query = "UPDATE users SET user_Name='%s'  WHERE id='%s' ;" % (name,  id)
        interact_db(query, query_type='commit')

    if request.form['user_Email'] != '':
       email = request.form['user_Email']
       query = "UPDATE users SET  user_Email='%s'  WHERE id='%s' ;" % ( email , id)
       interact_db(query, query_type='commit')

    flash("Your details have been successfully updated!",'success')
    return redirect('/assignment4')



# -------------------- PartB --------------------- #


# -------- B3 --------- #
@assignment_4.route('/assignment4/users')
def json_users_table_func():
    query = 'select * from users'
    users_list = app.interact_db(query, query_type='fetch')
    return jsonify(users_list)

# -------- B4 --------- #

@assignment_4.route('/assignment4/outer_source')
def outer_source_func():
    return render_template('outer_source.html')



@assignment_4.route('/fetch_Backend')
def fetch_be_func():
    Id = request.args['back_id']
    userRes= requests.get(f'https://reqres.in/api/users/{ Id }')
    Details=userRes.json()
    for Details_Key, Details_Values in Details.items():
        for key in Details_Values:
            if key == 'avatar':
                user_picture = Details_Values['avatar']
            if key == 'first_name':
                user_FirstName=Details_Values['first_name']
            if key == 'last_name':
                user_LastName = Details_Values['last_name']
            if key == 'email':
             user_Email = Details_Values['email']

    return render_template('outer_source.html',user_FirstName=user_FirstName,user_LastName=user_LastName,
                                            user_Email = user_Email ,user_picture=user_picture )




@assignment_4.route('/assignment4/restapi_users', defaults={'id': 100100100})
@assignment_4.route('/assignment4/restapi_users/<int:id>')
def restapi_id( id ):
    if id == 100100100:
      query = "select * FROM users WHERE id='100100100';"
    else:
      query = "select * from users where id='%s';" % (id)

    users_list = interact_db(query, query_type='fetch')
    if (users_list == []):
        return jsonify("There is NO user with the ID you entered")
    return jsonify(users_list)


