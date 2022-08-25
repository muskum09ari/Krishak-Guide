from flask import Flask, render_template, request, Markup,session, redirect, url_for, flash, Response
import requests
import config
import sqlite3
# from forms import LoginForm
import datetime as dt
import os
import bcrypt

def weather_fetch(city_name):
    """
    Fetch and returns the temperature and humidity of a city
    :params: city_name
    :return: temperature, humidity
    """
    api_key = config.weather_api_key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        y = x["main"]

        temperature = round((y["temp"] - 273.15), 2)
        humidity = y["humidity"]
        return temperature, humidity
    else:
        return None
@ app.route('/')
def home():
    title = 'Krishak Guide - Home'
    return render_template('index.html', title=title)
#=================================login signup==================
@ app.route('/login')
def login():
    title = 'Krishak Guide - Home'
    return render_template('login.html', title=title)

@app.route('/logout')
def logout():
    if 'username' in session:  
        session.pop('username',None)  
        return redirect('/');  
    else:  
        return '<p>user already logged out</p>'  

UPLOAD_FOLDER = './static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
@ app.route('/register', methods = ['GET', 'POST'])
def registerpage():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        email = request.form['email']
        file1 = request.files['file1']
        if 'file1' not in request.files:
            return 'there is no file1 in form!'
        path = os.path.join(app.config['UPLOAD_FOLDER'], str(username)+ ".jpg")
        file1.save(path)
        path = str(path)
        print(path)
        try:
            with sqlite3.connect("login.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO users (username,password,email,path) values (?,?,?,?)",(username,hashed,email,path))
                con.commit()
                flash("Successfully Registered")
                return redirect('/login')
        except:
            msg= "Again"
            return render_template("Register.html",msg=msg)
    return render_template("Register.html")

if __name__ == '__main__':
    app.run(debug=False, port='7000')
