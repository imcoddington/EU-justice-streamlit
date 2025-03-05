"""
Module Name:    Password Check
Author:         Carlos Alberto Toruño Paniagua
Date:           June 7th, 2024
Description:    This module contains the code for inserting a grouped menu on side bar
This version:   June 7th, 2024
"""
from st_pages import Page, Section, show_pages, add_page_title
def insert_smenu():
    add_page_title()
    show_pages(
        [
            Page("0_Home.py", "Home"),
            Section("Explore the Data"),
            Page("pages/1_A2J_Dashboard.py", "Justice Journey", in_section=True),
            Page("pages/2_Justice_Gap.py", "Justice Gap", in_section = True),
            Page("pages/8_Information.py", "Information", in_section=False)
        ]
    )