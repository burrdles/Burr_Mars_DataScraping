    # SCRAPE MARS FEATURED IMAGE
    #JPL Mars Space Image website
    mars_img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(mars_img_url)

    #Set up Main URL
    jpl_url = 'https://www.jpl.nasa.gov'

    #Parse HTML
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    browser.visit(mars_img_url)
    browser.click_link_by_partial_text('FULL IMAGE')

    #Parse through html
    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')

    #retrieve partial url for full image
    mars_image = image_soup.find('img', class_='fancybox-image')['src']
    mars_data['featured_url'] = jpl_url + mars_image


    # SCRAPE MARS WEATHER
    # Twitter with Mars weather updates
    weather_url = 'https://twitter.com/marswxreport?lang=en'

    # Retrieve page with the requests module
    response = requests.get(weather_url)
    # Parse HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    #Retrieve most recent weather facts
    mars_data['mars_weather'] = soup.find('p', class_='TweetTextSize').text

    # SCRAPE MARS FACTS TABLE
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
    mars_df.to_html('mars_fact_table.html', index = None)

    # SCRAPE MARS HEMISPHERE IMAGES
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
        img_info.append({'Title': img_title, 'Image_URL': img_url})