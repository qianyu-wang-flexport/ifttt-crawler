import csv
import requests
from BeautifulSoup import BeautifulSoup
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# flag = 1 = collection
# flag = 2 = services
FLAG_COLLECTION = "collection"
FLAG_SERVICES = "services"
FLAG_MAKERS = "makers"


# def load_page_javascript_selenium():
#
# 	option = webdriver.ChromeOptions()
# 	option.add_argument("--incognito")
#
# 	browser = webdriver.Chrome(executable_path='/Users/faysal/PycharmProjects/scrap_ifttt/chromedriver',
# 							   chrome_options=option)
#
# 	browser.get("https://ifttt.com/instagram")
# 	time.sleep(1)
#
# 	elem = browser.find_element_by_tag_name("body")
#
# 	no_of_pagedowns = 50
#
# 	while no_of_pagedowns:
# 		elem.send_keys(Keys.PAGE_DOWN)
# 		time.sleep(1.0)
# 		no_of_pagedowns -= 1
# 		try:
# 			browser.find_element_by_xpath('//*[@id="more"]').click()
# 		except:
# 			print("Finished Loading...")
#
# 	html = browser.page_source
#
# 	soup = BeautifulSoup(html)
# 	main = soup.find('main', {'class': 'container web'})
#
# 	try:
# 		litag = main.find('ul').findAll('li', {'class': 'web-applet-card'})
# 		for tag in litag:
# 			receipe_link = tag.find('a').get('href')
# 			title = tag.find('span', {'class': 'title'})
#
# 			div_content = tag.find('div', {"class": "content"})
# 			by = div_content.find('b').text
# 			div_meta = tag.find('div', {"class": "meta"})
# 			result = div_meta.find('span')
# 			number_of_user = result.text
#
# 			div_works_with = div_meta.find('div', {"class": "works-with"})
# 			try:
# 				works_with = div_works_with.find('img').get('title')
# 			except:
# 				works_with = "Not Present"
#
# 			channel_name = "dummy"
# 			# str = url.split("/")
# 			# if flag == FLAG_COLLECTION:
# 			# 	channel_name = str[4]
# 			# if flag == FLAG_SERVICES:
# 			# 	channel_name = str[3]
# 			# if flag == FLAG_MAKERS:
# 			# 	channel_name = str[4]
#
# 			str = receipe_link.split("/")
# 			receipe = str[4]
# 			write_to_file(channel_name, title.text, receipe, by, works_with, number_of_user)
# 	except:
# 		print("li tag Error")



def most_used_receipe(url, flag):

	option = webdriver.ChromeOptions()
	option.add_argument("--incognito")

	browser = webdriver.Chrome(executable_path='/Users/faysal/PycharmProjects/scrap_ifttt/chromedriver',
							   chrome_options=option)

	browser.get(url)
	time.sleep(1)

	elem = browser.find_element_by_tag_name("body")

	# no_of_pagedowns = 50

	while True:
		elem.send_keys(Keys.PAGE_DOWN)
		time.sleep(1.5)
		# no_of_pagedowns -= 1
		try:
			if flag == FLAG_MAKERS:
				browser.find_element_by_xpath('//*[@class="btn btn-primary"]').click()
			else:
				browser.find_element_by_xpath('//*[@id="more"]').click()
		except:
			print(url+"  Finished Loading...")
			break

	html = browser.page_source


	# response = requests.get(url)
	# html = response.content
	soup = BeautifulSoup(html)
	main = soup.find('main',{'class':'container web'})

	try:
		litag = main.find('ul').findAll('li',{'class':'web-applet-card'})
		for tag in litag:
			receipe_link = tag.find('a').get('href')
			title = tag.find('span',{'class':'title'})

			div_content = tag.find('div',{"class":"content"})
			by = div_content.find('b').text
			div_meta = tag.find('div',{"class":"meta"})
			result = div_meta.find('span')
			number_of_user = result.text

			div_works_with = div_meta.find('div',{"class":"works-with"})
			try:
				works_with = div_works_with.find('img').get('title')
			except:
				works_with = "Not Present"

			str = url.split("/")
			if flag == FLAG_COLLECTION:
				channel_name = str[4]
			if flag == FLAG_SERVICES:
				channel_name = str[3]
			if flag == FLAG_MAKERS:
				channel_name = str[4]

			str = receipe_link.split("/")
			receipe = str[4]
			write_to_file(channel_name, title.text, receipe_link, receipe, by, works_with, number_of_user)
	except:
		print(url+"li tag Error")

	browser.close()


def write_to_file(url, title, receipe_link, receipe, by, works_with, number_user):
	outfile = open("./stat_maker.csv", "a")
	writer = csv.writer(outfile)
	title=title.encode('utf-8')
	by = by.encode('utf-8')
	works_with = works_with.encode('utf-8')
	if "k" in number_user:
		try:
			number_user = float(number_user.replace('k',''))*1000
		except:
			print number_user
	writer.writerow([url,title,receipe_link,receipe,by,works_with,number_user])

def write_to_txt(data):
	out = open('./out.csv','a')
	out.write(data)
	out.flush()
	out.close()

def fetch_collection_url():
	url= 'https://ifttt.com/collections'
	list = []
	response = requests.get(url)
	html = response.content

	soup = BeautifulSoup(html)
	main = soup.find('main',{'class':'container web'})
	litag = main.find('ul').findAll('li',{'class':'collection-tile'})

	for tag in litag:
			anchortag = tag.find('a')
			list.append('https://ifttt.com'+ anchortag.get('href'))

	return list


def fetch_services_url():
	url = 'https://ifttt.com/search/services'
	list = []

	response = requests.get(url)
	html = response.content

	soup = BeautifulSoup(html)
	main = soup.find('main', {'class': 'container web'})
	litag = main.find('ul').findAll('li', {'class': 'service-tile'})

	for tag in litag:
		anchortag = tag.find('a')
		list.append('https://ifttt.com' + anchortag.get('href'))


	return list


def get_most_used_receipe_by_channel():

	url_list = fetch_services_url()
	for url in url_list:
		most_used_receipe(url, FLAG_SERVICES)


	# url_list = {'https://ifttt.com/augusthome','https://ifttt.com/hc_oven'}
	# for url in url_list:
	# 	most_used_receipe(url, FLAG_SERVICES)

	# url_list = fetch_collection_url()
	# for url in url_list:
	# 	most_used_receipe(url, FLAG_COLLECTION)

	# url_list = {'https://ifttt.com/p/nest'}
	# for url in url_list:
	# 	most_used_receipe(url, FLAG_MAKERS)

	#url_list = "https://ifttt.com/makers"
	#most_used_receipe(url_list, FLAG_MAKERS)


if __name__ == "__main__":
	# url = 'https://ifttt.com/amazon_alexa'
	# url_list = {'https://ifttt.com/collections/google', 'https://ifttt.com/amazon_alexa','https://ifttt.com/collections/ios','https://ifttt.com/collections/android'}




	get_most_used_receipe_by_channel()
	# load_page_javascript_selenium()



# install = ultag.findAll('div',{'class':'installs'})

# litag = ultag.find_all('li')

# print(litag)


# for litag in ultag.find_all('li'):
# 		print litag.text

# print ul

# list_of_rows = []
# for row in table.findAll('tr')[1:]:
#     list_of_cells = []
#     for cell in row.findAll('td'):
#         text = cell.text.replace('&nbsp;', '')
#         list_of_cells.append(text)
#     list_of_rows.append(list_of_cells)

# outfile = open("./inmates.csv", "wb")
# writer = csv.writer(outfile)
# writer.writerow(["Last", "First", "Middle", "Gender", "Race", "Age", "City", "State"])
# writer.writerows(list_of_rows)



# for div in soup.findAll('div', attrs={'class':'image'}):
#     print div.find('a')['href']
#     print div.find('a').contents[0]
#     print div.find('img')['src']


