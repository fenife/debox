import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

df = pd.DataFrame(np.random.randn(50, 20), columns=("col %d" % i for i in range(20)))

with st.sidebar:
    st.markdown("# Tool page")
                
    clear = st.button("clear shell")
    if clear:
        st.session_state.messages = []

@st.dialog("Cast your form")
def vote(item):
    with st.form("my_form"):
        st.write("Inside the form")
        slider_val = st.slider("Form slider")
        checkbox_val = st.checkbox("Form checkbox")

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write("slider", slider_val, "checkbox", checkbox_val)
 

col1, col2 = st.columns([1, 2], gap="small")

with col1:
    if st.button("form"):
        vote("form")

t = st.text_input("text", help="text")
st.write(t)
