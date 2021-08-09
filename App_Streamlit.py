
import streamlit as st
import warnings                     #The warn() function defined in the ‘warning‘ module is used to show warning messages.
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
import json
import time


# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False
# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
    conn.commit()

def login_user(username,password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data




def main():
    """ Common ML Dataset Explorer """
    st.title("Pesticide Residue Detection")
    st.subheader("Login and start Detection")
    
 
    menu = ["SignUp","Login"]
    choice = st.sidebar.selectbox("Menu",menu)

   
    if choice == "Login":
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password",type='password')
        if st.sidebar.checkbox("Login/Logout"):
            # if password == '12345':
            create_usertable()
            hashed_pswd = make_hashes(password)
            result = login_user(username,check_hashes(password,hashed_pswd)) #function call login_user
            if result:
                
                st.success("Logged In as {}".format(username))
                st.sidebar.success("login Success.")
                import pandas
                from sklearn import linear_model
                data1 = pandas.read_csv("pesticide.csv")
                df=data1.sample(frac=1)
                X = df[['PH', 'TVOC']]
                y = df['Residue']
                regr = linear_model.LinearRegression()
                regr.fit(X, y)

                import requests
                x = requests.get('https://pesticide-ece52-default-rtdb.firebaseio.com/.json')
                data = x.json()
                st.image("air.png",width=200)
                air = data["tvoc"]
                ph  = data["ph"]
                predictedPR = regr.predict([[ph, air]])
                airstr = "Pesticide : "+ str(predictedPR[0]) +"%"
                st.subheader(airstr)
                intair = int(predictedPR)
            
                if(intair >30):
                    st.error("Pesticide Residue Detected")
                else:
                    st.success("No Pesticide Residue Detected")
                if st.button("Detect Pesticide Residue"):
                    x = requests.get('https://pesticide-ece52-default-rtdb.firebaseio.com/.json')
                    data = x.json()
                    air = data["tvoc"]
                    ph  = data["ph"]
                    predictedPR = regr.predict([[ph, air]])
                    airstr = "Pesticide : "+ str(predictedPR[0]) +"%"
                    
            else:
                st.error("Login Failed")            
                        

                    
    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password",type='password')

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user,make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")




if __name__ == '__main__':
    main()

