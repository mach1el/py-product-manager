import os,sys,sqlite3
import xml.dom.minidom as dom
from xml.dom.minidom import Document
sys.dont_write_bytecode = True

dbf = os.path.join(os.path.abspath(os.path.dirname(__file__)),'database','products.db')

class Product(object):
	def __init__(self,pid=None,
					 name=None ,
					 category=None , 
					 size=None , 
					 price=None, 
					 released_year=None, 
					 pic=None):
		super(Product,self).__init__()
		self.pid = pid
		self.pic = pic
		self.name = name
		self.size = size
		self.price = price
		self.category = category
		self.released_year = released_year
	
	@staticmethod
	def select_product():
		list_product = []
		conn = sqlite3.connect(dbf)
		cursor = conn.execute("SELECT * FROM PRODUCTS")
		for row in cursor:
			list_product.append(row)
		conn.close()
		return list_product

	def add_product(self):
		result = False
		conn = sqlite3.connect(dbf)
		sql = "INSERT INTO products (name, category, size, released_year, price, image) VALUES (?, ?, ?, ?, ?, ?)"
		if conn.execute(sql,(self.name, self.category, self.size, self.released_year, self.price, self.pic)):
			result = True
			conn.commit()
			conn.close()
		return result

	def update_product(self):
		conn = sqlite3.connect(dbf)
		cursor = conn.cursor()
		sql = ''' UPDATE PRODUCTS
					SET price = ? , released_year = ?
					WHERE id = ?
		'''
		cursor.execute(sql,(self.price,self.released_year,self.pid))
		conn.commit()
		conn.close()

	def delete_product(self):
		conn = sqlite3.connect(dbf)
		cursor = conn.cursor()
		sql = ''' DELETE from products where id = ?'''
		cursor.execute(sql,(self.pid,))
		conn.commit()
		conn.close()

	@staticmethod
	def generate_xml_from_db():
		data = Product.select_product()
		doc = Document()
		root_xml = doc.createElement('Products')
		doc.appendChild(root_xml)

		for product in data:
			child_node = doc.createElement('product' + str(product[0]))
			child_node.setAttribute('category',product[2])
			root_xml.appendChild(child_node)

			name = doc.createElement('name')
			name.appendChild(doc.createTextNode(product[1]))
			child_node.appendChild(name)

			size = doc.createElement('size')
			size.appendChild(doc.createTextNode(str(product[3])))
			child_node.appendChild(size)

			price = doc.createElement('price')
			price.appendChild(doc.createTextNode(str(product[5])))
			child_node.appendChild(price)

			released_year = doc.createElement('released_year')
			released_year.appendChild(doc.createTextNode(str(product[4])))
			child_node.appendChild(released_year)

			image = doc.createElement('image')
			image.appendChild(doc.createTextNode(os.path.join(os.path.abspath(os.path.dirname(__file__)),'images',product[6])))
			child_node.appendChild(image)
		return doc