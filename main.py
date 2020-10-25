# Importing stuff
from tkinter import *
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import pickle
import webbrowser
from PIL import ImageTk,Image
from tkinter import messagebox

# Variables
money = pickle.load(open("money.dat","rb"))
stockmain = ""

# Configure the menu
root_menu = Tk()
root_menu.title("MENU")
root_menu.geometry("200x200")
root_menu.grid_columnconfigure(2, weight=1)

# Defining the functions
def f_lookup():
	# Configure the lookup menu
	root_lookup = Tk()
	root_lookup.title("LOOKUP")
	root_lookup.geometry("200x200")
	root_lookup.grid_columnconfigure(2, weight=1)

	# Creating the entry options
	ent_lookup = Entry(root_lookup, borderwidth = 5)
	ent_lookup.grid(row = 0, column = 2, padx = 3, pady = 3)
	
	# Defining the search button
	def f_search():
		global stockmain
		def main():
			global stockmain
			symbol = ent_lookup.get()
			stock_price = 0
			result = requests.get(f"https://money.cnn.com/quote/quote.html?symb={symbol}").text
			soup = BeautifulSoup(result, features="lxml")
			stock_price = soup.find("span",attrs = {"streamformat": "ToHundredth"})
			try:
				stock_price = str(stock_price)
				stock_price = stock_price.split("<")
				stock_price = stock_price[1]
				stock_price = stock_price.split(">")
				stock_price = stock_price[1]
				stock_price = list(stock_price)
				if "," in stock_price:
					stock_price.remove(",")
				for i in stock_price:
					stockmain = stockmain + i
				stock_price = float(stockmain)
				stock_price_str = str(stockmain)+ " $"
				stock_label = Label(root_lookup, text = f"{stock_price_str}")
				stock_label.grid(row = 3, column = 2, padx = 3, pady = 3)
				label_help = Label(root_lookup, text = "For more info click")
				label_help.grid(row = 4,column = 2, padx = 3, pady = 3)
			except:
				messagebox.showinfo("Error", "Enter a valid symbol")
				root_lookup.destroy()
		
			def stats():
				webbrowser.open(f"https://money.cnn.com/quote/quote.html?symb={symbol}")
			btn_stats = Button(root_lookup,text = "help", command = stats)
			btn_stats.grid(row = 5,column = 2, padx = 3, pady = 3)
		main()
	btn_lookup_lookup = ttk.Button(root_lookup, text = "Lookup", command = f_search)
	btn_lookup_lookup.grid(row = 1, column = 2, pady = 3, padx = 3)
def f_buy():
	global stockmain
	stockmain = ""
	# Configure the lookup menu
	root_buy = Tk()
	root_buy.title(f"Stonks-Buy-{money}$ left")
	root_buy.geometry("200x200")
	root_buy.grid_columnconfigure(2, weight=1)

	# Creating the entry options
	ent_lookup = Entry(root_buy, borderwidth = 3)
	ent_lookup.grid(row = 0, column = 2, padx = 3, pady = 3)
	
	# Defining the search button
	def f_search_buy():
		global stockmain
		symbol = ent_lookup.get()
		stock_price = 0
		result = requests.get(f"https://money.cnn.com/quote/quote.html?symb={symbol}").text
		soup = BeautifulSoup(result, features="lxml")
		stock_price = soup.find("span",attrs = {"streamformat": "ToHundredth"})
		try:
			stock_price = str(stock_price)
			
			stock_price = stock_price.split("<")
			
			stock_price = stock_price[1]
			
			stock_price = stock_price.split(">")
			
			stock_price = stock_price[1]
			
			stock_price = list(stock_price)
			
			if "," in stock_price:
				stock_price.remove(",")
				
			for i in stock_price:
				stockmain = stockmain + i
				
			stock_price = float(stockmain)
			
			stock_label = Label(root_buy, text = f"{stockmain}$")
			stock_label.grid(row = 3, column = 2, padx = 3, pady = 3)
		except:
			messagebox.showinfo("Error", "Enter a valid symbol")
			root_buy.destroy()
		label_help = Label(root_buy, text = "For more info click")
		label_help.grid(row = 5,column = 2, padx = 3, pady = 3)		
		def stats():
			webbrowser.open(f"https://money.cnn.com/quote/quote.html?symb={symbol}")
		btn_stats = Button(root_buy,text = "help", command = stats)
		btn_stats.grid(row = 6,column = 2, padx = 3, pady = 3)
		# Creating the quantity
		label_quantity = Label(root_buy, text = "Enter the quantity (only 1 to 10)")
		label_quantity.grid(row = 7, column = 2, padx = 3, pady = 3)
		ent_quantity = Entry(root_buy)
		ent_quantity.grid(row = 8, column = 2, padx = 3, pady = 3)

		def enter_quantity():
			global stockmain
			global stock_price
			global money
			quantity = int(ent_quantity.get())
			if quantity > 10 or quantity < 1:
				messagebox.showinfo("Error", "Renter the quantity lesser than 10 and greater than 1")
			else:
				stockmain = float(stockmain)
				price = float(stockmain * quantity)
				if price > money:
					messagebox.showinfo("Error",f"You only have {money}$ but the cost is {price}$")
		# Creating the Quantity button
		btn_enter_quantity = ttk.Button(root_buy, text = "Enter", command = enter_quantity)
		btn_enter_quantity.grid(row = 9, column = 2, padx = 3, pady = 3)
		# Config the menu
		root_buy.geometry("250x300")
		
		# Creating the buttons
	btn_lookup_buy = ttk.Button(root_buy, text = "Lookup", command = f_search_buy)
	btn_lookup_buy.grid(row = 1, column = 2, pady = 3, padx = 3)
def f_help():
	webbrowser.open("https://shikhar006.github.io/stonks/help.html")
# Creating the buttons
btn_lookup = ttk.Button(root_menu, text = "Lookup", command = f_lookup)
btn_lookup.grid(row = 0, column = 2, padx = 3, pady = 5)

btn_buy = ttk.Button(root_menu, text = "Buy Stock", command = f_buy )
btn_buy.grid(row = 1, column = 2, padx = 3, pady = 3)

btn_help = ttk.Button(root_menu, text = "Help", width = 9, command = f_help)
btn_help.grid(row = 3, column = 2, padx = 3, pady = 3)

# Ending
root_menu.mainloop()