import sqlite3

class Db:
    def __init__(self):
        self.conn = sqlite3.connect('parking.db')
        # создание объекта класса cursor, используемый для взаимодействия с БД
        self.c = self.conn.cursor()
        # выполнение запроса к БД
        self.c.execute('''
                        CREATE TABLE IF NOT EXISTS db(
                            id INTEGER PRIMARY KEY,
                            spot TEXT,
                            car_count INTEGER DEFAULT 0,
                            name TEXT,
                            year INTEGER,
                            body TEXT,
                            colour TEXT,
                            engine TEXT,
                            number TEXT)''')
        self.conn.commit()

    def add_spot(self, spot):
        self.c.execute('''INSERT INTO db (spot) VALUES (?)''', (spot,))
        self.c.execute('''UPDATE db SET car_count = car_count, name=0, year=0, body=0, colour=0, 
                    engine=0, number=0 WHERE spot = ?''', (spot,))
        self.conn.commit()
        print(f"Место {spot} добавлено")
    def delete_spot(self, spot):
        self.c.execute('''DELETE FROM db WHERE spot = ?''', (spot,))
        self.c.execute("SELECT name FROM db")
        self.c.execute('''UPDATE db SET car_count = car_count - 1, name=0, year=0, body=0, colour=0, 
                        engine=0, number=0 WHERE spot = ?''', (spot,))
        print(f'Место {spot} удалено')
        self.conn.commit()

    def add_car(self, spot, name, year, body, colour, engine, number):
        self.c.execute('''UPDATE db SET car_count = car_count + 1, name = ?, 
                    year = ?, body = ?, colour = ?, engine = ?, number = ? WHERE spot = ?''', (name, year, body, colour,
                                                                                               engine, number, spot))
        self.conn.commit()
        print(f"Машина {name} добавлена на место {spot}")
    def delete_car(self, spot):
        self.c.execute('''UPDATE db SET car_count = car_count - 1, name=0, year=0, body=0, colour=0, 
                    engine=0, number=0 WHERE spot = ?''', (spot,))
        self.c.execute("SELECT car_count FROM db")
        res = self.c.fetchone()[0]
        if res < 0:
            self.c.execute("UPDATE db SET car_count = 0")
            print(f"Машина была удалена с места {spot}")
        self.conn.commit()

    def view_parking(self):
        self.c.execute('''SELECT * FROM db''')
        result = self.c.fetchall()
        if result:
            print("-" * 20)
            print("Стоянка авто")
            for row in result:
                print(f"Место: {row[1]}")
                print(f"Количество машин: {row[2]}")
                print(f"Марка авто: {row[3]}")
                print(f"Год выпуска авто: {row[4]}")
                print(f"Тип кузова: {row[5]}")
                print(f"Цвет кузова: {row[6]}")
                print(f"Тип двигателя: {row[7]}")
                print(f"Гос.номер: {row[8]}")
                print("-" * 20)
        else:
            print("Парковка пуста!")


db = Db()

while True:
    print("-" * 20)
    print('1) Добавить место')
    print('2) Удалить место')
    print('3) Добавить машину и параметры к ней')
    print('4) Удалить машину')
    print('5) Показать всю парковку')
    print('6) Выход')
    print("-" * 20)
    ch = input('Введите номер: ')

    if ch == '1':
        spot = input('Введите номер места: ')
        db.c.execute('''SELECT * FROM db WHERE spot = ?''', (spot,))
        if db.c.fetchone():
            print(f'Место с номером {spot} уже существует. Попробуйте добавить другое место')
        else:
            db.add_spot(spot)

    elif ch == '2':
        spot = input('Введите номер места: ')
        db.c.execute('''SELECT * FROM db WHERE spot = ?''', (spot,))
        if not db.c.fetchone():
            print(f'Мест с номером {spot} не существует. Попробуйте сначала добавить место')
        else:
            db.delete_spot(spot)

    elif ch == '3':
        spot = input('Введите номер места: ')
        db.c.execute('''SELECT * FROM db WHERE spot = ?''', (spot,))
        if not db.c.fetchone():
            print("-" * 20)
            print(f'Мест с номером {spot} не существует. Попробуйте сначала добавить место')
        else:
            name = input('Введите марку авто: ')
            year = input('Введите Год выпуска авто: ')
            body = input('Введите Тип кузова: ')
            colour = input('Введите Цвет кузова: ')
            engine = input('Введите Тип двигателя: ')
            number = input('Введите Гос.номер: ')
            db.add_car(spot, name, year, body, colour, engine, number)

    elif ch == '4':
        spot = input('Введите номер места, откуда нужно удалить авто: ')
        db.c.execute('''SELECT * FROM db WHERE spot = ?''', (spot,))
        if not db.c.fetchone():
            print("-" * 20)
            print(f'Мест с номером {spot} не существует. Попробуйте сначала добавить место')
        else:
            db.delete_car(spot)

    elif ch == '5':
        db.view_parking()

    elif ch == '6':
        break

    else:
        print('Выбран неверный номер')


















