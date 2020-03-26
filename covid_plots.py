from covid_global_class import *



# total current (confirmed-deaths) cases vs days since 100 cases
sinceCases    = 1000
smoothingDays = 5
thisSeries    = 'current'

usCurrent    = np.convolve(Covid('US').getSeries(thisSeries,minCases=sinceCases), np.ones((smoothingDays,))/smoothingDays, mode='valid')
chinaCurrent = np.convolve(Covid('China').getSeries(thisSeries,minCases=sinceCases), np.ones((smoothingDays,))/smoothingDays, mode='valid')
italyCurrent = np.convolve(Covid('Italy').getSeries(thisSeries,minCases=sinceCases), np.ones((smoothingDays,))/smoothingDays, mode='valid')
germanyCurrent    = np.convolve(Covid('Germany').getSeries(thisSeries,minCases=sinceCases), np.ones((smoothingDays,))/smoothingDays, mode='valid')

figure(1)
yscale('log')
plot(usCurrent,'b-')
plot(chinaCurrent,'r-')
plot(italyCurrent,'g-')
plot(germanyCurrent,'y-')

# total current (confirmed-deaths) cases vs days since 100 cases
# add recoveries when you can
# needs fix to reading recoveries file; same encoding problem as county data?
sinceCases    = 1000
smoothingDays = 5
thisSeries    = 'current'

usCurrentRate    = np.convolve(Covid('US').getLogD(thisSeries,minCases=sinceCases,frac=True), np.ones((smoothingDays,))/smoothingDays, mode='valid')
chinaCurrentRate = np.convolve(Covid('China').getLogD(thisSeries,minCases=sinceCases,frac=True), np.ones((smoothingDays,))/smoothingDays, mode='valid')
italyCurrentRate = np.convolve(Covid('Italy').getLogD(thisSeries,minCases=sinceCases,frac=True), np.ones((smoothingDays,))/smoothingDays, mode='valid')
germanyCurrentRate    = np.convolve(Covid('Germany').getLogD(thisSeries,minCases=sinceCases,frac=True), np.ones((smoothingDays,))/smoothingDays, mode='valid')

figure(2)
plot(usCurrentRate,'b-')
plot(chinaCurrentRate,'r-')
plot(italyCurrentRate,'g-')
plot(germanyCurrentRate,'y-')
plot(1.0+0.0*chinaCurrentRate,'k-.')


# deaths vs days since 10 deaths
sinceCases    = 10
smoothingDays = 5
thisSeries    = 'deaths'

usDeaths    = np.convolve(Covid('US').getSeries(thisSeries,minCases=sinceCases), np.ones((smoothingDays,))/smoothingDays, mode='valid')
chinaDeaths = np.convolve(Covid('China').getSeries(thisSeries,minCases=sinceCases), np.ones((smoothingDays,))/smoothingDays, mode='valid')
italyDeaths = np.convolve(Covid('Italy').getSeries(thisSeries,minCases=sinceCases), np.ones((smoothingDays,))/smoothingDays, mode='valid')
germanyDeaths    = np.convolve(Covid('Germany').getSeries(thisSeries,minCases=sinceCases), np.ones((smoothingDays,))/smoothingDays, mode='valid')
figure(3)
yscale('log')
plot(usDeaths,'b-')
plot(chinaDeaths,'r-')
plot(italyDeaths,'g-')
plot(germanyDeaths,'y-')

# deaths rate vs days since 10 deaths
# add recoveries when you can
# needs fix to reading recoveries file; same encoding problem as county data?
#sinceCases    = 100
#smoothingDays = 5
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
