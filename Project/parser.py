import selenium.common.exceptions
from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from extra_functions import *


# короче всё это дело ВООБЩЕ не доделано оно работает, но 100% будут всякий баги и проблемы да и плюс костыли есть
# в общем я спешил что бы успеть сделать до сегодня потом всё пофикшу (запятых не будет)
def get_data(d, w, r_id):
    data, menu = {}, []

    # мне лень писать комментарии нормально, потом напишу ᗜ˰ᗜ
    NAME = ("xpath", "//a[@class='card-title-view__title-link']")
    ADDRESS = ("xpath", "//div[@class='business-contacts-view__address-link']")
    DESC = ("xpath", "//div[@class='business-story-entry-view__description']")
    OPENING_H_BUTTON = ("xpath", "//div[@class='business-card-working-status-view__main']")
    OPENING_HRS = ("xpath", "//div[@class='business-working-intervals-view__interval']")
    RATING = ("xpath", "//div[@class='business-card-view']//span[@class='business-rating-badge-view__rating-text']")

    data["id"] = r_id
    data["type"] = "ресторан"
    data["title"] = w.until(EC.presence_of_element_located(NAME)).text
    data["address"] = d.find_element(*ADDRESS).text
    data["rating"] = d.find_element(*RATING).text.replace(",", ".")

    print(data["title"], data["address"])
    data["description"] = d.find_element(*DESC).text if len(d.find_elements(*DESC)) > 0 else ""
    data["time"] = get_opening_hours(d, w, OPENING_H_BUTTON, OPENING_HRS)

    # переходим на вкладку с меню если она есть
    button = d.find_elements("xpath", "//div[@class='tabs-select-view__title _name_menu']")
    if len(button) > 0:
        button[0].click()
        menu = get_menu(w)
        data["menu"] = menu

    # переходим на вкладку с картинками
    d.find_element("xpath", "//div[@class='tabs-select-view__title _name_gallery']").click()
    IMAGES = ("xpath", "//img[@class='media-wrapper__media']")
    # на это внимания не обращайте пока что
    # идея была в получении нескольких изображений, но я хз как это запихнуть адекватно в sql таблицу
    gallery = get_gallery(w, IMAGES)
    data["img"] = gallery[1]
    data["gallery"] = gallery
    print(d.current_url)
    data["mapLink"] = "/".join(d.current_url.split("/")[:7])
    data["mapUrl"] = get_interactive_map(d.current_url, data["mapLink"])
    print(f"restaurant {r_id}, done\n")

    return data


def get_opening_hours(d, w, button_locator, days_locator):
    d.find_element(*button_locator).click()

    days = w.until(EC.visibility_of_all_elements_located(days_locator))

    return " ".join([day.text for day in days])


def get_gallery(w, imgs_locator):
    gallery = []
    imgs = w.until(EC.presence_of_all_elements_located(imgs_locator))
    for img in imgs:
        if "get-vh" not in img.get_attribute("src"):
            gallery.append(img.get_attribute("src"))
        if len(gallery) > 3:
            break
    return gallery


def get_menu(w):
    menu = {}

    CATEGORIES = ("xpath", "//div[contains(@class, 'business-full-items-grouped-view__category')]")
    ITEMS_LOCATOR = ("xpath", ".//div[contains(@class, 'business-full-items-grouped-view__item _view_')]")
    NAME = ("xpath", ".//div[contains(@class, 'view__title')]")
    PRICE = ("xpath", ".//*[contains(@class, 'view__price')]")
    DESC = ("xpath", ".//*[contains(@class, 'view__description')]")

    for category in w.until(EC.presence_of_all_elements_located(CATEGORIES)):
        category_name = category.find_element("xpath", ".//div[contains(@class, "
                                                       "'business-full-items-grouped-view__title')]").text

        items = category.find_elements(*ITEMS_LOCATOR)

        menu[category_name] = []
        img_flag = items[0].find_element(*NAME).get_attribute("class") == "related-item-photo-view__title"

        for item in items:
            menu_obj = {"name": item.find_element(*NAME).text,
                        "price": item.find_element(*PRICE).text}

            desc = item.find_elements(*DESC)
            menu_obj["desc"] = desc[0].text if desc else ""

            if img_flag:
                img = item.find_elements("xpath", ".//img")

                if img:
                    menu_obj["photo"] = img[0].get_attribute("src")

                else:
                    driver.execute_script("arguments[0].scrollIntoView({block: 'nearest', behavior: 'instant'});",
                                          item)

                    item_wait = WebDriverWait(item, 1)
                    try:
                        menu_obj["photo"] = item_wait.until(EC.presence_of_element_located(("xpath",
                                                                                            ".//img"))).get_attribute(
                            "src")
                    except selenium.common.exceptions.TimeoutException:
                        menu_obj["photo"] = "static/main/img/cafes/no-image.jpg"
            else:
                menu_obj["photo"] = "static/main/img/cafes/no-image.jpg"

            menu[category_name].append(menu_obj)

    return menu


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
DATA = []

while True:

    elements = driver.find_elements("xpath",
                                    "//li[@class='search-snippet-view']//div["
                                    "@class='search-business-snippet-view__head']")

    if i < len(elements):

        element = elements[i]
        i += 1

        driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'instant'});",
                              elements[i - 1])

        if i >= len(elements):
            driver.execute_script("arguments[0].scrollTop += 300;", scrollable_element)

        element.click()
        DATA.append(get_data(driver, wait, i))
    else:
        break

save_to_json(DATA)
