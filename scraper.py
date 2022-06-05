# Importing all the required liverraies
import bs4
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from . import parse, get_info

# Main amazon url for scraping
url ="https://www.amazon.in/gp/bestsellers/?ref_=nav_cs_bestsellers"

HEADERS ={"User-Agent":"CHrome/Version 101.0.4951.67 (Official Build) (64-bit)", 
    "Accept-Encoding":"gzip, deflate", 
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
    "DNT":"1","Connection":"close", 
    "Upgrade-Insecure-Requests":"1"}

# Now we downloading the page 
response = requests.get(url, headers=HEADERS)

# Here we are saving the content to a file 
"""with open("amazon.html","w") as f:
    f.write(response.text)"""

# we now reading our html file and printing the first 500 characters
with open("amazon.html","r") as f:
    html_content = f.read()
# html_content[0:500]

# Parsing the web page information 
content = bs(html_content, "html.parser")
type(content) # bs4.BeautifulSoup

# Now we are accessing the parent's tag and finding all information 
doc = content.find("div", class_ ="_p13n-zg-nav-tree-all_style_zg-browse-group__88fbz")
hearder_link_tags = doc.find_all("div", role = 'treeitem')

############## finding and geting different item categories description and Url 
topics_link = []
for tag in hearder_link_tags[0:]:
        topics_link.append({
        "title": tag.text.strip(),
        "url": "https://www.amazon.in" + tag.find("a")["href"] })
################# stored in dictionary
table_topics = { k:[ d.get(k) for d in topics_link]
                   for k in set().union(*topics_link)}
# It returns variety of 62 categories.

all_arcticle_tag, all_topics_description, all_topics_url = parse(table_topics, 2)
# This returns Categories description and url with its tags

# We successfully downloaded 55 out of 62 pages.

##### This function will return all the product data
data = get_info(all_arcticle_tag, all_topics_description, all_topics_url)

Scrape_data = pd.DataFrame(data)
Scrape_data.shape # (1650, 8) 

# Now storing the Scrape_data  into CSV file 
Scrape_data.to_csv('AmazonBestProduct.csv', index=None)
