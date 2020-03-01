# ## Web Scraping Homework - Mission to Mars

#Import Dependancies
from splinter import Browser
import pymongo
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time
import re


def init_browser():
    executable_path = {'executable_path': '/Users/tmill/Downloads/chromedriver_win32/chromedriver.exe'}
    return Browser ('chrome', **executable_path, headless=False)

def scrape_info():
    browser = init_browser()
 
    mars_data = {}

# ### Nasa Mars News
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(5)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    articles = soup.find("div", class_="list_text")

    news_title = articles.find("div", class_="content_title").text
    print(news_title)

    news_p = articles.find("div", class_ ="article_teaser_body").text
    print(news_p)

    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p

    

    # ### JPL Mars Space Images
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

    time.sleep(3)

    image_html = browser.html
    image_soup = BeautifulSoup(image_html, 'html.parser')    

    image = image_soup.find("article", attrs={"class":"carousel_item"})
    image_string = image["style"]
    image_link = re.findall(r"'(.*?)'",image_string)
    featured_image_url = "https://www.jpl.nasa.gov" + image_link[0]
    print(featured_image_url)

    mars_data["featured_image_url"] = featured_image_url

      

    # ### Mars Weather
    driver = webdriver.Chrome()
    weather_url = "https://twitter.com/marswxreport?lang=en"
    driver.get(weather_url)
    time.sleep(5)

    body = driver.find_element_by_tag_name("body")
    body.send_keys(Keys.PAGE_DOWN)

    weather_html = driver.page_source
    weather_soup = BeautifulSoup(weather_html,"html.parser")

    weather = weather_soup.find_all(class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")
    for tweet in weather:
        if tweet.text.split(" ")[0] == "InSight":
            mars_weather = tweet.text 
            break
    print(mars_weather)

    mars_data["mars_weather"] = mars_weather

    

    # ### Mars Facts
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)

    time.sleep(3)

    data = pd.read_html(facts_url)
    data = pd.DataFrame(data[0])
    mars_facts = data.to_html(header = False, index = False)
    print(mars_facts)

    mars_data["mars_facts"] = mars_facts

    
    

    # ### Mars Hemispheres
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)

    time.sleep(3)

    hemi_html = browser.html
    hemi_soup = BeautifulSoup(hemi_html,"html.parser")


    hemisphere_image_urls = []
    hemi_dict = {"title": [], "img_url": []}

    products = hemi_soup.find("div", class_="result-list")
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        link = hemisphere.find("img", class_="thumb")["src"]
        im_link = "https://astrogeology.usgs.gov" + link
        hemi_dict = {"title": title, "image_url":im_link}
        hemisphere_image_urls.append(hemi_dict)
        
    print(hemisphere_image_urls)

    mars_data["hemisphere_image_urls"] = hemisphere_image_urls

# Close the browser after scraping
    browser.quit()
    driver.quit()
    # Return results
    return mars_data
