# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""
Demo
Author: Lijie Huang@BNU
Email: huanglijie.seal@gmail.com
Last modified: 2012-02-01

---------------------------
- All Copyrights reserved -
---------------------------

"""
from PyQt4.QtGui import QApplication
import nibabel.nifti1 as nifti

import window

def main():
    app = QApplication([])

    #app.setWindowIcon(QIcon(""))
    win = window.MainWindow()

    win.show()
    app.exec_()

if __name__ == '__main__':
    main()
