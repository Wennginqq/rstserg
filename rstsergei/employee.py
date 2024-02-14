from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from database import mysql
import MySQLdb.cursors

employeeBlueprint = Blueprint("employee", __name__, template_folder="templates")

@employeeBlueprint.route('/employee', methods =['GET', 'POST'])
def showEmployee():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select * from employee')
    employees = cursor.fetchall()
    cursor.close()
    return render_template('employee.html', employees=employees)

@employeeBlueprint.route('/employee/add', methods = ['GET', 'POST'])
def addEmployee():
    if request.method == 'GET':
        return render_template('addemployee.html')
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        position = request.form.get('position')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('insert into employee set firstname = %s, lastname = %s, position = %s', 
                    (firstname, lastname, position))
        mysql.connection.commit()
        cursor.close()
        return redirect('/employee')

@employeeBlueprint.route('/employee/about', methods =['GET', 'POST'])
def aboutEmployee():
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from employee where employeeId=%s', (request.args.get('employeeId'),))
        employees = cursor.fetchone()
        cursor.close()
        return render_template('aboutemployee.html', employees=employees)
    if request.method == 'POST':
        id = request.form.get('id')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        position = request.form.get('position')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('update employee set firstname = %s, lastname = %s, position = %s where employeeId=%s', 
                    (firstname, lastname, position, id))
        mysql.connection.commit()
        cursor.close()
        return redirect('/employee')

@employeeBlueprint.route('/employee/delete', methods =['GET', 'POST'])
def deleteEmployee():
    employeeId = request.args.get('employeeId')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('delete from employee where employeeId = %s', ([employeeId]))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('employee.showEmployee'))