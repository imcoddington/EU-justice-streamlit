"""
Project:        EU Copilot App
Module Name:    Datamap Page
Author:         Carlos Alberto Toruño Paniagua
Date:           October 23rd, 2023
Description:    This module contains the code of the Data Maps tab for the EU Copilot App
This version:   October 23rd, 2023
"""

import streamlit as st
from tools import sidemenu

# Page config
st.set_page_config(
    page_title = "Info",
    page_icon  = "⛩️"
)

# Reading CSS styles
with open("styles.css") as stl:
    st.markdown(f"<style>{stl.read()}</style>", 
                unsafe_allow_html=True)

# Sidebar menu
sidemenu.insert_smenu()

# Header and explanation
# st.markdown("<h1 style='text-align: center;'>Information</h1>", 
#             unsafe_allow_html=True)
st.markdown(
    """
    <b>Author(s):</b> 
    <ul>
        <li>Isabella Coddington</li>
    </ul>

    <h4>Source Code:</h4>
    <p class='jtext'>
    The Access to Justice Dashboard was programmed entirely in Python using the <a href="https://streamlit.io/" target="_blank">Streamlit</a>
    web framework. The code is publicly available in this 
    <a href="https://github.com/WJP-DAU/EU-justice-streamlit" target="_blank">GitHub Repository</a>.
    </p>

    <h4>Disclaimer:</h4>

    <p class='jtext'>
    The information provided in this online tool is for general informational purposes only. While the previously
    stated author(s) strive to provide accurate and up-to-date information, we make no representations or 
    warranties of any kind, express or implied, about the completeness, accuracy, reliability, suitability, or 
    availability with respect to the information, products, services, or related data contained in this app 
    for any purpose. Any reliance you place on such information is therefore strictly at your own risk.
    </p>

    <p class='jtext'>
    Please note that the data presented in this online tool <b>SHOULD NOT</B> be taken as 
    official information from the <strong style="color:#003249">World Justice Project</strong>, 
    and any errors or omissions are solely the responsibility of the previously stated author(s).
    For the latest official information available you should visit the 
    <a href="https://worldjusticeproject.org/" target="_blank">
    official website of the World Justice Project
    </a>.
    </p>

    <p class='jtext'>
    This online tool is a personal project of the  previously stated author(s). Every effort is made to keep 
    the tool up and running smoothly. The <strong style="color:#003249">World Justice Project</strong> takes no 
    responsibility, nor will be liable for any information displayed in this app or by the unavailability or
    interruption in its service.
    </p>

    <p class='jtext'>
    The inclusion of any links in this online tool does not necessarily imply a recommendation or endorse 
    the views expressed within them.
    </p>

    <h4>License:</h4>
    """,
    unsafe_allow_html = True
)