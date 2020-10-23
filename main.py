# Importing stuff
from tkinter import *
import requests
from bs4 import BeautifulSoup
import time
import pickle
import webbrowser
from PIL import ImageTk,Image

# Check for function main
a = True
# Configure the menu
root_menu = Tk()
root_menu.title("MENU")
root_menu.geometry("200x200")
root_menu.grid_columnconfigure(2, weight=1)

# Creating the frames (Making it look good)
frame_lookup = LabelFrame(root_menu, text = "Search for symbol", padx = 1, pady = 1)
frame_lookup.grid(row = 0, column = 2)
frame_lookup.grid_columnconfigure(2, weight=1)

# Defining the functions
def f_lookup():
	global a
	# Configure the lookup menu
	root_lookup = Tk()
	root_lookup.title("LOOKUP")
	root_lookup.geometry("200x200")
	root_lookup.grid_columnconfigure(2, weight=1)

	# Creating the entry options
	ent_lookup = Entry(root_lookup, borderwidth = 5)
	ent_lookup.grid(row = 0, column = 2)
	
	# Defining the search button
	def f_search():
		global a
		def main():
			global a
			symbol = ent_lookup.get()
			if a == True:
				stock_price = ""
				result = requests.get(f"https://money.cnn.com/quote/quote.html?symb={symbol}").text
				soup = BeautifulSoup(result, features="lxml")
				stock_price = soup.find("span",attrs = {"streamformat": "ToHundredth"})
				stock_price = str(stock_price)
				stock_price = stock_price.split("<")
				stock_price = stock_price[1]
				stock_price = stock_price.split(">")
				stock_price = stock_price[1]
				stock_price = float(stock_price)
				stock_label = Label(root_lookup, text = stock_price)
				stock_label.grid(row = 3, column = 2)
				time.sleep(3)
				a = False
			else:
				stock_price = ""
				result = requests.get(f"https://money.cnn.com/quote/quote.html?symb={symbol}").text
				soup = BeautifulSoup(result, features="lxml")
				stock_price = soup.find("span",attrs = {"streamformat": "ToHundredth"})
				stock_price = str(stock_price)
				stock_price = stock_price.split("<")
				stock_price = stock_price[1]
				stock_price = stock_price.split(">")
				stock_price = stock_price[1]
				stock_price = float(stock_price)
				stock_label.config(text = stock_price )
				time.sleep(3)
				a = True
		while True:
			main()
	# Creating the buttons
	btn_lookup = Button(root_lookup, text = "Lookup", command = f_search)
	btn_lookup.grid(row = 1, column = 2, pady = 2, padx = 2)

# Creating the buttons
btn_lookup = Button(frame_lookup, text = "Lookup", command = f_lookup)
btn_lookup.grid(row = 0, column = 2)

# Ending
root_menu.mainloop()