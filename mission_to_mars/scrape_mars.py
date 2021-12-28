import pandas as pd
# import requests
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    # featured image scrape
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # visit browser url
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    # create html and parse
    html = browser.html
    soup = bs(html, "html.parser")

    # scrape latest image and assign to variable
    img = [i.get("src") for i in soup.find_all("img", class_="headerimage fade-in")]

    # concat main url with image url
    # assign to variable to access later
    featured_image_url = url + img[0]

    # latest news

    # visit browser url
    news_url = "https://redplanetscience.com/"
    browser.visit(news_url)

    # create html and parse
    html_1 = browser.html
    soup_1 = bs(html_1, "html.parser")

    # assign latest news title to a variable to access later
    latest_news = soup_1.find_all("div", class_="content_title")[0]
    latest_news_title = latest_news.text

    # assign latest news paragraph to a variable to access later
    paragraph = soup_1.find_all("div", class_="article_teaser_body")[0]
    latest_news_paragraph = paragraph.text

    # hemisphere image scrape

    # visit browser url
    hemi_url = "https://marshemispheres.com/"
    browser.visit(hemi_url)

    # create empty list for each hemisphere image
    hemisphere_image_urls = []


    # scrape images by looping through
    # get image title and image url
    for i in range(4):
        html = browser.html
        soup = bs(html, "html.parser")
    
        title = soup.find_all("h3")[i].get_text()
        browser.find_by_tag('h3')[i].click()
    
        html = browser.html
        soup = bs(html, "html.parser")
    
        img_url = soup.find("img", class_="wide-image")["src"]
    
        hemisphere_image_urls.append({
            "title": title,
            "img_url": hemi_url + img_url
        })
        browser.back()

    # access and assign each title and image a variable    
    title1 = hemisphere_image_urls[0]["title"]
    image1 = hemisphere_image_urls[0]["img_url"]
    
    title2 = hemisphere_image_urls[1]["title"]
    image2 = hemisphere_image_urls[1]["img_url"]

    title3 = hemisphere_image_urls[2]["title"]
    image3 = hemisphere_image_urls[2]["img_url"]

    title4 = hemisphere_image_urls[3]["title"]
    image4 = hemisphere_image_urls[3]["img_url"]
          

    # mars earth table

    # visit browser url
    table_url = "https://galaxyfacts-mars.com/"
    browser.visit(table_url)

    # create html and parse
    html_3 = browser.html
    soup_3 = bs(html_3, "html.parser")

    # scrape the mars earth comparison table and assign variable
    table = soup_3.find_all("table", class_="table")[0]

    # create variable for just table headers for data frame
    table_header = [i.text for i in table("th")]

    # create variable for mars column contents
    mars_column = [i.text for i in table("span", class_="orange")]

    # create variable for earth column contents
    earth_column = [i.text for i in table("span", class_="purple")]

    # create data frame
    table_df = {"Description": table_header, "Mars": mars_column, "Earth": earth_column}
    df = pd.DataFrame(table_df)
    df.set_index("Description", inplace=True)

    # remove the /t from last row of earth temp info
    df["Earth"] = df["Earth"].str.replace("\t", "")

    # convert table to html text
    comparison_table = df.to_html(classes="table table-striped")

    browser.quit()


    # dictionary for database access
    
    mars_data = {
    "latest_title": latest_news_title,
    "latest_paragraph" : latest_news_paragraph,
    "featured_image": featured_image_url,
    "html_table": comparison_table,
    "hemisphere_scrape": hemisphere_image_urls,
    "title1": title1,
    "title2": title2,
    "title3": title3,
    "title4": title4,
    "image1": image1,
    "image2": image2,
    "image3": image3,
    "image4": image4,

    }

    return mars_data