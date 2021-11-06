import sqlite3
import sys

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QMainWindow

#grhrh
class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("1.ui",self)
        self.signup_btn.clicked.connect(self.openSignUpScreen)
        self.login_btn.clicked.connect(self.login)

    def login(self):  # Функция кнопки Войти
        username = self.usernameField.text()
        password = self.passwordField.text()

        if len(username)==0 or len(password)==0:
            self.error_label.setText("Введите значения!")
            print("Введите значения!")
        else:
            con = sqlite3.connect('users_db.db')
            cur = con.cursor()

            try:
                cur.execute("SELECT password FROM users WHERE username = '%s'" % username)
                result = cur.fetchone()[0]
                if password == result:
                    global currentSessionName
                    currentSessionName = username
                    self.error_label.setText("Вы успешно зашли!")
                    print("Вы успешно зашли!")
                    con.close()
                    # Переход в основное меню игры
                else:
                    self.error_label.setText("Вы ввели неверный пароль!")
                    print("Вы ввели неверный пароль")

            except TypeError:
                self.error_label.setText("Вы ввели несущствующее имя пользователя!")
                print("Вы ввели несущствующее имя пользователя")
                con.close()



    def openSignUpScreen(self):
        signupScreen = SignupScreen()
        widget.addWidget(signupScreen)
        widget.setCurrentIndex(widget.currentIndex()+1)


class SignupScreen(QDialog):
    def __init__(self):
        super(SignupScreen, self).__init__()
        loadUi("2.ui",self)
        self.signup_btn_2.clicked.connect(self.signUp)

    def signUp(self):  # Функция кнопка Зарегистрироваться
        username = self.usernameField_2.text()
        password = self.passwordField_2.text()

        if len(username)==0 or len(password)==0:
            self.error_label_2.setText("Введите значения!")
            print("Введите значения!")
        else:
            con = sqlite3.connect('users_db.db')
            cur = con.cursor()

            try:
                cur.execute("INSERT INTO users VALUES (?, ?)", (username, password))
                cur.execute("INSERT INTO liderboard VALUES (?, ?, ?)", (username, 0, 0))

                for row in cur.execute('SELECT * FROM users ORDER BY username'):
                    print(row)
                for row in cur.execute('SELECT * FROM liderboard ORDER BY username'):
                    print(row)
                con.commit()
                con.close()
                widget.setCurrentIndex(widget.currentIndex() - 1)

            except sqlite3.IntegrityError:
                print("Данное имя пользователя уже используется!")
                self.error_label_2.setText("Вы ввели сущствующее имя пользователя!")

class GameMenu(QDialog):
    def __init__(self):
        super(GameMenu, self).__init__()
        loadUi("")


app = QApplication(sys.argv)
widget = QStackedWidget()

mainwindow = MainWindow()
widget.addWidget(mainwindow)
widget.resize(500,500)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Выход")