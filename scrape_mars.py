from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo 
import datetime
import time
from pprint import pprint
  
def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)
    mars_mission_dict = dict()

    ### NASA Mars News
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    html = browser.html 
    news_soup = BeautifulSoup(html, 'html.parser')
    try :
        news_title = news_soup.find('ul', class_="item_list").find('li',class_="slide").find('div',class_="content_title").text
        #print(news_title) 
        news_p = news_soup.find('ul',class_="item_list").find('li',class_="slide").find('div',class_="article_teaser_body").text
        #print(news_p)

    except  AttributeError as error:
        print(error)    

    mars_news_dict = dict()
    mars_news_dict["Mars_news_title"] = news_title
    mars_news_dict["Mars_news_p"] = news_p
    #pprint(mars_news_dict)
    
    
    ### JPL Mars Space Images - Featured Image
    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(featured_image_url)
    featured_image = browser.find_by_id('full_image')
    featured_image.click()
    mars_image_html = browser.html
    #print(full_img_html)
    mars_image_soup = BeautifulSoup(mars_image_html, "html.parser")
    featured_image_title = mars_image_soup.find(class_='media_feature_title').text
    mars_image_href = mars_image_soup.find(class_='carousel_item').a['data-fancybox-href']
    featured_image_url = "https://www.jpl.nasa.gov" + mars_image_href
    #print(featured_image_title)
    #print(featured_image_url)

    mars_feature_dict = dict()
    mars_feature_dict["Mars_featured_image_title"] = featured_image_title
    mars_feature_dict["Mars_featured_image_url"] = featured_image_url
    #pprint(mars_feature_dict)

    ### Mars Weather
    time.sleep(10)
    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_weather_url)
    mars_weather_html = browser.html
    mars_weather_soup = BeautifulSoup(mars_weather_html, 'html.parser')
    mars_weather_tweet = mars_weather_soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    #pprint(mars_weather_tweet)

    mars_weather_dict = dict()
    mars_weather_dict["Mars_weather_tweet"] = mars_weather_tweet
    #pprint(mars_weather_dict)

    ### Mars Facts
    mars_facts_url = "http://space-facts.com/mars/"
    mars_facts_df = pd.read_html(mars_facts_url)
    mars_factstable_df = mars_facts_df[0]
    #mars_factstable_df.columns = ['Fact', 'Value']
    #pprint(mars_factstable_df)

    #mars_factstable_df.set_index("Fact")
    #mars_factstable_df.to_html("templates/mars_facts.html", index=False)
    mars_facts_html = mars_factstable_df.to_html("templates/mars_facts.html", classes="mars_facts table")
    mars_facts_dict = dict()
    mars_facts_dict["Mars_facts_table"] = mars_facts_html
    #pprint(mars_facts_dict)

    ### Mars Hemispheres
    mars_hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    hemisphere_images_urls = []
    browser.visit(mars_hemispheres_url)
    time.sleep(10)
    mars_hemispheres_html = browser.html
    mars_hemispheres_soup = BeautifulSoup(mars_hemispheres_html, "html.parser")
    #print(mars_hemispheres_soup)
    mars_hemispheres_response = mars_hemispheres_soup.find('div', class_="collapsible results")
    hemispheres_response_items = mars_hemispheres_response.find_all('div',class_='item')
    for h in hemispheres_response_items:
        response_item_title = h.h3.text
        #print(response_item_title)
        response_item_url  = "https://astrogeology.usgs.gov" + h.find('a',class_='itemLink product-item')['href']
        #print(response_item_url)
        browser.visit(response_item_url)
        response_item_html = browser.html
        response_item_soup = BeautifulSoup(response_item_html, 'html.parser')
        hemisphere_image_url = response_item_soup.find('div', class_='downloads').find('li').a['href']
        #print(hemisphere_image_url)
        mars_hemisphere_dict = dict()
        mars_hemisphere_dict['title'] = response_item_title
        mars_hemisphere_dict['img_url'] = hemisphere_image_url
        hemisphere_images_urls.append(mars_hemisphere_dict)
    #hemisphere_images_urls

    mars_hemispheres_dict = dict()
    mars_hemispheres_dict["Hemisphere_image_urls"] = hemisphere_images_urls
    #mars_hemispheres_dict

    ### Mars Mission Dictionary
    mars_mission_dict =  {
        "News_Title": news_title,
        "News_Summary" : news_p,
        "Featured_Image_Title" : featured_image_title,
        "Featured_Image_url" : featured_image_url,
        "Weather_Tweet" : mars_weather_tweet,
        "Facts" : mars_facts_html,
        "Hemisphere_Image_urls": hemisphere_images_urls
    }
    return mars_mission_dict
