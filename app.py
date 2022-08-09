import sys
from PyQt5 import QtChart
from PyQt5 import QtGui
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QDialog,QApplication, QMainWindow, QStackedWidget,QWidget
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
import json
import datetime
from PyQt5.QtCore import *
import random
from PyQt5.QtGui import QFont, QPainter, QPen
import os
#gui.py file from gui.ui
from gui import Ui_WindowsWellbeing

#add your json path here
os.chdir="dist"
PATH_TO_JSON=""+"tracker.json"

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # colours for piechart slice
        self.colors=['#00ed77','#cfb000','#0066ff','#8000ff','#e00000','#d100e0']

        self.ui = Ui_WindowsWellbeing()
        self.ui.setupUi(self)
        #loadUi("gui.ui",self)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.link.setOpenExternalLinks(True)
        #button click to switch page
        self.btEvents()
        isTodayDataFound=self.gather_data_today()
        if(isTodayDataFound==False):
            self.ui.foreAndBackStackedToday.setCurrentIndex(2)
        else:
            self.ui.foreAndBackStackedToday.setCurrentIndex(0)
        
        ####################################################
        ###############today's foreground chart#############
        #chart preparation here

        #creating series for piechart
        self.ui.seriesTodayFr = QPieSeries()
        self.ui.seriesTodayFr.setHoleSize(0.5)
        #chart
        self.ui.chartTodayFr = QChart()
        self.ui.chartTodayFr.addSeries(self.ui.seriesTodayFr)
        self.ui.chartTodayFr.createDefaultAxes()
        self.ui.chartTodayFr.legend().hide()
        mins=self.calculateTotalMinsToday("foreground")
        self.ui.chartTodayFr.setTitle(f"Foreground running apps (total {mins} mins )")

        self.ui.chartTodayFr.legend().setVisible(True)
        self.ui.chartTodayFr.legend().setAlignment(Qt.AlignRight)
        self.ui.chartTodayFr.setAnimationOptions(QChart.SeriesAnimations)
        
        #chartview
        self.ui.chartviewTodayFr = QChartView(self.ui.chartTodayFr)
        self.ui.chartviewTodayFr.setRenderHint(QPainter.Antialiasing)
        self.ui.todayFrQhbox.addWidget(self.ui.chartviewTodayFr)
        self.update_series_today_fr()
        #self.show()
        
        
        
        ####################################################
        ###############today's background chart#############
        #chart preparation here

        #creating series for piechart
        self.ui.seriesTodayBk = QPieSeries()
        self.ui.seriesTodayBk.setHoleSize(0.5)
        #chart
        self.ui.chartTodayBk = QChart()
        self.ui.chartTodayBk.addSeries(self.ui.seriesTodayBk)
        self.ui.chartTodayBk.createDefaultAxes()
        self.ui.chartTodayBk.legend().hide()
        mins=self.calculateTotalMinsToday("background")
        self.ui.chartTodayBk.setTitle(f"Running apps (minimized/background) (total {mins} mins )")
        self.ui.chartTodayBk.legend().setVisible(True)
        self.ui.chartTodayBk.legend().setAlignment(Qt.AlignRight)
        self.ui.chartTodayBk.setAnimationOptions(QChart.SeriesAnimations)
        #chartview
        self.ui.chartviewTodayBk = QChartView(self.ui.chartTodayBk)
        self.ui.chartviewTodayBk.setRenderHint(QPainter.Antialiasing)
        self.ui.backgroundQhbox.addWidget(self.ui.chartviewTodayBk)
        self.update_series_today_bk()

        ########### create previous data chart#####################
        ###########################################################
        		#creating series for piechart
        self.ui.seriesPrevFr = QPieSeries()
        self.ui.seriesPrevFr.setHoleSize(0.5)
        #chart
        self.ui.chartPrevFr = QChart()
        self.ui.chartPrevFr.addSeries(self.ui.seriesPrevFr)
        self.ui.chartPrevFr.createDefaultAxes()
        self.ui.chartPrevFr.legend().hide()
        

        self.ui.chartPrevFr.legend().setVisible(True)
        self.ui.chartPrevFr.legend().setAlignment(Qt.AlignBottom)
        self.ui.chartPrevFr.setAnimationOptions(QChart.SeriesAnimations)
        
        #chartview
        self.ui.chartViewPrevFr = QChartView(self.ui.chartPrevFr)
        self.ui.chartViewPrevFr.setRenderHint(QPainter.Antialiasing)
        self.ui.prevFrQhbox.addWidget(self.ui.chartViewPrevFr)
        
        ####################################################
        ###############previous's background chart#############

        #creating series for piechart
        self.ui.seriesPrevBk = QPieSeries()
        self.ui.seriesPrevBk.setHoleSize(0.5)
        #chart
        self.ui.chartPrevBk = QChart()
        self.ui.chartPrevBk.addSeries(self.ui.seriesPrevBk)
        self.ui.chartPrevBk.createDefaultAxes()
        self.ui.chartPrevBk.legend().hide()
        self.ui.chartPrevBk.legend().setVisible(True)
        self.ui.chartPrevBk.legend().setAlignment(Qt.AlignBottom)
        self.ui.chartPrevBk.setAnimationOptions(QChart.SeriesAnimations)
        #chartview
        self.ui.chartViewPrevBk = QChartView(self.ui.chartPrevBk)
        self.ui.chartViewPrevBk.setRenderHint(QPainter.Antialiasing)
        self.ui.prevBkQhbox.addWidget(self.ui.chartViewPrevBk)
        
        #############prev date signal#############
        self.ui.date_select.dateChanged.connect(self.get_prev_data)
        #############set current index of prev page to point no data########
        self.set_prev_page_no_data()
        yestarday=datetime.date.today()-datetime.timedelta(days=1)
        min_date=(yestarday-datetime.timedelta(days=10)).strftime("%Y-%m-%d")
        max_date=yestarday.strftime("%Y-%m-%d")
        qt_min_date=QtCore.QDate.fromString(min_date, 'yyyy-MM-dd')
        qt_max_date=QtCore.QDate.fromString(max_date, 'yyyy-MM-dd')
        self.ui.date_select.setMaximumDate(qt_max_date)
        self.ui.date_select.setMinimumDate(qt_min_date)
        self.ui.date_select.setDate(qt_max_date)
        
        #########show window########
        self.show()

        #####################################################
        #timer to call fn continuosly after certain interval
        timer = QTimer(self, interval=60000, timeout=self.update_today)
        timer.start()


    def get_previous_foreground_apps(self):
        if(self.ui.foreAndBackStackedPrev.currentIndex()!=0):
            self.ui.foreAndBackStackedPrev.setCurrentIndex(0)

    def get_previous_background_apps(self):
        if(self.ui.foreAndBackStackedPrev.currentIndex()!=1):
            self.ui.foreAndBackStackedPrev.setCurrentIndex(1)
    
    def set_prev_page_no_data(self):
        self.ui.foreAndBackStackedPrev.setCurrentIndex(2)

    def get_prev_data(self):
        date_input=self.ui.date_select.date().toPyDate().strftime(f"%Y-%m-%d")
        data=self.gather_previous_data(date_input)
        if(data==False):
            self.set_prev_page_no_data()
        else:
            self.update_series_prev_fr(data)
            self.update_series_prev_bk(data)
            if(self.ui.foreAndBackStackedPrev.currentIndex()==2):
                self.ui.foreAndBackStackedPrev.setCurrentIndex(0)


    def update_series_prev_fr(self,data):
        total_time=0        
        self.ui.seriesPrevFr.clear()
        if(data==False):
            return
        
        cleaned={}
        count=0
        for app,time in sorted(data['foreground_apps'].items(), key=lambda x: int(x[1][:-3]), reverse=True):
            intTime=int(time[:-3])
            total_time+=intTime
            if(count<5):
                cleaned[app]=intTime
            else:
                cleaned['others']=cleaned.get('others',0)+intTime
            count+=1
        index=0
        for appname,time in cleaned.items():
            _slice=self.ui.seriesPrevFr.append(appname,time)
            _slice.setBrush(QtGui.QColor(self.colors[index]))
            index+=1
        for slice in self.ui.seriesPrevFr.slices():
            #print(slice.label(),slice.value())
            slice.setLabel("{} {}mins".format(slice.label(),int(slice.value())))
        self.ui.seriesPrevFr.clicked.connect(self.explode_slice_foreground_prev)
        self.ui.chartPrevFr.setTitle(f"Foreground running apps (total {total_time} mins )")
        
    def update_series_prev_bk(self,data):    
        self.ui.seriesPrevBk.clear()
        if(data==False):
            return
        cleaned={}
        count=0
        total_time=0
        for app,time in sorted(data['background_apps'].items(), key=lambda x: int(x[1][:-3]), reverse=True):
            intTime=int(time[:-3])
            total_time+=intTime
            if(count<5):
                cleaned[app]=intTime
            else:
                cleaned['others']=cleaned.get('others',0)+intTime
            count+=1
        index=0
        for appname,time in cleaned.items():
            _slice=self.ui.seriesPrevBk.append(appname,time)
            _slice.setBrush(QtGui.QColor(self.colors[index]))
            index+=1
        for slice in self.ui.seriesPrevBk.slices():
            #print(slice.label(),slice.value())
            slice.setLabel("{} {}mins".format(slice.label(),int(slice.value())))
        self.ui.seriesPrevBk.clicked.connect(self.explode_slice_background_prev)
        self.ui.chartPrevBk.setTitle(f"Running apps (minimized/background) (total {total_time} mins )")

    ######updating today's graphs#########
    def update_today(self):
        todayData=self.gather_data_today()
        if(todayData==False):
            self.ui.foreAndBackStackedToday.setCurrentIndex(2)
            return
        self.update_series_today_fr()
        self.update_series_today_bk()

    ###to listen button events
    def btEvents(self):
        #main bt today,prev,about
        self.ui.todayBt.clicked.connect(self.today_screen)
        self.ui.prevBt.clicked.connect(self.prev_screen)
        self.ui.aboutBt.clicked.connect(self.aboutScreen)
        #today's foreground and background bt
        self.ui.foregroundBt.clicked.connect(self.today_foreground_bt)
        self.ui.backgroundBt.clicked.connect(self.today_background_bt)
        #previous foreground and background bt
        self.ui.foregroundBt_prev.clicked.connect(self.previous_foreground_bt)
        self.ui.backgroundBt_prev.clicked.connect(self.previous_background_bt)

    def calculateTotalMinsToday(self,param):
        data=self.gather_data_today()
        if(data==False):
            return False
        foregroundAppTuple=list(data['foreground_apps'].items())
        backgroundAppTuple=list(data['background_apps'].items())
        foregroundTotalMinsToday=0
        backgroundTotalMinsToday=0
        for i in foregroundAppTuple:
            foregroundTotalMinsToday+=int(i[1][:-3])
        for i in backgroundAppTuple:
            backgroundTotalMinsToday+=int(i[1][:-3])
        if(param=="total"):
            return foregroundTotalMinsToday+backgroundTotalMinsToday
        elif(param=="foreground"):
            return foregroundTotalMinsToday
        return backgroundTotalMinsToday    
        
    def previous_foreground_bt(self):
        date_input=self.ui.date_select.date().toPyDate().strftime(f"%Y-%m-%d")
        data=self.gather_previous_data(date_input)
        if(data==False):
            self.set_prev_page_no_data()
        else:
            self.update_series_prev_fr(data)
            self.ui.foreAndBackStackedPrev.setCurrentIndex(0)
        

    def previous_background_bt(self):
        date_input=self.ui.date_select.date().toPyDate().strftime(f"%Y-%m-%d")
        data=self.gather_previous_data(date_input)
        if(data==False):
            self.set_prev_page_no_data()
        else:
            self.update_series_prev_bk(data)
            self.ui.foreAndBackStackedPrev.setCurrentIndex(1)

    def today_foreground_bt(self):
        #switching between foreground and background for today
        if(self.gather_data_today()==False):
            self.ui.foreAndBackStackedToday.setCurrentIndex(2)
        else:
            self.ui.foreAndBackStackedToday.setCurrentIndex(0)

    def today_background_bt(self):
        #switching between foreground and background for today
        if(self.gather_data_today()==False):
            self.ui.foreAndBackStackedToday.setCurrentIndex(2)
        else:
            self.ui.foreAndBackStackedToday.setCurrentIndex(1)

    #####screen index of StackedWidget for today,prev day and about######
    def today_screen(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def prev_screen(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def aboutScreen(self):
        self.ui.stackedWidget.setCurrentIndex(2)
    ######################################################################

    #########gather data from json#############
    def gather_data_today(self):
        today=datetime.date.today()
        #print(today)
        with open(PATH_TO_JSON) as f:
            try:
                data=json.load(f)
                data=data['data']
            except:
                print("issue")
                sys.exit()

        todayFound=False
        for stat in data:
            if(stat['date']==str(today)):
                todayFound=True
                todayStat=stat
        if(todayFound==False):
            #print that no data for today
            return todayFound
        else:
            #create chart in page index 0
            #print(todayStat)
            return todayStat

    
    ###########get previous data
    def gather_previous_data(self,date):
        with open(PATH_TO_JSON) as f:
            try:
                data=json.load(f)
                data=data['data']
            except:
                print("issue")
                sys.exit()

        date_found=False
        for stat in data:
            if(stat['date']==date):
                date_found=True
                prevStat=stat
                break
        if(date_found==False):
            #print that no data for today
            return date_found
        else:
            #create chart in page index 0
            #print(prevStat)
            return prevStat

    #########today's foreground series############
    def update_series_today_fr(self):
        data=self.gather_data_today()
        self.ui.seriesTodayFr.clear()
        if(data==False):
            return
        
        cleaned={}
        count=0
        for app,time in sorted(data['foreground_apps'].items(), key=lambda x: int(x[1][:-3]), reverse=True):
            intTime=int(time[:-3])
            if(count<5):
                cleaned[app]=intTime
            else:
                cleaned['others']=cleaned.get('others',0)+intTime
            count+=1
        index=0
        for appname,time in cleaned.items():
            _slice=self.ui.seriesTodayFr.append(appname,time)
            _slice.setBrush(QtGui.QColor(self.colors[index]))
            index+=1
        for slice in self.ui.seriesTodayFr.slices():
            #print(slice.label(),slice.value())
            slice.setLabel("{} {}mins".format(slice.label(),int(slice.value())))
        self.ui.seriesTodayFr.clicked.connect(self.explode_slice_foreground)
    #########today's background series############
    def update_series_today_bk(self):
        data=self.gather_data_today()
        self.ui.seriesTodayBk.clear()
        if(data==False):
            return
        cleaned={}
        count=0
        for app,time in sorted(data['background_apps'].items(), key=lambda x: int(x[1][:-3]), reverse=True):
            intTime=int(time[:-3])
            if(count<5):
                cleaned[app]=intTime
            else:
                cleaned['others']=cleaned.get('others',0)+intTime
            count+=1
        index=0
        for appname,time in cleaned.items():
            _slice=self.ui.seriesTodayBk.append(appname,time)
            _slice.setBrush(QtGui.QColor(self.colors[index]))
            index+=1
        for slice in self.ui.seriesTodayBk.slices():
            #print(slice.label(),slice.value())
            slice.setLabel("{} {}mins".format(slice.label(),int(slice.value())))
        self.ui.seriesTodayBk.clicked.connect(self.explode_slice_background)
        

    def explode_slice_foreground(self,curr_slice):
        for slice in self.ui.seriesTodayFr.slices():
            if(slice.isExploded()):
                slice.setExploded(False)
                slice.setLabelVisible(False)
        curr_slice.setExploded(True)
        curr_slice.setExplodeDistanceFactor(0.10)
        curr_slice.setLabelVisible(True)

    def explode_slice_background(self,curr_slice):
        for slice in self.ui.seriesTodayBk.slices():
            if(slice.isExploded()):
                slice.setExploded(False)
                slice.setLabelVisible(False)
        curr_slice.setExploded(True)
        curr_slice.setExplodeDistanceFactor(0.10)
        curr_slice.setLabelVisible(True)

    def explode_slice_foreground_prev(self,curr_slice):
        for slice in self.ui.seriesPrevFr.slices():
            if(slice.isExploded()):
                slice.setExploded(False)
                slice.setLabelVisible(False)
        curr_slice.setExploded(True)
        curr_slice.setExplodeDistanceFactor(0.10)
        curr_slice.setLabelVisible(True)

    def explode_slice_background_prev(self,curr_slice):
        for slice in self.ui.seriesPrevBk.slices():
            if(slice.isExploded()):
                slice.setExploded(False)
                slice.setLabelVisible(False)
        curr_slice.setExploded(True)
        curr_slice.setExplodeDistanceFactor(0.10)
        curr_slice.setLabelVisible(True)


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = MainWindow()
    application.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

