from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import QtCore, QtGui, QtWidgets


class AddEditObjectWindow(QtWidgets.QMainWindow):
    def __init__(self, mode="add", parent=None):
        super().__init__(parent)
        self.ui = Ui_AddEditObjectWindow()
        self.ui.setupUi(self, mode)
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)

        # Подключение кнопок
        self.ui.save_button.clicked.connect(self.save_object)
        self.ui.cancel_button.clicked.connect(self.close)



    def save_object(self):
        # Логика сохранения (аналогично сотрудникам)
        if self.validate():
            print("Объект сохранен")  # Заменить на реальное сохранение
            self.close()

    def validate(self):
        # Проверка заполнения полей
        if not self.ui.name_input.text().strip():
            self.show_error("Укажите название объекта")
            return False
        return True

    def show_error(self, text):
        msg = QtWidgets.QMessageBox(self)
        msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        msg.setText(text)
        msg.setWindowTitle("Ошибка")
        msg.exec()


class Ui_AddEditObjectWindow(object):
    def setupUi(self, AddEditObjectWindow, mode="add"):
        AddEditObjectWindow.setObjectName("AddEditObjectWindow")
        AddEditObjectWindow.resize(500, 450)
        AddEditObjectWindow.setWindowTitle("Добавить объект" if mode == "add" else "Редактировать объект")
        AddEditObjectWindow.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        AddEditObjectWindow.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.centralwidget = QtWidgets.QWidget(AddEditObjectWindow)
        AddEditObjectWindow.setCentralWidget(self.centralwidget)

        self.background = QtWidgets.QFrame(self.centralwidget)
        self.background.setGeometry(0, 0, 500, 450)
        self.background.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #a1c4fd, stop:1 #c2e9fb);
                border-radius: 10px;
            }
        """)

        # ✕ Кнопка
        self.exit_button = QtWidgets.QPushButton(parent=AddEditObjectWindow)
        self.exit_button.setGeometry(QtCore.QRect(460, 10, 30, 30))
        self.exit_button.setText("✕")
        self.exit_button.setStyleSheet("""
            QPushButton {
                background: none;
                border: none;
                font-size: 18px;
                color: white;
            }
            QPushButton:hover {
                color: #ffdddd;
            }
        """)
        self.exit_button.clicked.connect(AddEditObjectWindow.close)


        # Заголовок
        self.title_label = QtWidgets.QLabel(self.background)
        self.title_label.setGeometry(30, 20, 440, 40)
        self.title_label.setText("Добавить объект" if mode == "add" else "Редактировать объект")
        self.title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: white;")

        # Поля
        self.name_input = self.create_input("Название объекта", 90)
        self.address_input = self.create_input("Адрес объекта", 150)

        self.foreman_combo = QtWidgets.QComboBox(self.background)
        self.foreman_combo.setGeometry(50, 210, 400, 40)
        self.foreman_combo.setStyleSheet(self.input_style())
        # self.foreman_combo.addItems(["Прораб 1", "Прораб 2"])  # добавим позже из БД

        # Кнопки
        self.save_button = QtWidgets.QPushButton("💾 Сохранить", self.background)
        self.save_button.setGeometry(80, 300, 150, 50)

        self.cancel_button = QtWidgets.QPushButton("❌ Отмена", self.background)
        self.cancel_button.setGeometry(270, 300, 150, 50)

        for btn in [self.save_button, self.cancel_button]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #7da2f2;
                    color: white;
                    border-radius: 20px;
                    font-size: 15px;
                }
                QPushButton:hover {
                    background-color: #5c8ee6;
                }
            """)



    def create_input(self, placeholder, y):
        input_field = QtWidgets.QLineEdit(self.background)
        input_field.setGeometry(50, y, 400, 40)
        input_field.setPlaceholderText(placeholder)
        input_field.setStyleSheet(self.input_style())
        return input_field

    def input_style(self):
        return """
            QLineEdit, QComboBox {
                border: 2px solid #b0d4ff;
                border-radius: 20px;
                background-color: white;
                padding: 10px;
                font-size: 15px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #7da2f2;
            }
        """




if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = AddEditObjectWindow(mode="add")
    window.show()
    app.exec()
