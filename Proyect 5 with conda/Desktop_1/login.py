import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,QMessageBox, QCheckBox)
from PyQt6.QtGui import QFont,QPixmap


class Login(QWidget):
  
  def __init__(self) :
    super().__init__()
    self.initiation_UI()
  
  #Window . Dimensions, background color, and generate a form that has all the funtions.
  def initiation_UI(self):
    self.setGeometry(725,300,350,250)
    self.setWindowTitle('Тренажер дыхания')
    self.setStyleSheet("background-color:#caf0f8;")
    self.generate_formulary()
    self.show()
    
  def generate_formulary(self):
    self.is_logged = False
    
    #target one
    self.label = QLabel(self)
    self.label.setGeometry(185,5,200,50) #left, top, width, height
    self.label.setText('Вход')
    
    #User label
    user_label = QLabel(self)
    user_label.setText("Элек.почта: ")
    user_label.setFont(QFont('Arial', 10))
    user_label.move(20,54)    
    
    
    self.user_input = QLineEdit(self)
    self.user_input.resize(250, 24)
    self.user_input.move(90,50)
    
    #Password label
    password_label = QLabel(self)
    password_label.setText("Пароль: ")
    password_label.setFont(QFont('Arial', 10))
    password_label.move(20,86)
    
    
    self.password_input = QLineEdit(self)
    self.password_input.resize(250, 24)
    self.password_input.move(90,82)
    self.password_input.setEchoMode(
      QLineEdit.EchoMode.Password
      )
    
    #look password
    self.check_view_passwor = QCheckBox(self)
    self.check_view_passwor.setText("см. пароль")
    self.check_view_passwor.move(90,110)
    self.check_view_passwor.clicked.connect(self.show_password)
    
    #target two if need a registration
    self.label = QLabel(self)
    self.label.setGeometry(95,130,100,50) #left, top, width, height
    self.label.setText('У вас нет аккаунта?')
    
    login_button_one = QPushButton(self)
    login_button_one.setText('Зарегистрироваться')
    login_button_one.resize(220,30) #with, heigth button
    login_button_one.move(90, 175)
    login_button_one.clicked.connect(self.register_user_one)
    
  
  def show_password(self):  
    pass #slot for the moment
  
  def register_user_one(self):
    pass  #slot for the moment
  

 #for ejecute the wondow and close   
if __name__== "__main__":
  app = QApplication(sys.argv)
  login = Login() 
  sys.exit(app.exec())
    
  

