from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from database import mysql
from collections import Counter
import MySQLdb.cursors

scheduleBlueprint = Blueprint("schedule", __name__, template_folder="templates")

@scheduleBlueprint.route('/schedule', methods =['GET', 'POST'])
def showSchedule():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select recordId, caption, day_of_shift, schedule_has_employee.employee_employeeId, employee.lastname, employee.position from schedule join schedule_has_employee on recordId=schedule_has_employee.schedule_recordId join employee on schedule_has_employee.employee_employeeId=employee.employeeId ORDER BY day_of_shift DESC')
    schedule = cursor.fetchall()
    cursor.close()
    
    return render_template('schedule.html', schedule=schedule)

@scheduleBlueprint.route('/schedule/add', methods =['GET', 'POST'])
def addEntry():
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from employee')
        employee = cursor.fetchall()
        cursor.close()
        return render_template('addscheduleentry.html', employee=employee)
    if request.method == 'POST':
        mes = ''
        shiftDay = request.form.get('date')
        formlist = request.form.to_dict()
        formlist.popitem()
        values = formlist.values()
        counter = Counter(values)
        for val in counter:
            if counter[val] > 1:
                mes = 'Сотрудники не должны повторяться'
                break
        if mes != '':
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('select * from employee')
            employee = cursor.fetchall()
            cursor.close()
            return render_template('addscheduleentry.html', employee=employee, mes=mes)
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('insert into schedule set day_of_shift=%s', ([shiftDay]))
            mysql.connection.commit()
            
            cursor.execute('select recordId from schedule order by recordId desc LIMIT 1')
            lastOrderId = cursor.fetchone()
            for val in formlist:
                cursor.execute('insert into schedule_has_employee set schedule_recordId = %s, employee_employeeId = %s', (lastOrderId['recordId'], int(formlist[val])))
                mysql.connection.commit()
            cursor.close()

        return redirect('/schedule')
