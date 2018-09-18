import os,sys,shutil
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk,Image
from product import Product
from database import DBHandler

class AutoScrollbar(ttk.Scrollbar):
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)
    def pack(self, **kw):
        raise TclError("cannot use pack with this widget")
    def place(self, **kw):
        raise TclError("cannot use place with this widget")

def win1():
	mainframe = Frame(root,bg="white")
	mainframe.grid(column = 0, row = 0, sticky = (N, W, E, S))
	mainframe.columnconfigure(0, weight = 1)
	mainframe.rowconfigure(0, weight = 1)

	Label(master=mainframe, text="Username",bg="white").grid(row = 0, column = 0)
	Entry(master=mainframe, textvariable=var_user).grid(row = 0, column= 1)
	Label(master=mainframe, text="Password",bg="white").grid(row = 1, column = 0)
	Entry(master=mainframe, show="*", textvariable=var_pass).grid(row =1, column = 1)
	Button(mainframe, text = 'Login', command = win2,bg="white").grid(row = 2, column = 1, sticky = W)

	root.bind('<Return>',win2)
	root.mainloop()

def win2(event = None):
	global var_user, var_pass
	username = var_user.get()
	password = var_pass.get()
	flag = DBHandler.check_user(username,password)
	if flag:
		messagebox.showinfo("Info","Welcome to ASUS laptop manager")
		root.withdraw()
		new = Toplevel(bg="white")
		new.title('Manager')
		new.geometry("700x500+330+100")
		new.resizable(0, 0)

		menubar = Menu(new,bg="white")
		option = Menu(menubar, tearoff=0,bg="white")
		option.add_command(label="Add product", command=win3)
		option.add_command(label="Find product", command=win4)
		option.add_command(label="Update product",command=win5)
		option.add_command(label="Delete product",command=win6)
		option.add_command(label="Generate database to xml",command=win7)
		option.add_separator()
		option.add_command(label="Quit", command=new.quit)
		menubar.add_cascade(label="Menu", menu= option)

		mainframe = Frame(new,bg="white")
		mainframe.grid(column = 0, row = 0, sticky = (N, W, E, S))
		mainframe.columnconfigure(1, weight = 1)
		mainframe.rowconfigure(1, weight = 1)

		new.config(menu=menubar)

		file = os.path.join(os.path.abspath(os.path.dirname(__file__)),"images","asus_banner.jpg")
		ifile = Image.open(file)
		ifile = ifile.resize((700,500),Image.ANTIALIAS)
		img = ImageTk.PhotoImage(ifile) 
		L = Label(master=mainframe, image=img,bg="white")
		L.image = img
		L.grid(row=0, column=1, sticky=W)

	else:
		messagebox.showwarning("Warning", "Authentication failed!")
		var_user.set("")
		var_pass.set("")

def win3():
	root.withdraw()
	new = Toplevel(bg="white")
	new.title('Add new product')
	new.geometry("450x170+500+180")
	new.resizable(0, 0)

	mainframe = Frame(new,bg="white")
	mainframe.grid(column = 0, row = 0, sticky = (N, W, E, S))
	mainframe.columnconfigure(0, weight = 1)
	mainframe.rowconfigure(0, weight = 1)

	Label(master=mainframe, text="Product name",bg="white").grid(row = 0, column = 0)
	Entry(master=mainframe, width=50, textvariable=var_name).grid(row = 0, column = 1)
	Label(master=mainframe, text="Category",bg="white").grid(row = 1,column = 0)
	Entry(master=mainframe, width=50,textvariable=var_category).grid(row = 1,column = 1)
	Label(master=mainframe, text="Size",bg="white").grid(row = 2, column = 0)
	Entry(master=mainframe, width=50, textvariable=var_size).grid(row = 2, column = 1) 
	Label(master=mainframe, text="Released year",bg="white").grid(row = 3, column = 0)
	Entry(master=mainframe, width=50, textvariable=var_released_year).grid(row= 3, column = 1) 
	Label(master=mainframe, text="Price",bg="white").grid(row = 4, column = 0)
	Entry(master=mainframe, width=50, textvariable=var_price).grid(row =4, column = 1)
	Label(master=mainframe, text="Picture",bg="white").grid(row = 5, column = 0)
	Label(master=mainframe, textvariable=var_picture,bg="white", width=25).grid(row = 5, column = 1, sticky = W)
	Button(mainframe, text='Choose file...', command=upload_file,bg="white").grid(row = 5, column = 1, sticky=E)
	Button(mainframe, text = 'Add new product', command = add_to_db,bg="white").grid(row = 6, column = 1, sticky = W)
	Button(mainframe,text='Cancel',command=new.destroy,bg="white").grid(row = 6,column = 1,sticky = N)

def win4():
	root.withdraw()
	new = Toplevel(bg="white")
	new.resizable(0,0)
	new.title('Find Product')

	vscroll = AutoScrollbar(new)
	vscroll.grid(row = 0,column = 1,sticky = "ns")
	hscroll = AutoScrollbar(new,orient = HORIZONTAL)
	hscroll.grid(row = 1,column = 0,sticky = "ew")

	global canvas
	canvas = Canvas(new,
					width = 600,
					height = 450,
					bg = "white",
					yscrollcommand = vscroll.set,
					xscrollcommand = hscroll.set)
	canvas.grid(row = 0,column = 0,sticky = "nsew")

	vscroll.config(command = canvas.yview)
	hscroll.config(command = canvas.xview)

	new.grid_rowconfigure(0,weight = 1)
	new.grid_columnconfigure(0,weight = 1)

	frame = Frame(canvas,bg="white",highlightthickness=0)
	frame.rowconfigure(1,weight = 1)
	frame.columnconfigure(1,weight = 1)
	
	Label(frame, text="Product name",relief="flat",bg="white").grid(row = 0, column =0,sticky = "nsew")
	Entry(frame,width=20,textvariable=var_name).grid(row = 0, column = 1,sticky = "nsew")
	Button(frame, text = 'Find',bg="white", command =lambda:find_product(frame)).grid(row = 0, column = 2, sticky = "N")
	canvas.create_window(0, 0,anchor = 'nw',window = frame)

def win5():
	root.withdraw()
	new = Toplevel(bg="white")
	new.title('Update product')
	new.geometry("350x320+150+150")
	new.resizable(0, 0)

	mainframe = Frame(new,bg="white")
	mainframe.grid(column = 0, row = 0, sticky = (N, W, E, S))
	mainframe.columnconfigure(0, weight = 1)
	mainframe.rowconfigure(0, weight = 1)

	Label(master=mainframe, text="Product's ID",bg="white").grid(row = 0,column = 0)
	Entry(master=mainframe, width=30, textvariable=var_id).grid(row =0, column = 1)
	Button(master=mainframe,text='Display product info',bg="white",command= lambda:display_product_info(new,mainframe)).grid(row = 1, column = 1,sticky = "nw")
	Button(master=mainframe, text = 'Cancel',bg = 'white',command = new.destroy).grid(row = 1,column = 1,sticky = "es")


def win6():
	root.withdraw()
	new = Toplevel(bg="white")
	new.title('Delete Product')
	new.geometry("400x150+440+130")
	new.resizable(0, 0)

	mainframe = Frame(new,bg="white")
	mainframe.grid(column = 0, row = 0, sticky = (N, W, E, S))
	mainframe.columnconfigure(0, weight = 1)
	mainframe.rowconfigure(0, weight = 1)

	Label(master=mainframe, text="Product's ID",bg="white",relief="raised").grid(row = 0, column= 0)
	Entry(master=mainframe, width=40, textvariable=var_id).grid(row =0, column = 1)
	Button(mainframe, text = 'Delete',bg="white", command = delete_product).grid(row = 1, column = 1, sticky = (N,W,E))
	Button(mainframe, text = 'Cancel',bg="white", command = new.destroy).grid(row = 1,column = 1,sticky = (N,E,W))

def win7():
	root.withdraw()
	new = Toplevel(bg="white")
	new.resizable(0,0)
	new.title('Generate database')

	menubar = Menu(new,bg="white")
	option = Menu(menubar, tearoff=0,bg="white")
	option.add_command(label="Generate",command = xml_generator)
	option.add_command(label="Quit", command = new.quit)
	menubar.add_cascade(label="Option", menu= option)

	vscroll = AutoScrollbar(new)
	vscroll.grid(row = 0,column = 1,sticky = "ns")
	hscroll = AutoScrollbar(new,orient = HORIZONTAL)
	hscroll.grid(row = 1,column = 0,sticky = "ew")

	canvas = Canvas(new,
					width = 700,
					height = 450,
					bg = "white",
					yscrollcommand = vscroll.set,
					xscrollcommand = hscroll.set)
	canvas.grid(row = 0,column = 0,sticky = "nsew")

	vscroll.config(command = canvas.yview)
	hscroll.config(command = canvas.xview)

	new.grid_rowconfigure(0,weight = 1)
	new.grid_columnconfigure(0,weight = 1)

	frame = Frame(canvas,bg="white")
	frame.rowconfigure(1,weight = 1)
	frame.columnconfigure(1,weight = 1)

	new.config(menu=menubar)

	info  = (u"Product",u"Category",u"Size",u"Released year",u"Price",u"Image")
	for i,item in enumerate(info):
		Label(frame,text=u"%s" % item,bg="white",fg="grey",borderwidth=1,relief="raised",padx=5,pady=5).grid(column=i,row=2,sticky='news')

	r = 3
	list_products = Product.select_product()
	for product in list_products:
		imgf = os.path.join(ROOT,'images',product[6])
		Label(frame, text=product[1],borderwidth=5,relief="flat",bg="white").grid(row=r,column=0,sticky="nsew")
		Label(frame, text=product[2],borderwidth=5,relief="flat",bg="white").grid(row=r,column=1,sticky="nsew")
		Label(frame, text=product[3],borderwidth=5,relief="flat",bg="white").grid(row=r,column=2,sticky="nsew")
		Label(frame, text=product[4],borderwidth=5,relief="flat",bg="white").grid(row=r,column=3,sticky="nsew")
		Label(frame, text=product[5],borderwidth=10,relief="flat",bg="white").grid(row=r,column=4,sticky="nsew")
		Label(frame, text=imgf,borderwidth=10,relief="flat",bg="white").grid(row=r,column=5,sticky="nsew")
		r +=1
	canvas.create_window(0, 0,anchor = 'nw',window = frame)
	frame.update_idletasks()
	canvas.config(scrollregion = canvas.bbox("all"))
	canvas.bind("<Button-4>", lambda event: canvas.yview('scroll',-1,'units'))
	canvas.bind("<Button-5>", lambda event: canvas.yview('scroll',1,'units'))

def upload_file():
	des = os.path.join(ROOT,'images')
	file_path = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
	if (os.path.isfile(file_path)):
		shutil.copy(file_path, des)
		fname = str(file_path).split('/')[-1:][0]
		messagebox.showinfo( "File moving...", "Success: " + fname)
		global var_picture
		var_picture.set(fname)
	else:
		messagebox.showwarning( "File moving...", "Fail")

def add_to_db():
	global var_name, var_category , var_size, var_released_year, var_price, var_picture

	name = var_name.get()
	category = var_category.get()
	size = var_size.get()
	price = int(var_price.get())
	released_year = float(var_released_year.get())
	pic = var_picture.get()

	product = Product(None, name, category , size, price, released_year, pic)
	result = product.add_product()

	if result:
		messagebox.showinfo("Success", "Add new product successes!")
	else:
		messagebox.showwarning("Fail", "Add new product failed!")

def find_product(mainframe):
	global var_name

	name = var_name.get()
	list_products = Product.select_product()

	info  = (u"Product",u"Category",u"Size",u"Released year",u"Price",u"Image")
	for i,item in enumerate(info):
		Label(mainframe,text=u"%s" % item,bg="white",fg="grey",borderwidth=2,relief="raised").grid(column=i,row=1,sticky='nsew')
	r = 2
	count = 0

	for product in list_products:
		if product[1].lower().find(name.lower()) != -1:
			Label(mainframe, text=product[1],borderwidth=5,relief="flat",bg="white").grid(row=r,column=0,sticky="nsew")
			Label(mainframe, text=product[2],borderwidth=5,relief="flat",bg="white").grid(row=r,column=1,sticky="nsew")
			Label(mainframe, text=product[3],borderwidth=5,relief="flat",bg="white").grid(row=r,column=2,sticky="nsew")
			Label(mainframe, text=product[4],borderwidth=5,relief="flat",bg="white").grid(row=r,column=3,sticky="nsew")
			Label(mainframe, text=product[5],borderwidth=10,relief="flat",bg="white").grid(row=r,column=4,sticky="nsew")

			file = os.path.join(ROOT,'images',product[6])
			ifile = Image.open(file)
			ifile = ifile.resize((135,120),Image.ANTIALIAS)
			img = ImageTk.PhotoImage(ifile)
			L = Label(master=mainframe, borderwidth=10, relief = "flat", image=img,bg="white")
			L.image = img
			L.grid(row=r, column=5, sticky="nsew")

			r +=1
			count+=1

	mainframe.update_idletasks()
	canvas.config(scrollregion = canvas.bbox("all"))
	canvas.bind("<Button-4>", lambda event: canvas.yview('scroll',-1,'units'))
	canvas.bind("<Button-5>", lambda event: canvas.yview('scroll',1,'units'))

	if count==0:
		messagebox.showwarning( "Fail", "Could not find product")

def display_product_info(new,mainframe):
	global var_id
	pid = var_id.get()
	list_products = Product.select_product()

	found = None
	for product in list_products:
		try:
			if isinstance(int(pid),int):
				if int(pid) == int(product[0]):
					found = product
					break;
		except ValueError:
			messagebox.showerror("Error","Your input is string instead of number")
			break;

	if found == None:
		messagebox.showwarning("Warning","Product not found")
	else:
		var_id.set(found[0])
		var_name.set(found[1])
		var_category.set(found[2])
		var_size.set(found[3])
		var_price.set(found[5])
		var_released_year.set(found[4])

		file = os.path.join(ROOT,'images',found[6])
		ifile = Image.open(file)
		ifile = ifile.resize((180,120),Image.ANTIALIAS)
		img = ImageTk.PhotoImage(ifile)
		L = Label(master=mainframe, borderwidth=10, relief = "flat", image=img,bg="white")
		L.image = img
		L.grid(row=2, column=1,sticky = "nwe")

		Label(master=mainframe, text="Product name",bg="white").grid(row = 3, column= 0)
		Label(master=mainframe, width=30,textvariable=var_name,bg="white",fg="cyan").grid(row = 3, column = 1)
		Label(master=mainframe, text="Size",bg="white").grid(row = 4,column = 0)
		Entry(master=mainframe, width=30,textvariable=var_size).grid(row = 4,column = 1)
		Label(master=mainframe, text="Category",bg="white").grid(row = 5,column =0)
		Label(master=mainframe, textvariable = var_category,bg = "white",fg = "cyan").grid(row = 5,column = 1)
		Label(master=mainframe, text="Price",bg="white").grid(row = 6,column = 0)
		Entry(master=mainframe, width=30,textvariable=var_price).grid(row = 6, column = 1)
		Label(master=mainframe, text="Released year",bg="white").grid(row = 7,column = 0)
		Entry(master=mainframe, width=30,textvariable=var_released_year).grid(row = 7, column = 1)

		Button(mainframe, text = 'Update', command = update_product,bg="white").grid(row = 8, column = 1,sticky = "w")
		Button(mainframe, text = 'Cancel', command = new.destroy,bg="white").grid(row = 8,column = 1,sticky = "s")

def update_product():
	global var_id,var_price,var_released_year

	product_id = var_id.get()
	product_price = var_price.get()
	released_year = var_released_year.get()
	list_products = Product.select_product()

	found = False
	for product in list_products:
		if int(product_id) == int(product[0]):
			answer = messagebox.askokcancel("Update confirm","Do you really want to update ?")
			if answer:
				handler = Product(pid = product_id,price = product_price, released_year = released_year)
				handler.update_product()
				messagebox.showinfo("Confirm","Product have been updated")
			found = True
			break

	if found == False:
		messagebox.showwarning("Warning","Product not found !!!")

def delete_product():
	global var_id
	product_id = var_id.get()
	list_products = Product.select_product()
	
	found = False
	for product in list_products:
		try:
			if isinstance(int(product_id),int):
				if int(product_id) == int(product[0]):
					answer = messagebox.askokcancel("Delete confirm","Do you really want to delete ?")
					if answer:
						handler = Product(pid = product_id)
						handler.delete_product()
					found = True
					break;
				
		except ValueError:
			messagebox.showerror("Error","Your input is string instead of number")
			break;

	if found == False:
		messagebox.showwarning("Warning","Could not find product !")

def xml_generator():
	if sys.platform == 'linux':
		initialdir = "/home/$USER"
	else:
		initialdir = "/"

	answer = messagebox.askokcancel("Generate file","Do you want to generate database to XML file ?")
	if answer:
		filename =  filedialog.asksaveasfilename(initialdir = "/home/$USER",title = "Select file",filetypes = (("xml files","*.xml"),("all files","*.*")))
		if filename == ():
				pass
		else:
			xml = Product.generate_xml_from_db()
			xml.writexml(open(file = filename,mode = 'w',encoding = 'utf-8'),indent = '',addindent = '',newl = '')
			messagebox.showinfo("Info","Writed database to %s" % filename)

 
if __name__ == '__main__':
	ROOT = os.path.abspath(os.path.dirname(__file__))
	DBHandler.generate_user_db_file()
	DBHandler.generate_product_db_file()

	root = Tk()
	root.title('Login')
	root.resizable(0, 0)
	root.style = ttk.Style()
	root.style.theme_use('clam')
	root.geometry("220x100+550+220")
	root.configure(background='white')
	root.quit()

	var_id = StringVar()
	var_user = StringVar()
	var_pass = StringVar()
	var_name = StringVar()
	var_size = StringVar()
	var_price = StringVar()
	var_picture = StringVar()
	var_category = StringVar()
	var_released_year = StringVar()
	
	sys.exit(win1())