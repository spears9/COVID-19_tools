#from covid_global_class import *
from covid_joint_class import *





plotPath = '/Users/spears9/Files/personal/covid_19/plots/current/'

# total current (confirmed-deaths) cases vs days since 100 cases
figNum = 1
sinceCases    = 1000
thisSeries    = 'current'
order         = 'series'
plotFile = 'currentCases.png'
places = ['US','China','Italy','Germany']
styles = ['b-','r-','g-','y-']
plotGlobal(figNum,places,thisSeries,order,styles=styles,sinceCases=sinceCases,smoothingDays=1)
yscale('log')
savefig(plotPath+plotFile)

# total current (confirmed-deaths) rates vs days since 100 cases
figNum = 2
sinceCases    = 1000
thisSeries    = 'current'
order         = 'rates'
plotFile = 'currentRates.png'
places = ['US','China','Italy','Germany']
styles = ['b-','r-','g-','y-']
plotGlobal(figNum,places,thisSeries,order,styles=styles,sinceCases=sinceCases)
savefig(plotPath+plotFile)




# deaths vs days since 10 deaths
figNum = 3
sinceCases    = 10
thisSeries    = 'deaths'
order         = 'series'
plotFile = 'deathCases.png'
places = ['US','China','Italy','Germany']
styles = ['b-','r-','g-','y-']
plotGlobal(figNum,places,thisSeries,order,styles=styles,sinceCases=sinceCases)
yscale('log')
savefig(plotPath+plotFile)


# deaths rate vs days since 10 deaths
# add recoveries when you can
# needs fix to reading recoveries file; same encoding problem as county data?
#sinceCases    = 100
smoothingDays = 5
#thisSeries    = 'deaths'

usDeathsRate      = np.convolve(Covid('US').getLogD(thisSeries,minCases=sinceCases,frac=True), np.ones((smoothingDays,))/smoothingDays, mode='valid')
chinaDeathsRate   = np.convolve(Covid('China').getLogD(thisSeries,minCases=sinceCases,frac=True), np.ones((smoothingDays,))/smoothingDays, mode='valid')
italyDeathsRate   = np.convolve(Covid('Italy').getLogD(thisSeries,minCases=sinceCases,frac=True), np.ones((smoothingDays,))/smoothingDays, mode='valid')
germanyDeathsRate = np.convolve(Covid('Germany').getLogD(thisSeries,minCases=sinceCases,frac=True), np.ones((smoothingDays,))/smoothingDays, mode='valid')

figure(4)
plot(usDeathsRate,'b-')
plot(chinaDeathsRate,'r-')
plot(italyDeathsRate,'g-')
plot(germanyDeathsRate,'y-')
plot(1.0+0.0*chinaDeathsRate,'k-.')
plotFile = 'deathRates.png'
savefig(plotPath+plotFile)



# fatality rate: fatalities vs infections
sinceCases    = 1000
smoothingDays = 5

thisSeries    = 'confirmed'
usConfirmed    = np.convolve(Covid('US').getSeries(thisSeries,minCases=sinceCases), np.ones((smoothingDays,))/smoothingDays, mode='valid')
usN = len(usConfirmed)
chinaConfirmed = np.convolve(Covid('China').getSeries(thisSeries,minCases=sinceCases), np.ones((smoothingDays,))/smoothingDays, mode='valid')
chinaN = len(chinaConfirmed)
italyConfirmed = np.convolve(Covid('Italy').getSeries(thisSeries,minCases=sinceCases), np.ones((smoothingDays,))/smoothingDays, mode='valid')
italyN = len(italyConfirmed)
#sinceCases=0
germanyConfirmed    = np.convolve(Covid('Germany').getSeries(thisSeries,minCases=sinceCases), np.ones((smoothingDays,))/smoothingDays, mode='valid')
germanyN = len(germanyConfirmed)

thisSeries    = 'deaths'
sinceCases    = 0
usDeaths    = np.convolve(Covid('US').getSeries(thisSeries,minCases=sinceCases), np.ones((smoothingDays,))/smoothingDays, mode='valid')
usDeaths    = usDeaths[-usN:]
chinaDeaths = np.convolve(Covid('China').getSeries(thisSeries,minCases=sinceCases), np.ones((smoothingDays,))/smoothingDays, mode='valid')
chinaDeaths = chinaDeaths[-chinaN:]
italyDeaths = np.convolve(Covid('Italy').getSeries(thisSeries,minCases=sinceCases), np.ones((smoothingDays,))/smoothingDays, mode='valid')
italyDeaths = italyDeaths[-italyN:]
germanyDeaths    = np.convolve(Covid('Germany').getSeries(thisSeries,minCases=sinceCases), np.ones((smoothingDays,))/smoothingDays, mode='valid')
germanyDeaths    = germanyDeaths[-germanyN:]


figure(5)
yscale('log')
xscale('log')
plot(chinaConfirmed,chinaDeaths,'r-')
plot(usConfirmed,usDeaths,'b-')
plot(italyConfirmed,italyDeaths,'g-')
plot(germanyConfirmed,germanyDeaths,'y-')
x = arange(1000,chinaConfirmed[-1])
ylo = .001*x
y1  = .01*x
y5  = .05*x
y10 = .1*x
plot(x,ylo,'k-.')
plot(x,y1,'k-.')
plot(x,y5,'k-.')
plot(x,y10,'k-.')
plotFile = 'deathVsConfirmed.png'
savefig(plotPath+plotFile)

# deaths vs days since 10 deaths
figNum = 6
sinceCases    = 0
thisSeries    = 'confirmed'
order         = 'curve'
plotFile = 'confirmedCurve.png'
places = ['US','China','Italy','Germany']
styles = ['b-','r-','g-','y-']
plotGlobal(figNum,places,thisSeries,order,styles=styles,sinceCases=sinceCases,smoothingDays=10)
savefig(plotPath+plotFile)
