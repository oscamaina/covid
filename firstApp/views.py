from django.shortcuts import render
import pandas as pd

df3 = pd.read_json('https://cdn.jsdelivr.net/gh/highcharts/highcharts@v7.0.0/samples/data/world-population-density.json')

# Create your views here.
def indexPage(request):
	confirmedGlobal=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
	totalCount = confirmedGlobal[confirmedGlobal.columns[-1]].sum()
	barPlotData= confirmedGlobal[['Country/Region',confirmedGlobal.columns[-1]]].groupby('Country/Region').sum()
	barPlotData = barPlotData.reset_index()
	barPlotData.columns =['Country/Region', 'values']
	barPlotData = barPlotData.sort_values(by='values', ascending=False)
	barPlotVals=barPlotData['values'].values.tolist()
	countryNames=barPlotData['Country/Region'].values.tolist()
	dataForMap = mapData(barPlotData,countryNames)
	context = {'totalCount':totalCount, 'countryNames': countryNames, 'barPlotVals':barPlotVals, 'dataForMap':dataForMap}
	return render(request, 'index.html', context)

def mapData(barPlotData,countryNames):
	dataForMap=[]
	for i in countryNames:
	    try:
	        tempdf=df3[df3['name']==i]
	        temp={}
	        temp["code3"] = list(tempdf['code3'].values)[0]
	        temp["name"] = i
	        temp["value"] = barPlotData[barPlotData['Country/Region']==i]['values'].sum()
	        temp["code"]=list(tempdf['code'].values)[0]
	        dataForMap.append(temp)
	    except:
	        pass
	return dataForMap