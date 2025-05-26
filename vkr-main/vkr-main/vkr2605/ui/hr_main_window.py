from PyQt6 import QtWidgets, QtCore

class Ui_HRMainWindow(object):
    def setupUi(self, HRMainWindow, full_name="HR-специалист"):
        HRMainWindow.setObjectName("HRMainWindow")
        HRMainWindow.resize(1000, 600)
        HRMainWindow.setWindowTitle("HR Панель")
        HRMainWindow.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        HRMainWindow.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        # Центральный виджет
        self.centralwidget = QtWidgets.QWidget(HRMainWindow)
        HRMainWindow.setCentralWidget(self.centralwidget)

        # Фон
        self.background = QtWidgets.QFrame(self.centralwidget)
        self.background.setGeometry(0, 0, 1000, 600)
        self.background.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ff9a9e, stop:1 #fad0c4);
                border-radius: 10px;
            }
        """)

        # Навигационная панель
        self.nav_panel = QtWidgets.QFrame(self.background)
        self.nav_panel.setGeometry(0, 0, 200, 600)
        self.nav_panel.setStyleSheet("background-color: rgba(255, 255, 255, 0.95); border-top-left-radius: 10px; border-bottom-left-radius: 10px;")

        self.title = QtWidgets.QLabel("Навигация", self.nav_panel)
        self.title.setGeometry(20, 20, 160, 30)
        self.title.setStyleSheet("font-size: 18px; font-weight: bold;")

        # Кнопки
        self.employee_btn = self.create_button(self.nav_panel, "Сотрудники", 70)
        self.assignments_btn = self.create_button(self.nav_panel, "История", 125)
        self.exit_btn = self.create_button(self.nav_panel, "Выход", 530)

        self.employee_btn.clicked.connect(self.open_employees)
        self.assignments_btn.clicked.connect(self.open_logs)

        # Основная зона
        self.main_area = QtWidgets.QFrame(self.background)
        self.main_area.setGeometry(200, 0, 800, 600)
        self.main_area.setStyleSheet("background-color: rgba(255, 255, 255, 0.95); border-top-right-radius: 10px; border-bottom-right-radius: 10px;")

        # Приветствие
        self.welcome_label = QtWidgets.QLabel(self.main_area)
        self.welcome_label.setGeometry(40, 20, 700, 40)
        self.welcome_label.setStyleSheet("font-size: 22px; font-weight: 500;")
        self.welcome_label.setText(f"Добро пожаловать, {full_name} (HR)")

        # Дашборд-индикаторы
        self.dashboard_cards = []

        self.create_dashboard_card("Сотрудников", "132", 60, "#ffb6b9")
        self.create_dashboard_card("Просроченные документы", "8", 230, "#fcd5ce")
        self.create_dashboard_card("Активных проектов", "5", 400, "#b5ead7")
        self.create_dashboard_card("Нарушений", "3", 570, "#f9dc5c")

        # Кнопка ✕ (в правом верхнем углу)
        self.exit_button = QtWidgets.QPushButton(parent=HRMainWindow)
        self.exit_button.setGeometry(QtCore.QRect(960, 10, 30, 30))
        self.exit_button.setObjectName("exit_button")
        self.exit_button.setText("✕")
        self.exit_button.setStyleSheet("""
            QPushButton {
                background: none;
                border: none;
                font-size: 18px;
                color: #ff9a9e;
            }
            QPushButton:hover {
                color: #ffdddd;
            }
        """)
        self.exit_button.clicked.connect(HRMainWindow.close)


    def create_button(self, parent, text, y):
        button = QtWidgets.QPushButton(text, parent)
        button.setGeometry(20, y, 160, 40)
        button.setStyleSheet("""
            QPushButton {
                background-color: #ff9a9e;
                color: white;
                border-radius: 20px;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #e55b50;
            }
        """)
        return button

    def create_dashboard_card(self, title, value, x, color):
        card = QtWidgets.QFrame(self.main_area)
        card.setGeometry(x, 100, 180, 120)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 15px;
            }}
        """)
        label_title = QtWidgets.QLabel(title, card)
        label_title.setGeometry(10, 10, 160, 30)
        label_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")
        label_value = QtWidgets.QLabel(value, card)
        label_value.setGeometry(10, 50, 160, 50)
        label_value.setStyleSheet("font-size: 32px; font-weight: bold; color: #222;")
        self.dashboard_cards.append(card)

    def open_employees(self):
        from ui.employee_window import EmployeeWindow
        self.employee_window = EmployeeWindow()
        self.employee_window.show()



    def open_logs(self):
        from ui.log_window import LogWindow
        self.logwin = LogWindow()
        self.logwin.show()



# Пример запуска
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_HRMainWindow()
    ui.setupUi(window, full_name="Иванова Елена")
    window.show()
    sys.exit(app.exec())