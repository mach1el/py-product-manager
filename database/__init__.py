import os,sys,json,sqlite3
sys.dont_write_bytecode=True

ROOT = os.path.abspath(os.path.dirname(__file__))
user_db_file = os.path.join(ROOT,'userdb.json')
product_db_file = os.path.join(ROOT,'products.db')

class DBHandler(object):

	@staticmethod
	def check_user(username,password):
		Correct = False

		with open(user_db_file,'r') as jsfile:
			data = json.load(jsfile)
			for d in data['users']:
				user,passwd = set(d.keys()),set(d.values())
				if "".join(user) == username and "".join(passwd) == password:
					Correct = True
		return Correct

	@staticmethod
	def generate_user_db_file():
		data = {
			"users" : [
						{"admin" : "root"},
						{"michael" : "gwarrior"},
						{"spec" : "tre"}
					]
		}
		if os.path.isfile(user_db_file):
			pass
		else:
			with open(user_db_file,'w+') as jsfile:
				json.dump(data,jsfile,indent=4)

	@staticmethod
	def generate_product_db_file():
		if os.path.isfile(product_db_file):
			pass
		else:
			conn = sqlite3.connect(product_db_file)
			sql = '''
			CREATE TABLE products (
					id INTEGER PRIMARY KEY,
					name TEXT NOT NULL,
					category TEXT NOT NULL,
					size REAL NOT NULL,
					released_year INTEGER NOT NULl,
					price REAL NOT NULL,
					image TEXT NOT NULL
			);'''
			conn.execute(sql)
			conn.close()

			DBHandler.add_products_to_db()

	@staticmethod
	def add_products_to_db():
		conn = sqlite3.connect(product_db_file)
		p1 = "INSERT INTO products (name, category, size, released_year, price, image) \
				VALUES ('ux430','zenbook',13,2017,1000,'asus_ux430_2017.jpg')" 
		p2 = "INSERT INTO products (name, category, size, released_year, price, image) \
				VALUES ('ux550','zenbook',15,2018,1200,'asus_ux430_2017.jpg')" 
		p3 = "INSERT INTO products (name, category, size, released_year, price, image) \
				VALUES ('flip S','zenbook',13.3,2018,1200,'asus_flip_s_2017.jpg')"
		p4 = "INSERT INTO products (name, category, size, released_year, price, image) \
				VALUES ('Rog Scar 2','ROG',15,2018,1400,'asus_rog_scar_strix_2.jpg')"

		for p in [p1,p2,p3,p4]:
			conn.execute(p)
			conn.commit()
		conn.close()
