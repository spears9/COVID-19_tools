#read COVID-19 data

#for US county and state level data, use CovidCounty class
# read COVID-19 data from:
# https://static.usafacts.org/public/data/covid-19/covid_confirmed_usafacts.csv
# https://static.usafacts.org/public/data/covid-19/covid_deaths_usafacts.csv

# for global country data, use Covid class
# https://github.com/CSSEGISandData/COVID-19.git

# my local repo: /Users/spears9/repos/COVID-19

from pylab import *
import csv
import pdb
#use pdb.pm() to do a postmortem in flight
ion()

filePathCounty  = '/Users/spears9/repos/COVID-19_USAfacts/'
filePath        = '/Users/spears9/repos/COVID-19/csse_covid_19_data/csse_covid_19_time_series/'

def getDataCounty(filePathCounty):
    #confirmedFile = 'covid_confirmed_usafacts_u.csv'
    #deathsFile = 'covid_deaths_usafacts_u.csv'
    confirmedFile = 'covid_confirmed_usafacts.csv'
    deathsFile = 'covid_deaths_usafacts.csv'
    data       = []
    countyFIPS = []
    county     = []
    state      = []
    stateFIPS  = []
    with open(filePathCounty+confirmedFile,'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        heads = spamreader.next()
        for row in spamreader:
            data.append(row)
            #countyFIPS.append(row[0])
            #county.append(row[1])
            #state.append(row[2])
            #stateFIPS.append(row[3])
    matData = matrix(data)
    if matData[1,-1] == '':
        confirmed = array(matData[:,4:-1],dtype=int32)
    else:
        confirmed = array(matData[:,4:],dtype=int32)
    data = []
    with open(filePathCounty+deathsFile,'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        heads = spamreader.next()
        for row in spamreader:
            data.append(row)
            countyFIPS.append(row[0])
            county.append(row[1])
            state.append(row[2])
            stateFIPS.append(row[3])
    matData = matrix(data)
    #protect against empty strings in final column
    if matData[1,-1] == '':
        deaths = array(matData[:,4:-1],dtype=int32)
    else:
        deaths = array(matData[:,4:],dtype=int32)
    #ncol  = len(heads)-4
    #confirmed = loadtxt(filePath+confirmedFile,delimiter=',',skiprows=1,usecols= tuple(arange(4,ncol+2,1)))
    #deaths    = loadtxt(filePath+deathsFile,delimiter=',',skiprows=1,usecols= tuple(arange(4,ncol+2,1)))
    recovered = deaths - deaths  # all zeros, since no longer reporting
    current   = confirmed-deaths -recovered #, but stopped reporting
    return countyFIPS, county, state, stateFIPS, confirmed,recovered,deaths,current

def getData(filePath):
    # getData needs similar correction using matrix, array trick as getDataCounty
    # then add reh recovered data more completely
    #confirmedFile = 'time_series_19-covid-Confirmed.csv'
    #deathsFile    = 'time_series_19-covid-Deaths.csv'
    #recoveredFile = 'time_series_19-covid-Recovered.csv'
    confirmedFile = 'time_series_covid19_confirmed_global.csv'
    deathsFile = 'time_series_covid19_deaths_global.csv'
    recoveredFile = 'time_series_covid19_recovered_global.csv'
    state     = []
    country   = []
    data      = []
    with open(filePath+confirmedFile,'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        heads = spamreader.next()
        for row in spamreader:
            data.append(row)
            state.append(row[0])
            country.append(row[1])
    ncol  = len(heads)-2
    #    confirmed = loadtxt(filePath+confirmedFile,delimiter=',',skiprows=1,usecols= tuple(arange(4,ncol+2,1)))
    #    recovered = loadtxt(filePath+recoveredFile,delimiter=',',skiprows=1,usecols= tuple(arange(4,ncol+2,1)))
    #    deaths    = loadtxt(filePath+deathsFile,delimiter=',',skiprows=1,usecols= tuple(arange(4,ncol+2,1)))
    # hack to fix broken CSSE data
    confirmed = loadtxt(filePath+confirmedFile,delimiter=',',skiprows=1,usecols= tuple(arange(4,ncol+2,1)))
    #recovered = loadtxt(filePath+recoveredFile,delimiter=',',skiprows=1,usecols= tuple(arange(4,ncol+2,1)))
    recovered = confirmed - confirmed  # all zeros, since no longer reporting
    deaths    = loadtxt(filePath+deathsFile,delimiter=',',skiprows=1,usecols= tuple(arange(4,ncol+2,1)))
    current   = confirmed-deaths -recovered #, but stopped reporting
    return state, country, confirmed,recovered,deaths,current

def getPlaceIndex(place,placeName):
    if placeName == "all":
        ind = arange(len(place))
    else:
        ind = where(isin(place,placeName))[0]
    return ind

class CovidCounty(object):
    def __init__(self,placeName):
        self._cache = [None, None] # cached results
        self.placeName    = placeName
        self.countyFIPS, self.county, self.state, self.stateFIPS, self.confirmed, self.recovered, self.deaths, self.current = getDataCounty(filePathCounty)
        if shape(where(isin(self.state,self.placeName)))[1] > 0:
            self.ind = getPlaceIndex(self.state,self.placeName)
            self.region = 'state'
        else:
            self.ind = getPlaceIndex(self.county,self.placeName)
            self.region = 'county'

    def getSeries(self,type,minCases=0):
        if type=='confirmed':
            localData = self.confirmed
        if type=='deaths':
            localData = self.deaths
        if type=='recovered':
            localData = self.recovered
        if type=='current':
            localData = self.current
        part       = localData[self.ind,:] # keep localData associated with placeName
        fullSeries = sum(part,axis=0)      # sum to get a single time series if localData is for a distributed country
        keep = where(fullSeries>=minCases)
        return fullSeries[keep]

#    def getCountySeries(self,

    def getLogD(self,type,minCases=0,frac=False):
        series = self.getSeries(type,minCases)
        Dseries = series[1:]-series[0:-1]
        Aseries = (series[1:]+series[0:-1])/2.
        #protect against divide by zero when there are no cases for two or more days
        fixlocs = where(isin(Aseries,0))
        #Dseries[fixlocs]=log(1)
        Aseries[fixlocs]=1
        #return logDerivative of log(1) so frac value is 1 when no cases        
        LD      = Dseries/Aseries
        if frac:
            LD = exp(LD)
        return LD

class Covid(object):
    def __init__(self,placeName):
        self._cache = [None, None] # cached results
        self.placeName    = placeName
        self.state, self.country, self.confirmed, self.recovered, self.deaths, self.current = getData(filePath)
        if shape(where(isin(self.country,self.placeName)))[1] > 0:
            self.ind = getPlaceIndex(self.country,self.placeName)
            self.region = 'country'
        else:
            self.ind = getPlaceIndex(self.state,self.placeName)
            self.region = 'state'

    def getSeries(self,type,minCases=0):
        if type=='confirmed':
            localData = self.confirmed
        if type=='deaths':
            localData = self.deaths
        if type=='recovered':
            localData = self.recovered
        if type=='current':
            localData = self.current
        part       = localData[self.ind,:] # keep localData associated with placeName
        fullSeries = sum(part,axis=0)      # sum to get a single time series if localData is for a distributed country
        keep = where(fullSeries>=minCases)
        return fullSeries[keep]

    def getLogD(self,type,minCases=0,frac=False):
        series = self.getSeries(type,minCases)
        Dseries = series[1:]-series[0:-1]
        Aseries = (series[1:]+series[0:-1])/2.
        #protect against divide by zero when there are no cases for two or more days
        fixlocs = where(isin(Aseries,0))
        Dseries[fixlocs]=log(1)
        Aseries[fixlocs]=1
        #return logDerivative of log(1) so frac value is 1 when no ases
        LD      = Dseries/Aseries
        if frac:
            LD = exp(LD)
        return LD


# smooth = np.convolve(Covid('Texas').getLogD('current',minCases=10,frac=True), np.ones((5,))/5, mode='valid')


# define a useful global plotting function
def plotGlobal(figNum,places,thisSeries,order,sinceCases=100,smoothingDays=4,styles=['k-']):
    # thisSeries, type of data: current, deaths, recovered, confirmed
    # order: cases, derivative
    # sinceCases: minCases for time alignment
    # smoothingDays: days over which to boxcar average
    # places: list of placeName strings to be plotted on common plot; loop over places
    figure(figNum)
    if order == 'series':
        if len(styles)==1:
            for j in arange(len(places)):
                placeCurrent = np.convolve(Covid(places[j]).getSeries(thisSeries,minCases=sinceCases), np.ones((smoothingDays,))/smoothingDays, mode='valid')
                plot(placeCurrent,styles)
        else:
            for j in arange(len(places)):
                placeCurrent = np.convolve(Covid(places[j]).getSeries(thisSeries,minCases=sinceCases), np.ones((smoothingDays,))/smoothingDays, mode='valid')
                plot(placeCurrent,styles[j])
    if order == 'rates':
        if len(styles)==1:
            for j in arange(len(places)):
                placeCurrent = np.convolve(Covid(places[j]).getLogD(thisSeries,minCases=sinceCases,frac=True), np.ones((smoothingDays,))/smoothingDays, mode='valid')
                plot(placeCurrent,styles)
        else:
            for j in arange(len(places)):
                placeCurrent = np.convolve(Covid(places[j]).getLogD(thisSeries,minCases=sinceCases,frac=True), np.ones((smoothingDays,))/smoothingDays, mode='valid')
                plot(placeCurrent,styles[j])
    if order == 'curve':
        print('curve')
        if len(styles)==1:
            for j in arange(len(places)):
                placeCurrent = np.convolve(Covid(places[j]).getSeries(thisSeries,minCases=sinceCases), np.ones((smoothingDays,))/smoothingDays, mode='valid')
                curve = np.convolve(placeCurrent[1:]-placeCurrent[0:-1], np.ones((smoothingDays,))/smoothingDays, mode='valid')
                plot(curve,styles)
        else:
            for j in arange(len(places)):
                placeCurrent = np.convolve(Covid(places[j]).getSeries(thisSeries,minCases=sinceCases), np.ones((smoothingDays,))/smoothingDays, mode='valid')
                curve = np.convolve(placeCurrent[1:]-placeCurrent[0:-1], np.ones((smoothingDays,))/smoothingDays, mode='valid')
                plot(curve,styles[j])                
