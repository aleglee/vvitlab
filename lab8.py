import sys
import psycopg2
from psycopg2.extras import execute_values

from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                             QTableWidgetItem, QPushButton, QMessageBox, QButtonGroup)


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self._connect_to_db()

        self.setWindowTitle("Shedule")

        self.vbox = QVBoxLayout(self)

        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)

        self._create_shedule_tab()

    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="timetable",
                                     user="postgres",
                                     password="1940",
                                     host="localhost",
                                     port="5432")

        self.cursor = self.conn.cursor()

    def _create_shedule_tab(self):
        self.shedule_tab = QWidget()
        self.teacher_tab = QWidget()
        self.subject_tab = QWidget()
        self.tabs.addTab(self.shedule_tab, "Timetable")
        self.tabs.addTab(self.teacher_tab, "Teachers")
        self.tabs.addTab(self.subject_tab, "Subjects")

        self.update_shedule_button = QPushButton("Update")

        self.svbox_day = QVBoxLayout()
        self.svbox_teachers = QVBoxLayout()
        self.svbox_subjects = QVBoxLayout()

        self.days_buttons = [[], [], [], [], []]

        # Timetable
        # -------------------------------------
        self.days = self.create_table_days()

        self.tables_days = self._create_day_table()

        for i in range(len(self.tables_days)):
            self._update_day_table(i)
        # -------------------------------------

        # Teachers
        # -------------------------------------
        self.teachers = self.create_table_teachers()

        self.tables_teachers = self._create_teacher_table()

        for i in range(len(self.tables_teachers)):
            self._update_teacher_table(i)
        # -------------------------------------

        # Subjects
        # -------------------------------------
        self.subjects = self.create_table_subjects()

        self.tables_subjects = self._create_subject_table()

        for i in range(len(self.tables_subjects)):
            self._update_subject_table(i)
        # -------------------------------------
        # self.shbox_mon1.addWidget(self.gbox_mon)

        # self.shbox_mon2.addWidget(self.update_shedule_button)

        # self.gbox_mon.setLayout(self._create_day_table(1))

        # self.gbox_tue.setLayout(self._create_day_table(2))

        # self.update_shedule_button = QPushButton("Update")
        # self.shbox2.addWidget(self.update_shedule_button)
        self.update_shedule_button.clicked.connect(self._update_shedule)

        self.shedule_tab.setLayout(self.svbox_day)
        self.teacher_tab.setLayout(self.svbox_teachers)
        self.subject_tab.setLayout(self.svbox_subjects)

    def create_table_subjects(self):
        subjects = []
        for subject in range(1, 10):
            gbox = QGroupBox(f'Subject {subject}')
            shbox1 = QHBoxLayout()
            shbox2 = QHBoxLayout()

            shbox1.addWidget(gbox)
            self.svbox_subjects.addLayout(shbox1)
            self.svbox_subjects.addLayout(shbox2)
            subjects.append(gbox)
        return subjects

    def _create_subject_table(self):
        tables = []
        for i in range(0, 9):
            table = QTableWidget()
            table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(["Class", "Subject", "Subject_type", ""])

            mvbox = QVBoxLayout()
            mvbox.addWidget(table)
            # self.gbox_mon.setLayout(self.mvbox_monday)
            self.subjects[i].setLayout(mvbox)
            tables.append(table)
        return tables

    def _update_subject_table(self, x):
        self.cursor.execute(f"SELECT * FROM class WHERE subject={x}")
        records = list(self.cursor.fetchall())

        # self.monday_table.setRowCount(len(records) + 1)
        self.tables_subjects[x-1].setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")

            self.tables_subjects[x-1].setItem(i, 0,
                                          QTableWidgetItem(str(r[0])))
            self.tables_subjects[x-1].setItem(i, 1,
                                          QTableWidgetItem(str(r[1])))
            self.tables_subjects[x-1].setItem(i, 2,
                                          QTableWidgetItem(str(r[2])))
            self.tables_subjects[x-1].setCellWidget(i, 3, joinButton)

            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_table(num, x, 3))

        self.tables_subjects[x-1].resizeRowsToContents()

    def create_table_teachers(self):
        teachers = []
        for teacher in range(1, 14):
            gbox = QGroupBox(f'Teacher {teacher}')
            shbox1 = QHBoxLayout()
            shbox2 = QHBoxLayout()

            shbox1.addWidget(gbox)
            self.svbox_teachers.addLayout(shbox1)
            self.svbox_teachers.addLayout(shbox2)
            teachers.append(gbox)
        return teachers

    def _create_teacher_table(self):
        tables = []
        for i in range(0, 13):
            table = QTableWidget()
            table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(["Subject", "Teacher", "Class", ""])

            mvbox = QVBoxLayout()
            mvbox.addWidget(table)
            # self.gbox_mon.setLayout(self.mvbox_monday)
            self.teachers[i].setLayout(mvbox)
            tables.append(table)
        return tables

    def _update_teacher_table(self, x):
        self.cursor.execute(f"SELECT * FROM teacher_subject WHERE teacher={x}")
        records = list(self.cursor.fetchall())

        # self.monday_table.setRowCount(len(records) + 1)
        self.tables_teachers[x-1].setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")

            self.tables_teachers[x-1].setItem(i, 0,
                                          QTableWidgetItem(str(r[0])))
            self.tables_teachers[x-1].setItem(i, 1,
                                          QTableWidgetItem(str(r[1])))
            self.tables_teachers[x-1].setItem(i, 2,
                                          QTableWidgetItem(str(r[2])))
            self.tables_teachers[x-1].setCellWidget(i, 3, joinButton)

            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_table(num, x, 2))

        self.tables_teachers[x-1].resizeRowsToContents()

    def create_table_days(self):
        days = []
        for day in range(1, 6):
            if day == 1: text = 'Понедельник'
            if day == 2: text = 'Вторник'
            if day == 3: text = 'Среда'
            if day == 4: text = 'Четверг'
            if day == 5: text = 'Пятница'
            gbox = QGroupBox(text)
            shbox1 = QHBoxLayout()
            shbox2 = QHBoxLayout()

            shbox1.addWidget(gbox)
            self.svbox_day.addLayout(shbox1)
            self.svbox_day.addLayout(shbox2)
            days.append(gbox)
        return days

    def _create_day_table(self):
        tables = []
        for i in range(0, 5):
            table = QTableWidget()
            table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

            table.setColumnCount(7)
            table.setHorizontalHeaderLabels(["Subject", "Week", "Day", "Class", "Time", "Room", ""])

            mvbox = QVBoxLayout()
            mvbox.addWidget(table)
            # self.gbox_mon.setLayout(self.mvbox_monday)
            self.days[i].setLayout(mvbox)
            tables.append(table)
        return tables

    def create_buttons(self, x):
        b = []
        for i in range(x):
            b.append(QPushButton('Join'))
        return b

    def _update_day_table(self, x):
        a = []
        self.cursor.execute(f"SELECT * FROM timetable WHERE day={x}")
        records = list(self.cursor.fetchall())

            # self.monday_table.setRowCount(len(records) + 1)
        self.tables_days[x-1].setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            self.days_buttons[x - 1] = self.create_buttons(len(records))

            self.tables_days[x-1].setItem(i, 0,
                                          QTableWidgetItem(str(r[0])))
            self.tables_days[x-1].setItem(i, 1,
                                          QTableWidgetItem(str(r[1])))
            self.tables_days[x-1].setItem(i, 2,
                                          QTableWidgetItem(str(r[2])))
            self.tables_days[x-1].setItem(i, 3,
                                          QTableWidgetItem(str(r[3])))
            self.tables_days[x-1].setItem(i, 4,
                                          QTableWidgetItem(str(r[4])))
            self.tables_days[x-1].setItem(i, 5,
                                          QTableWidgetItem(str(r[5])))
            self.tables_days[x-1].setCellWidget(i, 6, joinButton)


            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_table(num, x, 1))
            #try:
                #for z in range(len(self.days_buttons[0])):
                    #self.days_buttons[0][z].clicked.connect(lambda ch, num=i: self._change_day_from_table(num, 1))
                #for z in range(len(self.days_buttons[1])):
                    #self.days_buttons[1][z].clicked.connect(lambda ch, num=i: self._change_day_from_table(num, 2))
                #for z in range(len(self.days_buttons[2])):
                    #self.days_buttons[1][z].clicked.connect(lambda ch, num=i: self._change_day_from_table(num, 3))
                #for z in range(len(self.days_buttons[3])):
                    #self.days_buttons[1][z].clicked.connect(lambda ch, num=i: self._change_day_from_table(num, 4))
                #for z in range(len(self.days_buttons[4])):
                    #self.days_buttons[1][z].clicked.connect(lambda ch, num=i: self._change_day_from_table(num, 5))
                #except:
                    #pass
            self.tables_days[x-1].resizeRowsToContents()



    def _change_day_from_table(self, rowNum, day, table):
        # rowNum - номер строки
        row = list()
        if table == 1:
            for i in range(self.tables_days[day-1].columnCount()):
                try:
                    row.append(self.tables_days[day-1].item(rowNum, i).text())
                except:
                    row.append(None)
            print(row)

            try:
                self.cursor.execute(f"UPDATE timetable SET week = {row[1]} WHERE id = {row[0]}")
                self.cursor.execute(f"UPDATE timetable SET day = {row[2]} WHERE id = {row[0]}")
                self.cursor.execute(f"UPDATE timetable SET class = {row[3]} WHERE id = {row[0]}")
                self.cursor.execute(f"UPDATE timetable SET class_time = {row[4]} WHERE id = {row[0]}")
                self.cursor.execute(f"UPDATE timetable SET room_number = '{row[5]}' WHERE id = {row[0]}")
                self.conn.commit()
            except Exception as exc:
                QMessageBox.about(self, "Error", "Enter all fields")

        if table == 2:
            for i in range(self.tables_teachers[day-1].columnCount()):
                try:
                    row.append(self.tables_teachers[day-1].item(rowNum, i).text())
                except:
                    row.append(None)
            print(row)

            try:
                pass
                self.cursor.execute(f"UPDATE teacher_subject SET id = {row[0]} WHERE teacher = {row[1]}")
                self.cursor.execute(f"UPDATE teacher_subject SET class = {row[2]} WHERE teacher = {row[1]}")
                self.conn.commit()
            except Exception as exc:
                print(exc)
                QMessageBox.about(self, "Error", "Enter all fields")

        if table == 3:
            for i in range(self.tables_subjects[day - 1].columnCount()):
                try:
                    row.append(self.tables_subjects[day - 1].item(rowNum, i).text())
                except:
                    row.append(None)
            print(row)

            try:
                pass
                self.cursor.execute(f"UPDATE class SET id = {row[0]} WHERE subject = {row[1]}")
                self.cursor.execute(f"UPDATE class SET subject_type = {row[2]} WHERE subject = {row[1]}")
                self.conn.commit()
            except Exception as exc:
                print(exc)
                QMessageBox.about(self, "Error", "Enter all fields")



    def _update_shedule(self):
        pass
        # self._update_monday_table()



app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())