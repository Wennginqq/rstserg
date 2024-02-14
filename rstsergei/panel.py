from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from database import mysql
import MySQLdb.cursors

panelBlueprint = Blueprint("panel", __name__, template_folder="templates")

@panelBlueprint.route('/panel', methods =['GET', 'POST'])
def showPanel():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select recordId, caption, day_of_shift, schedule_has_employee.employee_employeeId, employee.lastname, employee.position from schedule join schedule_has_employee on recordId=schedule_has_employee.schedule_recordId join employee on schedule_has_employee.employee_employeeId=employee.employeeId where day_of_shift = CURDATE() ORDER BY day_of_shift ASC')
    panelSchedule = cursor.fetchall()
    cursor.execute('select * from orders join employee on orders.employeeId=employee.employeeId where order_date = CURDATE()')
    panelOrders = cursor.fetchall()
    cursor.close()
    return render_template('panel.html', panelSchedule=panelSchedule, panelOrders=panelOrders)