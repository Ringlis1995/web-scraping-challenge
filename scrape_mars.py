from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd 

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    listings = {}

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")
    slide_element = news_soup.select_one("ul.item_list li.slide")   

    news_title = slide_element.find("div", class_="content_title").get_text()
    listings ["news_title"] = news_title
    
    news_p = slide_element.find("div", class_="article_teaser_body").get_text()
    listings ["news_p"] = news_p


    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    fullimage = browser.find_by_id("full_image")
    fullimage.click()
    moreinfo = browser.links.find_by_partial_text("more info")
    moreinfo.click()
    image_soup = BeautifulSoup(browser.html, "html.parser")
    full_image_element = image_soup.select_one(".main_image").get("src")
    full_image_element
    image_url = f"https://www.jpl.nasa.gov{full_image_element}"
    listings ["image_url"] = image_url

    mars_facts_df = pd.read_html("https://space-facts.com/mars/")[0]
    mars_facts_df
    mars_facts_df.columns=["Description", "Mars"]
    mars_facts_df.set_index("Description", inplace=True)
    mars_facts_df
    listings ["mars_facts"] = mars_facts_df.to_html()

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    links = browser.find_by_css("a.product-item h3")
    hemisphere_image_urls = []

    for i in range (len(links)):
        hemisphere = {}
        browser.find_by_css("a.product-item h3")[i].click()
        element = browser.links.find_by_text("Sample").first
        hemisphere["img_url"] = element["href"]
        hemisphere["title"] = browser.find_by_css("h2.title").text
        hemisphere_image_urls.append(hemisphere)
        browser.back()

    listings ["hemisphere_image_urls"] = hemisphere_image_urls

    return listings