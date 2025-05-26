from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_EmployeeProfileWindow(object):
    def setupUi(self, EmployeeProfileWindow):
        EmployeeProfileWindow.setObjectName("EmployeeProfileWindow")
        EmployeeProfileWindow.resize(800, 600)
        EmployeeProfileWindow.setWindowTitle("Профиль сотрудника")
        EmployeeProfileWindow.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        EmployeeProfileWindow.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.centralwidget = QtWidgets.QWidget(EmployeeProfileWindow)
        EmployeeProfileWindow.setCentralWidget(self.centralwidget)

        self.background = QtWidgets.QFrame(self.centralwidget)
        self.background.setGeometry(0, 0, 800, 600)
        self.background.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffdde1, stop:1 #ee9ca7);
                border-radius: 10px;
            }
        """)

        # ✕ Кнопка
        self.exit_button = QtWidgets.QPushButton(parent=EmployeeProfileWindow)
        self.exit_button.setGeometry(QtCore.QRect(760, 10, 30, 30))
        self.exit_button.setObjectName("exit_button")
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
        self.exit_button.clicked.connect(EmployeeProfileWindow.close)

        # Заголовок
        self.title_label = QtWidgets.QLabel(self.background)
        self.title_label.setGeometry(30, 20, 600, 40)
        self.title_label.setText("Профиль сотрудника")
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")

        # Вкладки
        self.tab_widget = QtWidgets.QTabWidget(self.background)
        self.tab_widget.setGeometry(30, 80, 740, 480)
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: white;
                border-radius: 10px;
            }
            QTabBar::tab {
                background: #ffb6c1;
                padding: 10px;
                border-radius: 10px;
                margin: 2px;
            }
            QTabBar::tab:selected {
                background: #ff9a9e;
                color: white;
            }
        """)

        # Вкладка 1 — Личные данные
        self.tab_info = QtWidgets.QWidget()
        self.tab_widget.addTab(self.tab_info, "📋 Личные данные")

        self.name_label = QtWidgets.QLabel("ФИО:", self.tab_info)
        self.name_label.setGeometry(30, 30, 200, 30)
        self.name_value = QtWidgets.QLabel("", self.tab_info)
        self.name_value.setGeometry(250, 30, 400, 30)

        self.birth_label = QtWidgets.QLabel("Дата рождения:", self.tab_info)
        self.birth_label.setGeometry(30, 70, 200, 30)
        self.birth_value = QtWidgets.QLabel("", self.tab_info)
        self.birth_value.setGeometry(250, 70, 400, 30)

        self.profession_label = QtWidgets.QLabel("Профессия:", self.tab_info)
        self.profession_label.setGeometry(30, 110, 200, 30)
        self.profession_value = QtWidgets.QLabel("", self.tab_info)
        self.profession_value.setGeometry(250, 110, 400, 30)

        self.status_label = QtWidgets.QLabel("Статус:", self.tab_info)
        self.status_label.setGeometry(30, 150, 200, 30)
        self.status_value = QtWidgets.QLabel("", self.tab_info)
        self.status_value.setGeometry(250, 150, 400, 30)

        # Вкладка 2 — Документы
        self.tab_docs = QtWidgets.QWidget()
        self.tab_widget.addTab(self.tab_docs, "📎 Документы")

        self.docs_table = QtWidgets.QTableWidget(self.tab_docs)
        self.docs_table.setGeometry(20, 20, 700, 400)
        self.docs_table.setColumnCount(3)
        self.docs_table.setHorizontalHeaderLabels(["Тип документа", "Срок действия", "Статус"])
        self.docs_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.docs_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

        # Вкладка 3 — Объекты
        self.tab_projects = QtWidgets.QWidget()
        self.tab_widget.addTab(self.tab_projects, "🏗 Объекты")

        self.project_list = QtWidgets.QListWidget(self.tab_projects)
        self.project_list.setGeometry(20, 20, 700, 400)

        # Вкладка 4 — Нарушения
        self.tab_violations = QtWidgets.QWidget()
        self.tab_widget.addTab(self.tab_violations, "⚠ Нарушения")

        self.violations_table = QtWidgets.QTableWidget(self.tab_violations)
        self.violations_table.setGeometry(20, 20, 700, 400)
        self.violations_table.setColumnCount(3)
        self.violations_table.setHorizontalHeaderLabels(["Дата", "Тип нарушения", "Комментарий"])
        self.violations_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)


# Пример запуска
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_EmployeeProfileWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec())
