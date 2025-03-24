import streamlit as st
import re
import sqlite3 
import pickle
import bz2
import pandas as pd
import numpy as np
import random

st.set_page_config(
    page_title="Multi-Syndrome Classification",
    page_icon="fevicon.webp",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None
)

# -------------------- ADVANCED CSS INJECTION --------------------
# We'll do a glassmorphic effect for the container, a dynamic gradient background,
# and more stylish transitions for elements.

# Generate random gradient or color combos
random_seed = random.randint(1, 100000)
colors = [
    "#ff9a9e", "#fad0c4", "#fbc2eb", "#a1c4fd", "#c2e9fb",
    "#d4fc79", "#96e6a1", "#84fab0", "#8fd3f4", "#e0c3fc"
]
import random
gradient1 = random.choice(colors)
gradient2 = random.choice(colors)
while gradient2 == gradient1:
    gradient2 = random.choice(colors)

st.markdown(rf"""
    <style>
    /* Dynamic animated gradient background */
    @keyframes gradientBG {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    .stApp, .reportview-container {{
        background: linear-gradient(135deg, {gradient1}, {gradient2});
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }}

    /* Glassmorphic container: a translucent, blurred background */
    .main .block-container {{
        margin-top: 2rem !important;
        margin-bottom: 2rem !important;
        padding: 2rem !important;
        background: rgba(255, 255, 255, 0.25) !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.18) !important;
        transition: all 0.3s ease-in-out !important;
    }}

    /* Sidebar with subtle gradient */
    [data-testid="stSidebar"] {{
        background: linear-gradient(135deg, rgba(255,255,255,0.7), rgba(255,255,255,0.4)) !important;
        backdrop-filter: blur(5px) !important;
        -webkit-backdrop-filter: blur(5px) !important;
        border-radius: 0 16px 16px 0 !important;
        transition: all 0.3s ease-in-out !important;
    }}

    /* Buttons with gradient background and stylish hover */
    .stButton>button {{
        background: linear-gradient(135deg, #6e8efb, #a777e3) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        border: none !important;
        transition: transform 0.3s, background 0.3s !important;
        font-weight: 600 !important;
    }}
    .stButton>button:hover {{
        background: linear-gradient(135deg, #5a7be0, #9a62dd) !important;
        transform: translateY(-3px) scale(1.03) !important;
    }}

    /* Input fields with focus glow */
    .stTextInput>div>div>input {{
        border-radius: 10px !important;
        border: 1px solid #ccc !important;
        padding: 10px !important;
        box-shadow: 0 0 3px rgba(0,0,0,0.1) !important;
        transition: box-shadow 0.3s !important;
    }}
    .stTextInput>div>div>input:focus {{
        outline: none !important;
        box-shadow: 0 0 6px rgba(0,0,0,0.2) !important;
        border: 1px solid #6e8efb !important;
    }}
    </style>
""", unsafe_allow_html=True)
# ----------------------------------------------------------------

conn = sqlite3.connect('data.db')
c = conn.cursor()

# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(FirstName TEXT,LastName TEXT,Mobile TEXT,City TEXT,Email TEXT,password TEXT,Cpassword TEXT)')

def add_userdata(FirstName,LastName,Mobile,City,Email,password,Cpassword):
    c.execute('INSERT INTO userstable(FirstName,LastName,Mobile,City,Email,password,Cpassword) VALUES (?,?,?,?,?,?,?)',(FirstName,LastName,Mobile,City,Email,password,Cpassword))
    conn.commit()

def login_user(Email,password):
    c.execute('SELECT * FROM userstable WHERE Email =? AND password = ?',(Email,password))
    data = c.fetchall()
    return data

def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data

def delete_user(Email):
    c.execute("DELETE FROM userstable WHERE Email="+"'"+Email+"'")
    conn.commit()

st.title("Multi-Syndrome Classification")

menu = ["Home","Login","SignUp"]
choice = st.sidebar.selectbox("Menu",menu)

if choice=="Home":
    st.markdown(
        """
        <p align="justify">
        <b style="color:black">
        Multi-Syndrome diseases as Diabetes, Anemia, Thalassemia, Heart illnesses, Thrombocytopenia, and Health is important for the diagnosis and treatment within the sphere of healthcare. This paper offers a new approach to the categorization of syndromes employing machine learning approaches. In machine learning Procedure, the Random Forest Algorithm, and the Extra Trees modules are used to improve the classifier’s speed and ability to avoid noise data. Feature selection techniques are employed in extracting features from different medical data sources and thus enhancing discriminant property of made models. A cost-benefit analysis is therefore commenced, whereby the performance of the combined ensemble models is compared with that of the conventional single-model techniques. Numerous studies that examine medical datasets show that our approach to ensemble learning significantly outperforms other frameworks for the investigation of a range of conditions. This study greatly enriches the knowledge of syndrome classification and provides a reliable adjacent syntactic classifier for clinicians and scholars who are involved in various types of disorders.
        </b>
        </p>
        """,
        unsafe_allow_html=True
    )
    
if choice=="Login":
    Email = st.sidebar.text_input("Email")
    Password = st.sidebar.text_input("Password",type="password")
    b1=st.sidebar.checkbox("Login")
    if b1:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, Email):
            create_usertable()
            if Email=='a@a.com' and Password=='123':
                st.success("Logged In as {}".format("Admin"))
                Email=st.text_input("Delete Email")
                if st.button('Delete'):
                    delete_user(Email)
                user_result = view_all_users()
                clean_db = pd.DataFrame(user_result,columns=["FirstName","LastName","Mobile","City","Email","password","Cpassword"])
                st.dataframe(clean_db)
            else:
                result = login_user(Email,Password)
                if result:
                    st.success("Logged In as {}".format(Email))
                    menu2 = ["K-Nearest Neighbors", "Decision Tree", "Random Forest",
                             "Naive Bayes","ExtraTreesClassifier"]
                    choice2 = st.selectbox("Select ML",menu2)
                    sfile1 = bz2.BZ2File('features.pkl', 'r')
                    selected_features=pickle.load(sfile1)
                    choices=[]
                    k=0
                    for feature in selected_features:
                        opt = ["False","True"]
                        choice = st.selectbox(feature,opt)
                        if choice=="True":
                            choices.append(1)
                        else:
                            choices.append(0)
                        k=k+1
                    b2=st.button("Predict")
                    sfile = bz2.BZ2File('model.pkl', 'r')
                    model=pickle.load(sfile)
                    tdata=choices
                    df=pd.read_csv("Disease precaution.csv")
                    df = df.applymap(lambda x: x.strip().lower() if isinstance(x, str) else x)
                    diseases=['drug reaction','allergy','common cold', 'chickenpox', 
                              'neonatal jaundice', 'pneumonia', 'infectious gastroenteritis']
                    df["Disease"]=df["Disease"].str.replace("chicken pox","chickenpox")
                    df["Disease"]=df["Disease"].str.replace("jaundice","neonatal jaundice")
                    df["Disease"]=df["Disease"].str.replace("gastroenteritis","infectious gastroenteritis")
                    df = df[df['Disease'].isin(diseases)]
                    df = df.fillna("")
                    df['Precautions'] = df[['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']].apply(lambda x: ', '.join(x), axis=1)
                    df.drop(columns=['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4'], inplace=True)
                    df.reset_index(inplace=True,drop=True)
                    
                    
                    if b2:
                        if len(np.unique(tdata))==1:
                            if np.unique(tdata)==1:
                                st.success("Please Contact Nearest Doctor")
                            else:
                                st.success("You are healthy")
                        else:
                                
                            if choice2=="K-Nearest Neighbors":
                                test_prediction = model[0].predict([tdata])
                                query=test_prediction[0]
                                score=np.amax(model[0].predict_proba([tdata]))
                                st.success(query)
                                st.success("Probability: "+str(score))            
                            if choice2=="Decision Tree":
                                test_prediction = model[1].predict([tdata])
                                query=test_prediction[0]
                                score=np.amax(model[1].predict_proba([tdata]))
                                st.success(query)
                                st.success("Probability: "+str(score))
                            if choice2=="Random Forest":
                                test_prediction = model[2].predict([tdata])
                                query=test_prediction[0]
                                score=np.amax(model[2].predict_proba([tdata]))
                                st.success(query)
                                st.success("Probability: "+str(score))
                            if choice2=="Naive Bayes":
                                test_prediction = model[3].predict([tdata])
                                query=test_prediction[0]
                                score=np.amax(model[3].predict_proba([tdata]))
                                st.success(query)
                                st.success("Probability: "+str(score))
                            if choice2=="ExtraTreesClassifier":
                                test_prediction = model[4].predict([tdata])
                                query=test_prediction[0]
                                score=np.amax(model[4].predict_proba([tdata]))
                                st.success(query)
                                st.success("Probability: "+str(score))
                            st.success(df[df['Disease']==query]["Precautions"].to_numpy()[0])
                else:
                    st.warning("Incorrect Email/Password")
        else:
            st.warning("Not Valid Email")
                
           
if choice=="SignUp":
    Fname = st.text_input("First Name")
    Lname = st.text_input("Last Name")
    Mname = st.text_input("Mobile Number")
    Email = st.text_input("Email")
    City = st.text_input("City")
    Password = st.text_input("Password",type="password")
    CPassword = st.text_input("Confirm Password",type="password")
    b2=st.button("SignUp")
    if b2:
        pattern=re.compile("(0|91)?[7-9][0-9]{9}")
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if Password==CPassword:
            if (pattern.match(Mname)):
                if re.fullmatch(regex, Email):
                    create_usertable()
                    add_userdata(Fname,Lname,Mname,City,Email,Password,CPassword)
                    st.success("SignUp Success")
                    st.info("Go to Logic Section for Login")
                else:
                    st.warning("Not Valid Email")         
            else:
                st.warning("Not Valid Mobile Number")
        else:
            st.warning("Pass Does Not Match")
