import pymysql
from db_config import mysql
from werkzeug.security import check_password_hash
import smtplib
from passlib.hash import sha256_crypt
			
def login(email, pwd):
	conn = None;
	cursor = None;
	
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		
		sql = "SELECT hname, email, pwd FROM user WHERE email=%s"
		sql_where = (email,)
		
		cursor.execute(sql, sql_where)
		row = cursor.fetchone()
		print(row[2])
		if row:
			if sha256_crypt.verify(pwd, row[2]):
				return row[0]
				
		return None

	except Exception as e:
		print(e)

	finally:
		if cursor and conn:
			cursor.close()
			conn.close()
def user_exist(email):
	conn = None;
	cursor = None;
	
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		
		sql = "SELECT email FROM user WHERE email=%s"
		sql_where = (email,)
		
		cursor.execute(sql, sql_where)
		row = cursor.fetchone()
		
		if row:
			return True
		return False

	except Exception as e:
		print(e)

	finally:
		if cursor and conn:
			cursor.close()
			conn.close()
			

def register(name, hname, address, district, pincode, phno, email, pwd):
	conn = None;
	cursor = None;
	
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		sql = "INSERT INTO user(name, hname, address, district, pincode, phno, email, pwd) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
		data = (name, hname, address, district, pincode, phno, email, sha256_crypt.encrypt(pwd))
		
		cursor.execute(sql, data)
		
		conn.commit()

	except Exception as e:
		print(e)

	finally:
		if cursor and conn:
			cursor.close()
			conn.close()
			
def registerh(hname, haddress, lat, lng, hdistrict, hpincode, hphno, hemail, vnum, vuse, vavail):
	conn = None;
	cursor = None;
	
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		sql = "INSERT INTO hospital(hname, haddress, lat, lng, hdistrict, hpincode, hphno, hemail, vnum, vuse, vavail) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		data = (hname, haddress, lat, lng, hdistrict, hpincode, hphno, hemail, vnum, vuse, vavail)
		
		cursor.execute(sql, data)
		
		conn.commit()

	except Exception as e:
		print(e)

	finally:
		if cursor and conn:
			cursor.close()
			conn.close()
