from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_ObjectProfileWindow(object):
    def setupUi(self, ObjectProfileWindow):
        ObjectProfileWindow.setObjectName("ObjectProfileWindow")
        ObjectProfileWindow.resize(800, 600)
        ObjectProfileWindow.setWindowTitle("Профиль объекта")
        ObjectProfileWindow.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        ObjectProfileWindow.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.centralwidget = QtWidgets.QWidget(ObjectProfileWindow)
        ObjectProfileWindow.setCentralWidget(self.centralwidget)

        self.background = QtWidgets.QFrame(self.centralwidget)
        self.background.setGeometry(0, 0, 800, 600)
        self.background.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #a1c4fd, stop:1 #c2e9fb);
                border-radius: 10px;
            }
        """)

        # ✕ Кнопка
        self.exit_button = QtWidgets.QPushButton(parent=ObjectProfileWindow)
        self.exit_button.setGeometry(QtCore.QRect(760, 10, 30, 30))
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
        self.exit_button.clicked.connect(ObjectProfileWindow.close)

        self.back_button = QtWidgets.QPushButton("←", self.background)
        self.back_button.setGeometry(30, 550, 60, 40)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #333;
                font-size: 14px;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        # Поведение по умолчанию: просто закрытие окна
        

        # Заголовок
        self.title_label = QtWidgets.QLabel(self.background)
        self.title_label.setGeometry(30, 20, 600, 40)
        self.title_label.setText("Профиль объекта")
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")

        # Блок информации
        self.info_frame = QtWidgets.QFrame(self.background)
        self.info_frame.setGeometry(30, 80, 740, 120)
        self.info_frame.setStyleSheet("background-color: rgba(255,255,255,0.9); border-radius: 10px;")

        self.name_label = QtWidgets.QLabel("Название:", self.info_frame)
        self.name_label.setGeometry(20, 20, 150, 25)
        self.name_label.setStyleSheet("font-weight: bold;")
        self.name_value = QtWidgets.QLabel("", self.info_frame)
        self.name_value.setGeometry(180, 20, 500, 25)

        self.address_label = QtWidgets.QLabel("Адрес:", self.info_frame)
        self.address_label.setGeometry(20, 50, 150, 25)
        self.address_label.setStyleSheet("font-weight: bold;")
        self.address_value = QtWidgets.QLabel("", self.info_frame)
        self.address_value.setGeometry(180, 50, 500, 25)

        self.foreman_label = QtWidgets.QLabel("Прораб:", self.info_frame)
        self.foreman_label.setGeometry(20, 80, 150, 25)
        self.foreman_label.setStyleSheet("font-weight: bold;")
        self.foreman_value = QtWidgets.QLabel("", self.info_frame)
        self.foreman_value.setGeometry(180, 80, 500, 25)

        # Заголовок таблицы
        self.staff_title = QtWidgets.QLabel(self.background)
        self.staff_title.setGeometry(30, 220, 600, 30)
        self.staff_title.setText("Сотрудники, прикреплённые к объекту")
        self.staff_title.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")

        # Таблица сотрудников
        self.staff_table = QtWidgets.QTableWidget(self.background)
        self.staff_table.setGeometry(30, 260, 740, 280)
        self.staff_table.setColumnCount(3)
        self.staff_table.setHorizontalHeaderLabels(["ФИО", "Профессия", "Допущен?"])
        self.staff_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.staff_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.staff_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border-radius: 10px;
            }
            QHeaderView::section {
                background-color: #b0d4ff;
                padding: 4px;
                font-weight: bold;
                border: 1px solid white;
            }
        """)

# Пример запуска
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_ObjectProfileWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec())
