# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""Implementation of several pyqt4 GUI classes for ImagePro.

Module PyQt4, numpy and qimage2ndarray are required.

Author: Lijie Huang @BNU
Email: huanglijie.seal@gmail.com

ATTENTION:
    Stop thinking, man! just code it! Done is better than perfect.

"""

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class MainWindow(QMainWindow):
    """Class MainWindow provides basic dataset and methods for storing and
    building a GUI window.

    Example:
    --------

    >>> from PyQt4.QtGui import QApplication
    >>> import window
    >>> app = QApplication([])
    >>> win = window.MainWindow()
    >>> win.show()
    >>> app.exec_()

    """
    def __init__(self, parent=None):
        """Initalize an instance of MainWindow"""
        # Inherited from QMainWindow
        super(MainWindow, self).__init__(parent)

        # initial a label for displaying image
        self.image_label = QLabel()
        self.image_label.setBackgroundRole(QPalette.Dark)
        self.image_label.setSizePolicy(QSizePolicy.Ignored,
                                       QSizePolicy.Ignored)
        self.image_label.setScaledContents(True)

        # initial a scroll area
        self.scrollarea = QScrollArea()
        self.scrollarea.setBackgroundRole(QPalette.Dark)
        self.scrollarea.setWidget(self.image_label)

        # set window title
        self.setWindowTitle('ImagePro')
        # set window icon
        self.setWindowIcon(QIcon("./icons/icon.png"))
        self.setCentralWidget(self.scrollarea)
        self.resize(500, 400)
        
        # image zoom-in factor
        self.scale_factor = 0

        self.create_actions()
        self.create_menus()

    def open(self):
        """Open a dialog window and select a image file"""
        image_name = QFileDialog.getOpenFileName(self,
                                                 'Select an image',
                                                 QDir.currentPath())
        if not image_name.isEmpty():
            try:
                image = QImage(image_name)
            except:
                QMessageBox.information(self,
                                        'ImagePro',
                                        'Cannot load ' + image_name + '.')
            else:
                self.image_label.setPixmap(QPixmap.fromImage(image))
                self.scale_factor = 1.0

                self.open_act.setEnabled(False)
                self.remove_act.setEnabled(True)
                self.fit_to_window_act.setEnabled(True)
                self.show_toolbar_act.setEnabled(True)
                self.show_toolbar_act.setChecked(True)
                self.show_toolbar()
                self.update_actions()

                if not self.fit_to_window_act.isChecked():
                    self.image_label.adjustSize()

    def remove(self):
        """remove current display"""
        self.image_label.clear()
        self.image_label.resize(400, 300)
        self.open_act.setEnabled(True)
        self.remove_act.setEnabled(False)
        self.fit_to_window_act.setEnabled(False)
        self.show_toolbar_act.setEnabled(False)
        self.show_toolbar_act.setChecked(False)
        self.show_toolbar()
        self.fit_to_window_act.setChecked(True)
        self.update_actions()
        self.fit_to_window_act.setChecked(False)


    def zoom_in(self):
        """Zoom in image for 1.25 times"""
        self.scale_image(1.25)

    def zoom_out(self):
        """Zoom out image for 0.8 times"""
        self.scale_image(0.8)

    def normal_size(self):
        self.image_label.adjustSize()
        self.scale_factor = 1.0
        self.update_actions()

    def fit_to_window(self):
        fit_to_window = self.fit_to_window_act.isChecked()
        self.scrollarea.setWidgetResizable(fit_to_window)
        if not fit_to_window:
            self.normal_size()

        self.update_actions()

    def about(self):
        """Self-description"""
        QMessageBox.about(self,
                          self.tr("About ImageePro"),
                          self.tr("<p>The <b>ImagePro</b> could do simple "
                                  "image processing</p>"))
        
    def create_actions(self):
        """Create actions"""
        # open image file action
        self.open_act = QAction(QIcon("./icons/open.png"),
                                self.tr("&Open..."),
                                self)
        self.open_act.setShortcut(self.tr("Ctrl+O"))
        self.connect(self.open_act, SIGNAL("triggered()"), self.open)

        # remove image action
        self.remove_act = QAction(self.tr("&Remove..."), self)
        self.remove_act.setShortcut(self.tr("Ctrl+R"))
        self.remove_act.setEnabled(False)
        self.connect(self.remove_act, SIGNAL("triggered()"), self.remove)

        # exit action
        self.exit_act = QAction(QIcon("./icons/quit.png"),
                                self.tr("&Quit"),
                                self)
        self.exit_act.setShortcut(self.tr("Ctrl+Q"))
        self.connect(self.exit_act,
                     SIGNAL("triggered()"),
                     self.close)

        # show toolbar action
        self.show_toolbar_act = QAction(self.tr("toolbar"), self)
        self.show_toolbar_act.setCheckable(True)
        self.show_toolbar_act.setEnabled(False)
        self.connect(self.show_toolbar_act,
                     SIGNAL("triggered()"),
                     self.show_toolbar)

        # zoom in action
        self.zoom_in_act = QAction(QIcon("./icons/zoom_in.png"),
                                   self.tr("Zoom In (25%)"),
                                   self)
        self.zoom_in_act.setShortcut(self.tr("Ctrl++"))
        self.zoom_in_act.setEnabled(False)
        self.connect(self.zoom_in_act, SIGNAL("triggered()"), self.zoom_in)

        # zoom out action
        self.zoom_out_act = QAction(QIcon("./icons/zoom_out.png"),
                                    self.tr("Zoom Out (25%)"),
                                    self)
        self.zoom_out_act.setShortcut(self.tr("Ctrl+-"))
        self.zoom_out_act.setEnabled(False)
        self.connect(self.zoom_out_act, SIGNAL("triggered()"), self.zoom_out)

        # normal size action
        self.normal_size_act = QAction(QIcon("./icons/normal_size.png"),
                                       self.tr("Normal &Size"),
                                       self)
        self.normal_size_act.setShortcut(self.tr("Ctrl+S"))
        self.normal_size_act.setEnabled(False)
        self.connect(self.normal_size_act,
                     SIGNAL("triggered()"),
                     self.normal_size)

        # fit to window action
        self.fit_to_window_act = QAction(QIcon("./icons/full_screen.png"),
                                         self.tr("&Fit to window"),
                                         self)
        self.fit_to_window_act.setCheckable(True)
        self.fit_to_window_act.setEnabled(False)
        self.fit_to_window_act.setShortcut(self.tr("Ctrl+F"))
        self.connect(self.fit_to_window_act,
                     SIGNAL("triggered()"),
                     self.fit_to_window)

        # self-description action
        self.about_act = QAction(self.tr("About"), self)
        self.connect(self.about_act, SIGNAL("triggered()"), self.about)

        # about Qt action
        self.about_qt_act = QAction(self.tr("About Qt"), self)
        self.connect(self.about_qt_act,
                     SIGNAL("triggered()"),
                     qApp, 
                     SLOT("aboutQt()"))

    def create_menus(self):
        """Create menus"""
        # menu File
        self.file_menu = self.menuBar().addMenu(self.tr("&File"))
        self.file_menu.addAction(self.open_act)
        self.file_menu.addAction(self.remove_act)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_act)

        # menu View
        self.view_menu = self.menuBar().addMenu(self.tr("&View"))
        self.view_menu.addAction(self.show_toolbar_act)

        # menu Tool
        self.tool_menu = self.menuBar().addMenu(self.tr("&Tool"))
        self.tool_menu.addAction(self.zoom_in_act)
        self.tool_menu.addAction(self.zoom_out_act)
        self.tool_menu.addAction(self.normal_size_act)
        self.tool_menu.addSeparator()
        self.tool_menu.addAction(self.fit_to_window_act)

        # menu Help
        self.help_menu = self.menuBar().addMenu(self.tr("&Help"))
        self.help_menu.addAction(self.about_act)
        self.help_menu.addAction(self.about_qt_act)

    def create_toolbar(self):
        """Create toolbar"""
        self.toolbar = QToolBar()
        self.toolbar.addAction(self.zoom_in_act)
        self.toolbar.addAction(self.zoom_out_act)
        self.toolbar.addAction(self.normal_size_act)
        self.toolbar.addAction(self.fit_to_window_act)

    def show_toolbar(self):
        """change toolbar visiability"""
        if self.show_toolbar_act.isChecked():
            self.create_toolbar()
            self.addToolBar(self.toolbar)
        else:
            self.removeToolBar(self.toolbar)

    def update_actions(self):
        """Update action status"""
        self.zoom_in_act.setEnabled(not self.fit_to_window_act.isChecked())
        self.zoom_out_act.setEnabled(not self.fit_to_window_act.isChecked())
        self.normal_size_act.setEnabled(not self.fit_to_window_act.isChecked())

    def scale_image(self, factor):
        """Display image of spcific size"""
        self.scale_factor *= factor
        new_size = self.scale_factor * self.image_label.pixmap().size()
        self.image_label.resize(new_size)

        self.adjust_scrollbar(factor)

        self.zoom_in_act.setEnabled(self.scale_factor < 3.0)
        self.zoom_out_act.setEnabled(self.scale_factor > 0.333)

    def adjust_scrollbar(self, factor):
        # horizontal bar config
        pre_value = self.scrollarea.horizontalScrollBar().value()
        page_step = self.scrollarea.horizontalScrollBar().pageStep()
        new_value = factor * pre_value + ((factor - 1) * page_step/2)
        self.scrollarea.horizontalScrollBar().setValue(new_value)

        # vertical bar config
        pre_value = self.scrollarea.verticalScrollBar().value()
        page_step = self.scrollarea.verticalScrollBar().pageStep()
        new_value = factor * pre_value + ((factor - 1) * page_step/2)
        self.scrollarea.verticalScrollBar().setValue(new_value)

