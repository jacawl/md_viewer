# importing libraries
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import markdown
import sys
import os
from os.path import abspath
import bs4 as bs


class ScrollLabel(QScrollArea):

    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)

        # making widget resizable
        self.setWidgetResizable(True)

        # making qwidget object
        content = QWidget(self)
        self.setWidget(content)

        # vertical box layout
        lay = QVBoxLayout(content)

        # creating label
        self.label = QLabel(content)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.label.setWordWrap(True)

        # adding label to the layout
        lay.addWidget(self.label)

    def setText(self, text):
        self.label.setText(text)


class Window(QWidget):

    def __init__(self, widges, titles):
        QWidget.__init__(self)

        # create layout
        layout = QGridLayout()
        self.setLayout(layout)

        # create tab widget object
        tabwidget = QTabWidget()

        # for widgets passed into window create a tab
        for i in range(len(widges)):
            tabwidget.addTab(widges[i], titles[i])
        
        # Set style - NEED TO ADD CUSTOMIZATION
        stylesheet = """ 
                        QTabBar::tab:selected {background: #669999;}
                        QTabBar::tab {background: #c2d6d6;}
                        QWidget>QWidget{background: #c2d6d6;}
                        QWidget{background: #c2d6d6;}
                        """
        self.setStyleSheet(stylesheet)

        # add tabwidget to layout
        layout.addWidget(tabwidget, 0, 0)

        # set intitial size
        self.resize(500, 900)


# call to add color to specific tags
def setElementColor(name, el):
    # match name:
    #     case 'h1':
    #         el.attrs['style'] =  'color: #01d7f7'
    #     case 'h2':
    #         el.attrs['style'] =  'color: #01d7f7'    
    #     case 'h3':
    #         el.attrs['style'] =  'color: #01d7f7'
    #     case 'h4':
    #         el.attrs['style'] =  'color: #01d7f7'
    #     case 'h5':
    #         el.attrs['style'] =  'color: ##ddddbb'

    return el


def getHTMLfromMD(files, path):

    print(files)
    # init arrays
    scroll_widgets = []
    titles = []

    # read files passed in
    for file in files:
        
        # get name of each file for tab label
        file_name = file.split('\\')
        titles.append(file_name[len(file_name)-1])

        # try to open file with utf-8 encoding - NEED TO ADD OTHER ENCODING
        try: 

            # open file, convert to html
            text = open(file, 'r', encoding='utf-8')
            md = text.read()
            html_text = markdown.markdown('{}'.format(md))

            # pass html to bs4 obj to loop through elements, to set colors
            soup = bs.BeautifulSoup(html_text, features="html.parser")
            all_elements = soup.findAll()
            for el in all_elements:
                el.attrs['style'] =  'color: #1f2e2e;font-family: Consolas'

            # turn html into scrollable label to view in window
            scrollHTML = ScrollLabel()
            scrollHTML.setText(soup.decode('utf-8'))
            scroll_widgets.append(scrollHTML)

        except:
            print('file must be utf-8 encoded.')
    
    # return array of widgets, file names, and path of folder
    return scroll_widgets, titles, path


def getWidgets():
    if len(sys.argv) == 1:
        # if no arg supplied perform on current directory
        path = abspath(os.curdir)
        files = []

        # extract markdown files
        for file in os.listdir(path):
                if file.endswith(".md"):
                    files.append(os.path.join(path, file))
        
        # if no files are found 
        if len(files) == 0:
            print('No MD files in folder.')
        else:
            return getHTMLfromMD(files, path)
    else: 
        # Get first arg and check if path exists, use abs path to convert relative path to abs
        path = abspath(sys.argv[1])
        files = []

        # if path exists extract markdown files
        if os.path.exists(os.path.join(os.getcwd(), path, path)) == True:
            for file in os.listdir(path):
                if file.endswith(".md"):
                    files.append(os.path.join(path, file))
            
            # if no files are found 
            if len(files) == 0:
                print('No MD files in folder.')
            else:
                return getHTMLfromMD(files, path)
        else:
            print('No such directory.')


# create pyqt5 app
App = QApplication(sys.argv)

# get files
widgets = getWidgets()
print(len(widgets[0]))

# if there are files in widget
if widgets != None:
    screen = Window(widgets[0], widgets[1])
    screen.setWindowTitle(widgets[2])
    screen.show()

    # start the app
    sys.exit(App.exec())