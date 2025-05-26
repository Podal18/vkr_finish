from PyQt6 import QtCore, QtWidgets

class Ui_ForemanMainWindow(object):
    def setupUi(self, ForemanMainWindow, full_name="Прораб"):
        ForemanMainWindow.setObjectName("ForemanMainWindow")
        ForemanMainWindow.resize(1000, 600)
        ForemanMainWindow.setWindowTitle("Foreman Панель")
        ForemanMainWindow.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        ForemanMainWindow.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.centralwidget = QtWidgets.QWidget(ForemanMainWindow)
        ForemanMainWindow.setCentralWidget(self.centralwidget)

        # Фон
        self.background = QtWidgets.QFrame(self.centralwidget)
        self.background.setGeometry(0, 0, 1000, 600)
        self.background.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #a1c4fd, stop:1 #c2e9fb);
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

        self.projects_btn = self.create_button(self.nav_panel, "Объекты", 70)
        self.projects_btn.clicked.connect(self.open_projects)
        self.staff_btn = self.create_button(self.nav_panel, "Сотрудники объекта", 125)
        self.exit_btn = self.create_button(self.nav_panel, "Выход", 530)

        # Центральная панель
        self.main_area = QtWidgets.QFrame(self.background)
        self.main_area.setGeometry(200, 0, 800, 600)
        self.main_area.setStyleSheet("background-color: rgba(255, 255, 255, 0.95); border-top-right-radius: 10px; border-bottom-right-radius: 10px;")

        self.welcome_label = QtWidgets.QLabel(self.main_area)
        self.welcome_label.setGeometry(40, 20, 700, 40)
        self.welcome_label.setStyleSheet("font-size: 22px; font-weight: 500;")
        self.welcome_label.setText(f"Добро пожаловать, {full_name} (Foreman)")

        self.create_dashboard_card("Объектов", "2", 60, "#c2e9fb")
        self.create_dashboard_card("Работников на объекте", "25", 300, "#d0f4de")
        self.create_dashboard_card("Нарушений", "1", 540, "#ffcdd2")

        # ✕ кнопка
        self.exit_button = QtWidgets.QPushButton(parent=ForemanMainWindow)
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
        self.exit_button.clicked.connect(ForemanMainWindow.close)


    def create_button(self, parent, text, y):
        button = QtWidgets.QPushButton(text, parent)
        button.setGeometry(20, y, 160, 40)
        button.setStyleSheet("""
            QPushButton {
                background-color: #64b5f6;
                color: white;
                border-radius: 20px;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #42a5f5;
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

    def open_projects(self):
        from ui.object_window import ObjectWindow
        self.objwin = ObjectWindow()
        self.objwin.show()



# Пример запуска
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_ForemanMainWindow()
    ui.setupUi(window, full_name="Петров П.П.")
    window.show()
    sys.exit(app.exec())
