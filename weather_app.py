from tkinter import *
from tkinter import messagebox
from configparser import ConfigParser

from datetime import datetime

import requests
import json


urlAPI = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

configFile = 'config.ini'
config = ConfigParser()
config.read(configFile)
apiKey = config['apiKey']['key']



def getWeather(city):
    result = requests.get(urlAPI.format(city, apiKey))  #format works specially with '{}' brackets
    if result:
        jsonRes = result.json()
        #to receive (City, Country, temperCelsius, icon, weather)
        city = jsonRes['name']
        country = jsonRes['sys']['country']
        temperKelvin = jsonRes['main']['temp']
        temperCelsius = temperKelvin - 273.15
        icon = jsonRes['weather'][0]['icon']
        weather = jsonRes['weather'][0]['main']
        final = (city, country, temperCelsius, icon, weather)   #it's touple
        return final
    else:
        return None

def storeHist(cityName):

     if cityName != '':
        with open('Data/search_history.json') as json_file:
            cityStored = json.load(json_file)
            for i in range(4, 0, -1):
                cityStored[str(i)] = cityStored[str(i-1)]
            cityStored['0'] = cityName
        with open('Data/search_history.json', 'w') as outfile:
            outfile.truncate(0)
            json.dump(cityStored, outfile)


def search() :
    city = cityText.get()
    weather = getWeather(city)
    if weather:
        locationLbl['text'] = '{}, {}'.format(weather[0],weather[1])
        img['file'] = 'weather_icons/{}.png'.format(weather[3])
        temperLbl['text'] = '{:.2f}°C'.format(weather[2])
        weatherLbl['text'] = weather[4]
        app.focus
        storeHist(city)
    else:
        messagebox.showerror('Wrong Location Chosen', '"{}" is not found!'.format(city))

def cityReps(city):
    with open('Data/city_list.json', encoding = "UTF-8") as json_file:
        allCities = json.load(json_file)
    repIds = []
    for checkedCityEntry in allCities:
        if checkedCityEntry['name'] == city:
            repIds.append(checkedCityEntry['id'])
    return repIds

def multipleCitiesFound():
    cityChoosingWind = Tk()
    cityChoosingWind.title = "Cities With Such Name:"
    cityChoosingWind.geometry("200x250")

    indicesCities = cityReps(locationLbl['text'].split(',')[0])

    with open('Data/city_list.json', encoding = "UTF-8") as json_file:
            allCities = json.load(json_file)

    shownOptions = []
    for checkedIndex in indicesCities:
        for checkedCityEntry in allCities:
            if checkedCityEntry['id'] == checkedIndex:
                shownOptions.append(checkedCityEntry['name'] + ', ' + checkedCityEntry['country'])

    def searchTheChosenCity():
        if(variableOptions.get() != 'Choose city:'):
            cityText.set(variableOptions.get())
            search()
            cityChoosingWind.destroy()
    
    shownOptions = list(set(shownOptions))

    if len(shownOptions) < 2:
        citiesNotFoundLbl = Label(cityChoosingWind, text = 'No alternatives found.')  
        citiesNotFoundLbl.pack()
    else:
        variableOptions = StringVar(cityChoosingWind)
        variableOptions.set('Choose city:') # default value
        menuCities = OptionMenu(cityChoosingWind, variableOptions, *shownOptions)
        menuCities.pack()

        chosenSearchBtn = Button(cityChoosingWind, text = 'Search this', command = searchTheChosenCity)
        chosenSearchBtn.pack()

    cityChoosingWind.mainloop()


def getWeatherDetails():
    city = cityText.get()
    res = requests.get(urlAPI.format(city, apiKey))
    if res:
        jsonRes = res.json()
        #to receive (coord1, coord2, detDescr, minTemp, maxTemp, windSpeed, pressure, humidity, locTime)
        coordLon = jsonRes['coord']['lon']
        coordLat = jsonRes['coord']['lat']
        detDescr = jsonRes['weather'][0]['description']
        tempMin = jsonRes['main']['temp_min'] - 273.15
        tempMax = jsonRes['main']['temp_max'] - 273.15
        windSpeed = jsonRes['wind']['speed']
        pressure = jsonRes['main']['pressure']
        humid = jsonRes['main']['humidity']
        shiftFromUTC = jsonRes['timezone']
        theDateTimeMes = datetime.utcfromtimestamp(int(jsonRes['dt']) + int(shiftFromUTC)).strftime('%Y-%m-%d %H:%M:%S')
        theDateTime = datetime.fromtimestamp(datetime.utcnow().timestamp()+int(shiftFromUTC)).strftime('%Y-%m-%d %H:%M:%S')
        finalRet = (coordLon, coordLat, detDescr, tempMin, tempMax, windSpeed, pressure, humid, theDateTimeMes, theDateTime)   #it's touple
        return finalRet
    else:
        return None


def openDescr():
    detailsApp = Tk()
    detailsApp.title("Weather description window")
    detailsApp.geometry("700x350")

    locLbl = Label(detailsApp, text = locationLbl['text'], font = ('bold', 20))
    locLbl.pack()

    coordinatesLbl = Label(detailsApp, text = 'Coordinates')
    coordinatesLbl.pack()

    descriptionLbl = Label(detailsApp, text = 'Description')
    descriptionLbl.pack()

    minTemperatoreLbl = Label(detailsApp, text = 'Min Temperature')
    minTemperatoreLbl.pack()

    maxTemperatoreLbl = Label(detailsApp, text = 'Max Temperature')
    maxTemperatoreLbl.pack()

    windSpLbl = Label(detailsApp, text = 'Wind Speed')
    windSpLbl.pack()

    atmPressureLbl = Label(detailsApp, text = 'Atmospheric Pressure')
    atmPressureLbl.pack()

    humidLbl = Label(detailsApp, text = 'Humidity')
    humidLbl.pack()

    locDateTimeMesLbl = Label(detailsApp, text = 'Date and Time')
    locDateTimeMesLbl.pack()

    locDateTimeLbl = Label(detailsApp, text = 'Local Date and Time')
    locDateTimeLbl.pack()

    theDetails = getWeatherDetails()

    if theDetails:
        coordinatesLbl['text'] = '{}, {}'.format(theDetails[1], theDetails[0])
        descriptionLbl['text'] = 'There is: {}'.format(theDetails[2])
        minTemperatoreLbl['text'] = 'Minimal Temperature: {:.2f}°C'.format(theDetails[3])
        maxTemperatoreLbl['text'] = 'Maximal Temperature: {:.2f}°C'.format(theDetails[4])
        windSpLbl['text']= 'Speed of Wind: {} m/s'.format(theDetails[5])
        atmPressureLbl['text'] = 'Atmospheric Pressure: {} hPa'.format(theDetails[6])
        humidLbl['text'] = 'Humidity level: {} %'.format(theDetails[7])
        locDateTimeLbl['text'] = 'Local Date and Time of the request: {}'.format(theDetails[9])
        locDateTimeMesLbl['text'] = 'Local Date and Time of last measurements: {}'.format(theDetails[8])
    else:
        messagebox.showerror('Error', 'Cannot find location')

    detailsApp.mainloop()

#in quick_tabs_cities the cities are stored in JSON format (for 3 buttons):
#quickCitiesData = {
#    '1': 'Rzeszow',
#    '2': 'Casablanca',
#    '3': 'Vinnytsia'
#}

def quickRun(ind):
    if ind == 1:
        cityText.set(quickSearch1Btn['text'])
    if ind == 2:
        cityText.set(quickSearch2Btn['text'])
    if ind == 3:
        cityText.set(quickSearch3Btn['text'])
    search()

def writeQuickBut(ind):
    if cityText.get() != '':
        with open('Data/quick_tabs_cities.json') as json_file:
            dataCities = json.load(json_file)
        if ind == 1:
            quickSearch1Btn['text'] = cityText.get()
            dataCities['1'] = quickSearch1Btn['text']
        if ind == 2:
            quickSearch2Btn['text'] = cityText.get()
            dataCities['2'] = quickSearch2Btn['text']
        if ind == 3:
            quickSearch3Btn['text'] = cityText.get()
            dataCities['3'] = quickSearch3Btn['text']
        with open('Data/quick_tabs_cities.json', 'w') as outfile:
            outfile.truncate(0)
            json.dump(dataCities, outfile)

def historyDisplay():
    with open('Data/search_history.json') as json_file:
        historyCities = json.load(json_file)
    historyOptions = []
    
    #historyOptions[0] = historyCities['city1']
    #historyOptions[1] = historyCities['city2']
    for histIndex in range(5):
        historyOptions.append(historyCities[str(histIndex)])

    def searchChosenCity (chosenCity):
        if(chosenCity != 'Last searches:'):
            cityText.set(chosenCity)
            search()
        menuHist.destroy()

    dropdownSet = StringVar(app)
    dropdownSet.set('Last searches:') 
    menuHist = OptionMenu(app, dropdownSet, *historyOptions, command =  searchChosenCity)
    menuHist.pack()

app = Tk()
app.title("Weather app")
app.geometry('700x350')

cityText = StringVar()
cityEntry = Entry(app, textvariable = cityText)
cityEntry.pack() #placing it on the screen

searchBtn = Button(app, text = 'Search weather', width = 12, command = search)
searchBtn.pack()

locationLbl = Label(app, text = 'Location', font = ('bold', 20))
locationLbl.pack()

img = PhotoImage(file = '')
image = Label(app, image = img)
image.pack()

temperLbl = Label(app, text = 'Temperature')
temperLbl.pack()

weatherLbl = Label(app, text = 'Weather')
weatherLbl.pack()


otherCitiesBtn = Button(app, text = 'Other Cities "{}"'.format(cityText.get()), command = multipleCitiesFound)
otherCitiesBtn.pack()


detailedDescrBtn = Button(app, text = 'View Details', width = 15, command = openDescr)
detailedDescrBtn.pack()



pencilImg = PhotoImage(file = 'tech_icons/pencil.png')
writeQuick1Btn = Button(app, image = pencilImg, command = lambda: writeQuickBut(1))
writeQuick1Btn.place(x = 480, y = 200)

writeQuick2Btn = Button(app, image = pencilImg, command = lambda: writeQuickBut(2))
writeQuick2Btn.place(x = 480, y = 225)

writeQuick3Btn = Button(app, image = pencilImg, command = lambda: writeQuickBut(3))
writeQuick3Btn.place(x = 480, y = 250)


with open('Data/quick_tabs_cities.json') as json_file:
    dataCities = json.load(json_file)

quickSearch1Btn = Button(app, text = dataCities['1'], width = 25, command = lambda: quickRun(1))
quickSearch1Btn.place(x=500,y=200)

quickSearch2Btn = Button(app, text = dataCities['2'], width = 25, command = lambda: quickRun(2))
quickSearch2Btn.place(x=500,y=225)

quickSearch3Btn = Button(app, text = dataCities['3'], width = 25, command = lambda: quickRun(3))
quickSearch3Btn.place(x=500,y=250)


historyBtn = Button(app, text = 'History', command = historyDisplay)
historyBtn.pack()
 
app.mainloop()