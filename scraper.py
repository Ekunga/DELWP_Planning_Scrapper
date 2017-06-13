#############
#  Scraper to pull data from Department of Environment, Land, Water and Planning
#
#	 https://www2.delwp.vic.gov.au/
#   
#    Found at;
#    https://lodgement.planning-permits.delwp.vic.gov.au/
#
#
#############

#!/usr/bin/env python
# -*- coding: utf-8 -*-


import scraperwiki
from lxml import html, etree
from datetime import datetime
import requests
import cx_Oracle 

sub_url = 'https://lodgement.planning-permits.delwp.vic.gov.au'
url = 'https://lodgement.planning-permits.delwp.vic.gov.au/search-register'
global item_ref
item_ref = []
global item
item = []
global debug
debug= 'false'
global max_pages
max_pages = 32
global sql_query
sql_query = []
global column_names
columns_names = []
global column_values
column_values = []
global exit
exit = 'false'

item_ref.append(['Application','//span[@class="app-name"]/a/text()'])
item_ref.append(['Application_Link','//span[@class="app-name"]/a/@href'])
item_ref.append(['Created','//td[@data-label="Created"]/div/text()'])
item_ref.append(['Description','//td[@data-label="Description"]/div/text()'])
item_ref.append(['Properties','//td[@data-label="Properties"]/div/text()'])
item_ref.append(['Status','//td[@data-label="Status"]/div/text()'])

if debug == 'true': print(item_ref)

if debug == 'true': print(len(item_ref))

page_scrape = 1
while page_scrape <= max_pages:
	url = ''.join(['https://lodgement.planning-permits.delwp.vic.gov.au/search-register?page=',str(page_scrape)])
	item = []
	if debug == 'true': print(url)
	page = requests.get(url)
	page_details = html.fromstring(page.content)

	#Scrape Data
	item_to_scrape = 0
	while item_to_scrape < len(item_ref):
		item.append([item_ref[item_to_scrape][0],page_details.xpath(item_ref[item_to_scrape][1])])
		if debug == 'true': print('Item Name:',item[item_to_scrape][0])
		if debug == 'true': print('Item:',item[item_to_scrape][1][0])
		item_to_scrape = item_to_scrape + 1

	if debug == 'true': print('Number of Records:',len(item[0][1]))

	item_to_scrape = 0
	item_to_display = 0

	#Loops through each Item and displays all Data
	while item_to_display < len(item[0][1]):

		if debug == 'true': print('Next Record')
		column_names = []
		column_values = []
		while item_to_scrape < len(item_ref):


			value = item[item_to_scrape][1][item_to_display]

			value = value.splitlines()
			value = ' '.join(value)

			column_names.append(item[item_to_scrape][0])



# Checks if Application currently exists
			if (item[item_to_scrape][0] == 'Application'):
				sql = "Select Distinct Application from data where Application ='"+str(value)+"'"
				#print(sql)
				scraperwiki.sql.execute(sql)

				for row in cur:
					print('All Complete')
					exit = 'true' 
					item_to_scrape = len(item_ref)
					item_to_display = len(item[0][1]) + 1
					page_scrape = max_pages + 1

			if exit == 'false':
				if item[item_to_scrape][0] == 'Application_Link': 
					fixed_value = ''.join([sub_url,value.strip()])
				else: 
					fixed_value = value.strip()
				fixed_value = fixed_value.replace("'","''")
				
				fixed_value = fixed_value.replace("&","\&")
				

				column_values.append(fixed_value)

			item_to_scrape = item_to_scrape + 1


# Inserts Data

		if  exit =='false':
			column_name = 0
			sql_part_1 = "Insert into data ("
			sql_part_2 = ','.join(column_names)
			sql_part_3 = ") Values ('"
			sql_part_4 = "','".join(column_values)
			sql_part_5 = "')"
			sql 

			scraperwiki.sql.execute(str)

			sql = ''.join([sql_part_1,sql_part_2,sql_part_3,sql_part_4,sql_part_5])
			scraperwiki.sql.execute(sql)


		item_to_scrape = 0
		item_to_display = item_to_display + 1
	page_scrape = page_scrape + 1

