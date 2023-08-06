## @namespace xulpymoney.xulpymoney
## @brief Main Xulpymoney script.
from PyQt5.QtWidgets import  QDialog, qApp
from datetime import datetime
from logging import info
from xulpymoney.mem import MemXulpymoney
from xulpymoney.ui.frmAccess import frmAccess
from xulpymoney.ui.frmMain import frmMain, frmMainProductsMaintenance
from sys import exit

def main():
    from PyQt5 import QtWebEngineWidgets # To avoid error must be imported before QCoreApplication
    dir(QtWebEngineWidgets)
    
    mem=MemXulpymoney()
    mem.run()
    mem.frmAccess=frmAccess("xulpymoney","frmAccess")
    mem.frmAccess.setResources(":/xulpymoney/books.png", ":/xulpymoney/xulpymoney.png")
    mem.frmAccess.setLabel(qApp.translate("Mem","Please login to the Xulpymoney database"))
    mem.frmAccess.exec_()

    if mem.frmAccess.result()==QDialog.Accepted:
        mem.setConnection(mem.frmAccess.con, "Qt")
        mem.load_db_data() 
        mem.settings=mem.frmAccess.settings      

        if mem.isProductsMaintenanceMode():
            mem.frmMain=frmMainProductsMaintenance(mem)
        else:
            mem.frmMain = frmMain(mem)
        mem.frmMain.show()
        info("Xulpymoney start time was {}".format(datetime.now()-mem.inittime))
        exit(mem.app.exec_())
