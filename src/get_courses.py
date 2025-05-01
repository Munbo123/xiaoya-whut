import os
from concurrent.futures import ThreadPoolExecutor,as_completed
import time
from selenium.webdriver.common.by import By

from Xiaoya_Script import Xiaoya_scrpit



working_path = os.path.dirname(__file__)

def func1(course_num):
    xiaoya = Xiaoya_scrpit(working_path=working_path)
    xiaoya.login('1023000971','nf3039755985',True)
    driver = xiaoya.driver
    courses = driver.find_elements(by=By.CSS_SELECTOR,value='.aia_course_card > .ta_mainInfo > span:nth-child(1)')
    print(len(courses))
    course = courses[course_num]
    course.click()
    res = xiaoya._AllTaskName()
    return res

course_nums = [0,1,2,3]
results = []

with ThreadPoolExecutor(max_workers=8) as executor:
    futures = {executor.submit(func1, num): num for num in course_nums}
    for future in as_completed(futures):
        results.append(future.result())

print(results)