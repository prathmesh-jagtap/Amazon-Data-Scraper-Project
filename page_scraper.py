# This file contain all the function which is 
# used to scrape the data form amazon website
from bs4 import BeautifulSoup as bs
import requests
import time

def fetch(url):
    ''' The function take url and headers to download and parse the page using request.get and BeautifulSoup library
    it return a parent tag of type BeautifulSoup object
    
    Argument:
    -url(string): web page url to be downloaded and parse
    
    Return:
    -doc(Beautiful 0bject): it's the parent tag containing the information that we need parsed from the page'''
    HEADERS= {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
    response = requests.get(url, headers= HEADERS)
    if response.status_code != 200:
        print("Status code:", response.status_code)
        raise Exception("Failed to link to web page\t " + url)
    page_content  = bs(response.text, "html.parser")
    doc = page_content.findAll('div', attrs={'id':'gridItemRoot'})
    return doc

def parse_page(table_topics, pageNo):
    """The function take all topic categories and number of page to parse for each topic as input, apply get request to download each
    page, the use Beautifulsoup to parse the page. the function output are article_tags list containing all pages content, t_description
    list containing correspponding topic or categories then an url list for corresponding Url.
    
    Argument:
    -table_topics(dict): dictionary containing topic description and url
    -pageNo(int): number of page to parse per topic
    
    Return:
    -article_tags(list): list containing successfully parsed pages content where each index is a Beautifulsoup type
    -t_description(list): list containing  successfully parsed topic description
    -t_url(list): list containing successfully parsed page topic url
    -fail_tags(list): list containing pages url that failed first parsing 
    -failed_topic(list): list contaning pages topic description that failed first parsing
    """
    article_tags, t_description, t_url, fail_tags, failed_topic =[], [], [], [], []
    for i in range(0,len(table_topics["url"])):
         # take the url
        topic_url = table_topics["url"][i]
        topics_description =  table_topics["title"][i]
        try:
            for j in range(1, pageNo+1):
                ref = topic_url.find("ref")
                url = topic_url[:ref]+"ref=zg_bs_pg_"+str(j)+"?ie=UTF8&pg="+str(j)
                time.sleep(10)
                #use resquest to obtain HMTL page content
                doc = fetch(url)
                if len(doc)==0:
                    print("failed to parse page - {}".format(url))
                    fail_tags.append(url)
                    failed_topic.append(topics_description)
                else:
                    print("Sucsessfully parse:",url)
                    article_tags.append(doc)
                    t_description.append(topics_description)
                    t_url.append(topic_url) 
        except Exception as e:
            print(e)
    return article_tags,t_description,t_url,fail_tags,failed_topic

def reparse_failed_page(fail_page_url,failed_topic):
    """The function take topic categories url, and description that failed to be accessible due to captcha in the first parsing process,
     try to fetch and parse thoses page for a second time.the function return article_tags list containing all pages content, topic_description, 
     topic_url and other pages url and topic that failed to load content again.
    
    Argument:
    -fail_page_url(dict): list containing failed first parsing web page url 
    -failed_topic(int): list contaning failed first parsing ictionary containing topic description and url
    
    Return:
    -article_tags2(list): list containing successfully parsed pages content where each index is a Beautifulsoup type
    -t_description(list): list containing  successfully parsed topic description
    -t_url(list): list containing successfully parsed page topic url
    -fail_p(list): list containing pages url that failed again 
    -fail_t(list): list contaning pages topic description that failed gain 
    """
    print("check if there is any failed pages, then print number:", len(fail_page_url))
    article_tag2, topic_url, topic_d, fail_p, fail_t = [],[],[],[],[]
    try:
        for i in range(len(fail_page_url)):
            time.sleep(20)
            doc = fetch(fail_page_url[i])
            if len(doc)==0:
                print("page {} failed again".format(fail_page_url[i]))
                fail_p.append(fail_page_url[i])
                fail_t.append(failed_topic[i])
            else:
                article_tag2.append(doc)
                topic_url.append(fail_page_url[i])
                topic_d.append(failed_topic[i])
    except Exception as e:
        print(e)
    return article_tag2,topic_d,topic_url,fail_p,fail_t

def parse(table_topics, pageNo):
    """The function take table_topics, and number of page to parse for ecah topic url, the main purpose of this funtion is 
     to realize a double attempt to parse maximum number of pages it can. It's a combination of result getting from first 
     and second parse.
     
     Argument
     -table_topics(dict): dictionary containing topic description and url
     -pageNo(int): number of page to parse per topic
     
     Return:
     -all_arcticle_tag(list): list containing all successfully parsed pages content where each index is a Beautifulsoup type
     -all_topics_description(list): list containing  all successfully parsed topic description
     -all_topics_url(list): list containing all successfully parsed page topic url
    """
    article_tags, t_description, t_url, fail_tags, failed_topic = parse_page(table_topics, pageNo)

    if len(fail_tags)!=0:
        article_tags2, t_description2, t_url2, fail_tags2, failed_topic2 = reparse_failed_page(fail_tags, failed_topic)
        all_arcticle_tag = [*article_tags, *article_tags2]
        all_topics_description = [*t_description, *t_description2]
        all_topics_url = [*t_url,*t_url2]
        #return all_arcticle_tag,all_topics_description,all_topics_url
    else:
        print("successfully parsed all pages")
        all_arcticle_tag = article_tags
        all_topics_description = t_description
        all_topics_url = t_url
       # return article_tags,t_description,t_url,fail_tags,failed_topic
    return all_arcticle_tag, all_topics_description, all_topics_url

