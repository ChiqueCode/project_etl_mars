# Dependancies
from splinter import Browser
from bs4 import BeautifulSoup
import time

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
    
    return all_of_mars
