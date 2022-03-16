import rest
from app import app
import pymysql
import dao
import platform
from db_config import mysql
from flask import render_template,jsonify, Response
import getpass
import smtplib
from flask import jsonify, request, session, redirect, url_for, json
from passlib.hash import sha256_crypt
from flask_mail import Mail, Message
from db_config import mail
from itsdangerous import URLSafeSerializer, SignatureExpired
import pdfcrowd
s = URLSafeSerializer('secretthistime!')
	
@app.route('/')
def login_page():
	return render_template('login.html')
@app.route('/logout')
def logout_page():
	return render_template('login.html')
@app.route('/logout1')
def logout_pages():
	return render_template('login.html')

@app.route('/back')
def back_page():
	return render_template('index.html')
@app.route('/registers')
def home_reg():
	return render_template('signup.html')
@app.route('/next')
def next_page():
	return render_template('signup1.html')

@app.route('/update')
def home_pages():
	return render_template('emailsend.html')

@app.route('/total')
def total():

	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT hname, vnum, vuse, vavail FROM hospital")
		data = cursor.fetchall()

		return render_template('total.html', data=data)
		
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()


@app.route('/pdf')
def pdf():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT hname, vnum, vuse, vavail FROM hospital")
		data = cursor.fetchall()
		client = pdfcrowd.HtmlToPdfClient('demo', 'ce544b6ea52a5621fb9d55f8b542d14d')
		rendered_template = render_template('Ventilator_details.html', data=data)
		rendered_template = rendered_template.encode('utf-8') 
		
		pdf = client.convertString(rendered_template)
		response = Response(pdf, mimetype='application/pdf')
		response.headers['Cache-Control'] = 'max-age=0'
		response.headers['Accept-Ranges'] = 'none'
 		response.headers['Content-Disposition'] = 'attachment; filename="Ventilator_details.pdf"'
 		return response
	except pdfcrowd.Error as why:
		return Response(why.getMessage(),
  	status=why.getCode(),
  	mimetype='text/plain')
	finally:
		cursor.close() 
		conn.close()

 

def patch(module):
    def decorate(func):
        setattr(module, func.func_name, func)
        return func
    return decorate

@patch(platform)
def platform():
    return 'AppEngine'

@app.route('/edit')
def editpage():
	conn = None;
	cursor = None;
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT hname FROM hospital")
		names = cursor.fetchall()
	
		name = session['username']
	
		for row in names:
			if row['hname'] in name:
				cursor.execute("SELECT vnum, vuse, vavail FROM hospital WHERE hname=%s", name)
				data = cursor.fetchall()
				return render_template('homepage.html', names=data)
		
	
	except Exception as e:
		print(e)
	finally:
		if cursor and conn:
			cursor.close()
			conn.close()

	
	return render_template('homepage.html')




@app.route('/index')
def google_pie_chart():
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		

		cursor.execute("SELECT  COUNT(hname) AS name, SUM(vnum) AS  'num' , SUM(vuse) AS 'use', SUM(vavail) AS 'avail' FROM hospital")
		datas = cursor.fetchall()

		cursor.execute("SELECT hname FROM hospital")
		names = cursor.fetchall()
		
		
		for row in datas:
			data = {'Ventilator' : 'Usage', 'Ventilators in Use' : row['use'], 'Available Ventilators' : row['avail']} 

	
		return render_template('index.html', data=data, table=datas, names=names)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()	
		


@app.route('/searchbyhospital/<hname>')
def usersse(hname):
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT hname, vnum, vuse, vavail, lat, lng, haddress FROM hospital WHERE hname= %s",hname)
		datase = cursor.fetchall()
		
	
		return jsonify(datase)
		
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()



@app.route('/searchLikeHospital/<hname>')
def searchUsers(hname):
	hname='%'+hname+'%'
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT hname FROM `hospital`WHERE `hname` LIKE %s",hname)
		
		pattern = cursor.fetchall()		
		return jsonify(pattern)
		
		
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()



@app.route('/edit', methods=['PUT'])
def update_hos():
	conn = None;
	cursor = None;
	try:
		_json = request.json
		_vnum = _json['vnum']
		_vuse = _json['vuse']
		_vavail = _json['vavail']
		_hname = _json['hname']
	
		# validate the received values
		if _vnum and _vuse and _vavail and request.method == 'PUT':
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT hname FROM hospital")
			names = cursor.fetchall()
	
			name = session['username']	
			
			for row in names:
				if row['hname'] in name:
				
					sql = "UPDATE hospital SET vnum=%s, vuse=%s, vavail=%s WHERE hname=%s"
					data = (_vnum, _vuse, _vavail, _hname,)
					val = cursor.execute(sql, data)
					
					
					conn.commit()
					
					return jsonify(names)
				
		else:
			resp = jsonify({'message' : 'Bad Request - invalid credendtials'})
			resp.status_code = 400
			return resp
	except Exception as e:
		print(e)
	finally:
		if cursor and conn:
			cursor.close()
			conn.close()

		
@app.route('/map')
def usermap():
  conn = None
  cursor = None
  try:
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT lat, lng,vnum, haddress FROM hospital")
    addresses = cursor.fetchall()
    all_coods = []
    for add in addresses:
      address_details = {
      "lat": add['lat'], 
      "lng": add['lng'],
      "title": add['vnum'],
			"title1": add['haddress'],
			}
      all_coods.append(address_details)
    
    return jsonify({'cordinates': all_coods})
  except Exception as e:
		print(e)
  finally:
		cursor.close() 
		conn.close()




@app.route('/email', methods=['PUT'])
def edit_user():
	conn = None;
	cursor = None;
	try:
		_json = request.json
		_email = _json['email']
	
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT email FROM user")
		names = cursor.fetchall()
			
			
		for row in names:
			if _email == row['email'] and  request.method == 'PUT' :
				if _email != None:
					cursor.execute("SELECT name FROM user WHERE email=%s", _email)
					datas = cursor.fetchone()
					data = datas['name']
			
					token = s.dumps(_email, salt='email-confirm')
					msg = Message('Please Reset your Password', sender = 'lisha@pumexinfotech.com', recipients = [_email])
					link = url_for('confirm_email', token=token, _external=True)

					msg.html = render_template('newsletters.html', token=token, link=link, data=data )
					mail.send(msg)
					return jsonify(datas)
				
			else:
				resp = jsonify({'message' : 'No email'})
				resp.status_code = 400
				return resp
	except Exception as e:
		print(e)
	finally:
		if cursor and conn:
			cursor.close()
			conn.close()		

@app.route('/confirm_email/<token>')
def confirm_email(token):
	try:
		email = s.loads(token, salt='email-confirm', )
	except SignatureExpired:
		return '<h1>The token is expired!</h1>'
	
	return render_template('new.html', email=email)


@app.route('/passwd', methods=['PUT'])
def update_p():
	conn = None;
	cursor = None;
	try:
		_json = request.json
		_email = _json['username']
		_pwd = _json['password']
	
		# validate the received values
		if _email and _pwd and request.method == 'PUT':
			if _email != None:
				_hashed_password = sha256_crypt.encrypt(_pwd)
				conn = mysql.connect()
				cursor = conn.cursor()
				

				sql = "UPDATE user SET pwd=%s WHERE email=%s"
				data = (_hashed_password, _email,)
				cursor.execute(sql, data)
				conn.commit()
				
			return	jsonify({"redirect": "/"})
		else:
			resp = jsonify({'message' : 'Bad Request - invalid credendtials'})
			resp.status_code = 400
			return resp
	except Exception as e:
		print(e)
	finally:
		if cursor and conn:
			cursor.close()
			conn.close()





if __name__ == "__main__":
    app.run()
