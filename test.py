import sys
from PyQt4 import QtGui,QtCore

class SystemTrayIcon(QtGui.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtGui.QMenu(parent)
        quitAction = menu.addAction("Exit")
        QtCore.QObject.connect(quitAction,QtCore.SIGNAL("triggered()"), self.quit)
        self.setContextMenu(menu)

    def quit(self): 
        QtGui.QApplication.quit()

    def main():
        app = QtGui.QApplication(sys.argv)

        w = QtGui.QWidget()
        trayIcon = SystemTrayIcon(QtGui.QIcon("../images/SubBoxIcon.png"), w)

        trayIcon.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
    main()
