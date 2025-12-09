import sqlite3
import json


def get_file_links(filename):
    with open("data/" + filename, "r") as f:
        links = [i.strip("\n") for i in f.readlines()]
    return links


def get_interactive_map(link, r):
    ll = link.split("ll=")[1].split("&mode")[0].split("%2C")
    r = "/".join(r.split("/")[4:])
    return (f"<iframe src=\"https://yandex.ru/map-widget/v1/{r}/?ll={ll[0]}%{ll[1]}&z=17\" width=\"500"
            f"\" height=\"400\" frameborder=\"0\"></iframe>")


def save_to_json(data):
    with open("main/static/main/data/items.json", "w", encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


def create_sql():
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    command1 = '''
        CREATE TABLE IF NOT EXISTS restaurants (
            restaurant_id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT,
            address TEXT,
            opening_h TEXT,
            img_link TEXT
        )
        '''

    cursor.execute(command1)

    # да я знаю что price не должен быть текстовым
    # потому пофикшу (честно)
    command2 = '''
            CREATE TABLE IF NOT EXISTS menu (
                menu_id INTEGER PRIMARY KEY,
                restaurant_id TEXT,
                name TEXT,
                description TEXT,
                price TEXT,
                img_link TEXT
            )
            '''

    cursor.execute(command2)


def save_data(data, menu, id):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO restaurants 
        (restaurant_id, name, description, address, opening_h, img_link) 
        VALUES (?, ?, ?, ?, ?, ?)''',
                   (id, data["name"], data["desc"], data["address"], data["opening-h"], data["img"]))

    for i in menu:
        cursor.execute('''INSERT INTO menu 
                    (restaurant_id, name, description, price, img_link) VALUES (?, ?, ?, ?, ?)''',
                       (id, i["name"], i["desc"], i["price"], i["img"]))

    conn.commit()