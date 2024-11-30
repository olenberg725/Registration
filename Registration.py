import sqlite3
# Создание базы дaнных registration.db
db_reg = sqlite3.connect('registration.db')
print('Подключились к базе данных')
cur = db_reg.cursor()
# Создание таблицы users_data и заполнение данными тестового пользователя ('Ivan', 'qwer1234', '1234')
cur.executescript("""CREATE TABLE IF NOT EXISTS users_data(
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Login TEXT NOT NULL,
    Password TEXT NOT NULL,
    Code TEXT NOT NULL);

    INSERT INTO users_data(Login, Password, Code)
    VALUES ('Ivan', 'qwer1234', '1234');
""")
db_reg.commit()
print('Таблица users_data создана')
print('Тестовый пользователь создан')
print('Регистрация нового пользователя - введите 1\n'
      'Aвторизация в системе - введите 2\n'
      'Восстановление пароля - введите 3')

def select_all():
    # Запрос на вывод содержимого таблицы users_data
    cur.execute("""SELECT * FROM users_data""")
    lists = cur.fetchall()  # Результат запроса
    # Создание списка, содержащего логины пользователей
    result = []
    for i in range(len(lists)):
        result.append(lists[i][1].lower())
    return result

def select_on_login(user_login):
    # Поиск пользователя в базе данных
    login = []
    login.append(user_login)
    login = tuple(login)
    cur.execute("""SELECT Login, Password, Code FROM users_data WHERE Login = (?);""", login)
    lists = cur.fetchone()
    return lists      # Возвращаем результат вида (Login, Password, Code)

def user_registration():
    # Создание списка, содержащего логины пользователей
    UserData = select_all()
    # Создание списка с данными пользователя
    usdata = []
    # Ввод логина пользователя
    login = input('Введите login \n')
    if login.isalpha():
        # Проверка логина на уникальность
        if login.lower() in UserData:
            return f'Пользователь с таким именем уже существует.'
        else:
            # Вносим логин в список с данными пользователя
            usdata.append(login)
            password_1 = input('Введите пароль\n')
            if password_1.isidentifier():
                password_2 = input('Повторите пароль\n')
                if password_1 == password_2:
                    # Вносим пароль в список с данными пользователя
                    usdata.append(password_1)
                    code = input('Ввведите четырехзначный код для восстановления пароля\n')
                    # Вносим четырехзначный код для восстановления пароля в список с данными пользователя
                    if code.isdigit() and len(code) == 4:
                        usdata.append(code)
                        return tuple(usdata)  # Возвращаем результат вида (Login, Password, Code)
                    else:
                        return f'Некоректный код'
                else:
                    return f'Пароли не совпадают.'
            else:
                return f'Пароль некорретный'
    else:
        return f'Введите корректный логин, состоящий из букв русского или латинского алфавита'

def user_authorization():
    # Ввод логина пользователя
    user_login = input('Введите login: \n')
    # Поиск пользователя в базе данных и проверка на корректность введенных данных
    lists = select_on_login(user_login)
    if lists is None:
        # Логин введен неверно
        return f'Введите корректный login'
    else:
        # Логин введен верно
        # Ввод и проверка пароля
        password = input('Введите пароль: \n')
        if password == lists[1]:
            # Пароль введен верно
            return f'Авторизация прошла успешно'
        else:
            # Пароль введен неверно
            return f'Неверный пароль.'

def recovery_pass():
    # Ввод логина пользователя
    user_login = input('Введите login: \n')
    # Создание данных пользователя типа (Password, Login)
    new_param = []
    # Поиск пользователя в базе данных и проверка на корректность введенных данных
    lists = select_on_login(user_login)
    if lists is None:
        return f'Введите корректный login.'
    else:
        # Ввод и проверка кода для восстановления пароля
        code = input('Ввведите четырехзначный код для восстановления пароля: \n')
        if code == lists[2]:
            # Создание и проверка нового пароля
            password_1 = input('Введите новый пароль: \n')
            if password_1.isidentifier():
                password_2 = input('Повторите новый пароль: \n')
                if password_1 == password_2:
                    # Заполнение данных пользователя
                    new_param.append(password_1)
                    new_param.append(user_login)
                    # Вывод результата в виде (Password, Login)
                    return tuple(new_param)
                else:
                    return f'Пароли не совпадают.'
            else:
                return f'Пароль некорретный'
        else:
            return f'Код неверный.'

# Выбор задачи (ввод одного из значений списка(1, 2, 3)):
# 1.регистрация нового пользователя
# 2.авторизация в системе
# 3.восстановление пароля по коду

user_enter = input()
# регистрация нового пользователя
if user_enter == '1':
    user_param = user_registration()
    if len(user_param) == 3 and type(user_param) == tuple:
        # Внесение данных пользователя в таблицу users_data
        cur.execute("""INSERT INTO users_data(Login, Password, Code)
        VALUES (?, ?, ?);""", user_param)
        db_reg.commit()
    else:
        print(user_param)
# авторизация в системе
elif user_enter == '2':
    print(user_authorization())
# восстановление пароля по коду
elif user_enter == '3':
    recovery = recovery_pass()
    if  len(recovery) == 3 and type(recovery) == tuple:
        cur.execute("""UPDATE users_data SET Password = (?) WHERE Login = (?);""", recovery)
        db_reg.commit()
        print('Пароль успешно изменен')
    else:
        print(recovery)
        print('Повторите попытку. Будьте внимательны при вводе данных.')

# Исключаем ввод номера операции, не входящей в список (1, 2, 3)
else:
    print('Данной операции не существует.')

