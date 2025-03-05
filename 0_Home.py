"""
Project:        EU Copilot App
Module Name:    Master app script
Author:         Carlos Alberto Toruño Paniagua
Date:           October 19th, 2023
Description:    This module contains the home page code for the EU Copilot App
This version:   October 23rd, 2023
"""

import streamlit as st
import pandas as pd
from tools import sidemenu

# Page config
st.set_page_config(
    page_title = "Home",
    page_icon  = "house"
)

# Reading CSS styles
with open("styles.css") as stl:
    st.markdown(f"<style>{stl.read()}</style>", 
                unsafe_allow_html=True)


# st.markdown("<h1 style='text-align: center;'>EU-S Copilot</h1>", 
#             unsafe_allow_html=True)
st.markdown(
    """
    <p class='jtext'>
    The <strong style="color:#003249">Access to Justice Dashboard</strong> is a web app designed to assist WJP and other stakeholders 
    in gaining insights to experience related justice data in the EU.
    </p>
    
    <p class='jtext'>
    In the <strong style="color:#003249">Justice Journey tab</strong>, you'll find interactive visualizations which outline several dimensions
    of Access to Justice, including the Legal Process, Representation and Advice, and Hardships faced. This data is available both as the total sample,
    and disaggregated by Economic Status and Gender.
    </p>

    <p class='jtext'>
    In <strong style="color:#003249">Justice Gap tab</strong> you will find country and EU level estimations of the proportion of individuals in 
    the Justice Gap, which considers whether an individual faced barriers in accessing information or representation, experienced significant time delays,
    was denied a fair outcome, and was able to resolve their problem fully. This results in a 'justice score' which we use as a measure of the extent to which
    someone's justice needs were met. Membership in the Justice Gap indicates that less than 2/3rds of justice needs were met for a respondent.

    The Justice Journey tab also includes estimations of the effect of certain sociodemographics in increasing or decreasing the lifelihood that someone
    is in the justice gap. These estimations were derived using binomial logistic regression in R.
    </p>


    """,
    unsafe_allow_html = True
)