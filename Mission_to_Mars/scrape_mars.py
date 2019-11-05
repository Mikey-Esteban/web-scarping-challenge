# Import Dependencies to web scrape
import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser


# function to set up chromedriver for scrape
def use_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

# RUN WEB SCRAPER
def scrape():
    browser = use_browser()

    # Dictionary for scraped data
    mars_data = {}

###############
##########  NEWS
###############

    # url of page to be scraped
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)

    # set an html object to be used by BeautifulSoup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # save the latest title and paragraph text
    news_title = soup.find('div', class_='content_title').text
    news_p_text = soup.find('div', class_='article_teaser_body').text

    # Add news data to mars dictionary
    mars_data['news_title'] = news_title
    mars_data['news_info'] = news_p_text

###############
##########  FEATURED IMAGE
###############

    # Visit JPL Mars Space Image site
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    main_site = 'https://www.jpl.nasa.gov'
    browser.visit(url2)

    # Scrape the browser into a BeautifulSoup object and use BS to find the image of mars
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # find all imgs
    images = soup.find_all('img', class_='thumb')

    # loop to find alt='Insight', then pull out the corresponding src
    for image in images:
        if image['alt'] == 'InSight':
            url = image['src']

    # Add src to rest of http
    featured_image_url = main_site + url

    # Add img url to mars dictionary
    mars_data['featured_image_url'] = featured_image_url

###############
##########  TWITTER
###############

    # Visit Mars Weather Twitter Account
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)

    # Scrape the browser into a BeautifulSoup object and use BS to find the image of mars
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find the latest tweet
    # take away new lines and the pic info text
    tweet = soup.find('p', class_='TweetTextSize').text.replace('\n', ' ').replace('pic.twitter.com/jicxvaUZh1', '')

    # Add tweet to mars dictionary
    mars_data['tweet_info'] = tweet

###############
##########  MARS FACTS
###############

    # Visit Mars Facts webpage
    mars_facts_url = 'https://space-facts.com/mars/'

    # use pandas to read html into a table dataframe
    result = pd.read_html(mars_facts_url)
    mars_df = result[0]

    # Rename Columns
    mars_df = mars_df.rename(columns={0:'Values'})
    mars_df = mars_df.rename(columns={1:'Mars'})
    mars_df = mars_df.set_index('Values')

    # Convert to an HTML Table
    mars_html_table = mars_df.to_html().replace('\n', '')
    mars_html_table

    # Add table to dictionary
    mars_data['html_table'] = mars_html_table

###############
##########  MARS HEMISPHERE IMAGES
###############

    # Hold base and each hemi's urls
    base_url = 'https://astrogeology.usgs.gov'
    cerebus_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    schiaparelli_url ='https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    syrtis_major_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    valles_marineris_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'

    hemis = [cerebus_url, schiaparelli_url, syrtis_major_url, valles_marineris_url]
    img_list = []

    # Loop through each url
    for hemi in hemis:
        browser.visit(hemi)

        # Scrape the browser into a BeautifulSoup object and use BS to find the image of mars
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        # Cerebus Hemisphere
        img = soup.find('img', class_='wide-image')['src']
        title = soup.find('h2', class_='title').text.replace(' Enhanced', '')
        # create the full link
        full_img = base_url + img

        # append name and full_img to img_list
        img_list.append({'title':title, 'img_url':full_img})

    # add hemisphere images list to mars data
    mars_data['hemi_imgs'] = img_list

    return mars_data

# Python program to executable
# main directly
if __name__ == '__main__':
    scrape()
