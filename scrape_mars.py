# Dependancies
from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd
import pprint

# init the browser before scraping 
def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=True)

def scrape():
    browser = init_browser()
    all_of_mars = {}

    # scrape the news and title 
    url ='https://mars.nasa.gov/news/'
    browser.visit(url)
    
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    all_of_mars["news_title"] = soup.find("div", class_="content_title").a.get_text()

    all_of_mars["news_paragraph"] = soup.find("div", class_="rollover_description_inner").text

    # scraping images
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(3)
    browser.click_link_by_partial_text("more info")
    time.sleep(3)
     
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    png_path = soup.find('figure', class_='lede').find('a').find('img')['src']

    base_url = "https://www.jpl.nasa.gov"
    featured_image_url = base_url + png_path

    all_of_mars["featured_image_url"] = featured_image_url

    # scraping weather results 
    url = "https://twitter.com/marswxreport?lang=en"

    browser.visit(url)   
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    all_of_mars["weather"] = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text.strip().split("hPapic.twitter.com/8SrPjAhpGZ")[0]

    # mars facts 
    url = ('https://space-facts.com/mars/')
    raw_table = pd.read_html(url)
    
    mars_facts_df = raw_table[0]
    mars_facts_df.columns = ['Parameters', 'Values']

    html_mars_table = mars_facts_df.to_html()
    
    all_of_mars["facts"] = html_mars_table
    
    # Scrape the images 
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    hemisphere_image_urls = []
    results = soup.find_all('div', class_ = 'item')

    base_url = 'https://astrogeology.usgs.gov/'
    pprint.PrettyPrinter(indent=4).pprint("results: " + str(results))

    for result in results:
        title = result.find('h3').text
        print(title);
        
        # point to the link for the next page
        link = result.find('a', class_='itemLink')['href']
        
        # need to tell bowser to go to the link
        browser.visit(base_url + link)
        html = browser.html  # reads an html
        soup = BeautifulSoup(html, 'html.parser')
        
        #grabbing the whole img url
        img_url = soup.find('img', class_='wide-image')['src']
        final_url = base_url + img_url
        
        # adding the dictionary to the list
        hemisphere_image_urls.append({'Title':title, "URL": final_url})

    all_of_mars["images"] = hemisphere_image_urls
    print(hemisphere_image_urls)

    return all_of_mars
