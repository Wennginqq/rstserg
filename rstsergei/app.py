from flask import Flask, render_template, request, redirect, url_for, session, Blueprint

import config
from login import loginBlueprint
from employee import employeeBlueprint
from panel import panelBlueprint
from menu import menuBlueprint
from orders import ordersBlueprint
from schedule import scheduleBlueprint
from inventory import inventoryBlueprint
import database

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.config['MYSQL_HOST'] = database.MYSQL_HOST
app.config['MYSQL_USER'] = database.MYSQL_USER
app.config['MYSQL_PASSWORD'] = database.MYSQL_PASSWORD
app.config['MYSQL_DB'] = database.MYSQL_DB
app.config['MYSQL_CURSORCLASS'] = database.MYSQL_CURSORCLASS

app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
database.mysql.init_app(app)

app.register_blueprint(loginBlueprint)
app.register_blueprint(employeeBlueprint)
app.register_blueprint(panelBlueprint)
app.register_blueprint(menuBlueprint)
app.register_blueprint(ordersBlueprint)
app.register_blueprint(scheduleBlueprint)
app.register_blueprint(inventoryBlueprint)

@app.route('/', methods=['GET', 'POST'])
def default():
    return redirect('/login')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)