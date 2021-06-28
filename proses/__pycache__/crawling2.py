from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import csv
def initDriver():
    # chrome_options = webdriver.ChromeOptions()
# Chrome v75 and lower:
# chrome_options.add_argument("--headless") 
# Chrome v 76 and above (v76 released July 30th 2019):
    # chrome_options.headless = False
    path="C:\\Users\\fak\\Downloads\\Compressed\\chromedriver_win32_3\\chromedriver.exe"
    driver=webdriver.Chrome(path)
    loadPageTimot = 100
    driver.set_page_load_timeout(loadPageTimot)
    return driver

def scrollDown(driver, currentDocumentHeight):
    currentDocumentHeight = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    sleep(5)
    currentDocumentHeight = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    sleep(5)

    return currentDocumentHeight

def getTweet(driver):
    articles = driver.find_elements_by_xpath("//article//div[@lang='in']")
    tweet = [article.text for article in articles]
    
    return tweet

def getTweets(driver, totalTweet, secondToSleep):
    import time
    resultTweet = []
    currentDocHeight = 0


    while(len(resultTweet) < totalTweet):
        currentTweetOnPage = getTweet(driver)
        for t in currentTweetOnPage:
            if t not in resultTweet:
                resultTweet.append(t)

        docHeight = scrollDown(driver, secondToSleep)
        print(currentDocHeight)
        print(docHeight)
        if currentDocHeight == docHeight:
            break
        
        currentDocHeight = docHeight
       
            
    return resultTweet

# def getTweetByKeyword(keyword, total, tahun, year):
#     driver = initDriver()
#     # %20-filter%3Alinks\
#     url='https://twitter.com/search?f=live&q=film%20{}%20lang%3Aid%20until%3A{}%20since%3A{}%20-filter%3Alinks&src=typed_query'.format(keyword,year,tahun)
#     # url='https://twitter.com/search?q=film%20{}&src=typed_query&f=live'.format(keyword)
#     driver.get(url)
#     sleep(10)
#     return getTweets(driver, total, 12)

def getTweet(keyword, total, tahun, year):
    driver1 = initDriver()
    # %20-filter%3Alinks\
    url1='https://twitter.com/search?f=live&q=film%20{}%20lang%3Aid%20until%3A{}%20since%3A{}&src=typed_query'.format(keyword,year,tahun)
    # url='https://twitter.com/search?q=film%20{}&src=typed_query&f=live'.format(keyword)
    # driver1.get(url1)
    driver1.get(url1)
    sleep(10)
    return getTweets(driver1, total, 12)