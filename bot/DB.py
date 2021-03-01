import sqlite3


class Connection:
    """
    return: database connection object
    """
    def __init__(self):
        self.conn = sqlite3.connect('data.db')
        self.cursor = self.conn.cursor()

    def write(self, json):
        """
        write currency value to datatbase
        :param json: dict <currency:value>
        :return: None
        """
        try:
            self.cursor.executemany("""INSERT INTO currency VALUES(?, ?);""", json.items())
        except Exception as e:
            iter_json = iter(json.items())
            for i in range(len(json)):
                try:
                    currency = next(iter_json)
                    try:
                        self.cursor.execute("""INSERT INTO currency VALUES(?, ?);""", currency)
                    except:
                        self.cursor.execute("""UPDATE currency SET curr_value = ? 
                                                            where curr_name = ?;""", (currency[1], currency[0]))
                except StopIteration:
                    break
        self.conn.commit()

    def get_all(self):
        """
        get all values from database
        :return: dict <currency:value>
        """
        self.cursor.execute("""SELECT * FROM currency""")
        return {i[0]: i[1] for i in self.cursor.fetchall()}

    def get(self, currency):
        """
        :param currency:
        :return: value from currency
        """
        self.cursor.execute("""SELECT curr_value FROM currency WHERE curr_name = ?;""", (currency, ))
        return self.cursor.fetchone()


def init_db():
    """
    initialisation database before start work
    :return: None
    """
    connection = Connection()
    connection.cursor.execute("""CREATE TABLE IF NOT EXISTS currency(
        curr_name TEXT PRIMARY KEY, 
        curr_value FLOAT);
                            """)
    connection.conn.commit()
