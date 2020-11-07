# Importing modules
import pickle
import webbrowser
from tkinter import *
from tkinter import messagebox, ttk
import os

import requests
from bs4 import BeautifulSoup

# Syntax dict ##(name: bought price:quantity:final price)##

os.system("pip install lxml")
# Variables
try:
	money = pickle.load(open("money.dat", "rb"))
	stocks = pickle.load(open("stocks.dat", "rb"))
except:
	stocks = {}
	pickle.dump(stocks, open("stocks.dat", "wb"))
	money = 1000
	pickle.dump(money, open("money.dat", "wb"))
stockmain = ""


# Configure the menu
root_menu = Tk()
root_menu.title("MENU")
root_menu.geometry("200x210")
root_menu.grid_columnconfigure(2, weight=1)

# Defining the functions


def f_lookup():
	# Configure the lookup menu
	root_lookup = Tk()
	root_lookup.title("LOOKUP")
	root_lookup.geometry("200x200")
	root_lookup.grid_columnconfigure(2, weight=1)

	# Creating the entry options
	ent_lookup = Entry(root_lookup, borderwidth=5)
	ent_lookup.grid(row=0, column=2, padx=3, pady=3)

	# Defining the search button
	def f_search():
		symbol = ""
		global stockmain
		#stockmain = ""

		def main():
			global stockmain
			symbol = ent_lookup.get()
			stock_price = 0
			stockmain = ""
			result = requests.get(
				f"https://money.cnn.com/quote/quote.html?symb={symbol}").text
			soup = BeautifulSoup(result, features="lxml")
			stock_price = soup.find(
				"span", attrs={"streamformat": "ToHundredth"})
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
				stock_price_str = str(stockmain) + " $"
				stock_label = Label(root_lookup, text=f"{stock_price_str}")
				stock_label.grid(row=3, column=2, padx=3, pady=3)
				label_help = Label(root_lookup, text="For more info click")
				label_help.grid(row=4, column=2, padx=3, pady=3)
			except:
				messagebox.showinfo("Error", "Enter a valid symbol")
				root_lookup.destroy()

			def stats():
				webbrowser.open(
					f"https://money.cnn.com/quote/quote.html?symb={symbol}")
			btn_stats = Button(root_lookup, text="help", command=stats)
			btn_stats.grid(row=5, column=2, padx=3, pady=3)
		main()
	btn_lookup_lookup = ttk.Button(
		root_lookup, text="Lookup", command=f_search)
	btn_lookup_lookup.grid(row=1, column=2, pady=3, padx=3)


def f_buy():
	global stockmain

	# Configure the lookup menu
	root_buy = Tk()
	root_buy.title(f"Stocks-Buy-{money}$ left")
	root_buy.geometry("200x200")
	root_buy.grid_columnconfigure(2, weight=1)

	# Creating the entry options
	ent_lookup = Entry(root_buy, borderwidth=3)
	ent_lookup.grid(row=0, column=2, padx=3, pady=3)

	# Defining the search button
	def f_search_buy():
		global stockmain
		stockmain = ""
		symbol = ""
		symbol = ent_lookup.get()

		stock_price = 0
		result = requests.get(
			f"https://money.cnn.com/quote/quote.html?symb={symbol}").text
		soup = BeautifulSoup(result, features="lxml")
		stock_price = soup.find("span", attrs={"streamformat": "ToHundredth"})
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
			stock_label = Label(root_buy, text=f"{stock_price}$")
			stock_label.grid(row=3, column=2, padx=3, pady=3)
			stockmain = stock_price
		except:
			messagebox.showinfo("Error", "Enter a valid symbol")
			root_buy.destroy()
		label_help = Label(root_buy, text="For more info click")
		label_help.grid(row=5, column=2, padx=3, pady=3)

		def stats():
			webbrowser.open(
				f"https://money.cnn.com/quote/quote.html?symb={symbol}")
		btn_stats = Button(root_buy, text="help", command=stats)
		btn_stats.grid(row=6, column=2, padx=3, pady=3)
		# Creating the quantity
		label_quantity = Label(
			root_buy, text="Enter the quantity (only 1 to 10)")
		label_quantity.grid(row=7, column=2, padx=3, pady=3)
		ent_quantity = Entry(root_buy)
		ent_quantity.grid(row=8, column=2, padx=3, pady=3)

		def enter_quantity():
			global stockmain
			global stock_price
			global money

			quantity = int(ent_quantity.get())
			if quantity > 10 or quantity < 1:
				messagebox.showinfo(
					"Error", "Renter the quantity lesser than 10 and greater than 1")
			else:
				stockmain = float(stockmain)
				price = float(stockmain * quantity)
				if price > money:
					messagebox.showinfo(
						"Error", f"You only have {money}$ but the cost is {price}$")
				else:
					try:
						label_total_price.destroy()
					except:
						pass
					label_total_price = Label(
						root_buy, text=f"{price}$ is total price", width=60)
					label_total_price.grid(row=10, column=2, padx=3, pady=3)

					# Defining the buying button
					def last_conform():
						global money

						stock_price_final = stockmain * quantity
						stocks[symbol] = [stockmain,
										  quantity, stock_price_final]
						root_buy.destroy()
						messagebox.showinfo(
							"Bought", f"The stock {symbol} has been bought for {price}$ of quantity {quantity} for {stockmain}$ per share.")
						pickle.dump(stocks, open("stocks.dat", "wb"))
						money = money - stock_price_final
						money = round(money, 2)
						pickle.dump(money, open("money.dat", "wb"))

					# Creating the final button for buying
					btn_continue = Button(
						root_buy, text="Continue?", command=last_conform)
					btn_continue.grid(row=11, column=2, padx=3, pady=3)

		# Creating the Quantity button
		btn_enter_quantity = ttk.Button(
			root_buy, text="Enter", command=enter_quantity)
		btn_enter_quantity.grid(row=9, column=2, padx=3, pady=3)

		# Config the menu
		root_buy.geometry("250x320")

		# Creating the buttons
	btn_lookup_buy = ttk.Button(root_buy, text="Lookup", command=f_search_buy)
	btn_lookup_buy.grid(row=1, column=2, pady=3, padx=3)


def f_help():
	webbrowser.open("https://shikhar006.github.io/stocks/help.html")


def f_money():
	messagebox.showinfo("Funds", f"Money left {money}$")


def f_view():
	# Making the view menu
	root_view = Tk()
	root_view.title("View")

	# Creating the column names
	label_stock_name_index = Label(root_view, text="Symbol", width=15)
	label_stock_name_index.grid(row=0, column=0, padx=5, pady=5)

	label_bought_price_index = Label(root_view, text="Bought For", width=15)
	label_bought_price_index.grid(row=0, column=1, padx=5, pady=5)

	label_quantity_index = Label(root_view, text="Quantity", width=10)
	label_quantity_index.grid(row=0, column=2, padx=5, pady=5)

	label_current_price_index = Label(
		root_view, text="Current Price", width=10)
	label_current_price_index.grid(row=0, column=3, padx=5, pady=5)

	label_selling_percent_index = Label(
		root_view, text="loss or profit %", width=15)
	label_selling_percent_index.grid(row=0, column=4, padx=5, pady=5)

	label_selling_dollars_index = Label(
		root_view, text="loss or profit $", width=15)
	label_selling_dollars_index.grid(row=0, column=5, padx=5, pady=5)

	def __main__():
		b = True
		if b == True:
			a = 1
			for i in stocks:
				stock_main = ""

				label_stock_name = Label(root_view, text=i, width=15)
				label_stock_name.grid(row=a, column=0, padx=5, pady=5)

				label_bought_price = Label(
					root_view, text=stocks[i][0], width=15)
				label_bought_price.grid(row=a, column=1, padx=5, pady=5)

				label_quantity = Label(root_view, text=stocks[i][1], width=10)
				label_quantity.grid(row=a, column=2, padx=5, pady=5)

				stock_symbol = i
				result = requests.get(
					f"https://money.cnn.com/quote/quote.html?symb={stock_symbol}").text
				soup_2 = BeautifulSoup(result, features="lxml")
				stock_price_current = soup_2.find(
					"span", attrs={"streamformat": "ToHundredth"})
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

				label_stock_price_current = Label(
					root_view, text=stock_price_current, width=10)
				label_stock_price_current.grid(row=a, column=3, padx=5, pady=5)

				def __high__():

					selling_dollars = stock_price_current - \
						stocks[stock_symbol][0]

					selling_percent = (selling_dollars /
									   stocks[stock_symbol][0]) * 100
					selling_percent = round(selling_percent, 2)
					selling_percent = str(selling_percent)
					selling_percent = selling_percent + "%"

					selling_dollars = stock_price_current - \
						stocks[stock_symbol][0]
					selling_dollars = round(selling_dollars, 2)
					selling_dollars = str(selling_dollars)
					selling_dollars = selling_dollars + "$"

					label_selling_percent = Label(
						root_view, text=selling_percent, width=15)
					label_selling_percent.grid(row=a, column=4, padx=5, pady=5)

					label_selling_dollars = Label(
						root_view, text=selling_dollars, width=15)
					label_selling_dollars.grid(row=a, column=5, padx=5, pady=5)

				__high__()

				a = a + 1

		# except:
		#	messagebox.showinfo("Error", "First buy some stock")
		#	root_view.destroy()
	__main__()


def f_sell():
	#global stockmain
	root_sell = Tk()
	root_sell.title("Sell")
	stock = Entry(root_sell)
	stock.grid(row=0, column=0, padx=10, pady=10)

	def __sell__():
		stock_symbol = stock.get()
		if stock_symbol in stocks:
			stock_main = ""
			result = requests.get(
				f"https://money.cnn.com/quote/quote.html?symb={stock_symbol}").text
			soup = BeautifulSoup(result, features="lxml")
			stock_price_current = soup.find(
				"span", attrs={"streamformat": "ToHundredth"})
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
			stock_price_current = float(stock_price_current)
			ent_quantity = Entry(root_sell)
			ent_quantity.insert(0, "Enter the quantity: ")
			ent_quantity.grid(row=2, column=0, padx=10, pady=10)

			def __Enter__():
				#global stock_price_current

				stock_symbol = stock.get()
				if stock_symbol in stocks:
					stock_main = ""
					result = requests.get(
						f"https://money.cnn.com/quote/quote.html?symb={stock_symbol}").text
					soup = BeautifulSoup(result, features="lxml")
					stock_price_current = soup.find(
						"span", attrs={"streamformat": "ToHundredth"})
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
					stock_price_current = float(stock_price_current)

				quantity = ent_quantity.get()
				quantity = int(quantity)
				stock_quantity = int(stocks[stock_symbol][1])
				if quantity > stock_quantity:
					messagebox.showinfo(
						"Error", "Quantity higher than you have")
					ent_quantity.delete(0, END)
				else:
					price = stock_price_current * quantity
					price = str(price)

					label_price = Label(root_sell, text="S.P = " + price + "$")
					label_price.grid(row=4, column=0, padx=10, pady=10)
					bought = stocks[stock_symbol][0] * quantity
					bought = str(bought)
					label_bought = Label(root_sell, text="C.P = " + bought + "$")
					label_bought.grid(row=5, column=0, padx=10, pady=10)

					price = float(price)

					def __enter__():
						
						global money
						money = money + price
						money = round(money, 2)
						pickle.dump(money, open("money.dat", "wb"))
						if quantity == stocks[stock_symbol][1]:
							del stocks [stock_symbol]
							pickle.dump(stocks, open("stocks.dat", "wb"))
							root_sell.destroy()
						else:
							quantity_stocks = int(stocks[stock_symbol][1])
							stocks[stock_symbol][1] = (quantity_stocks-quantity)
							stocks[stock_symbol][2]= stocks[stock_symbol][0] * stocks[stock_symbol][1]
							pickle.dump(stocks, open("stocks.dat", "wb"))
							root_sell.destroy()
							messagebox.showinfo("info",f"{stock_symbol} has been sold for {price}$")
					btn_continue = Button(root_sell, text="continue?", command=__enter__)
						
					btn_continue.grid(row=6, column=0, padx=10, pady=10)

			btn_enter = Button(root_sell, text="Enter", command=__Enter__)
			btn_enter.grid(row=3, column=0, padx=10, pady=10)
		else:
			messagebox.showinfo("Error", "the stock symbol is not bought yet")

	btn_stock = Button(root_sell, text="Enter", command=__sell__)
	btn_stock.grid(row=1, column=0, padx=10, pady=10)


# Creating the buttons
btn_lookup = ttk.Button(root_menu, text="Lookup", command=f_lookup)
btn_lookup.grid(row=0, column=2, padx=3, pady=5)

btn_buy = ttk.Button(root_menu, text="Buy Stock", command=f_buy)
btn_buy.grid(row=1, column=2, padx=3, pady=3)

btn_money_left = ttk.Button(root_menu, text="Funds", width=9, command=f_money)
btn_money_left.grid(row=2, column=2, padx=3, pady=3)

btn_view = ttk.Button(root_menu, text="View", width=9, command=f_view)
btn_view.grid(row=3, column=2, padx=3, pady=3)

btn_sell = ttk.Button(root_menu, text="Sell", width=9, command=f_sell)
btn_sell.grid(row=4, column=2, padx=3, pady=3)

btn_help = ttk.Button(root_menu, text="Help", width=9, command=f_help)
btn_help.grid(row=5, column=2, padx=3, pady=3)

# Ending
root_menu.mainloop()
