from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

if __name__ == '__main__':
    # initialize an instance of the chrome driver (browser)
    driver = webdriver.Chrome()

    # visit your target site
    links = {
        'Faculty of economics and management': 'https://ekursi.rta.lv/course/index.php?categoryid=4&browse=courses&perpage=600',
        'Faculty of engineering': 'https://ekursi.rta.lv/course/index.php?categoryid=2&browse=courses&perpage=600',
        'Faculty of education, languages and design': 'https://ekursi.rta.lv/course/index.php?categoryid=5&browse=courses&perpage=900',
        'Faculty of education, languages and design - Doctoral program Pedagogy: Social and Special pedagogy': 'https://ekursi.rta.lv/course/index.php?categoryid=72',
        'Centre for Lifelong Learning': 'https://ekursi.rta.lv/course/index.php?categoryid=59',
        'Center for Lifelong Learning - Use of laser technologies for innovative solutions in textile and leather products': 'https://ekursi.rta.lv/course/index.php?categoryid=67',
        'Center for Lifelong Learning - Education process based on competence approach, implementing special education programs': 'https://ekursi.rta.lv/course/index.php?categoryid=70',
        'Center for Lifelong Learning - Organization and management of the pedagogical process': 'https://ekursi.rta.lv/course/index.php?categoryid=71',
        'Other': 'https://ekursi.rta.lv/course/index.php?categoryid=1',
        'Other - Moodle and distance learning': 'https://ekursi.rta.lv/course/index.php?categoryid=73',

    }

    json_file = []
    for faculty_name, link in links.items():
        driver.get(link)

        # scraping logic...
        # find all courses
        course_infos = driver.find_elements(By.XPATH, '//div[contains(@class,"info")]')
        # extend all summary
        for course_info in course_infos:
            if course_info.text != '' and course_info.text != 'You are not logged in. (Log in)':
                try:
                    course_summary = course_info.find_element(By.XPATH, 'div[contains(@class,"moreinfo")]').find_element(By.XPATH, 'a[contains(@title,"Summary")]')
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(course_summary)).click()
                except:
                    pass
                
        # gather content for each course
        for course_info in course_infos:
            if course_info.text != '' and course_info.text != 'You are not logged in. (Log in)':
                try:
                    course_name = course_info.find_element(By.XPATH, '*[contains(@class,"coursename")]')
                    course_url = course_name.find_element(By.XPATH, 'a[contains(@class,"aalink")]').get_attribute('href') 
                    try:
                        course_content = course_info.find_element(By.XPATH, './parent::*').find_element(By.XPATH, 'div[contains(@class,"content")]').text
                    except:
                        course_content = ''
                    course_detail = {
                        "name": course_name.text,
                        "faculty": faculty_name,
                        "content": course_content,
                        "url": course_url
                    }
                    json_file.append(course_detail)
                except:
                    pass

    # write into json format
    with open("courses-rat.json", "w") as outfile: 
        json.dump(json_file, outfile)

    # release the resources allocated by Selenium and shut down the browser
    driver.quit()