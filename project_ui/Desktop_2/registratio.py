import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,QMessageBox, QCheckBox,QVBoxLayout)
from PyQt6.QtGui import QFont,QPixmap

class Registration(QWidget):
  
  def __init__(self) :
    super().__init__()
    self.initiation_UI()
  
  def initiation_UI(self):
    self.setGeometry(725,300,500,425)
    self.setWindowTitle('Тренажер дыхания')
    self.setStyleSheet("background-color:#caf0f8;")
    self.generate_formulary()
    self.show()
    
  def generate_formulary(self):
    self.is_logget =False
    
    #target registratio
    self.label = QLabel(self)
    self.label.setGeometry(220,5,100,50) #left, top, width, height
    self.label.setText('Регистрация')
    
    
    #introduction data users
    self.intro_data = QLineEdit(self)
    self.intro_data.setPlaceholderText("Фамилия")
    self.intro_data.resize(300,30) #with, heigth button
    self.intro_data.move(100,52)
    
    self.intro_data = QLineEdit(self)
    self.intro_data.setPlaceholderText("Имя")
    self.intro_data.resize(300,30) #with, heigth button
    self.intro_data.move(100,92)
    
    self.intro_data = QLineEdit(self)
    self.intro_data.setPlaceholderText("Отчество (при налачии)")
    self.intro_data.resize(300,30) #with, heigth button
    self.intro_data.move(100,132)
    
    self.intro_data = QLineEdit(self)
    self.intro_data.setPlaceholderText("Электронная почта")
    self.intro_data.resize(300,30) #with, heigth button
    self.intro_data.move(100,172)
    
    #pasword
    self.intro_data = QLineEdit(self)
    self.intro_data.setPlaceholderText("Парол")
    self.intro_data.resize(300,30) #with, heigth button
    self.intro_data.move(100,212)
    
    self.intro_data = QLineEdit(self)
    self.intro_data.setPlaceholderText("Парол")
    self.intro_data.resize(300,30) #with, heigth button
    self.intro_data.move(100,252)
    
    layout = QVBoxLayout()
    layout.addWidget(self.intro_data)
    
  
    #button registration
    loggin_button = QPushButton(self)
    loggin_button.setText('login')
    loggin_button.resize(220,30) #with, heigth button
    loggin_button.move(145,323)
    loggin_button.clicked.connect(self.register_user)
    
  def register_user(self):
    pass #port for the moment
  
    self.label = QLabel(self)
    self.label.setGeometry(145,600,100,50) #left, top, width, height
    self.label.setText("you have acoount")
    
    
    
    
    
if __name__== "__main__":
  app = QApplication(sys.argv)
  registratio = Registration() 
  sys.exit(app.exec())
    
  
