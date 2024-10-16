import tkinter as tk
from tkinter import *
from geopy.geocoders import Nominatim
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz

window = Tk()
window.title("weather app")
window.geometry("900x500")
window.resizable(False, False)

def getWeather():
    try:
        city = textfield.get()#getting the input from user

        if not city:
            raise ValueError("City name cannot be empty")

        geolocator = Nominatim(user_agent="geoapiExercise")
        location = geolocator.geocode(city)

        if location is None:
            raise ValueError("Invalid city name, please try again")

        # Get timezone information
        obj = TimezoneFinder()
        result = obj.timezone_at(lng=location.longitude, lat=location.latitude)

        if result is None:
            raise ValueError("Could not determine timezone for the city")

        # Get current time in the city's timezone
        home = pytz.timezone(result)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")
        clock.config(text=current_time)
        name.config(text="CURRENT WEATHER")

        # Fetch weather data from API
        api = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=06c921750b9a82d8f5d1294e1586276f"
        json_data = requests.get(api).json()

        if json_data['cod'] != 200:
            raise ValueError("Unable to retrieve weather data for this city")

        # Extract weather data
        condition = json_data['weather'][0]['main']
        description = json_data['weather'][0]['description']
        temp = int(json_data["main"]["temp"] - 273.15)
        pressure = json_data["main"]["pressure"]
        humidity = json_data["main"]["humidity"]
        wind = json_data["wind"]["speed"]

        # Update labels with weather data
        t.config(text=(temp, "°C"))
        c.config(text=(condition,"|","FEELS","LIKE",temp,"°C"))
        w.config(text=(wind, "km/h"))
        h.config(text=(humidity, "%"))
        d.config(text=description)
        p.config(text=pressure)

    except ValueError as ve:
        messagebox.showerror("Error", str(ve))
    except requests.exceptions.RequestException as re:
        messagebox.showerror("Error", "Network error. Please check your internet connection.")
    except Exception as e:
        messagebox.showerror("Error", "An unexpected error occurred: " + str(e))


#search box
search_image = PhotoImage(file="search.png")
myimage = Label (image = search_image)
myimage.place(x= 20,y=20)

textfield = Entry(window,justify = "center",width = 17,font = ("poppins",25,"bold"),bg ="#404040",fg="white",border = 0)
textfield.place(x= 50 , y = 40)
textfield.focus()

#search icon
search_icon = PhotoImage(file= "search_icon.png")
myimage_icon = Button(window,image=search_icon,borderwidth=0,cursor="hand2",bg="#404040",command=getWeather)
myimage_icon.place(x=400, y = 34)

#Logo
logo_icon = PhotoImage(file="logo.png")
logo = Label(image=logo_icon)
logo.place(x=150,y = 100)

#bottom box
box_icon = PhotoImage(file="box.png")
box = Label(image=box_icon)
box.pack(padx= 5,pady= 5 ,side=BOTTOM)

#time
name =Label(window,font=("arial",15,"bold"))
name.place(x=30,y=100)

clock = Label(window,font=("felix titling",20))
clock.place(x=30,y=130)


#label
label1 = Label(window,text="WIND",font=("felix titling",15,"bold"),fg="white",bg="#1ab5ef")
label1.place(x=120,y=400)

label2 = Label(window,text="HUMIDITY",font=("felix titling",15,"bold"),fg="white",bg="#1ab5ef")
label2.place(x=250,y=400)

label3 = Label(window,text="DESCRIPTION",font=("felix titling",15,"bold"),fg="white",bg="#1ab5ef")
label3.place(x=430,y=400)

label4 = Label(window,text="PRESSURE",font=("felix titling",15,"bold"),fg="white",bg="#1ab5ef")
label4.place(x=650,y=400)

#temparature
t = Label(font=("arial",70,"bold"),fg="#ee666d")
t.place(x=400,y = 150)

#condition
c= Label(font=("arial",15,"bold"))
c.place(x=400,y=250)

#wind
w = Label(text="...",font=("arial",20,"bold"),bg="#1ab5ef")
w.place(x=100,y=430)

#humidity
h=Label(text="...",font=("arial",20,"bold"),bg="#1ab5ef")
h.place(x=280,y=430)

#description
d =Label(text="...",font=("arial",20,"bold"),bg="#1ab5ef")
d.place(x=420,y=430)

#pressure
p =Label(text="...",font=("arial",20,"bold"),bg="#1ab5ef")
p.place(x=670,y=430)



window.mainloop()

