from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, send_from_directory
from flask import current_app
import os
from database import mysql
from werkzeug.utils import secure_filename
import config
import MySQLdb.cursors
from openpyxl import Workbook

inventoryBlueprint = Blueprint("inventory", __name__, template_folder="templates")

@inventoryBlueprint.route('/inventory', methods =['GET', 'POST'])
def showinventory():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select * from inventory')
    Items = cursor.fetchall()
    cursor.close()
    return render_template('inventory.html', Items=Items)

@inventoryBlueprint.route('/inventory/add', methods =['GET', 'POST'])
def addToInventory():
    if request.method == 'GET':
        return render_template('addtoinventory.html')
    if request.method == 'POST':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        name = request.form.get('name')
        invcode = request.form.get('code')
        amount = request.form.get('amount')
        invunit = request.form.get('unit')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('insert into inventory set name = %s, code = %s, amount = %s, unit = %s', 
                    (name, invcode, amount, invunit))
        mysql.connection.commit()
        cursor.close()
        return redirect('/inventory')

@inventoryBlueprint.route('/inventory/delete', methods =['GET', 'POST'])
def deleteFromInventory():
    invid = request.args.get('id')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('delete from inventory where inventoryId = %s', (invid,))
    mysql.connection.commit()
    cursor.close()
    return redirect('/inventory')

@inventoryBlueprint.route('/inventory/change', methods =['GET', 'POST'])
def changeInventory():
    invid = request.args.get('id')
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from inventory where inventoryId = %s', (invid,))
        items = cursor.fetchall()
        cursor.close()
        return render_template('changeinventorypos.html', items=items)
    if request.method == 'POST':
        name = request.form.get('name')
        invcode = request.form.get('code')
        amount = request.form.get('amount')
        invunit = request.form.get('unit')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('update inventory set name = %s, code = %s, amount = %s, unit = %s where inventoryId = %s', 
                    (name, invcode, amount, invunit, invid))
        mysql.connection.commit()
        cursor.close()
        return redirect('/inventory')

@inventoryBlueprint.route('/inventory/report', methods =['GET', 'POST'])
def createReportInventory():
        if request.method == 'GET':
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('select inventoryId as "ID", name as "Наименование", code as "Код", amount as "Кол-во", unit as "Ед.измерения" from inventory')
            items = cursor.fetchall()
            cursor.close()
            wb = Workbook()
            ws = wb.active
            fieldnames = ['ID', 'Наименование', 'Код', 'Кол-во', 'Ед.измерения']
            ws.append(fieldnames)
            for item in items:
                values = (item[k] for k in fieldnames)
                ws.append(values)
            wb.save('static/reports/инвентаризация.xlsx')
            return send_from_directory('static/reports/', 'инвентаризация.xlsx')