from selenium import webdriver 
 
# initialize an instance of the chrome driver (browser)
driver = webdriver.Chrome()
# visit your target site
# driver.get('https://scrapingclub.com/')
driver.get('https://www.ung.si/en/education/programmes-courses/')

# scraping logic...

# release the resources allocated by Selenium and shut down the browser
driver.quit()