import pymysql.cursors

def check_categories_table():
    # Connect to the database
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='ps_klocki',
                                 port=3307,
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM `categories`"
        cursor.execute(sql)
        result = cursor.fetchone()
        result_all = cursor.fetchall()
        #print(result_all)

    return result_all


#check_categories_table()

def insert_categories(data):
    # Connect to the database
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='ps_klocki',
                                 use_unicode=True,
                                 charset="utf8",
                                 port=3307,
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO categories (category_name) " \
                  "VALUES (%s)"
            cursor.executemany(sql, data)

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

    finally:
        connection.close()

def delete_categories_table():
    # Connect to the database
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='ps_klocki',
                                 port=3307,
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        # Read a single record
        sql = "DELETE FROM categories"
        cursor.execute(sql)

    connection.commit()
    connection.close()

def delete_products():
    # Connect to the database
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='ps_klocki',
                                 use_unicode=True,
                                 charset="utf8",
                                 port=3307,
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "DELETE FROM products"
            cursor.execute(sql)

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

    finally:
        connection.close()

def insert_products(data):
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     db='ps_klocki',
                                     use_unicode=True,
                                     charset="utf8",
                                     port=3307,
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO products (id, name, code, categories, old_price, netto_price, brutto_price, cena_sprzedazy_brutto, discount, discount_amount" \
                      ", F_wiek, F_typ, F_kategoria, F_kolor, F_waga, F_wymiar, F_material, F_liczba_el, description) " \
                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.executemany(sql, data)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

            '''with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT * FROM `products`"
                cursor.execute(sql)
                result = cursor.fetchone()
                print(result)'''
        finally:
            connection.close()


def delete_images():
    # Connect to the database
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='ps_klocki',
                                 use_unicode=True,
                                 charset="utf8",
                                 port=3307,
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "DELETE FROM images"
            cursor.execute(sql)

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

    finally:
        connection.close()


def insert_images(data):
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     db='ps_klocki',
                                     use_unicode=True,
                                     charset="utf8",
                                     port=3307,
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO images (name, url_disk, url_localhost, other) " \
                      "VALUES (%s, %s, %s, %s)"
                cursor.executemany(sql, data)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

        finally:
            connection.close()

