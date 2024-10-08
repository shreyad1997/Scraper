# -*- coding: utf-8 -*-
"""Programming Project

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1d1-DShI64bVYlKmMARq8RhbkAtjWYKWc
"""



# #Change these keywords
# #Each keyword generates a separate csv file

# keywords = ["data analysis", "business analyst"]


# for objKey in keywords:
#   convertToCSV(objKey)

import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the function to check if a value exists in a map and return it
def checkValandReturn(mapDescription, stringCheck):
    return mapDescription.get(stringCheck, "N/A")

# Define the function to convert data to CSV
def convertToCSV(keyword):
    index = 0
    article_list = []
    session = requests.Session()  # Use session for better performance and handling of persistent connections

    while True:
        url = f"https://www.upwork.com/ab/feed/jobs/rss?q={keyword}&sort=recency&user_location_match=1&paging={index}%3B10&api_params=1&securityToken=YOUR_SECURITY_TOKEN&userUid=YOUR_USER_UID&orgUid=YOUR_ORG_UID"
        try:
            response = session.get(url)
            response.raise_for_status()  # Check for HTTP request errors
            soup = BeautifulSoup(response.content, features='xml')
            articles = soup.findAll('item')

            if not articles:  # Exit the loop if no articles found
                break

            for a in articles:
                link = a.find('link').text
                title = a.find('title').text
                published = a.find('pubDate').text
                description = a.find('description').text
                description_cleaned = BeautifulSoup(description, "lxml").text
                mapDescription = {}

                # Cleaning and splitting the description content
                listItems = description.split('<b>')
                for item in listItems:
                    item = BeautifulSoup(item, "lxml").text
                    separatedObj = item.split(':')
                    if len(separatedObj) > 1:
                        mapDescription[separatedObj[0].strip()] = separatedObj[1].strip()

                article = {
                    'title': title,
                    'link': link,
                    'Date': published,
                    'Description': description_cleaned,
                    'Hourly_Range': checkValandReturn(mapDescription, "Hourly Range"),
                    'Category': checkValandReturn(mapDescription, "Category"),
                    'Skills': checkValandReturn(mapDescription, "Skills")
                }
                article_list.append(article)

            index += 10
        except requests.RequestException as e:
            print(f"Request error: {e}")
            break

    # Create dataframe and save to CSV
    if article_list:
        df = pd.DataFrame(article_list, columns=['title', 'link', 'Date', 'Description', 'Hourly_Range', 'Skills', 'Category'])
        df.to_csv(f'Upwork_Scraping_{keyword}.csv', index=False, encoding='utf-8')
    else:
        print(f"No articles found for keyword: {keyword}")

# Example usage
keywords = ["data"]

for objKey in keywords:
    convertToCSV(objKey)













"""# New section"""