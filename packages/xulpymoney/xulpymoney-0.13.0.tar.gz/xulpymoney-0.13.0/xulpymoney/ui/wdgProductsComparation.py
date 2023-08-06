from PyQt5.QtChart import QValueAxis
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QDialog, QVBoxLayout
from datetime import datetime
from xulpymoney.ui.myqtablewidget import mqtw
from xulpymoney.ui.Ui_wdgProductsComparation import Ui_wdgProductsComparation
from xulpymoney.datetime_functions import dtaware_day_end_from_date
from xulpymoney.objects.product import ProductComparation
from xulpymoney.ui.myqwidgets import qmessagebox
from xulpymoney.ui.myqcharts import  VCTemporalSeries

class wdgProductsComparation(QWidget, Ui_wdgProductsComparation):
    def __init__(self, mem,  product1=None,  product2=None, parent = None, name = None):
        QWidget.__init__(self,  parent)
        self.setupUi(self)
        self.mem=mem
        self.parent=parent

        if product1 is None:
            product1=self.mem.data.products.find_by_id(int(self.mem.settings.value("wdgProductsComparation/product1", "79228")))
        
        if product2 is None:
            product2=self.mem.data.products.find_by_id(int(self.mem.settings.value("wdgProductsComparation/product2", "79329")))

        self.selector1.setupUi(self.mem)
        self.selector1.label.setText(self.tr("Select a product to compare"))
        self.selector1.setSelected(product1)
        
        self.selector2.setupUi(self.mem)
        self.selector2.label.setText(self.tr("Select a product to compare"))
        self.selector2.setSelected(product2)
            
        self.cmbCompareTypes.setCurrentIndex(int(self.mem.settings.value("wdgProductsComparation/cmbCompareTypes", "0")))
        self.comparation=None

    def on_cmdComparation_released(self):
        inicio=datetime.now()
        if self.selector1.selected==None or self.selector2.selected==None:
            qmessagebox(self.tr("You must select a product to compare with"))
            return
        self.comparation=ProductComparation(self.mem, self.selector1.selected, self.selector2.selected)
        if self.viewCompare!=None:
            self.viewCompare.hide()
            self.verticalLayout.removeWidget(self.viewCompare)
        if self.comparation.canBeMade()==False:
            qmessagebox(self.tr("Comparation can't be made."))
            return

        self.deCompare.setMinimumDate(self.comparation.dates()[0])
        self.deCompare.setMaximumDate(self.comparation.dates()[len(self.comparation.dates())-1-1])#Es menos 2, ya que hay alguna funcion de comparation que lo necesita
        self.comparation.setFromDate(self.deCompare.date())

        self.viewCompare=VCTemporalSeries()
        if self.cmbCompareTypes.currentIndex()==0:#Not changed data

            ls1=self.viewCompare.appendTemporalSeries(self.comparation.product1.name.upper())#Line seies
            ls2=self.viewCompare.appendTemporalSeries(self.comparation.product2.name.upper())#Line seies
            dates=self.comparation.dates()
            closes1=self.comparation.product1Closes()
            closes2=self.comparation.product2Closes()
            for i,  date in enumerate(dates):
                self.viewCompare.appendTemporalSeriesData(ls1, dtaware_day_end_from_date(date, self.mem.localzone_name) , closes1[i])
                self.viewCompare.appendTemporalSeriesData(ls2, dtaware_day_end_from_date(date, self.mem.localzone_name) , closes2[i])
            
            # BEGIN DISPLAY)
            self.viewCompare.setAxisFormat(self.viewCompare.axisX, self.viewCompare.minx, self.viewCompare.maxx, 1)
            self.viewCompare.setAxisFormat(self.viewCompare.axisY, min(self.comparation.product1Closes()), max(self.comparation.product1Closes()),  0)
            axis3=QValueAxis()
            self.viewCompare.chart().addAxis(self.viewCompare.axisY, Qt.AlignLeft);
            self.viewCompare.chart().addAxis(self.viewCompare.axisX, Qt.AlignBottom);
            self.viewCompare.chart().addAxis(axis3, Qt.AlignRight)

            self.viewCompare.chart().addSeries(ls1)
            ls1.attachAxis(self.viewCompare.axisX)
            ls1.attachAxis(self.viewCompare.axisY)
            self.viewCompare.axisY.setRange(min(self.comparation.product1Closes()), max(self.comparation.product1Closes()))

            self.viewCompare.chart().addSeries(ls2)
            ls2.attachAxis(self.viewCompare.axisX)
            ls2.attachAxis(axis3)
            axis3.setRange (min(self.comparation.product2Closes()), max(self.comparation.product2Closes()))

            if self.viewCompare._allowHideSeries==True:
                for marker in self.viewCompare.chart().legend().markers():
                    try:
                        marker.clicked.disconnect()
                    except:
                        pass
                    marker.clicked.connect(self.viewCompare.on_marker_clicked)

            self.viewCompare.repaint()
            ###END DISPLAY

        elif self.cmbCompareTypes.currentIndex()==1:#Scatter
            pass

        elif self.cmbCompareTypes.currentIndex()==2:#Controlling percentage evolution.

            ls1=self.viewCompare.appendTemporalSeries(self.comparation.product1.name.upper())#Line seies
            ls2=self.viewCompare.appendTemporalSeries(self.comparation.product2.name.upper())#Line seies
            dates=self.comparation.dates()
            closes1=self.comparation.product1PercentageFromFirstProduct2Price()
            closes2=self.comparation.product2Closes()
            for i,  date in enumerate(dates):
                self.viewCompare.appendTemporalSeriesData(ls1, dtaware_day_end_from_date(date, self.mem.localzone_name) , closes1[i])
                self.viewCompare.appendTemporalSeriesData(ls2, dtaware_day_end_from_date(date, self.mem.localzone_name) , closes2[i])
            self.viewCompare.display()
        elif self.cmbCompareTypes.currentIndex()==3:#Controlling percentage evolution reducing leverage.
            ls1=self.viewCompare.appendTemporalSeries(self.comparation.product1.name.upper())#Line seies
            ls2=self.viewCompare.appendTemporalSeries(self.comparation.product2.name.upper())#Line seies
            dates=self.comparation.dates()
            closes1=self.comparation.product1PercentageFromFirstProduct2PriceLeveragedReduced()
            closes2=self.comparation.product2Closes()
            for i,  date in enumerate(dates):
                self.viewCompare.appendTemporalSeriesData(ls1, dtaware_day_end_from_date(date, self.mem.localzone_name) , closes1[i])
                self.viewCompare.appendTemporalSeriesData(ls2, dtaware_day_end_from_date(date, self.mem.localzone_name) , closes2[i])
            self.viewCompare.display()
        elif self.cmbCompareTypes.currentIndex()==4:#Controlling inverse percentage evolution.
            ls1=self.viewCompare.appendTemporalSeries(self.comparation.product1.name.upper())#Line seies
            ls2=self.viewCompare.appendTemporalSeries(self.comparation.product2.name.upper())#Line seies
            dates=self.comparation.dates()
            closes1=self.comparation.product1PercentageFromFirstProduct2InversePrice()
            closes2=self.comparation.product2Closes()
            for i,  date in enumerate(dates):
                self.viewCompare.appendTemporalSeriesData(ls1, dtaware_day_end_from_date(date, self.mem.localzone_name) , closes1[i])
                self.viewCompare.appendTemporalSeriesData(ls2, dtaware_day_end_from_date(date, self.mem.localzone_name) , closes2[i])
            self.viewCompare.display()
        elif self.cmbCompareTypes.currentIndex()==5:#Controlling inverse percentage evolution reducing leverage.
            ls1=self.viewCompare.appendTemporalSeries(self.comparation.product1.name.upper())#Line seies
            ls2=self.viewCompare.appendTemporalSeries(self.comparation.product2.name.upper())#Line seies
            dates=self.comparation.dates()
            closes1=self.comparation.product1PercentageFromFirstProduct2InversePriceLeveragedReduced()
            closes2=self.comparation.product2Closes()
            for i,  date in enumerate(dates):
                self.viewCompare.appendTemporalSeriesData(ls1, dtaware_day_end_from_date(date, self.mem.localzone_name) , closes1[i])
                self.viewCompare.appendTemporalSeriesData(ls2, dtaware_day_end_from_date(date, self.mem.localzone_name) , closes2[i])
            self.viewCompare.display()
        self.verticalLayout.addWidget(self.viewCompare)            

        self.mem.settings.setValue("wdgProductsComparation/product1", str(self.comparation.product1.id))
        self.mem.settings.setValue("wdgProductsComparation/product2", str(self.comparation.product2.id))
        self.mem.settings.setValue("wdgProductsComparation/cmbCompareTypes", str(self.cmbCompareTypes.currentIndex()))
        self.mem.settings.sync()

        print ("Comparation took {}".format(datetime.now()-inicio))

    def on_cmdComparationData_released(self):
        if self.comparation==None:
            qmessagebox(self.tr("You need to compare products first"))
            return
        d=QDialog(self)
        d.resize(800, 600)
        d.setWindowTitle(self.tr("Comparation data table"))
        mqtwQuotes=mqtw(d)
        mqtwQuotes.setSettings(self.mem.settings,"wdgProductsComparation" , "mqtwQuotes")
        mqtwQuotes.showSearchOptions(True)
        self.comparation.myqtablewidget(mqtwQuotes)
        lay = QVBoxLayout(d)
        lay.addWidget(mqtwQuotes)
        d.show()
