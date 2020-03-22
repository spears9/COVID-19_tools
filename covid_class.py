# read COVID-19 data from:
# https://github.com/CSSEGISandData/COVID-19.git
# load data, find histories by region
# find logarithmic derivatives

# my local repo: /Users/repos/COVID-19

from pylab import *
import csv
ion()

filePath      = '/Users/spears9/repos/COVID-19/csse_covid_19_data/csse_covid_19_time_series/'

def getData(filePath):
    confirmedFile = 'time_series_19-covid-Confirmed.csv'
    deathsFile    = 'time_series_19-covid-Deaths.csv'
    recoveredFile = 'time_series_19-covid-Recovered.csv'
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
    confirmed = loadtxt(filePath+confirmedFile,delimiter=',',skiprows=1,usecols= tuple(arange(4,ncol+2,1)))
    recovered = loadtxt(filePath+recoveredFile,delimiter=',',skiprows=1,usecols= tuple(arange(4,ncol+2,1)))
    deaths    = loadtxt(filePath+deathsFile,delimiter=',',skiprows=1,usecols= tuple(arange(4,ncol+2,1)))
    current   = confirmed-recovered-deaths
    return state, country, confirmed,recovered,deaths,current

def getPlaceIndex(place,placeName):
    ind = where(isin(place,placeName))[0]
    return ind

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
        Aseries = (series[1:]+series[0:-1])/2
        LD      = Dseries/Aseries
        if frac:
            LD = exp(LD)
        return LD
