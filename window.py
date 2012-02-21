# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""Implementation of several pyqt4 GUI classes for ImagePro.

Module PyQt4, numpy and qimage2ndarray are required.

Author: Lijie Huang @BNU
Email: huanglijie.seal@gmail.com
Last modified: 2012-02-20

ATTENTION:
    Stop thinking, man! just code it! Done is better than perfect.

"""

import sys

import numpy as np
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#from qimage2ndarray import gray2qimage

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
        # set window title
        self.setWindowTitle('ImagePro')
        # set window icon
        #self.setWindowIcon()
        self.setSizePolicy(QSizePolicy.Ignored,
                           QSizePolicy.Ignored)
        self.resize(500, 400)

        self.image = None
        self.scale_factor = 0
        self.label = None
        self.pen_status = False

        self.create_action()
        self.create_menus()

    def load_data(self):
        """Load template and activation map"""
        data = self.template.get_data()
        if not self.activation:
            for index in range(data.shape[2]):
                label_tmp = ImageLabel(index, data[:, :, index], data.max())
                self.label_list.append(label_tmp)
        else:
            active = self.activation.get_data()
            active = abs(active)
            for index in range(len(self.label_list)):
                self.label_list[index].load_active(active[:, :, index])

    def display_data(self):
        """Create several labels and display each frame"""
        central_widget = QWidget(self)
        central_widget.setSizePolicy(QSizePolicy.Ignored,
                                     QSizePolicy.Ignored)
        gridlayout = QGridLayout()
        central_widget.setLayout(gridlayout)

        for index in range(len(self.label_list)):
            row_index = index / 10
            col_index = index % 10

            self.label_list[index].disp_image(scaler = self.scale_factor)
            central_widget.layout().addWidget(self.label_list[index],
                                              row_index,
                                              col_index)

        scrollarea = QScrollArea()
        scrollarea.setBackgroundRole(QPalette.Dark)
        scrollarea.setWidget(central_widget)
        self.setCentralWidget(scrollarea)
        self.resize(self.centralWidget().widget().size())

    def remove_activation(self):
        self.open_active_act.setEnabled(True)
        self.remove_active_act.setEnabled(False)
        for index in range(len(self.label_list)):
            self.label_list[index].remove_active()

    def close_display(self):
        # change button status
        self.open_template_act.setEnabled(True)
        self.open_active_act.setEnabled(False)
        self.save_mask_act.setEnabled(False)
        self.close_act.setEnabled(False)
        self.remove_active_act.setEnabled(False)
        self.erase_act.setEnabled(False)
        self.pen_status = False

        self.label_list = []
        self.template = None
        self.activation = None
        self.scale_factor = 0

        self.removeToolBar(self.toolbar)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

    def open_template(self):
        """Open a dialog window and select the template file"""
        template_dir = r'/usr/local/neurosoft/fsl/data/standard'
        template_name = QFileDialog.getOpenFileName(
                                        self,
                                        'Open Template File',
                                        template_dir,
                                        'Nifti files (*.nii.gz)')
        if not template_name.isEmpty():
            try:
                #img = nifti.load(str(template_name))
                pass
            except:
                QMessageBox.information(self,
                                        'ROI Creator',
                                        'Cannot load ' + template_name + '.')
            else:
                self.scale_factor = 1.0
                # change the button status
                self.open_template_act.setEnabled(False)
                self.open_active_act.setEnabled(True)
                self.save_mask_act.setEnabled(True)
                self.close_act.setEnabled(True)
                self.erase_act.setEnabled(True)
                self.pen_status = True
                self.add_toolbar()
                # load template file
                self.template = img
                self.load_data()
                self.display_data()
                
    def open_activation(self):
        """Open a dialog and select activation map"""
        active_name = QFileDialog.getOpenFileName(self,
                                                  'Open Activation File',
                                                  QDir.currentPath(),
                                                  'Nifti files (*.nii.gz)')

        if not active_name.isEmpty():
            try:
                pass
                #img = nifti.load(str(active_name))
            except:
                QMessageBox.information(self,
                                        'ROI Creator',
                                        'Cannot load ' + active_name + '.')
            else:
                if not img.shape == self.template.shape:
                    QMessageBox.information(self,
                                            'ROI Creator',
                                            'Data dimension does not match.')
                else:
                    self.open_active_act.setEnabled(False)
                    self.remove_active_act.setEnabled(True)
                    self.overlap_act.setEnabled(True)
                    self.activation = img
                    self.load_data()
                    self.display_data()

    def about(self):
        """Self-description"""
        QMessageBox.about(self,
                          self.tr("About ROI Creator"),
                          self.tr("<p>The <b>ROI Creator</b> could draw ROI "
                             "manually.</p>"))

    def save_mask(self):
        """Save mask as a nifti file"""
        mask_path = QFileDialog.getSaveFileName(self,
                                                'Save mask file',
                                                QDir.currentPath(),
                                                'Nifti files (*.nii.gz)')
        if not mask_path.isEmpty():
            mask_img = self.template
            data = mask_img.get_data()
            for index in range(len(self.label_list)):
                temp = self.label_list[index].mask
                temp = np.abs(np.subtract(temp, 1))
                temp = np.rot90(np.rot90(np.rot90(temp)))
                data[:, :, index] = temp
            header = mask_img.get_header()
            header['cal_max'] = 1
            header['cal_min'] = 0
            mask_img._data.header = header
            nifti.save(mask_img, str(mask_path))
            print 'OK'
        
    def create_action(self):
        """Create actions"""
        # open template action
        self.open_template_act = QAction(self.tr("&Open standard"), self)
        self.open_template_act.setShortcut(self.tr("Ctrl+O"))
        self.connect(self.open_template_act, 
                     SIGNAL("triggered()"),
                     self.open_template)

        # open activation map action
        self.open_active_act = QAction(self.tr("&Add..."), self)
        self.open_active_act.setShortcut(self.tr("Ctrl+A"))
        self.open_active_act.setEnabled(False)
        self.connect(self.open_active_act,
                     SIGNAL("triggered()"),
                     self.open_activation)
        
        # remove overlay action
        self.remove_active_act = QAction(self.tr("&Remove..."), self)
        self.remove_active_act.setShortcut(self.tr("Ctrl+R"))
        self.remove_active_act.setEnabled(False)
        self.connect(self.remove_active_act,
                     SIGNAL("triggered()"),
                     self.remove_activation)

        # save mask action
        self.save_mask_act = QAction(self.tr("&Save mask"), self)
        self.save_mask_act.setShortcut(self.tr("Ctrl+S"))
        self.save_mask_act.setEnabled(False)
        self.connect(self.save_mask_act,
                     SIGNAL("triggered()"),
                     self.save_mask)

        # close display action
        self.close_act = QAction(self.tr("Close"), self)
        self.close_act.setShortcut(self.tr("Ctrl+W"))
        self.close_act.setEnabled(False)
        self.connect(self.close_act,
                     SIGNAL("triggered()"),
                     self.close_display)
        
        # exit action
        self.exit_act = QAction(self.tr("&Quit"), self)
        self.exit_act.setShortcut(self.tr("Ctrl+Q"))
        self.connect(self.exit_act,
                     SIGNAL("triggered()"),
                     self,
                     SLOT("close()"))
        
        # self-description action
        self.about_act = QAction(self.tr("About"), self)
        self.connect(self.about_act, SIGNAL("triggered()"), self.about)

        # about Qt action
        self.about_qt_act = QAction(self.tr("About Qt"), self)
        self.connect(self.about_qt_act,
                     SIGNAL("triggered()"),
                     qApp, 
                     SLOT("aboutQt()"))

        # select pen action
        self.pen_act = QAction(self.tr("pen"), self)
        self.pen_act.setEnabled(False)
        self.connect(self.pen_act, SIGNAL("triggered()"),self.select_pen)

        # select eraser action
        self.erase_act = QAction(self.tr("eraser"), self)
        self.erase_act.setEnabled(False)
        self.connect(self.erase_act, SIGNAL("triggered()"), self.select_eraser)

        # create overlap map
        self.overlap_act = QAction(self.tr("overlap"), self)
        self.overlap_act.setEnabled(False)
        self.connect(self.overlap_act, SIGNAL("triggered()"), self.make_overlap)

    def select_pen(self):
        self.pen_status = True
        #self.erase_status = False
        self.pen_act.setEnabled(False)
        self.erase_act.setEnabled(True)
        self.change_pen_status()

    def select_eraser(self):
        self.pen_status = False
        self.pen_act.setEnabled(True)
        self.erase_act.setEnabled(False)
        self.change_pen_status()

    def change_pen_status(self):
        for index in range(len(self.label_list)):
            self.label_list[index].pen_status = self.pen_status

    def make_overlap(self):
        for index in range(len(self.label_list)):
            self.label_list[index].overlap_active_mask()
        self.display_data()

    def create_menus(self):
        """Create menus"""
        # menu File
        self.file_menu = self.menuBar().addMenu(self.tr("&File"))
        self.file_menu.addAction(self.open_template_act)
        self.file_menu.addAction(self.open_active_act)
        self.file_menu.addAction(self.remove_active_act)
        self.file_menu.addAction(self.save_mask_act)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.close_act)
        self.file_menu.addAction(self.exit_act)

        # menu Help
        self.help_menu = self.menuBar().addMenu(self.tr("&Help"))
        self.help_menu.addAction(self.about_act)
        self.help_menu.addAction(self.about_qt_act)

    def add_toolbar(self):
        """Create a toolbar and several functional buttons"""
        # add a spinbox for zoom-scale selection
        self.spinbox = QSpinBox(self)
        self.spinbox.setMaximum(200)
        self.spinbox.setMinimum(50)
        self.spinbox.setSuffix('%')
        self.spinbox.setSingleStep(10)
        self.spinbox.setValue(100)
        self.connect(self.spinbox, SIGNAL('valueChanged(int)'),
                     self.refresh_display)
        
        # Add a toolbar
        self.toolbar = QToolBar()
        # functional buttons list
        self.toolbar.addWidget(self.spinbox)
        self.toolbar.addAction(self.pen_act)
        self.toolbar.addAction(self.erase_act)
        self.toolbar.addAction(self.overlap_act)
        self.addToolBar(self.toolbar)

    def refresh_display(self, event):
        """Refresh display as scale_factor changing"""
        val = self.spinbox.value()
        self.scale_factor = val / 100.0
        self.display_data()

class ImageLabel(QLabel):
    """Class ImageLabel provides basic dataset and methods for storing
    necessary data and volume display.

    """
    def __init__(self, index, data, max_inten, parent=None):
        super(ImageLabel, self).__init__(parent)
        #self.setStyleSheet("QLabel { background-color : red; }")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.data = np.rot90(data)
        self.activation = None
        self.hasActivation = False
        self.index = index
        self.mask = self.data * 0 + 1
        self._max_inten = max_inten
        self.pen_status = True
        # customized methods
        self.mouseMoveEvent = self._make_mask
        self.scale_factor = 1.0

    def load_active(self, data):
        self.activation = np.rot90(data)
        self.activation = np.abs(np.subtract(self.activation, 1))
        self.hasActivation = True

    def remove_active(self):
        self.activation = None
        self.hasActivation = False
    
    def overlap_active_mask(self):
        if self.hasActivation:
            temp1 = np.abs(np.subtract(self.activation, 1))
            temp2 = np.abs(np.subtract(self.mask, 1))
            temp = np.multiply(temp1, temp2)
            self.mask = np.abs(np.subtract(temp, 1))

    def _make_image(self):
        if self.data.max():
            image = gray2qimage(self.data, normalize=self._max_inten)
        else:
            image = gray2qimage(self.data)

        pixmap = QPixmap.fromImage(image)
        
        painter = QPainter()
        painter.begin(pixmap)
        self._disp_mask(painter)
        painter.end()
        return pixmap

    def disp_image(self, scaler=1.0):
        pixmap = self._make_image()
        orig_size = pixmap.size()
        new_pixmap = pixmap.scaled(scaler * orig_size)
        self.setPixmap(new_pixmap)
        self.resize(self.pixmap().size())
        self.scale_factor = scaler

    def _make_mask(self, evt):
        if self.pen_status:
            for i in range(-1, 2, 1):
                for j in range(-1, 2, 1):
                    try:
                        self.mask[int(round(evt.y()/self.scale_factor)) + i,
                                  int(round(evt.x()/self.scale_factor)) + j] = 0
                    except:
                        print 'Wrong coordinate'
        else:
            for i in range(-1, 2, 1):
                for j in range(-1, 2, 1):
                    try:
                        self.mask[int(round(evt.y()/self.scale_factor)) + i,
                                  int(round(evt.x()/self.scale_factor)) + j] = 1
                    except:
                        print 'Wrong coordinate'

        self.disp_image(scaler=self.scale_factor)

    def _disp_mask(self, painter):
        painter.backgroundMode = Qt.TransparentMode
        if self.hasActivation:
            painter.setPen(Qt.red)
            painter.setBrush(Qt.red)
            _active = gray2qimage(self.activation, normalize=0.5)
            painter.drawPixmap(0, 0, QBitmap.fromImage(_active))
        painter.setPen(Qt.blue)
        painter.setBrush(Qt.blue)
        _mask = gray2qimage(self.mask, normalize=0.5)
        painter.drawPixmap(0, 0, QBitmap.fromImage(_mask))

