# -*- coding: utf-8 -*-
"""
Dialog containing an IPython console.

:copyright:
    Mazama Science, IRIS
:license:
    GNU Lesser General Public License, Version 3
    (http://www.gnu.org/copyleft/lesser.html)
"""

from qtconsole.rich_ipython_widget import RichIPythonWidget
from qtconsole.inprocess import QtInProcessKernelManager
from PyQt5 import QtWidgets
from pyweed.gui.BaseDialog import BaseDialog


class EmbedIPython(RichIPythonWidget):

    def __init__(self, **kwarg):
        super(RichIPythonWidget, self).__init__()
        self.kernel_manager = QtInProcessKernelManager()
        self.kernel_manager.start_kernel()
        self.kernel = self.kernel_manager.kernel
        self.kernel.gui = 'qt4'
        self.kernel.shell.push(kwarg)
        self.kernel_client = self.kernel_manager.client()
        self.kernel_client.start_channels()


class ConsoleDialog(BaseDialog):
    def __init__(self, pyweed, parent=None):
        super(ConsoleDialog, self).__init__(parent=parent)
        self.widget = EmbedIPython(pyweed=pyweed)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.widget)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = ConsoleDialog()
    widget.show()
    sys.exit(app.exec_())
