from flask import Flask , render_template , request
import requests
import json

app = Flask(__name__)

API_KEY = '04c9f4944719cf8c730037388318c80c'
API_URL = ('http://api.openweathermap.org/data/2.5/weather?q={}&mode=json&units=metric&appid={}')

def query_API(city):
    print(API_URL.format(city,API_KEY))
    data = requests.get(API_URL.format(city,API_KEY)).json() # any data is turned into json format
    return data

@app.route('/')
def index():
    resp = query_API('London')
    print(resp)
    city = resp['name']
    temp = resp['main']['temp']
    country = resp['sys']['country']
    weather = resp['weather'][0]['description']
    icon_code = resp['weather'][0]['icon']
    humidity = resp['main']['humidity']
    feels_like = resp['main']['feels_like']
    pressure = resp['main']['pressure']
    windspeed = resp['wind']['speed']
    return render_template('index.html',city = city , temp = temp , country = country , weather = weather ,
                           icon_code = icon_code , humidity = humidity , feels_like = feels_like,pressure = pressure , windspeed = windspeed)

@app.route('/results',methods=['GET','POST'])
def results():
    input_city = request.form.get('city')
    resp = query_API(input_city)
    error = None
    if resp :
        if len(resp) <= 2:
            error = resp['message']
        else:
            city = resp['name']
            temp = resp['main']['temp']
            country = resp['sys']['country']
            weather = resp['weather'][0]['description']
            icon_code = resp['weather'][0]['icon']
            humidity = resp['main']['humidity']
            feels_like = resp['main']['feels_like']
            return render_template('index.html', city=city, temp=temp, country=country, weather=weather,
                                   icon_code=icon_code, humidity=humidity, feels_like=feels_like)
    return render_template("index.html", error=error)

if __name__ == '__main__':
    app.run(debug = True)
