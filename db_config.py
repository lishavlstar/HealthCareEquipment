from app import app
from flaskext.mysql import MySQL
from flask_mail import Mail, Message
import smtplib

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'toor'
app.config['MYSQL_DATABASE_DB'] = 'clientdb9'
app.config['MYSQL_DATABASE_HOST'] = '34.93.217.226'
mysql.init_app(app)

mail=Mail()
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'pumexdev@gmail.com'
app.config['MAIL_PASSWORD'] = 'team@pumeX'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
mail.init_app(app)





















































































































