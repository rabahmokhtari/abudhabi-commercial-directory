# ABU DHABI COMMERCIAL CHAMBER DIRECTORY
from helium import *
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


def wait_loading():
    # Waing 10 sc until pagination buttons are located
    WebDriverWait(browser, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "Polaris-Pagination__Button"))
    )


def get_number_of_enterprises():
    wait_loading()
    polaris_card_sections = browser.find_elements_by_class_name('Polaris-Card__Section')
    # first div in second polarris_card_sections containing the number of enterprises
    div_1st = polaris_card_sections[1].find_element_by_tag_name('div')

    _number_all_enterprise = [int(s) for s in div_1st.text.split() if s.isdigit()]
    return int(_number_all_enterprise[0])


def btn_pagination_previous():
    buttons_pagination = browser.find_elements_by_class_name('Polaris-Pagination__Button')
    return buttons_pagination[0]


def btn_pagination_next():
    return browser.find_element_by_xpath('//*[@id="AppFrameMain"]/div/div[2]/div/div[2]/div[2]/div[2]/div[3]/nav/button[2]')


def get_next_page():
    wait_element_by_xpath('//*[@id="AppFrameMain"]/div/div[2]/div/div[2]/div[2]/div[2]/div[3]/nav/button[2]')
    btn_next = btn_pagination_next()
    move_to_element(btn_next)
    is_remain = not btn_next.get_attribute('disabled') == "true"
    if is_remain:
        click(btn_next)
        wait_loading()
    return is_remain


def wait_element_by_text(name):
    WebDriverWait(browser, 100).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '{_name}')]".format(_name=name)))
    )


def wait_element_by_xpath(xpath):
    WebDriverWait(browser, 100).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )


def move_to_element(element):
    time.sleep(0.2)
    browser.execute_script("arguments[0].scrollIntoView();", element)  # I added this to ensure the element visibility
    desired_y = (element.size['height'] / 2) + element.location['y']
    window_h = browser.execute_script('return window.innerHeight')
    window_y = browser.execute_script('return window.pageYOffset')
    current_y = (window_h / 2) + window_y
    scroll_y_by = desired_y - current_y
    browser.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)


def process_all():
    wait_loading()
    n = get_number_of_enterprises()
    i = 1
    while True:
        print(i)
        polaris_dataTable = browser.find_element_by_class_name('Polaris-DataTable')
        data_table = polaris_dataTable.find_element_by_tag_name('table')
        rows = data_table.find_elements_by_tag_name('tr')
        # print(len(rows))
        for row in rows[1:]:  # 1: skip the first element
            print(i)
            tds = row.find_elements_by_tag_name('td')
            btn = tds[4].find_element_by_tag_name('button')
            move_to_element(btn)
            # browser.execute_script("arguments[0].click();", btn)
            click(btn)
            time.sleep(0.1)
            wait_element_by_text('عرض التفاصيل')
            click('عرض التفاصيل')
            time.sleep(0.1)
            wait_element_by_text('رقم العضوية الموحد:')
            print(row.text)
            click('إلغاء')
            print("company number : " + str(i))
            i = i + 1
            if i > n:
                return "Terminated successfully"
            #   time.sleep(1)
        get_next_page()


url = 'https://digital.abudhabichamber.ae/portal/#/commercial-directory'
browser = start_chrome(url)

browser.find_element(By.ID, "PolarisSelect1").click()
dropdown = browser.find_element(By.ID, "PolarisSelect1")
dropdown.find_element(By.XPATH, "//option[. = '20']").click()
browser.find_element(By.ID, "PolarisSelect1").click()

wait_element_by_text('بحث')
btn_search = browser.find_element_by_class_name('Polaris-Button--primary')
click(btn_search)

print(get_number_of_enterprises())
process_all()
