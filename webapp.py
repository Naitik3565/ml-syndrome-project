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

# ---------- ADVANCED CSS & PAGE REVEAL ANIMATION ----------
random_seed = random.randint(1, 100000)
colors = [
    "#ff9a9e", "#fad0c4", "#fbc2eb", "#a1c4fd", "#c2e9fb",
    "#d4fc79", "#96e6a1", "#84fab0", "#8fd3f4", "#e0c3fc"
]
gradient1 = random.choice(colors)
gradient2 = random.choice(colors)
while gradient2 == gradient1:
    gradient2 = random.choice(colors)

# Use an online GIF for the Home sidebar
gif_uri = (
    "https://media3.giphy.com/media/kU4mcmHfmV7YhuIj6J/giphy.gif?cid=6c09b952jde0zs8ef57caedbufi3t542i99cf63zjo7ryykh"
    "&ep=v1_stickers_search&rid=giphy.gif&ct=s"
)

# Updated paragraph text & word animation for Home page
paragraph_words = [
    "Multi-Syndrome", "diseases", "such", "as", "Diabetes,", "Anemia,", "Thalassemia,", "Heart", "illnesses,",
    "and", "Thrombocytopenia", "play", "a", "crucial", "role", "in", "healthcare", "diagnosis", "and", "treatment.",
    "This", "project", "introduces", "a", "novel", "approach", "to", "categorizing", "these", "syndromes", "using",
    "machine", "learning.", "Algorithms", "like", "Random", "Forest", "and", "Extra", "Trees", "help", "improve",
    "the", "classifier's", "speed", "and", "minimize", "noise,", "while", "feature", "selection", "techniques",
    "enhance", "model", "accuracy.", "A", "cost-benefit", "analysis", "compares", "ensemble", "models", "with",
    "traditional", "single-model", "techniques,", "providing", "valuable", "insights", "for", "clinicians", "and",
    "researchers."
]
drop_text_html = " ".join([f"<span>{word}</span>" for word in paragraph_words])

# Insert custom CSS for animations, transitions, and styling
st.markdown(rf"""
    <style>
    /* TWO-PANEL PAGE REVEAL (left & right) */
    .page-overlay {{
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        display: flex;
        z-index: 9999;
        pointer-events: none;
        background: none;
    }}
    .panel-left, .panel-right {{
        width: 50%;
        height: 100%;
        background: #fff;
    }}
    .panel-left {{
        animation: slideLeft 1.5s forwards;
    }}
    .panel-right {{
        animation: slideRight 1.5s forwards;
    }}
    @keyframes slideLeft {{
        0%   {{ transform: translateX(0); }}
        100% {{ transform: translateX(-100%); }}
    }}
    @keyframes slideRight {{
        0%   {{ transform: translateX(0); }}
        100% {{ transform: translateX(100%); }}
    }}

    /* Animate background (5s cycle) */
    @keyframes gradientBG {{
        0%   {{ background-position: 0% 50%; }}
        50%  {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    .stApp, .reportview-container {{
        background: linear-gradient(to top left, {gradient1}, {gradient2});
        background-size: 400% 400%;
        animation: gradientBG 5s ease infinite;
    }}

    /* Sparkle overlay behind content (optional) */
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        pointer-events: none;
        background: url("https://i.pinimg.com/originals/55/6d/ab/556dab3f9d1c3f2e7ec7bfeb8d2a6fa8.png") repeat;
        opacity: 0.2;
        animation: sparkleMove 8s linear infinite;
    }}
    @keyframes sparkleMove {{
        0%   {{ background-position: 0% 0%; }}
        100% {{ background-position: 100% 100%; }}
    }}

    /* Glassmorphic container for main content */
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
        position: relative;
        z-index: 1;
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

    /* Drop-sequence text animation for Home page */
    .home-text-container {{
        opacity: 0;
        animation: homeTextTransition 5s forwards;
    }}
    @keyframes homeTextTransition {{
        0%   {{ opacity: 0; transform: translateY(-50px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
    }}

    /* LOGIN PAGE IMAGE TRANSITION: continuous motion for the login page image */
    .login-image img {{
        animation: imageMotion 5s linear infinite alternate;
    }}
    @keyframes imageMotion {{
        0%   {{ transform: translate(100%, 100%); opacity: 0.5; }}
        50%  {{ transform: translate(-100%, -100%); opacity: 1; }}
        100% {{ transform: translate(100%, 100%); opacity: 0.5; }}
    }}

    /* Login container text transition effect for all elements inside the login container */
    #login-container * {{
        animation: loginTextTransition 5s ease-out;
    }}
    @keyframes loginTextTransition {{
        from {{ opacity: 0; transform: translateY(-50px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    </style>
""", unsafe_allow_html=True)

# Two sliding panels that reveal after 1.5s
st.markdown(
    """
    <div class="page-overlay">
      <div class="panel-left"></div>
      <div class="panel-right"></div>
    </div>
    """,
    unsafe_allow_html=True
)

# Hide the "Menu" label on the selectbox in the sidebar
choice = st.sidebar.selectbox("", ["Home", "Login", "SignUp"], label_visibility="collapsed")

# Database Setup
conn = sqlite3.connect('data.db')
c = conn.cursor()

def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(FirstName TEXT,LastName TEXT,Mobile TEXT,City TEXT,Email TEXT,password TEXT,Cpassword TEXT)')

def add_userdata(FirstName,LastName,Mobile,City,Email,password,Cpassword):
    c.execute('INSERT INTO userstable(FirstName,LastName,Mobile,City,Email,password,Cpassword) VALUES (?,?,?,?,?,?,?)',
              (FirstName,LastName,Mobile,City,Email,password,Cpassword))
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

# ------------------- HOME PAGE -------------------
if choice == "Home":
    # Show the optional GIF in the sidebar for Home page
    st.sidebar.markdown(
        f"""
        <div style="text-align:center; margin-top:1rem;">
          <img src="{gif_uri}" alt="Side GIF" style="width:100%; border-radius:10px;" />
        </div>
        """,
        unsafe_allow_html=True
    )
    # The paragraph text with drop-sequence animation wrapped in a container with transition
    st.markdown(
        f"""
        <div class="home-text-container" style="margin-top:1.5rem; text-align:justify; line-height:1.6;">
            {drop_text_html}
        </div>
        """,
        unsafe_allow_html=True
    )

# ------------------- LOGIN PAGE -------------------
elif choice == "Login":
    # Wrap the login page content in a container with an ID for transition effect
    st.markdown("<div id='login-container'>", unsafe_allow_html=True)
    
    # Only display the large image if the login checkbox is NOT checked
    b1 = st.sidebar.checkbox("Login")
    if not b1:
        st.markdown("<div class='login-image'>", unsafe_allow_html=True)
        st.image(
            "https://static.vecteezy.com/system/resources/previews/000/608/082/original/vector-set-of-doctor-cartoon-characters-medical-staff-team-concept.jpg",
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Sidebar login inputs remain unchanged
    Email = st.sidebar.text_input("Email")
    Password = st.sidebar.text_input("Password", type="password")
    
    # Place a small GIF in the sidebar (below the login fields)
    st.sidebar.image(
        "https://delinepal.com/assets/images/Account/63787-secure-login.gif",
        width=150
    )
    
    if b1:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, Email):
            create_usertable()
            if Email == 'a@a.com' and Password == '123':
                st.success("Logged In as Admin")
                Email_to_delete = st.text_input("Delete Email")
                if st.button('Delete'):
                    delete_user(Email_to_delete)
                user_result = view_all_users()
                clean_db = pd.DataFrame(
                    user_result,
                    columns=["FirstName", "LastName", "Mobile", "City", "Email", "password", "Cpassword"]
                )
                st.dataframe(clean_db)
            else:
                result = login_user(Email, Password)
                if result:
                    st.success(f"Logged In as {Email}")
                    menu2 = ["K-Nearest Neighbors", "Decision Tree", "Random Forest",
                             "Naive Bayes", "ExtraTreesClassifier"]
                    choice2 = st.selectbox("Select ML", menu2)
    
                    sfile1 = bz2.BZ2File('features.pkl', 'r')
                    selected_features = pickle.load(sfile1)
                    choices = []
                    for feature in selected_features:
                        opt = ["False", "True"]
                        sel = st.selectbox(feature, opt)
                        choices.append(1 if sel == "True" else 0)
    
                    b2 = st.button("Predict")
                    sfile = bz2.BZ2File('model.pkl', 'r')
                    model = pickle.load(sfile)
                    tdata = choices
    
                    df = pd.read_csv("Disease precaution.csv")
                    df = df.applymap(lambda x: x.strip().lower() if isinstance(x, str) else x)
                    diseases = [
                        'drug reaction', 'allergy', 'common cold', 'chickenpox',
                        'neonatal jaundice', 'pneumonia', 'infectious gastroenteritis'
                    ]
                    df["Disease"] = df["Disease"].str.replace("chicken pox", "chickenpox")
                    df["Disease"] = df["Disease"].str.replace("jaundice", "neonatal jaundice")
                    df["Disease"] = df["Disease"].str.replace("gastroenteritis", "infectious gastroenteritis")
                    df = df[df['Disease'].isin(diseases)]
                    df = df.fillna("")
                    df['Precautions'] = df[['Precaution_1','Precaution_2','Precaution_3','Precaution_4']].apply(
                        lambda x: ', '.join(x), axis=1
                    )
                    df.drop(columns=['Precaution_1','Precaution_2','Precaution_3','Precaution_4'], inplace=True)
                    df.reset_index(inplace=True, drop=True)
    
                    if b2:
                        if len(np.unique(tdata)) == 1:
                            if np.unique(tdata) == 1:
                                st.success("Please Contact Nearest Doctor")
                            else:
                                st.success("You are healthy")
                        else:
                            if choice2 == "K-Nearest Neighbors":
                                test_prediction = model[0].predict([tdata])
                                query = test_prediction[0]
                                score = np.amax(model[0].predict_proba([tdata]))
                                st.success(query)
                                st.success(f"Probability: {score}")
    
                            if choice2 == "Decision Tree":
                                test_prediction = model[1].predict([tdata])
                                query = test_prediction[0]
                                score = np.amax(model[1].predict_proba([tdata]))
                                st.success(query)
                                st.success(f"Probability: {score}")
    
                            if choice2 == "Random Forest":
                                test_prediction = model[2].predict([tdata])
                                query = test_prediction[0]
                                score = np.amax(model[2].predict_proba([tdata]))
                                st.success(query)
                                st.success(f"Probability: {score}")
    
                            if choice2 == "Naive Bayes":
                                test_prediction = model[3].predict([tdata])
                                query = test_prediction[0]
                                score = np.amax(model[3].predict_proba([tdata]))
                                st.success(query)
                                st.success(f"Probability: {score}")
    
                            if choice2 == "ExtraTreesClassifier":
                                test_prediction = model[4].predict([tdata])
                                query = test_prediction[0]
                                score = np.amax(model[4].predict_proba([tdata]))
                                st.success(query)
                                st.success(f"Probability: {score}")
    
                            st.success(df[df['Disease'] == query]["Precautions"].to_numpy()[0])
                else:
                    st.warning("Incorrect Email/Password")
        else:
            st.warning("Not Valid Email")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------- SIGNUP PAGE -------------------
elif choice == "SignUp":
    Fname = st.text_input("First Name")
    Lname = st.text_input("Last Name")
    Mname = st.text_input("Mobile Number")
    Email = st.text_input("Email")
    City = st.text_input("City")
    Password = st.text_input("Password", type="password")
    CPassword = st.text_input("Confirm Password", type="password")
    b2 = st.button("SignUp")
    if b2:
        import re
        pattern = re.compile("(0|91)?[7-9][0-9]{9}")
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if Password == CPassword:
            if pattern.match(Mname):
                if re.fullmatch(regex, Email):
                    create_usertable()
                    add_userdata(Fname, Lname, Mname, City, Email, Password, CPassword)
                    st.success("SignUp Success")
                    st.info("Go to Logic Section for Login")
                else:
                    st.warning("Not Valid Email")
            else:
                st.warning("Not Valid Mobile Number")
        else:
            st.warning("Pass Does Not Match")
