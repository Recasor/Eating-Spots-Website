import sqlite3


def get_file_links(filename):
    with open("data/" + filename, "r") as f:
        links = [i.strip("\n") for i in f.readlines()]
    return links


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