import sqlite3
import sys
import random as rnd

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QTableWidgetItem



class MainWindow(QDialog):

    currentSessionName = ""
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("1.ui", self)
        self.signup_btn.clicked.connect(self.openSignUpScreen)
        self.login_btn.clicked.connect(self.login)

    def login(self):  # Функция кнопки Войти
        username = self.usernameField.text()
        password = self.passwordField.text()

        if len(username) == 0 or len(password) == 0:
            self.error_label.setText("Введите значения!")
            print("Введите значения!")
        else:
            con = sqlite3.connect('users_db.db')
            cur = con.cursor()

            try:
                cur.execute("SELECT password FROM users WHERE username = '%s'" % username)
                result = cur.fetchone()[0]
                if password == result:
                    self.currentSessionName = username
                    gameMenuScreen.username_label.setText(username)
                    print(self.currentSessionName)
                    self.error_label.setText("")
                    print("Вы успешно зашли!")
                    con.close()
                    self.openGameMenuScreen()  # Переход в основное меню игры
                else:
                    self.error_label.setText("Вы ввели неверный пароль!")
                    print("Вы ввели неверный пароль")

            except TypeError:
                self.error_label.setText("Вы ввели несущствующее имя пользователя!")
                print("Вы ввели несущствующее имя пользователя")
                con.close()

    def openSignUpScreen(self):
        widget.setCurrentIndex(1)

    def openGameMenuScreen(self):
        widget.setCurrentIndex(2)

class SignupScreen(QDialog):
    def __init__(self):
        super(SignupScreen, self).__init__()
        loadUi("2.ui", self)
        self.signup_btn_2.clicked.connect(self.signUp)

    def signUp(self):  # Функция кнопка Зарегистрироваться
        username = self.usernameField_2.text()
        password = self.passwordField_2.text()

        if len(username) == 0 or len(password) == 0:
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
        loadUi("gamemenu_screen.ui", self)
        self.logout_bth.clicked.connect(self.logout)
        self.startGame_btn.clicked.connect(self.openGameScreen)
        self.liderboard_btn.clicked.connect(self.openLiderboardScreen)

    def logout(self):
        widget.setCurrentIndex(0)
        mainwindow.currentSessionName = ""

    def openGameScreen(self):
        widget.setCurrentIndex(3)

    def openLiderboardScreen(self):
        liderboardScreen.makeTable()
        widget.setCurrentIndex(4)



class GameScreen(QDialog):
    n_attempts = 0
    attempt = 0
    num = 0
    lowBorder = 0
    topBorder = 0

    def __init__(self):
        super(GameScreen, self).__init__()
        loadUi("game_screen.ui", self)
        self.startGame_btn_2.clicked.connect(self.startGame)

    def startGame(self):
        print(mainwindow.currentSessionName)
        a = self.spinBox_left.text()  # нижняя граница
        self.lowBorder = int(a)
        b = self.spinBox_right.text()
        self.topBorder = int(b)  # вернхяя граница

        self.n_attempts = 5
        print(self.lowBorder)
        print(self.topBorder)

        self.num = rnd.randint(self.lowBorder, self.topBorder)
        print(self.num)

        self.attempt = 1

        self.answer_btn.clicked.connect(self.answer)

    def answer(self):
        if self.attempt <= self.n_attempts:
            answer = self.answer_line.text()
            n = int(answer)
            if n < self.num:
                print("Заданное число меньше")
                self.textBrowser.append("Число {} меньше загаданного".format(n))
                attempt = self.n_attempts - self.attempt
                self.attempts_label.setText("Попыток: {}".format(attempt))
                self.attempt += 1
                # тепло или холодно число окрашивается в соот цвет и заносится в историю
            elif n > self.num:
                print("Заданное число больше")
                self.textBrowser.append("Число {} больше загаданного".format(n))
                attempt = self.n_attempts - self.attempt
                self.attempts_label.setText("Попыток: {}".format(attempt))
                self.attempt += 1
                # тепло или холодно число окрашивается в соот цвет и заносится в историю
            else:
                print("Вы угадали. Игра закончена")
                self.textBrowser.append("Вы угадали. Игра закончена")
                self.scores()
        else:
            print("Попытки закончились. Игра закончена")
            self.textBrowser.append("Попытки закончились. Игра закончена")
            self.scores()

    def scores(self):
        print(mainwindow.currentSessionName)
        con = sqlite3.connect('users_db.db')
        cur = con.cursor()

        radius = (self.topBorder - self.lowBorder) + 1
        score = 100 * (radius / self.attempt)
        print(score)

        cur.execute("UPDATE liderboard SET Score=Score + ?, games=games + 1 WHERE username = ?",
                    (score, mainwindow.currentSessionName))
        con.commit()
        con.close()


class LiderboardScreen(QDialog):
    def __init__(self):
        super(LiderboardScreen, self).__init__()
        loadUi("liderboard_screen.ui", self)


    def makeTable(self):
        con = sqlite3.connect('users_db.db')
        cur = con.cursor()
        cur.execute("SELECT Count(*) FROM liderboard")
        result = cur.fetchone()[0]
        print(result)

        self.tableWidget.clear()
        self.tableWidget.setColumnCount(3)
        #self.tableWidget.setRowCount(result)
        self.tableWidget.setHorizontalHeaderLabels(["Имя", "Очки", "Кол-во игр"])

        for username, Score, games in cur.execute("SELECT username, Score, games FROM liderboard"):
            row = self.tableWidget.rowCount()
            self.tableWidget.setRowCount(row + 1)

            self.tableWidget.setItem(row, 0, QTableWidgetItem(username))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(Score)))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(str(games)))





if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    widget = QStackedWidget()

    mainwindow = MainWindow()
    widget.addWidget(mainwindow)

    signupScreen = SignupScreen()
    widget.addWidget(signupScreen)

    gameMenuScreen = GameMenu()
    widget.addWidget(gameMenuScreen)

    gameScreen = GameScreen()
    widget.addWidget(gameScreen)

    liderboardScreen = LiderboardScreen()
    widget.addWidget(liderboardScreen)

    widget.resize(500, 500)
    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Выход")
