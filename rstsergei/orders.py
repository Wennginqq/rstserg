from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from database import mysql
import MySQLdb.cursors

ordersBlueprint = Blueprint("orders", __name__, template_folder="templates")

@ordersBlueprint.route('/orders', methods =['GET', 'POST'])
def showOrders():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select * from orders join employee on orders.employeeId=employee.employeeId')
    orders = cursor.fetchall()
    cursor.close()
    return render_template('orders.html', orders=orders)

@ordersBlueprint.route('/orders/about')
def aboutOrder():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select * from orders join employee on orders.employeeId=employee.employeeId where orderId = %s', (request.args.get('orderId'),))
    order = cursor.fetchone()
    cursor.execute('select orderId, menu.name, orders_has_menu.ordered_amount from orders join orders_has_menu on orders.orderId=orders_has_menu.orders_orderId join menu on orders_has_menu.menu_foodId=menu.foodId where orderId=%s',(request.args.get('orderId'),))
    foodInOrder = cursor.fetchall()
    return render_template('aboutorder.html', order=order, foodInOrder=foodInOrder)