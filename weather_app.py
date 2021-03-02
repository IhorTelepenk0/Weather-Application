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

quickTabsFile = 'Data/quick_tabs_cities.json'
historyFile = 'Data/search_history.json'
allCitiesFile = 'Data/city_list.json'

bgColor = '#62B0E5'


def getWeather(city):
    result = requests.get(urlAPI.format(city, apiKey))
    if result:
        jsonRes = result.json()
        city = jsonRes['name']
        country = jsonRes['sys']['country']
        temperKelvin = jsonRes['main']['temp']
        temperCelsius = temperKelvin - 273.15
        icon = jsonRes['weather'][0]['icon']
        weather = jsonRes['weather'][0]['main']
        final = (city, country, temperCelsius, icon, weather) #touple with with appropriate template will be returned
        return final
    else:
        return None

def storeHist(cityName):
     if cityName != '':
        with open(historyFile) as json_file:
            cityStored = json.load(json_file)
            for i in range(4, 0, -1):
                cityStored[str(i)] = cityStored[str(i-1)]
            cityStored['0'] = cityName
        with open(historyFile, 'w') as outfile:
            outfile.truncate(0)
            json.dump(cityStored, outfile)

def findAndDestoryDisplayedElems(window, type):
    allWidgets = window.place_slaves()
    for widget in allWidgets:
        if widget.winfo_class() == type:
            widget.destroy()

def search() :
    city = cityText.get()
    weather = getWeather(city)
    if weather:
        locationLbl['text'] = '{}, {}'.format(weather[0],weather[1])
        img['file'] = 'weather_icons/{}.png'.format(weather[3])
        temperLbl['text'] = '{:.2f}°C'.format(weather[2])
        weatherLbl['text'] = weather[4]
        app.focus()
        storeHist(city)
        detailedDescrBtn.place(relx = 0.5, rely = 0.8, anchor = CENTER)
        otherCitiesBtn['text'] = 'Other Cities "{}"'.format(cityText.get().split(',')[0])
        otherCitiesBtn.place(relx = 0.5, rely = 0.91, anchor = CENTER)
        if historyBtn.winfo_manager() == "" :
            historyBtn.place(relheight = 0.07, relx = 0.3, rely = 0.06)
            findAndDestoryDisplayedElems(app, 'Menubutton')
    else:
        messagebox.showerror('Wrong Location Chosen', '"{}" is not found.'.format(city))

def cityReps(city):
    with open(allCitiesFile, encoding = "UTF-8") as json_file:
        allCities = json.load(json_file)
    repIds = []
    for checkedCityEntry in allCities:
        if checkedCityEntry['name'] == city:
            repIds.append(checkedCityEntry['id'])
    return repIds

def multipleCitiesFound():
    cityChoosingWind = Tk()
    cityChoosingWind.title = "Cities With Such Name:"
    cityChoosingWind.geometry("200x100")

    indicesCities = cityReps(locationLbl['text'].split(',')[0])

    with open(allCitiesFile, encoding = "UTF-8") as json_file:
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
    detailsApp.geometry("500x250")
    detailsApp['bg'] = bgColor

    locLbl = Label(detailsApp, text = locationLbl['text'], font = ('bold', 20))
    locLbl['bg']=bgColor
    locLbl.pack()

    coordinatesLbl = Label(detailsApp, text = 'Coordinates')
    coordinatesLbl['bg']=bgColor
    coordinatesLbl.pack()

    descriptionLbl = Label(detailsApp, text = 'Description')
    descriptionLbl['bg']=bgColor
    descriptionLbl.pack()

    minTemperatureLbl = Label(detailsApp, text = 'Min Temperature')
    minTemperatureLbl['bg']=bgColor
    minTemperatureLbl.pack()

    maxTemperatureLbl = Label(detailsApp, text = 'Max Temperature')
    maxTemperatureLbl['bg']=bgColor
    maxTemperatureLbl.pack()

    windSpLbl = Label(detailsApp, text = 'Wind Speed')
    windSpLbl['bg']=bgColor
    windSpLbl.pack()

    atmPressureLbl = Label(detailsApp, text = 'Atmospheric Pressure')
    atmPressureLbl['bg']=bgColor
    atmPressureLbl.pack()

    humidLbl = Label(detailsApp, text = 'Humidity')
    humidLbl['bg']=bgColor
    humidLbl.pack()

    locDateTimeMesLbl = Label(detailsApp, text = 'Date and Time')
    locDateTimeMesLbl['bg']=bgColor
    locDateTimeMesLbl.pack()

    locDateTimeLbl = Label(detailsApp, text = 'Local Date and Time')
    locDateTimeLbl['bg']=bgColor
    locDateTimeLbl.pack()

    theDetails = getWeatherDetails()

    if theDetails:
        coordinatesLbl['text'] = '{}, {}'.format(theDetails[1], theDetails[0])
        descriptionLbl['text'] = 'There is: {}'.format(theDetails[2])
        minTemperatureLbl['text'] = 'Minimal Temperature: {:.2f}°C'.format(theDetails[3])
        maxTemperatureLbl['text'] = 'Maximal Temperature: {:.2f}°C'.format(theDetails[4])
        windSpLbl['text']= 'Speed of Wind: {} m/s'.format(theDetails[5])
        atmPressureLbl['text'] = 'Atmospheric Pressure: {} hPa'.format(theDetails[6])
        humidLbl['text'] = 'Humidity level: {} %'.format(theDetails[7])
        locDateTimeLbl['text'] = 'Local Date and Time of the request: {}'.format(theDetails[9])
        locDateTimeMesLbl['text'] = 'Local Date and Time of last measurements: {}'.format(theDetails[8])
    else:
        messagebox.showerror('Error', 'Cannot find location')

    detailsApp.mainloop()

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
        with open(quickTabsFile) as json_file:
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
        with open(quickTabsFile, 'w') as outfile:
            outfile.truncate(0)
            json.dump(dataCities, outfile)

def historyDisplay():
    
    with open(historyFile) as json_file:
        historyCities = json.load(json_file)
    historyOptions = []

    for histIndex in range(5):
        historyOptions.append(historyCities[str(histIndex)])

    def searchChosenCity (chosenCity):
        if(chosenCity != 'Last searches:'):
            cityText.set(chosenCity)
            historyBtn.place(relheight = 0.07, relx = 0.3, rely = 0.06)
            search()
            menuHist.destroy()
        
    dropdownSet = StringVar(app)
    dropdownSet.set('Last searches:') 
    menuHist = OptionMenu(app, dropdownSet, *historyOptions, command =  searchChosenCity)
    historyBtn.place_forget()
    menuHist.place(relheight = 0.07, relx = 0.21, rely = 0.06)

#the actual app GUI:

app = Tk()
app.title("Weather application")
app.geometry('700x350')
app['bg'] = bgColor

cityText = StringVar()
cityEntry = Entry(app, textvariable = cityText)
cityEntry.place(relwidth = 0.2, relheight = 0.07, relx = 0.39, rely = 0.06)

searchImg = PhotoImage(file = 'tech_icons/search_icon.png')
searchBtn = Button(app, image = searchImg, width = 12, command = search)
searchBtn['bg'] = '#FFFFFF'
searchBtn.place(relwidth = 0.04, relheight = 0.07, relx = 0.6, rely = 0.06)

locationLbl = Label(app, text = '', font = ('bold', 20), justify = CENTER)
locationLbl['bg'] = bgColor
locationLbl.place(relwidth = 0.38, relx = 0.5, rely = 0.25, anchor = CENTER)

img = PhotoImage(file = '')
image = Label(app, image = img, justify = CENTER)
image['bg'] = bgColor
image.place(relx = 0.5, rely = 0.44, anchor = CENTER)

temperLbl = Label(app, text = '', font = ('bold'), justify = CENTER)
temperLbl['bg'] = bgColor
temperLbl.place(relx = 0.5, rely = 0.6, anchor = CENTER)

weatherLbl = Label(app, text = '', justify = CENTER)
weatherLbl['bg'] = bgColor
weatherLbl.place(relx = 0.5, rely = 0.7, anchor = CENTER)


otherCitiesBtn = Button(app, text = 'Other Cities', command = multipleCitiesFound)


detailedDescrBtn = Button(app, text = 'View Details', width = 15, command = openDescr)


pencilImg = PhotoImage(file = 'tech_icons/pencil.png')
writeQuick1Btn = Button(app, image = pencilImg, command = lambda: writeQuickBut(1))
writeQuick1Btn.place(relx = 0.7, rely = 0.37, anchor = CENTER)

writeQuick2Btn = Button(app, image = pencilImg, command = lambda: writeQuickBut(2))
writeQuick2Btn.place(relx = 0.7, rely = 0.45, anchor = CENTER)

writeQuick3Btn = Button(app, image = pencilImg, command = lambda: writeQuickBut(3))
writeQuick3Btn.place(relx = 0.7, rely = 0.53, anchor = CENTER)


with open(quickTabsFile) as json_file:
    dataCities = json.load(json_file)

quickSearch1Btn = Button(app, text = dataCities['1'], width = 25, command = lambda: quickRun(1))
quickSearch1Btn.place(relx = 0.85, rely = 0.37, anchor = CENTER)

quickSearch2Btn = Button(app, text = dataCities['2'], width = 25, command = lambda: quickRun(2))
quickSearch2Btn.place(relx = 0.85, rely = 0.45, anchor = CENTER)

quickSearch3Btn = Button(app, text = dataCities['3'], width = 25, command = lambda: quickRun(3))
quickSearch3Btn.place(relx = 0.85, rely = 0.53, anchor = CENTER)


historyBtn = Button(app, text = 'History', command = historyDisplay)
historyBtn.place(relheight = 0.07, relx = 0.3, rely = 0.06)
 
app.mainloop()