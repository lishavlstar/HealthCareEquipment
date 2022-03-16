import dao
from app import app
from flask import jsonify, request, session, redirect, url_for
from db_config import mail
from flask_mail import Mail, Message
from flask import render_template,jsonify, flash
import smtplib

@app.route('/login', methods=['POST'])
def login():
	_json = request.json
	#print(_json)
	_username = _json['username']
	_password = _json['password']
	
	if _username and _password:
		user = dao.login(_username, _password)
		
		if user != None:
			session['username'] = user
			print(session['username'])
			
			return jsonify({"redirect": "/index"})

	resp = jsonify({'message' : 'Bad Request - invalid credendtials'})
	resp.status_code = 400
	return resp

@app.route('/logout')
def logout():
	if 'username' in session:
		session.pop('username', None)
	return jsonify({"redirect": "/"})
@app.route('/back')
def back():
	if 'username' in session:
		return jsonify({"redirect": "/index"})
@app.route('/logout1')
def logout1():
	if 'username' in session:
		session.pop('username', None)
	return jsonify({"redirect": "/"})

@app.route('/signup', methods=['POST'])
def signup():
	_json = request.json
	_name = _json['name']
	_hname = _json['hname']
	_address = _json['address']
	_district = _json['district']
	_pincode = _json['pincode']
	_phno = _json['phno']
	_email = _json['email']
	_pwd = _json['password']
	
	if  _name and  _address and _district and _pincode and _phno and _email and _pwd:
	
		user_exist = dao.user_exist(_email)
		
		if user_exist == True:
			resp = jsonify({'message' : 'User already registered'})
			resp.status_code = 409
			return resp
		else:		
			dao.register(_name, _hname, _address, _district, _pincode, _phno, _email, _pwd)
			msg = Message('Thank you for registering with us !', sender = 'lisha@pumexinfotech.com', recipients = [_email])
			msg.html = render_template('mail.html', data=_name, username=_email, pwd=_pwd )
			mail.send(msg)
			return jsonify({"redirect": "/next"})
			
			
	else:
		resp = jsonify({'message' : 'Bad Request - invalid parameters'})
		resp.status_code = 400
		return resp


@app.route('/signup1', methods=['POST'])
def signup1():
	_json = request.json
	_hname = _json['hname']
	_haddress = _json['haddress']
	_lat =  _json['lat']
	_lng =  _json['lng']
	_hdistrict = _json['hdistrict']
	_hpincode = _json['hpincode']
	_hphno = _json['hphno']
	_hemail = _json['hemail']
	_vnum = _json['vnum']
	_vuse = _json['vuse'] 
	_vavail = _json['vavail']
	key = None

	if  _hname and _haddress and _hdistrict and _hpincode and _hphno and _hemail and _vnum and _vuse and _vavail:
	
		user_exist = dao.user_exist(_hemail)
		
		if user_exist == True:
			resp = jsonify({'message' : 'User already registered'})
			resp.status_code = 409
			return resp
		else:		
			dao.registerh(_hname, _haddress, _lat, _lng, _hdistrict, _hpincode, _hphno, _hemail, _vnum,  _vuse,  _vavail )
			return jsonify(key)
			
			
	else:
		resp = jsonify({'message' : 'Bad Request - invalid parameters'})
		resp.status_code = 400
		return resp