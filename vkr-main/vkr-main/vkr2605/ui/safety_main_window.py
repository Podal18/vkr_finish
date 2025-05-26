from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_SafetyMainWindow(object):
    def setupUi(self, SafetyMainWindow, full_name="Инженер ОТ"):
        SafetyMainWindow.setObjectName("SafetyMainWindow")
        SafetyMainWindow.resize(1000, 600)
        SafetyMainWindow.setWindowTitle("Охрана труда")
        SafetyMainWindow.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        SafetyMainWindow.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.centralwidget = QtWidgets.QWidget(SafetyMainWindow)
        SafetyMainWindow.setCentralWidget(self.centralwidget)

        # Фон
        self.background = QtWidgets.QFrame(self.centralwidget)
        self.background.setGeometry(0, 0, 1000, 600)
        self.background.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #dce35b, stop:1 #45b649);
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

        self.docs_btn = self.create_button(self.nav_panel, "Документы", 70)
        self.docs_btn.clicked.connect(self.open_documents)
        self.reports_btn = self.create_button(self.nav_panel, "Отчёты", 125)
        self.reports_btn.clicked.connect(self.open_reports)
        self.exit_btn = self.create_button(self.nav_panel, "Выход", 530)

        # Центральная панель
        self.main_area = QtWidgets.QFrame(self.background)
        self.main_area.setGeometry(200, 0, 800, 600)
        self.main_area.setStyleSheet("background-color: rgba(255, 255, 255, 0.95); border-top-right-radius: 10px; border-bottom-right-radius: 10px;")

        self.welcome_label = QtWidgets.QLabel(self.main_area)
        self.welcome_label.setGeometry(40, 20, 700, 40)
        self.welcome_label.setStyleSheet("font-size: 22px; font-weight: 500;")
        self.welcome_label.setText(f"Добро пожаловать, {full_name} (Инженер ОТ)")

        self.create_dashboard_card("Истекающих медсправок", "5", 60, "#fce38a")
        self.create_dashboard_card("Истекающих допусков", "3", 300, "#f38181")
        self.create_dashboard_card("Инструктажей на сегодня", "12", 540, "#a8edea")

        # ✕ Кнопка
        self.exit_button = QtWidgets.QPushButton(parent=SafetyMainWindow)
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
        self.exit_button.clicked.connect(SafetyMainWindow.close)



    def create_button(self, parent, text, y):
        button = QtWidgets.QPushButton(text, parent)
        button.setGeometry(20, y, 160, 40)
        button.setStyleSheet("""
            QPushButton {
                background-color: #88d498;
                color: white;
                border-radius: 20px;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #5ec576;
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

    def open_reports(self):
        from ui.report_window import ReportWindow
        self.report_window = ReportWindow()
        self.report_window.show()

    def open_documents(self):
        from ui.document_window import DocumentWindow
        self.docwin = DocumentWindow()
        self.docwin.show()



# Пример запуска
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_SafetyMainWindow()
    ui.setupUi(window, full_name="Ильин Роман")
    window.show()
    sys.exit(app.exec())
