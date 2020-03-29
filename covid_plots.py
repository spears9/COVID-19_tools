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
figNum = 4
sinceCases    = 10
thisSeries    = 'deaths'
order         = 'rates'
plotFile = 'deathRates.png'
places = ['US','China','Italy','Germany']
styles = ['b-','r-','g-','y-']
plotGlobal(figNum,places,thisSeries,order,styles=styles,sinceCases=sinceCases)
savefig(plotPath+plotFile)


# fatality rate: fatalities vs infections

figNum = 5
sinceCases    = 1000
smoothingDays = 5
order         = 'deathrate'
plotFile = 'deathVsConfirmed.png'
places = ['US','China','Italy','Germany']
styles = ['b-','r-','g-','y-']
plotGlobal(figNum,places,thisSeries,order,styles=styles,sinceCases=sinceCases)
yscale('log')
xscale('log')
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
