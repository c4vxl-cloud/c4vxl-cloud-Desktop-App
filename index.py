import os, sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QWidget

class WebView(QWebEngineView):
    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)

        self.loadFinished.connect(self.handle_load_finished)
        self.page().profile().downloadRequested.connect(self.handle_download_request)

        self.parent = parent
        self.setContentsMargins(0, 0, 0, 0)
        self.installEventFilter(self)

        self.loaded = False
    
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        pass

    def contextMenuEvent(self, event):
        event.accept()
    
    def handle_load_finished(self, ok):
        if not ok and not self.loaded:
            self.hide()
            label = QLabel("Cloud not conntect!")
            label.setStyleSheet("font-size: 20px;font-family: Verdana;")
            label.setAlignment(Qt.AlignCenter)
            self.parent.layout.addWidget(label)
        self.loaded = ok
    
    def handle_download_request(self, download):
        download.accept()
        os.startfile(os.path.dirname(download.path()))
        self.loaded = True


class Application(QWidget):
    def __init__(self) -> None:
        super().__init__()

        # create window
        self.setWindowTitle("c4vxl cloud")
        self.setWindowIcon(QIcon("assets/favicon.png"))
        self.resize(1000, 700)
        self.show()

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)


        self.webview = WebView(self)
        self.webview.load(QUrl("https://cloud.c4vxl.de/cloud/"))
        self.layout.addWidget(self.webview)



if __name__ == "__main__":
    qapp = QApplication(sys.argv)
    app = Application()
    sys.exit(qapp.exec_())