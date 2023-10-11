from PyQt5 import QtCore, QtGui
import sys
import sealing_proc as seal

def handleVisibleChanged():
    if not QtGui.QGuiApplication.inputMethod().isVisible():
        return
    for w in QtGui.QGuiApplication.allWindows():
        if w.metaObject().className() == "QtVirtualKeyboard::InputView":
            keyboard = w.findChild(QtCore.QObject, "keyboard")
            if keyboard is not None:
                r = w.geometry()
                r.moveTop(keyboard.property("y"))
                w.setMask(QtGui.QRegion(r))
                return

if __name__ == "__main__":
    import sys
    # os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"
    app = seal.QtWidgets.QApplication(sys.argv)
    QtGui.QGuiApplication.inputMethod().visibleChanged.connect(handleVisibleChanged)

    ui = seal.Sealing()
    ui.show()
    # ui.showFullScreen()
    sys.exit(app.exec_())
