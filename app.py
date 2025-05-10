from flask import Flask, render_template, request
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib import const

app = Flask(__name__)

def get_nakshatra(moon_lon):
    nakshatra_index = int((moon_lon % 360) / (13 + 1/3))
    nakshatras = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha",
        "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
        "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
        "Uttara Bhadrapada", "Revati"
    ]
    return nakshatras[nakshatra_index]

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        dob = request.form['dob']
        tob = request.form['tob']
        place = request.form['place']
        lat = float(request.form['latitude'])
        lon = float(request.form['longitude'])

        dt = Datetime(dob, tob, '+05:30')
        pos = GeoPos(lat, lon)
        chart = Chart(dt, pos, IDs=const.LIST_OBJECTS)

        moon = chart.get(const.MOON)
        asc = chart.get(const.ASC)

        moon_sign = moon.sign
        asc_sign = asc.sign
        nakshatra = get_nakshatra(moon.lon)

        return render_template("report.html", name=name, gender=gender, dob=dob, tob=tob, place=place,
                               moon_sign=moon_sign, asc_sign=asc_sign, nakshatra=nakshatra)
    return render_template("form.html")

if __name__ == '__main__':
    app.run(debug=True)
