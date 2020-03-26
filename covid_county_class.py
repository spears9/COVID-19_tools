# read COVID-19 data from:
# https://static.usafacts.org/public/data/covid-19/covid_confirmed_usafacts.csv
# https://static.usafacts.org/public/data/covid-19/covid_deaths_usafacts.csv
# 
# load data, find histories by region
# find logarithmic derivatives

# my local repo: /Users/spears9/repos/COVID-19

from pylab import *
import csv
ion()

filePath      = '/Users/spears9/repos/COVID-19_USAfacts/'

def getData(filePath):
    confirmedFile = 'covid_confirmed_usafacts_u.csv'
    deathsFile = 'covid_deaths_usafacts_u.csv'
    data       = []
    countyFIPS = []
    county     = []
    state      = []
    stateFIPS  = []
    with open(filePath+confirmedFile,'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        heads = spamreader.next()
        for row in spamreader:
            data.append(row)
            #countyFIPS.append(row[0])
            #county.append(row[1])
            #state.append(row[2])
            #stateFIPS.append(row[3])
    matData = matrix(data)
    confirmed = array(matData[:,4:],dtype=int32)
    data = []
    with open(filePath+deathsFile,'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        heads = spamreader.next()
        for row in spamreader:
            data.append(row)
            countyFIPS.append(row[0])
            county.append(row[1])
            state.append(row[2])
            stateFIPS.append(row[3])
    matData = matrix(data)
    deaths = array(matData[:,4:],dtype=int32)
    #ncol  = len(heads)-4
    #confirmed = loadtxt(filePath+confirmedFile,delimiter=',',skiprows=1,usecols= tuple(arange(4,ncol+2,1)))
    #deaths    = loadtxt(filePath+deathsFile,delimiter=',',skiprows=1,usecols= tuple(arange(4,ncol+2,1)))
    recovered = deaths - deaths  # all zeros, since no longer reporting
    current   = confirmed-deaths -recovered #, but stopped reporting
    return countyFIPS, county, state, stateFIPS, confirmed,recovered,deaths,current

def getPlaceIndex(place,placeName):
    if placeName == "all":
        ind = arange(len(place))
    else:
        ind = where(isin(place,placeName))[0]
    return ind

class Covid(object):
    def __init__(self,placeName):
        self._cache = [None, None] # cached results
        self.placeName    = placeName
        self.countyFIPS, self.county, self.state, self.stateFIPS, self.confirmed, self.recovered, self.deaths, self.current = getData(filePath)
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
        Aseries = (series[1:]+series[0:-1])/2
        LD      = Dseries/Aseries
        if frac:
            LD = exp(LD)
        return LD


# smooth = np.convolve(Covid('Texas').getLogD('current',minCases=10,frac=True), np.ones((5,))/5, mode='valid')
