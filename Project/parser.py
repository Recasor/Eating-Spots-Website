from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from extra_functions import *


# кароче всё это дело ВООБЩЕ не доделано оно работает но 100% будут всякия баги и проблемы да и плюс костыли есть
# в общем я спешил что бы успеть сделать до сегодня потом всё пофикшу (запятых не будет)
def get_data(d, w, id):
    data, menu = {}, []

    # мне лень писать коментарии нормально, потом напишу ᗜ˰ᗜ
    NAME = ("xpath", "//a[@class='card-title-view__title-link']")
    ADDRESS = ("xpath", "//div[@class='business-contacts-view__address-link']")
    DESC = ("xpath", "//div[@class='business-story-entry-view__description']")
    OPENING_H = ("xpath", "//div[@class='business-card-working-status-view__text']")

    data["name"] = w.until(EC.presence_of_element_located(NAME)).text
    data["address"] = d.find_element(*ADDRESS).text
    data["desc"] = d.find_element(*DESC).text if len(d.find_elements(*DESC)) > 0 else "-"
    data["opening-h"] = d.find_element(*OPENING_H).text

    # переходим на вкладку с меню если она есть
    button = d.find_elements("xpath", "//div[@class='tabs-select-view__title _name_menu']")
    if len(button) > 0:
        button[0].click()

        OBJECTS = ("xpath", "//div[contains(@class, 'business-full-items-grouped-view__item _view_')]")
        objs = w.until(EC.presence_of_all_elements_located(OBJECTS))

        # сори за кривой способ
        img_flag = len(d.find_elements("xpath", "//div[contains(@class, 'business-full-items-grouped-view__item _view_')]//img")) > 0

        for elem in objs:
            menu_obj = {"name": elem.find_element("xpath", ".//div[contains(@class, 'view__title')]").text,
                        "price": elem.find_element("xpath", ".//*[contains(@class, 'view__price')]").text}

            desc = elem.find_elements("xpath", ".//*[contains(@class, 'view__description')]")
            menu_obj["desc"] = desc[0].text if len(desc) > 0 else "-"

            if img_flag:
                img = elem.find_elements("xpath", ".//img")

                if len(img) > 0:
                    menu_obj["img"] = img[0].get_attribute("src")

                # знаю что такой себе способ но я устал
                else:
                    driver.execute_script("arguments[0].scrollIntoView({block: 'nearest', behavior: 'instant'});", elem)
                    menu_obj["img"] = w.until(EC.presence_of_element_located(("xpath", ".//img"))).get_attribute("src")
            else:
                menu_obj["img"] = "-"

            menu.append(menu_obj)
    # переходим на вкладку с картинками
    d.find_element("xpath", "//div[@class='tabs-select-view__title _name_gallery']").click()

    IMAGES = ("xpath", "//img[@class='media-wrapper__media']")
    # на это внимания не обращайте пока что
    # идея была в получении нескольких изображений но я хз как это запихнуть адекватно в sql таблицу
    image_url = [img.get_attribute("src") for img in w.until(EC.presence_of_all_elements_located(IMAGES))[:1]][0]
    data["img"] = image_url

    save_data(data, menu, id)
    print("done")


chrome_options = webdriver.ChromeOptions()
chrome_options.page_load_strategy = "eager"
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--headless")

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 15, 0.5)

links = get_file_links("links.txt")
driver.get(links[0])

scrollable_element = wait.until(EC.element_to_be_clickable(("xpath", "//div[@class='scroll__container']")))
i = 0

while True:

    elements = driver.find_elements("xpath",
                                    "//li[@class='search-snippet-view']//div[@class='search-business-snippet-view__head']")

    if i < len(elements):

        element = elements[i]
        i += 1

        driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'instant'});",
                              elements[i - 1])

        if i >= len(elements):
            driver.execute_script("arguments[0].scrollTop += 300;", scrollable_element)

        element.click()
        get_data(driver, wait, i)
    else:
        break
