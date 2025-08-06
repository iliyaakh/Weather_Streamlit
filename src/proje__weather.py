import requests
import streamlit as st
import sqlite3

def get_city(city):
    url = f"http://api.weatherapi.com/v1/forecast.json?key=de5f1da10b0e470ea2a90124250408&q={city}&days=5"
    try:
        respoonse = requests.get(url)
        if respoonse.status_code != 200 :
            return'page not finde'
        else:
            respoonse = respoonse.json()
            rate = respoonse['location']['name']
            return rate
    except requests.RequestException:
        return None 
    

def get_date(city):
    url = f"http://api.weatherapi.com/v1/forecast.json?key=de5f1da10b0e470ea2a90124250408&q={city}&days=5"
    respoonse = requests.get(url)
    if respoonse.status_code != 200 :
        return'page not finde'
    else:
        respoonse = respoonse.json()
        rate = respoonse['location']['localtime']
        return rate

def get_temp_c(city):
    url = f"http://api.weatherapi.com/v1/forecast.json?key=de5f1da10b0e470ea2a90124250408&q={city}&days=5"
    respoonse = requests.get(url)
    if respoonse.status_code != 200 :
        return'page not finde'
    else:
        respoonse = respoonse.json()
        rate = respoonse['current']['temp_c']
        return rate
    
def get_temp_f(city):
    url = f"http://api.weatherapi.com/v1/forecast.json?key=de5f1da10b0e470ea2a90124250408&q={city}&days=5"
    respoonse = requests.get(url)
    if respoonse.status_code != 200 :
        return'page not finde'
    else:
        respoonse = respoonse.json()
        rate = respoonse['current']['temp_f']
        return rate
    
def get_condition(city):
    url = f"http://api.weatherapi.com/v1/forecast.json?key=de5f1da10b0e470ea2a90124250408&q={city}&days=5"
    respoonse = requests.get(url)
    if respoonse.status_code != 200 :
        return'page not finde'
    else:
        respoonse = respoonse.json()
        rate = respoonse['current']['condition']['text']
        return rate
    
def get_humidity(city):
    url = f"http://api.weatherapi.com/v1/forecast.json?key=de5f1da10b0e470ea2a90124250408&q={city}&days=5"
    respoonse = requests.get(url)
    if respoonse.status_code != 200 :
        return'page not finde'
    else:
        respoonse = respoonse.json()
        rate = respoonse['current']['humidity']
        return rate

    
con = sqlite3.connect('weather.db')
cursor = con.cursor()

sql_creat_table = ''' CREATE TABLE IF NOT EXISTS weather 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  city TEXT, tempC INTEGER, tempF INTEGER,
                  humidity TEXT, form TEXT, date_time TEXT)
                              '''
cursor.execute(sql_creat_table)
con.commit()


def insert(city, tempC, tempF, humidity, form, date_time):
    try:    
        cursor.execute('INSERT INTO weather (city, tempC, tempF, humidity, form, date_time) VALUES (?,?,?,?,?,?)',
                    (city, tempC, tempF, humidity, form, date_time))
        con.commit()
    except sqlite3.Error:
        st.error(f"Database error: sqlite3.error")

def delete(id):
    cursor.execute('DELETE FROM weather WHERE id = ?', (id,))
    con.commit()

def delete_all():
    cursor.execute('DELETE FROM weather')
    con.commit()

def read_where1(city):
    cursor.execute('SELECT * FROM weather WHERE city = ?', (city,))
    return cursor.fetchall()

def read_where2(id):
    cursor.execute('SELECT * FROM weather WHERE id = ?', (id,))
    return cursor.fetchall()

def read_full():
    cursor.execute('SELECT * FROM weather')
    return cursor.fetchall()

st.sidebar.title('setting')
setting = st.sidebar.selectbox('diagrees', ('weather','Delete from history','Delete all history',
                                            'search by ID','search by city','Make Table','About us'))

if setting == 'weather':
    st.title('Welcom to your Website')
    st.write('Check the weather for any city!')
    city = st.text_input('Enter your city : ').capitalize()
    
    if city:
        result = get_city(city)
        if result == None:
            st.error('Error : requests conection')
        elif result == 'page not finde':
            st.error('Error : Invalid name city')
        else:
            result2 = get_temp_c(city)
            result3 = get_temp_f(city)
            result4 = f'{get_humidity(city)}%' 
            result5 = get_condition(city)
            result6 = get_date(city)

            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.write("City :", result)
            col2.metric(f"Temp °C of {result}", f"{result2} °C")
            col3.metric(f"Temp °F of {result}", f"{result3} °F")
            col4.metric(f"Humidity of {result}", f'{result4}')
            with col5:
                st.write(f"Weather condition of {result} :", result5)
            
            if st.button('save'):    
                insert(result, result2, result3, result4, result5, result6)
                st.success('insert table')

elif setting == 'Delete from history':
    st.title('Delete by ID')
    id = st.number_input("Enter ID:", min_value=1, step=1)
    if st.button("Delete"):
        results = read_where2(id)
        if results:
            delete(id)
            st.success(f'Record with ID {id} deleted')
        else:
            st.error(f'No record found with ID {id}')

elif setting == 'Delete all history':
    st.title("Delete All History")
    if st.button("Confirm deletion"):
        delete_all()
        st.success("All records cleared")  

elif setting == 'search by city':
    city = st.text_input('Enter city :').capitalize()
    if st.button('search'):
        results = read_where1(city)
        if results:
            st.dataframe(results, column_config={"0": "ID", "1": "city", "2": "temp C", "3": "temp F", "4": "humidity", "5": "form", "6": "date & time"})
        else:
            st.info("No records found")

elif setting == 'search by ID':
    id = st.number_input('Enter id :', step = 1, min_value = 1)
    if st.button('search'):
        results = read_where2(id)
        if results:
            st.dataframe(results, column_config=
                         {"0": "ID", "1": "city", "2": "temp C", "3": "temp F", "4": "humidity", "5": "form", "6": "date & time"})
        else:
            st.info("No records found")
            
elif setting == 'Make Table':
    st.title("world of weather")
    data = read_full()
    if data:
        st.dataframe(data, column_config=
                     {"0": "ID", "1": "city", "2": "temp C", "3": "temp F", "4": "humidity", "5": "form", "6": "date & time"})
    else:
        st.info("No records in database")

elif setting == 'About us':
    st.title('About This Project')
    st.write("This Streamlit project, developed by Iliya, provides " \
    "real-time weather data for any city using the WeatherAPI. Store weather records, view history, and manage data easily.")
    st.title('Contact Us')

    st.write('you can contact us via :')
    col1 , col2 , col3 = st.columns(3)
    with col1 : 
        st.write('Telegram : @iliya_12344')
        st.link_button('Go to Telegram', 'https://t.me/iliya_12344')
    with col2 :
        st.markdown('Instagram : @iliyakh177')
        st.link_button('Go to Instagram', 'https://www.instagram.com/iliyakh177?igsh=dXpkNHM2OTl6OHho')
    with col3 :
        st.write('Email : iliyakh660@gmail.com')