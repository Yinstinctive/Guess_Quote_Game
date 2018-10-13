import requests
from bs4 import BeautifulSoup
from random import choice

mainpage = "http://quotes.toscrape.com/"
all_quotes = []
selected_quote = ""

def get_quote_from_page(page):
	page_num = page
	html = requests.get(f"{mainpage}/page/{page_num}/").text
	soup = BeautifulSoup(html,"html.parser")
	quote_list=soup.find_all(class_="quote")
	quote_scraped = []
	for quote in quote_list:
		text = quote.find(class_="text").get_text()
		author = quote.find(class_="author").get_text()
		about = quote.find("a")["href"]
		quote_scraped.append([text,author,mainpage+about])
	return quote_scraped

def count_pages():
	page_num = 1
	html = requests.get(f"{mainpage}/page/{page_num}/").text
	soup = BeautifulSoup(html, "html.parser")
	while soup.find(class_="next"):
		page_num += 1
		html = requests.get(f"{mainpage}/page/{page_num}/").text
		soup = BeautifulSoup(html, "html.parser")
	return page_num

def gather_all_quotes():
	for i in range(1,count_pages()+1):
		all_quotes.extend(get_quote_from_page(i))

def get_hint(url):
	html = requests.get(url).text
	soup = BeautifulSoup(html,"html.parser")
	born_date = soup.find(class_="author-born-date").get_text()
	born_location = soup.find(class_="author-born-location").get_text()
	return [born_date,born_location]

def play():
	gather_all_quotes()
	continue_game = True
	while continue_game:
		chances = 4
		selected_quote = choice(all_quotes)
		quote_display = selected_quote[0]
		answer = selected_quote[1]
		hint_link = selected_quote[2]
		date_and_location = get_hint(hint_link)
		hint_string = [f"Here's a hint: the author was born in {date_and_location[0]}", 
			f"Here's a hint: the author was born in {date_and_location[1]}", 
			f"Here's a hint: the author's first name start with {answer[0]}"]
		print("Here's a quote: ")
		print(quote_display)
		user_answer = input(f"Who said this? Guesses remaining: {chances}. ")
		hint_index = 0
		while chances>1:
			if user_answer != answer:
				if hint_index<3:
					print(hint_string[hint_index])
				hint_index += 1
				chances -= 1
				user_answer = input(f"Who said this? Guesses remaining: {chances}. ")
			else:
				print("You guessed correctly! Congratulations!")
				break
		play_again = input("Would you like to play again (y/n)? ")
		if play_again == "y":
			continue_game = True
		else:
			continue_game = False
play()


	