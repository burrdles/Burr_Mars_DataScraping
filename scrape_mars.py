# Dependencies
from bs4 import BeautifulSoup
import requests
import urllib.request
import pymongo
from splinter import Browser
import pandas as pd

mars_data = {}

def init_browser():
   # @NOTE: Replace the path with your actual path to the chromedriver
   executable_path = {"executable_path": "chromedriver.exe"}
   return Browser("chrome", **executable_path, headless=False)

def scrape_news():
   
   try:
      browser = init_browser()

      # **SCRAPE MARS NEWS**
      #NASA Mars News Website
      news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
      browser.visit(news_url)

      #Parse HTML
      news_html = browser.html
      soup = BeautifulSoup(news_html, 'html.parser')

      #News Title
      mars_data['news_title'] = soup.find('div', class_='bottom_gradient').text
      #News Teaser Senter
      mars_data['news_teaser'] = soup.find('div', class_='article_teaser_body').text

      return mars_data
   
   finally: 
      browser.quit()

def scrape_image():
   # **SCRAPE MARS FEATURED IMAGE**

   try:
      browser = init_browser()

      #JPL Mars Space Image website
      mars_img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
      browser.visit(mars_img_url)

      #Set up Main URL
      jpl_url = 'https://www.jpl.nasa.gov'

      #Parse HTML
      html = browser.html
      soup = BeautifulSoup(html, 'html.parser')
      
      #retrieve partial url for full image
      results = soup.find('article')['style']
      mars_image = results.replace('background-image: url(','').replace( ');', '')[1:-1]

      featured_url = jpl_url + mars_image
      
      # Display full link to featured image        
      featured_url 
      
      # Dictionary entry from FEATURED IMAGE       
      mars_data['featured_url'] = featured_url 

      return mars_data
   
   finally: 
      browser.quit()

def scrape_weather():
       
      # Twitter with Mars weather updates
      weather_url = 'https://twitter.com/marswxreport?lang=en'

      # Retrieve page with the requests module
      response = requests.get(weather_url)
      # Parse HTML
      soup = BeautifulSoup(response.text, 'html.parser')

      #Retrieve most recent weather facts and save to dictionary
      mars_weather = soup.find('p', class_='TweetTextSize').text
      mars_data['mars_weather'] = mars_weather

      return mars_data

def scrape_facts():
   
   # Twitter with Mars weather updates
   #URL with Mars Facts Table
   facts_url = 'https://space-facts.com/mars/'

   #Read tables form website
   tables = pd.read_html(facts_url)

   #Creat Dataframe of Mars Table
   df = tables[1]

   #Map Column Names
   mars_df = df[[0, 1]]
   mapping = {0: "Description", 1: "Value"}
   mars_df = mars_df.rename(columns=mapping)

   #Save Dataframe as HTML
   mars_facts = mars_df.to_html(classes = 'table table-striped')
   mars_data['mars_facts'] = mars_facts
    
   return mars_data

def scrape_hemispheres():
      
   try:
      browser = init_browser()

      hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
      browser.visit(hemisphere_url)

      html = browser.html
      soup = BeautifulSoup(html, 'html.parser')

      #Set up main URL
      usgs_url = 'https://astrogeology.usgs.gov'

      #Locate all images
      images = soup.find_all('div', class_='item')

      #Creat Lists to store dictionary of image titles and image urls
      img_info = []

      for image in images:
         # Store title     
         img_title = image.find('h3').text 
         
         #For each image, pull Partial URL for Image 
         #partial href
         partial_href = image.find('a')['href']

         #Set up Image URL to visit
         browser.visit(usgs_url + partial_href)
         visit_img_html = browser.html

         # Parse HTML and retrieve full image source  
         soup = BeautifulSoup(visit_img_html, 'html.parser')
         img_url = usgs_url + soup.find('img', class_='wide-image')['src']

         # Create Dictionary from lists
         img_info.append({'img_title': img_title, 'img_url': img_url})

      mars_data['img_info'] = img_info
      return mars_data

   finally:
      browser.quit()
      