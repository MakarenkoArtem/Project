import sqlite3


class Base_date:  # класс для работы с бд
    def __init__(self, title):  # название бд
        self.title = title

    def select(self, res, table, uslov=None, z=None,
               dr=[]):  # метод получения данных из бд
        """(res-[столбцы значение которых необходимо], table=название таблицы,
        uslov=and, or, None(если нет условия), z=[парные объекты сравнения],
        dr=[условия частичного сходства слов]]"""
        con = sqlite3.connect(self.title)
        cur = con.cursor()
        if uslov is not None:
            result = cur.execute(f'''SELECT {", ".join(res)} FROM {table}
    WHERE {f" {uslov} ".join([f"""{z[i]} = '{z[i + 1]}'""" for i in range(0, len(z), 2)] + dr)}''').fetchall()
        else:
            result = cur.execute(
                f'''SELECT {", ".join(res)} FROM {table}''').fetchall()
        if len(res) == 1 and res != ["*"]:
            result = [i[0] for i in result]
        con.close()
        return result

    def delete(self, table, uslov, z, dr=[]):  # метод удаления данных из бд
        """(table=название таблицы,
        uslov=and, or, None(если нет условия), z=[парные объекты сравнения],
        dr=[условия частичного сходства слов]"""
        con = sqlite3.connect(self.title)
        cur = con.cursor()
        cur.execute(
            f"""DELETE from {table} where {f" {uslov} ".join([f'''{z[i]} = "{z[i + 1]}"''' for i in range(0, len(z), 2)] + dr)}""")
        con.commit()
        con.close()

    def insert(self, table, res, z):  # метод дополнения данных в бд
        """(table=название таблицы, uslov=and, or, None(если нет условия),
        res-[столбцы значение которых необходимо], z=[парные объекты сравнения]"""
        con = sqlite3.connect(self.title)
        cur = con.cursor()
        cur.execute(
            f"""INSERT INTO {table}({str(res)}) VALUES ({', '.join(['?' for _ in range(len(z))])})""",
            z)
        con.commit()
        con.close()