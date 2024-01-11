from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_inside_elements_by_class_name(elements, target_inside_element):
    output = []
    for element in elements:
        output.append(element.find_element(By.CLASS_NAME, target_inside_element))
    return output

def get_attribute(elements, attribute):
    output = []
    for element in elements:
        output.append(element.get_attribute(attribute))
    return output

if __name__ == '__main__':
    # initialize an instance of the chrome driver (browser)
    driver = webdriver.Chrome()
    # visit your target site
    driver.get('https://www.ung.si/en/education/programmes-courses/')

    # scraping logic...

    # find tabs
    tabs = driver.find_element(By.CLASS_NAME, "program-course-search").find_elements(By.CSS_SELECTOR, 'ul>li>a')
    # to click course tab
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable(tabs[1])).click()
    
    # click more until the end
    is_end = True
    while is_end:
        try:
            more_button = driver.find_element(By.XPATH, '//button[contains(@class,"button is-primary is-fullwidth mt-5 mb-5")]')
            more_button.click()
        except:
            is_end = False

    # gather all course links
    target_section = 'segment search-result has-bottom-border is-hoverable'
    degree_programs = driver.find_elements(By.XPATH, '//section[contains(@class,"'+target_section+'")]')
    degree_programs_source = get_inside_elements_by_class_name(degree_programs, 'more')
    links = get_attribute(degree_programs_source,('href'))


    # release the resources allocated by Selenium and shut down the browser
    driver.quit()