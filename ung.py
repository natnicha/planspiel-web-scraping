from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import json

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


    # filter and keep only courses, not degree programs
    pattern = '''https://www.ung.si/en/schools/[\w-]*/programmes/()\w*/20*'''
    courses_links = [x for x in links if re.match(pattern, x)]

    json_file = []
    for course_link in courses_links:
        driver.get(course_link)
        sections = driver.find_elements(By.XPATH, '//div[contains(@class,"column is-12-tablet is-8-desktop text-content")]')
        
        if len(sections) >= 1:
            # course header
            header_section = sections[0]
            course_name = header_section.find_element(By.CSS_SELECTOR, 'h1').text
            degree_program = header_section.find_element(By.XPATH, '//div[contains(@class,"is-size-4 mb-4 pt-3")]').text

            # course content
            data = {}
            course_content = sections[1]
            data_topics = course_content.find_elements(By.CSS_SELECTOR, 'h2')

            for idx, data_topic in enumerate(data_topics):
                data_under_div = course_content.find_elements(By.CSS_SELECTOR, 'div')[idx]

                data_li_text = ''
                data_lis = data_under_div.find_elements(By.CSS_SELECTOR, 'ul>li')
                if len(data_lis)>0:
                    for data_li in data_lis:
                        data_li_text = data_li_text + '''\n ''' + data_li.text
                        
                data_p_text = ''
                data_ps = data_under_div.find_elements(By.CSS_SELECTOR, 'p')
                if len(data_ps)>0:
                    for data_p in data_ps:
                        data_p_text = data_p_text + '''\n ''' + data_p.text

                data[data_topic.text] = data_li_text + '''\n '''+ data_p_text


            # course property
            course_property_json = {}
            course_property_section = driver.find_element(By.XPATH, '//div[contains(@class,"sidebar-content study-course__data")]')
            course_property_section_details = course_property_section.find_elements(By.CSS_SELECTOR, 'p')
            course_property_section_bullet = course_property_section.find_elements(By.CSS_SELECTOR, 'ul')
            bullet_index = 0
            for course_property_section_detail in course_property_section_details:
                val = course_property_section_detail.text.split(":")
                if str(val[0]).strip()!="" and str(val[1]).strip().replace("\n","") == "" : # case bullet value 
                    course_property_json[val[0]] = course_property_section_bullet[bullet_index].text
                    bullet_index = bullet_index + 1
                elif str(val[0]).strip()!="" and str(val[1]).strip() != "": # case paragraph value
                    course_property_json[val[0]] = str(val[1]).strip()

            
            course = {
                "name": course_name,
                "degree-program": degree_program,
                "content": data,
                "property": course_property_json,
                "url": course_link
            }

            json_file.append(course)

    # write into json format
    with open("courses.json", "w") as outfile: 
        json.dump(json_file, outfile)

    # release the resources allocated by Selenium and shut down the browser
    driver.quit()