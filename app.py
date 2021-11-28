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


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("gui.ui",self)
        self.stackedWidget.setCurrentIndex(0)
        self.link.setOpenExternalLinks(True)
        #button click to switch page
        self.btEvents()
        isTodayDataFound=self.gather_data()
        if(isTodayDataFound==False):
            self.foreAndBackStackedToday.setCurrentIndex(2)
        else:
            self.foreAndBackStackedToday.setCurrentIndex(0)
        
        ####################################################
        ###############today's foreground chart#############
        #chart preparation here

        #creating series for piechart
        self.seriesTodayFr = QPieSeries()
        #chart
        self.chartTodayFr = QChart()
        self.chartTodayFr.addSeries(self.seriesTodayFr)
        self.chartTodayFr.createDefaultAxes()
        self.chartTodayFr.legend().hide()
        mins=self.calculateTotalMinsToday("foreground")
        self.chartTodayFr.setTitle(f"Foreground running apps (total {mins} mins )")
        self.chartTodayFr.legend().setVisible(True)
        self.chartTodayFr.legend().setAlignment(Qt.AlignRight)
        self.chartTodayFr.setAnimationOptions(QChart.SeriesAnimations)
        
        #chartview
        self.chartviewTodayFr = QChartView(self.chartTodayFr)
        self.chartviewTodayFr.setRenderHint(QPainter.Antialiasing)
        self.todayFrQhbox.addWidget(self.chartviewTodayFr)
        self.update_series_today_fr()
        #self.show()
        
        
        
        ####################################################
        ###############today's background chart#############
        #chart preparation here

        #creating series for piechart
        self.seriesTodayBk = QPieSeries()
        #chart
        self.chartTodayBk = QChart()
        self.chartTodayBk.addSeries(self.seriesTodayBk)
        self.chartTodayBk.createDefaultAxes()
        self.chartTodayBk.legend().hide()
        mins=self.calculateTotalMinsToday("background")
        self.chartTodayBk.setTitle(f"Running apps (minimized/background) (total {mins} mins )")
        self.chartTodayBk.legend().setVisible(True)
        self.chartTodayBk.legend().setAlignment(Qt.AlignRight)
        self.chartTodayBk.setAnimationOptions(QChart.SeriesAnimations)
        #chartview
        self.chartviewTodayBk = QChartView(self.chartTodayBk)
        self.chartviewTodayBk.setRenderHint(QPainter.Antialiasing)
        self.backgroundQhbox.addWidget(self.chartviewTodayBk)
        #self.chartTodayBk.setTheme(QChart.ChartThemeBlueCerulean)
        self.update_series_today_bk()
     
        #########show window########
        self.show()

        #####################################################
        #timer to call fn continuosly after certain interval
        timer = QTimer(self, interval=60000, timeout=self.update_today)
        timer.start()

    ######updating today's graphs#########
    def update_today(self):
        todayData=self.gather_data()
        if(todayData==False):
            self.foreAndBackStackedToday.setCurrentIndex(2)
            return
        self.update_series_today_fr()
        self.update_series_today_bk()

    ###to listen button events
    def btEvents(self):
        #main bt today,prev,about
        self.todayBt.clicked.connect(self.today_screen)
        self.prevBt.clicked.connect(self.prev_screen)
        self.aboutBt.clicked.connect(self.aboutScreen)
        #today's foreground and background bt
        self.foregroundBt.clicked.connect(self.today_foreground_bt)
        self.backgroundBt.clicked.connect(self.today_background_bt)

    def calculateTotalMinsToday(self,param):
        data=self.gather_data()
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
        

    def today_foreground_bt(self):
        #switching between foreground and background for today
        if(self.gather_data()==False):
            self.foreAndBackStackedToday.setCurrentIndex(2)
        else:
            self.foreAndBackStackedToday.setCurrentIndex(0)

    def today_background_bt(self):
        #switching between foreground and background for today
        if(self.gather_data()==False):
            self.foreAndBackStackedToday.setCurrentIndex(2)
        else:
            self.foreAndBackStackedToday.setCurrentIndex(1)

    #####screen index of StackedWidget for today,prev day and about######
    def today_screen(self):
        self.stackedWidget.setCurrentIndex(0)

    def prev_screen(self):
        self.stackedWidget.setCurrentIndex(1)

    def aboutScreen(self):
        self.stackedWidget.setCurrentIndex(2)
    ######################################################################

    #########gather data from json#############
    def gather_data(self):
        today=datetime.date.today()
        #print(today)
        with open(r"tracker.json") as f:
            try:
                data=json.load(f)
                data=data['data']
            except:
                sys.exit(app.exec_())

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

    #########today's foreground series############
    def update_series_today_fr(self):
        data=self.gather_data()
        self.seriesTodayFr.clear()
        if(data==False):
            return
        for app,time in data['foreground_apps'].items():
            intTime=int(time[:-3])
            self.seriesTodayFr.append(app,intTime)
        for slice in self.seriesTodayFr.slices():
            #print(slice.label(),slice.value())
            slice.setLabel("{} {}mins".format(slice.label(),int(slice.value())))
        

    #########today's background series############
    def update_series_today_bk(self):
        data=self.gather_data()
        self.seriesTodayBk.clear()
        if(data==False):
            return
        for app,time in data['background_apps'].items():
            intTime=int(time[:-3])
            self.seriesTodayBk.append(app,intTime)
        
        for slice in self.seriesTodayBk.slices():
            slice.setLabel("{} {}mins".format(slice.label(),int(slice.value())))


if __name__ == '__main__':
    app=QApplication(sys.argv)
    window=MainWindow()
    window.show()
    try:
        sys.exit(app.exec_())
    except:
        print("exiting")