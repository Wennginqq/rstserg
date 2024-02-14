from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, send_from_directory
from flask import current_app
import os
from database import mysql
from werkzeug.utils import secure_filename
from openpyxl import Workbook
import config
import MySQLdb.cursors

menuBlueprint = Blueprint("menu", __name__, template_folder="templates")

@menuBlueprint.route('/menu', methods =['GET', 'POST'])
def showMenu():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select * from menu')
    menuItems = cursor.fetchall()
    cursor.close()
    return render_template('menu.html', menuItems=menuItems)

@menuBlueprint.route('/menu/about', methods =['GET', 'POST'])
def aboutFood():
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from menu where foodId = %s', (request.args.get('foodId'),))
        menuItems = cursor.fetchone()

        cursor.execute('select * from food_category')
        category = cursor.fetchall()
        cursor.close()
        return render_template('aboutFood.html', menuItems=menuItems, category=category)
    else:
        r = request.files.get("img") 
        print(r.filename)
        if r.filename == '':
            filename = 'bim.png'
        else:
            filename = r.filename
            with open("static/images/"+r.filename, "wb") as fp: 
                for itm in r: fp.write(itm)
            fp.close()

        id = request.form.get('id')
        name = request.form.get('name')
        price = request.form.get('price')
        caption = request.form.get('caption')
        category = request.form.get('category')
        print(id)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE menu SET name = %s, price = %s, caption = %s, path_to_img = %s, food_category_categoryId = %s  where foodId = %s', 
                    (name, price, caption, filename, category, id))
        mysql.connection.commit()
        cursor.close()

        return redirect('/menu')

@menuBlueprint.route('/menu/add', methods =['GET', 'POST'])
def addMenuItem():
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from food_category')
        category = cursor.fetchall()
        cursor.close()
        return render_template('addmenuitem.html', category=category)
    else:
        r = request.files.get("img") 
        if r.filename == '':
            filename = 'bim.png'
        else:
            filename = r.filename
            with open("static/images/"+r.filename, "wb") as fp: 
                for itm in r: fp.write(itm)
            fp.close()

        name = request.form.get('name')
        price = request.form.get('price')
        caption = request.form.get('caption')
        category = request.form.get('category')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('insert into menu set name = %s, price = %s, caption = %s, path_to_img = %s, food_category_categoryId = %s', 
                    (name, price, caption, filename, category))
        mysql.connection.commit()
        cursor.close()
        return redirect('/menu')
    
@menuBlueprint.route('/menu/delete', methods =['GET', 'POST'])
def deleteFromMenu():
    foodID = request.args.get('foodId')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('delete from menu where foodId = %s', (foodID))
    mysql.connection.commit()
    cursor.close()
    return redirect('/menu')

@menuBlueprint.route('/menu/tostop', methods =['GET', 'POST'])
def toStoplist():
    foodID = request.args.get('foodId')
    stoplistStatus = 'недоступно'
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('update menu set stoplist = %s where foodId = %s', (stoplistStatus ,foodID))
    mysql.connection.commit()
    cursor.close()
    return redirect('/menu')

@menuBlueprint.route('/menu/fromstop', methods =['GET', 'POST'])
def fromStoplist():
    foodID = request.args.get('foodId')
    stoplistStatus = 'доступно'
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('update menu set stoplist = %s where foodId = %s', (stoplistStatus ,foodID))
    mysql.connection.commit()
    cursor.close()
    return redirect('/menu')

@menuBlueprint.route('/menu/stoplistreport', methods =['GET', 'POST'])
def createStoplistReport():
        if request.method == 'GET':
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('select foodId as "ID", name as "Наименование", stoplist as "Доступность" from menu where stoplist = "Недоступно"')
            items = cursor.fetchall()
            cursor.close()
            wb = Workbook()
            ws = wb.active
            fieldnames = ['ID', 'Наименование', 'Доступность']
            ws.append(fieldnames)
            for item in items:
                values = (item[k] for k in fieldnames)
                ws.append(values)
            wb.save('static/reports/стоплист.xlsx')
            return send_from_directory('static/reports/', 'стоплист.xlsx')