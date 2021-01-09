from tkinter import *
from tkinter import messagebox
from configparser import ConfigParser
import requests
#vs


urlAPI = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

configFile = 'config.ini'
config = ConfigParser()
config.read(configFile)
apiKey = config['apiKey']['key']
#print(apiKey)

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

#print(getWeather('London'))

def search() :
    city = cityText.get()
    weather = getWeather(city)
    if weather:
        locationLbl['text'] = '{},{}'.format(weather[0],weather[1])
        img['file'] = 'weather_icons/{}.png'.format(weather[3])
        temperLbl['text'] = '{:.2f}°C'.format(weather[2])
        weatherLbl['text'] = weather[4]
    else:
        messagebox.showerror('Error', 'Cannot find {}'.format(city))

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


app.mainloop()