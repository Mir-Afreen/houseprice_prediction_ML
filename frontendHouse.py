import streamlit as st
import requests

API_URL ='http://127.0.0.1:8000/prediction'
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background-color: #000000 !important;
}
            /* Streamlit wrapper */
[data-testid="stHeader"] {
    background: rgba(0,0,0,0) !important;
}
/* ===== FULL PAGE BLACK ===== */
.stApp {
    background-color: #000000;
}
/* ===== REAL CONTAINER BOX ===== */


section[data-testid="stMain"] > div {
    max-width: 720px;
    margin: 25px auto 0 auto;
    border: 2px solid #2A2F3A;
    border-radius: 12px;
    padding: 25px;
    background-color: #0E1117;
    box-shadow: 0 0 15px rgba(0,0,0,0.4);
}

/* Center all text */
section[data-testid="stMain"] * {
    text-align: center;
    color: #E8E8E8 !important;
}

/* ===== BUTTON ===== */
div.stButton > button {
    width: 100% !important;
    background-color: #1F6FEB !important;
    color: #E8E8E8 !important;
    border-radius: 8px;
}

div.stButton > button:hover {
    background-color: #1558C4 !important;
}

/* Inputs */
div[data-baseweb="input"] input {
    background-color: #1A1C24;
}

/* Radios horizontal */
div[role="radiogroup"] {
    display: flex;
    justify-content: center;
    gap: 20px;
}
/* Remove extra bottom container */
section[data-testid="stMain"] > div:nth-child(2) {
    display: none !important;
}



/* Remove extra gap */
.block-container {
    padding-bottom: 0rem !important;
}
</style>
""", unsafe_allow_html=True)


st.markdown('<div class="main-box">', unsafe_allow_html=True)

st.title("HOUSE_PRICE_PREDICTION")
col4, col5  = st.columns(2)
with col4:
    area =st.number_input('Enter the area of your house in sq feet')
    bedroom =st.number_input("Enter Quantity of bedrooms ")
with col5:
      pakinng =st.number_input("How many parking area ")
      stories =st.number_input("How many stories  ")
    
bathroom =st.number_input("Enter Quantity of bathroom ")
col1, col2 , col3 = st.columns(3)
with col1:
    mainroad =st.radio("Is there mainroad: ",['Yes','No'])
    aircondition =st.radio("Is there any aircondition system: ",['Yes','No'])
    
    
with col2:
      guesroom =st.radio("Is there any guestroom: ",['Yes','No'])
      prefarea =st.radio("Is this is a preference area: ",['Yes','No'])
with col3:
      basement =st.radio("Is there basement area: ",['Yes','No'])
    
def yn(value):
        return value.lower()
    
if st.button('Submit',use_container_width=True):
        user_dict = {  'area'  :area ,  #api : stremlit
                    'parking' :pakinng,
                    'mainroad' : yn(mainroad),
                    'bedrooms' : bedroom,
                    'bathroom' :bathroom,
                    'stories' : stories,
                    'preference_area' : yn(prefarea),
                    'aircondition' : yn(aircondition),
                    'guestroom' : yn(guesroom),
                    'basement' :yn(basement)
                      }
        try:
            respond = requests.post(API_URL , json= user_dict )
            if respond.status_code == 200:
                result = respond.json()
                st.success(f'the prediction of house is  :  {result['predict']}')
            else:
                st.error(f'api error{respond.status_code}')
        except requests.exceptions.ConnectionError: 
            st.error("error check fastapi server(port 8000)")

st.markdown('</div>', unsafe_allow_html=True)