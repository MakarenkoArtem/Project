from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import *
from PyQt5.QtGui import *
import pygame
import sys
import time

class ImageWidget(QWidget):
    def __init__(self,surface,parent=None):
        super(ImageWidget,self).__init__(parent)
        w=surface.get_width()
        h=surface.get_height()
        self.data=surface.get_buffer().raw
        self.image=QtGui.QImage(self.data,w,h,QtGui.QImage.Format_RGB32)

    def paintEvent(self,event):
        qp=QtGui.QPainter()
        qp.begin(self)
        qp.drawImage(0,0,self.image)
        qp.end()


class MainWindow(QMainWindow):
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        self.resize(1500, 700)
        pygame.init()
        s=pygame.Surface((1500,700))
        s.fill((64,128,192,224))
        running = True
        self.xy = None
        self.y = 0
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                print(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    xy, y = event.pos, 0
                elif event.type == pygame.QUIT:
                    running = False
            s.fill((0, 0, 255))
            if self.xy is not None:
                pygame.draw.circle(s,(255,0,255,0),self.xy,int(self.y))
                #pygame.draw.circle(screen, (255, 255, 0), xy, int(y))
                self.y += 0.4
            self.setCentralWidget(ImageWidget(s))
            self.show()
            clock.tick(25)
        pygame.quit()

    def mousePressEvent(self, event):
        if (event.button() == Qt.LeftButton):
            self.xy = (event.x(), event.y())
            self.y = 0





app=QApplication(sys.argv)
w=MainWindow()
w.show()
app.exec_()
