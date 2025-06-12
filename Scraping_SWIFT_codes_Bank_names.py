import os
import bs4
import requests
import pandas as pd

def table_to_df(table):
	return pd.DataFrame([[td.text for td in row.findAll('td')] for row in table.tbody.findAll('tr')])

def next_page(soup):
	next_link = soup.find('a', attrs={'rel':'next'})
	if next_link:
		return "http:" + next_link.get('href')
	return None

res = []
url = "http://bank-code.net/country/FRANCE-%28FR%29/"
counter = 0

while True:
	print(counter)
	try:
		page = requests.get(url)
		soup = bs4.BeautifulSoup(page.content, 'lxml')
		table = soup.find(name='table', attrs={'id':'tableID'})
		if table:
			res.append(table_to_df(table))
		
		next_url = next_page(soup)
		if not next_url:
			break
		url = next_url
		counter += 1
	except Exception as e:
		print(f"Error processing page {counter}: {e}")
		break

final_df = pd.concat(res, ignore_index=True)
final_df.to_csv("table.csv", index=False, sep=';', encoding='iso-8859-1')
