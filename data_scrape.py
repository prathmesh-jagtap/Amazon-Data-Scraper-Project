# This file contains all the actions to scrape data of 
# individual products and is stored in a CSV file.

def get_topic_url_item_description(doc, topic_description, topic_url):
    """The funtion takes a parent tag attribute, topic description and topic url as input, after finding the item name tags,
    the function return the item name(description), his corresponding topic(category) and his category url
    
    Argument:
    -doc(BeautifulSoup element): parents tag
    -topic_description(string): topic name or category
    -topic_url(string): topic url
    
    Return:
    -item_description(string): item name
    -topic_description(string):corresponding topic
    - topic_url(string): corresponding topic url
    """

    name = doc.find("div", attrs={'class':'_cDEzb_p13n-sc-css-line-clamp-3_g3dy1'})
    try:
        item_description = name.get_text()
    except:
        item_description = 'no Description'
    return item_description, topic_description, topic_url  

def get_item_price(d):
    """The function take a parent tag attribute as input and find for corresponding child tag(item price),
    then return maximum price and minimum price for corresponding item and 0 when no price is found
    
    Argument:
    -d(BeautifulSoup element): parent tag
    
    Return:
    -min_price(float): item minimum price
    -max_price(float): item maximum price
    """
    p = d.find("span", attrs={"class":"a-size-base a-color-price"})
    try :
        if "-" in p.text :
            min_price = float(((p.text).split("-")[0]).replace("₹",""))
            max_price = float((((p.text).split("-")[1]).replace(",","")).replace("₹",""))
        else :
            min_price = float(((p.text[:5]).replace(",","")).strip().replace("₹",""))
            max_price = 0.0
    except:
        min_price = 0.0
        max_price = 0.0
    return min_price, max_price

def get_item_rate(d):
    """The function take a parent tag attribute as input and find for corresponding child tag(rate),
    then return item rating out of 5, and 0.0 when can't find a rate
    
    Argument:
    -d(BeautifulSoup element): parent tag
    
    Return:
    -rating(float): item rating out or 5
    """
    rate = d.find("span", attrs={"class":"a-icon-alt"})
    try :
        rating = float(rate.text[:3])
    except:
        rating = 0.0
    return rating

def get_item_review(d):
    """The function take a parent tag attribute as input and find for corresponding child tag(costumers review),
    then return item review, and 0 when can't find number  of review
    
    Argument:
    -d(BeautifulSoup element): parent tag
    
    Return:
    -review(float): item costumer review
    """
    review = d.find("span", attrs ={"class":"a-size-small"})
    try :
        review = int((review.text).replace(",",""))
    except:
        review = 0
    return review

def get_item_url(d):
    """The function take a parent tag attribute as input and find for corresponding child tag(image),
    then return item image url, and 'no image' if can't find an image
    
    Argument:
    -d(BeautifulSoup element): parent tag
    
    Return:
    -img(float): item image url
    """
    url = d.find("a", attrs ={"class":"a-link-normal"})
    try:
        item_url = "https://www.amazon.in" + url.get('href')
    except:
        item_url = 'No image'
    return item_url

def get_info(article_tags,t_description,t_url):
    """The function take a list of pages content which each index is a Beautiful element that will be use to find parent 
    tag, list of topic description and topic url then the return a dictionary made of list of each item information data 
    such as: his corresponding topic, the topic url, the item description, minimum price(maximum price if exist), 
    item rating, costumer review, and item_url
    
    Argument:
    -article_tags(list): list containing all pages content where each index is a Beautifulsoup type
    -t_description(list): list containing  topic description
    -t_url(list): list containing topic url
    
    Return:
    -dictionary(dict): dictionary containing all item information data taken from each parse page topic
    """
    topic_description, topics_url, item, item_url = [],[],[],[]
    minimum_price, maximum_price, rating, costuomer_review = [],[],[],[]
    
    for idx in range(0,len(article_tags)):
        doc = article_tags[idx]#.findAll('div', attrs={'id':'zg-right-col'})
        for d in doc :
            names, topic_name, topic_url = get_topic_url_item_description(d, t_description[idx], t_url[idx])
            min_price, max_price = get_item_price(d)
            rate = get_item_rate(d)
            review = get_item_review(d)
            url = get_item_url(d)
            ####put each item data inside corresponding list
            item.append(names)
            topic_description.append(topic_name)
            topics_url.append(topic_url)
            minimum_price.append(min_price)
            maximum_price.append(max_price)
            rating.append(rate)
            costuomer_review.append(review)
            item_url.append(url)
    return {
           "Category": topic_description,
           "Category Url": topics_url,
           "Product Description": item,
           "Rating out of 5": rating,
           "Minimum_price": minimum_price,
           "Maximum_price": maximum_price,
           "Review" :costuomer_review,
           "Product Url" : item_url}
