# Importing modules
from tkinter import *
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import pickle
import webbrowser
from tkinter import messagebox

# Variables
try:
	money = pickle.load(open("money.dat","rb"))
except:
	money = 1000
	pickle.dump(money, open("money.dat", "wb"))
stockmain = ""

# Dictionary
try:
	stocks = pickle.load(open("stocks.dat", "rb"))
except:
	stocks = {}
	pickle.dump(stocks,open("stocks.dat","wb"))
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
		symbol = str(symbol)
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
			stock_label = Label(root_buy, text = f"{stock_price}$")
			stock_label.grid(row = 3, column = 2, padx = 3, pady = 3)
			stockmain = stock_price
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
				else:
					try:
						label_total_price.destroy()
					except:
						pass
					label_total_price = Label(root_buy, text = f"{price}$ is total price",width = 60)
					label_total_price.grid(row = 10, column = 2, padx = 3, pady = 3)

					# Defining the buying button
					def last_conform():
						global money
						stock_price_final = stockmain * quantity 
						stocks[symbol] = [stockmain,quantity,stock_price_final]
						messagebox.showinfo("Bought", f"The stock {symbol} has been bought for {price}$ of quantity {quantity} for {stockmain}$ per share.")
						pickle.dump(stocks,open("stocks.dat", "wb"))
						money = money - stock_price_final
						pickle.dump(money,open("money.dat", "wb"))

					# Creating the final button for buying
					btn_continue = Button(root_buy, text = "Continue?", command = last_conform)
					btn_continue.grid(row = 11, column = 2, padx = 3, pady = 3)

		# Creating the Quantity button
		btn_enter_quantity = ttk.Button(root_buy, text = "Enter", command = enter_quantity)
		btn_enter_quantity.grid(row = 9, column = 2, padx = 3, pady = 3)
		
		# Config the menu
		root_buy.geometry("250x320")
		
		# Creating the buttons
	btn_lookup_buy = ttk.Button(root_buy, text = "Lookup", command = f_search_buy)
	btn_lookup_buy.grid(row = 1, column = 2, pady = 3, padx = 3)
def f_help():
	webbrowser.open("https://shikhar006.github.io/stonks/help.html")

def f_money():
	messagebox.showinfo("Funds", f"Money left {money}$")

def f_view():
	# Making the view menu
	root_view = Tk()
	root_view.title("View")
	

	# Creating the column names
	label_stock_name_index = Label(root_view, text = "Symbol", width = 15 )
	label_stock_name_index.grid(row = 0, column = 0, padx = 5,pady = 5)
	
	label_bought_price_index = Label(root_view, text = "Bought For", width = 15)
	label_bought_price_index.grid(row = 0, column = 1, padx = 5,pady = 5)
	
	label_quantity_index = Label(root_view , text = "Quantity", width = 10)
	label_quantity_index.grid(row = 0, column = 2, padx = 5,pady = 5)
	
	label_current_price_index = Label(root_view, text = "Current Price", width = 10)
	label_current_price_index.grid(row = 0, column = 3, padx = 5,pady = 5)
	
	def __main__():
		stock_main = ""
		try:
			a = 1 
			for i in stocks:
				label_stock_name = Label(root_view, text = i, width = 15)
				label_stock_name.grid(row = a, column = 0, padx = 5,pady = 5)
				
				label_bought_price = Label(root_view, text = stocks[i][0], width = 15)
				label_bought_price.grid(row = a, column = 1, padx = 5,pady = 5)
				
				label_quantity = Label(root_view, text = stocks[i][1], width = 10)
				label_quantity.grid(row = a, column = 2, padx = 5,pady = 5)

				stock_symbol = i
				result = requests.get(f"https://money.cnn.com/quote/quote.html?symb={stock_symbol}").text
				soup_2 = BeautifulSoup(result, features="lxml")
				stock_price_current = soup_2.find("span",attrs = {"streamformat": "ToHundredth"})
				stock_price_current = str(stock_price_current)
				stock_price_current = stock_price_current.split("<")
				stock_price_current = stock_price_current[1]
				stock_price_current = stock_price_current.split(">")
				stock_price_current = stock_price_current[1]
				stock_price_current = list(stock_price_current)
				if "," in stock_price_current:
					stock_price_current.remove(",")
				for i in stock_price_current:
					stock_main = stock_main + i
				stock_price_current = float(stock_main)

				label_stock_price_current = Label(root_view, text = stock_price_current, width = 10)
				label_stock_price_current.grid(row = a, column = 3, padx = 5,pady = 5)

				a = a+1

		except:
			messagebox.showinfo("Error", "First buy some stock")
			root_view.destroy()
	__main__()

# Creating the buttons
btn_lookup = ttk.Button(root_menu, text = "Lookup", command = f_lookup)
btn_lookup.grid(row = 0, column = 2, padx = 3, pady = 5)

btn_buy = ttk.Button(root_menu, text = "Buy Stock", command = f_buy)
btn_buy.grid(row = 1, column = 2, padx = 3, pady = 3)

btn_money_left = ttk.Button(root_menu, text = "Funds", width = 9, command = f_money)
btn_money_left.grid(row = 2, column = 2, padx = 3, pady = 3)

btn_view = ttk.Button(root_menu, text = "View", width = 9, command = f_view)
btn_view.grid(row = 3, column = 2, padx = 3, pady = 3)

btn_help = ttk.Button(root_menu, text = "Help", width = 9, command = f_help)
btn_help.grid(row = 4, column = 2, padx = 3, pady = 3)

# Ending
root_menu.mainloop()