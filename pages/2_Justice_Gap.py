"""
Project:            EU Justice Dashboard
Module Name:        Dissecting the Justice Gap
Author:             Isabella Coddington
Date:               March 4, 2025
Description:        This module contains the code of the Justice Gap page on the EU Justice Dashboard. 
This version:       March 4, 2025
"""

# importing libraries
import re
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from tools import passcheck, sidemenu
import dropbox
import dropbox.files
from io import BytesIO
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import uuid 

# page configuration
st.set_page_config(
    page_title= "Dissecting the Justice Gap",
    page_icon = "📶",
)


# reading css styles
with open("styles.css") as stl:
    st.markdown(f"<style>{stl.read()}</style>",
                unsafe_allow_html=True)
    
# sidebar menu
sidemenu.insert_smenu()

if passcheck.check_password():
# Defining auth secrets (when app is already deployed)
    dbtoken  = st.secrets["dbtoken"]
    dbkey    = st.secrets["dbkey"]
    dbsecret = st.secrets["dbsecret"]


    atoken = passcheck.retrieve_DBtoken(dbkey, dbsecret, dbtoken)

    #####################################################################################################################
    #                                                        LOADING DATA                                               #
    #####################################################################################################################
        # Accessing Dropbox
    dbx = dropbox.Dropbox(atoken)

    # loading function
    @st.cache_data
    def load_DBfile(file, format, sheet=None):

        # accessing dropbox files
        __, res = dbx.files_download(f"/{file}")
        data = res.content

    # reading data frames
        with BytesIO(data) as file:
            if format == 'excel':
                df = pd.read_excel(file, sheet_name = sheet)
            if format == 'csv':
                df = pd.read_csv(file)
        return df
    # loading barriers csv
    justice_score_summary = load_DBfile("barriers.csv", format = 'csv')


    st.markdown(
        """
        <p class='jtext'>
        Welcome to dashboard we've created to <strong style="color:#003249">Dissect the Justice Gap</strong>. The data presented here is just a preview and 
        <b><i>BY NO MEANS should be considered final or official</i></b>.
        </p>
        <p class='jtext'>
        Galingan!
        </p>
        """,
        unsafe_allow_html = True
    )

    barrierstab, sociotab = st.tabs(["Distribution of Barriers", "Sociodemographic Effects"])
    with barrierstab:


        # User selects EU or specific countries
        country_selection = st.multiselect(
            "Please select countries (or all of EU) to compare: ",
            justice_score_summary['country_name_ltn'].unique(),
            default=["EU"]  # Start with the EU selected
        )

        ###########################################################
        #                   TOTAL SAMPLE                          #
        ###########################################################

        filtered_data = justice_score_summary[justice_score_summary['country_name_ltn'].isin(country_selection)]

        # Create a long-format DataFrame for easier plotting
        plot_data = filtered_data.melt(id_vars=["country_name_ltn"], 
                                    value_vars=['pct_in_gap', 'pct_not_in_gap'],
                                    var_name="Justice Gap Status",
                                    value_name="Percentage")

        fig_gap = px.bar(
            plot_data,
            x="Percentage",
            y="country_name_ltn",
            color="Justice Gap Status",
            orientation="h",
            barmode="stack",
            title="Justice Gap Across Selected Countries",
            text=plot_data["Percentage"].apply(lambda x: f"{x:.2f}%")
        )

        fig_gap.update_traces(
            hovertemplate="In <b>%{y}</b>, <b>%{x:.2f}%</b> of respondents who experienced a nontrivial <br>legal problem in the past two years were " +
                        "<b>%{customdata}</b>.<extra></extra>",
            customdata=plot_data["Justice Gap Status"].replace({"pct_in_gap": "in the justice gap", "pct_not_in_gap": "not in the justice gap"})
        )

        # Update layout to format text, remove legend, and hide y-axis label
        fig_gap.update_traces(
            textposition="inside",  
            insidetextanchor="middle",  
            textfont=dict(size=18, color="white")  
        )

        fig_gap.update_layout(
            showlegend=False,  
            yaxis_title="",  
            xaxis=dict(title="Percentage (%)"),  
            margin=dict(l=100, r=20, t=50, b=50),
            plot_bgcolor="white"
        )

        st.plotly_chart(fig_gap)


        demographics = st.selectbox(
            "Would you like to view the distribution of legal barriers faced for the total sample, or for a specific demographic? ",
            ['Total Sample', 'Disaggregated']
        )
        if demographics == "Disaggregated":
            demo = st.selectbox(
                    "Choose a disagreggation: ",
                    ['Gender', 'Income', 'Both']
                )

            if demo == "Gender":
                data = pd.read_csv('.streamlit/inputs/justice_gap_gend.csv')
                dem_groups = ["Male", "Female"]

            if demo == "Income":
                data = pd.read_csv('.streamlit/inputs/justice_gap_es.csv')
                dem_groups = [0,1]

            if demo == "Both":
                data = pd.read_csv('.streamlit/inputs/dem_breakdowns_justice_gap.csv')
                data['combined_group'] = data['gender'] + ', ' + data['fintight'].astype("string")
                dem_groups = ['Female, 0', 'Female, 1', 'Male, 0', 'Male, 1']



            selected_country = st.selectbox(
                    "Select a country to analyze barrier distribution (disaggregated): ",
                    country_selection
                )

            subset = data[data['country_name_ltn'] == selected_country]

            if subset.empty:
                st.warning(f"No data available for {selected_country}.")
            else:
                if demo == "Gender":
                    subset['group_label'] = subset['gender']
                elif demo == "Income":
                    subset['group_label'] = subset['fintight'].map({1: "Low ES", 0: "High ES"})
                elif demo == "Both":
                    subset['group_label'] = subset['gender'] + " - " + subset['fintight'].map({1: "Low ES", 0: "High ES"})
                

            barrier_melted = subset.melt(id_vars=['group_label'],
                                  value_vars=['pct_0_barriers', 'pct_1_barrier', 'pct_2_barrier', 'pct_3_barriers', 'pct_4_barriers'],
                                  var_name='Barrier Type',
                                  value_name='Percentage')
            barrier_melted['Barrier Type'] = barrier_melted['Barrier Type'].replace({
                'pct_0_barriers': 'No Barriers',
                'pct_1_barriers': '1 Barrier',
                'pct_2_barriers': '2 Barriers',
                'pct_3_barriers': '3 Barriers',
                'pct_4_barriers': '4 Barriers'
            })

            fig_barrier = px.bar(
                barrier_melted,
                x='Barrier Type',
                y='Percentage',
                color='group_label',
                barmode='stack',
                title=f"Stacked Barrier Distribution by {demo} in {selected_country}",
                labels={'Percentage': 'Percentage (%)', 'Barrier Type': 'Number of Barriers Faced', 'group_label': 'Demographic Group'}
            )
            fig_barrier.update_traces(hovertemplate="<b>%{y:.2f}%</b> experienced %{x}.")
            st.plotly_chart(fig_barrier, key=f"bar_chart_{selected_country}_{uuid.uuid4()}")

            group_labels = subset['group_label'].unique()


            # pie charts
            num_groups = len(group_labels)
            rows, cols = (1, 2) if num_groups == 2 else (2, 2)
            
            fig_pie = make_subplots(rows=rows, subplot_titles=subset['group_label'].values,cols=cols, specs=[[{"type": "domain"} for _ in range(cols)] for _ in range(rows)])
            
            row_idx, col_idx = 1, 1
            for group in group_labels:
                group_data = subset[subset['group_label'] == group]
                
                share_of_barriers = group_data.melt(id_vars=['group_label'],
                                                    value_vars=['pct_solution_barrier_barrier_1', 'pct_solution_barrier_barrier_2', 'pct_solution_barrier_barrier_3',
                                                                'pct_info_barrier_barrier_1', 'pct_info_barrier_barrier_2', 'pct_info_barrier_barrier_3',
                                                                'pct_dcf_barrier_barrier_1', 'pct_dcf_barrier_barrier_2', 'pct_dcf_barrier_barrier_3',
                                                                'pct_representation_barrier_barrier_1', 'pct_representation_barrier_barrier_2', 'pct_representation_barrier_barrier_3'],
                                                    var_name='Barrier Type',
                                                    value_name='Percentage')
                
                share_of_barriers['Barrier Type'] = share_of_barriers['Barrier Type'].replace({
                    'pct_solution_barrier_barrier_1': 'Solution', 'pct_solution_barrier_barrier_2': 'Solution', 'pct_solution_barrier_barrier_3': 'Solution',
                    'pct_info_barrier_barrier_1': 'Information', 'pct_info_barrier_barrier_2': 'Information', 'pct_info_barrier_barrier_3': 'Information',
                    'pct_dcf_barrier_barrier_1': 'Delays, Fairness, Cost', 'pct_dcf_barrier_barrier_2': 'Delays, Fairness, Cost', 'pct_dcf_barrier_barrier_3': 'Delays, Fairness, Cost',
                    'pct_representation_barrier_barrier_1': 'Representation', 'pct_representation_barrier_barrier_2': 'Representation', 'pct_representation_barrier_barrier_3': 'Representation'
                })
                
                fig_pie.add_trace(
                    go.Pie(
                        labels=share_of_barriers['Barrier Type'],
                        values=share_of_barriers['Percentage'],
                        name=group,
                        hole=0.4
                    ),
                    row=row_idx, col=col_idx
                )
                
                col_idx += 1
                if col_idx > cols:
                    col_idx = 1
                    row_idx += 1
            
            fig_pie.update_layout(title_text=f"Barrier Types by {demo} in {selected_country}", showlegend=True)
            st.plotly_chart(fig_pie, key=f"pie_chart_{selected_country}_{uuid.uuid4()}")

                                
        if demographics == "Total Sample":
            selected_country = st.selectbox(
                "Select a country to analyze barrier distribution:",
                country_selection
            )
            country_data = filtered_data[
                filtered_data["country_name_ltn"] == selected_country
                ]
            
            barrier_data = pd.DataFrame({
                "Barrier Type": ["No Barriers","1 Barrier", "2 Barriers", "3 Barriers", "4 Barriers"],
                "Percentage": [
                    country_data["pct_0_barriers"].values[0],
                    country_data["pct_1_barrier"].values[0], 
                    country_data["pct_2_barrier"].values[0], 
                    country_data["pct_3_barriers"].values[0], 
                    country_data["pct_4_barriers"].values[0]
                ]
            })


            fig_b  = px.bar(
                barrier_data,
                x="Barrier Type",
                y="Percentage",
                title=f"Barrier Distribution in {selected_country} ",
                labels={"Percentage": "Percentage (%)", "Barrier Type": "Number of Barriers Faced"},
                color="Barrier Type"  
            )
            fig_b.update_traces(
                hovertemplate = "<b>%{y:.2f}%</b> of respondents experienced %{x}. "
            )
            fig_b.update_layout(
                showlegend = False,
                yaxis = dict(range = [0,100])
            )

            st.plotly_chart(fig_b)


            share_of_barriers = pd.DataFrame({
                "Number of Barriers Faced" : [1, 2, 3],
                "Solution" : [
                    country_data['pct_solution_barrier_barrier_1'].values[0],
                    country_data['pct_solution_barrier_barrier_2'].values[0],
                    country_data['pct_solution_barrier_barrier_3'].values[0]
                ],
                "Information" : [
                    country_data['pct_info_barrier_barrier_1'].values[0],
                    country_data['pct_info_barrier_barrier_2'].values[0],
                    country_data['pct_info_barrier_barrier_3'].values[0]
                ],
                "Delays, Fairness, Cost" : [
                    country_data['pct_dcf_barrier_barrier_1'].values[0],
                    country_data['pct_dcf_barrier_barrier_2'].values[0],
                    country_data['pct_dcf_barrier_barrier_3'].values[0]
                ],
                "Representation" : [
                    country_data['pct_representation_barrier_barrier_1'].values[0],
                    country_data['pct_representation_barrier_barrier_2'].values[0],
                    country_data['pct_representation_barrier_barrier_3'].values[0]
                ]
            })

            # Barrier Types for Labels
            barrier_labels = ["Solution Barrier", "Delays, Cost or Fairness Barrier", "Information Barrier", "Representation Barrier"]
            barrier_count_labels = ["Experienced 1 Barrier", "Experienced 2 Barriers", "Experienced 3 Barriers"]

            # Create subplot layout with 1 row and 3 columns
            fig = make_subplots(
                rows=1, cols=3, 
                specs=[[{"type": "domain"}, {"type": "domain"}, {"type": "domain"}]]  # Each subplot is a pie chart
            )
            custom_colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]  # Blue, Orange, Green, Red


            # Add Pie Charts for Each Barrier Count
            for i, row in share_of_barriers.iterrows():
                fig.add_trace(
                    go.Pie(
                        labels=barrier_labels,
                        values=row[1:],  
                        hole=0.4,  
                        marker=dict(colors=custom_colors),  
                        hovertemplate="<b>%{label}</b>: <b>%{value:.2f}%</b><extra></extra>"

                    ),
                    row=1, col=i+1  
                )

            for i, label in enumerate(barrier_count_labels):
                fig.add_annotation(
                    text=f"<b>{label}</b>",  
                    x=i / 2,  
                    y=-0.1,  
                    showarrow=False,
                    font=dict(size=14)
                )

            # Format layout
            fig.update_layout(
                title_text=f"Distribution of Barrier Types by Barrier Count in {selected_country}",
                showlegend=True,
                legend=dict(
                    orientation="h",  
                    yanchor="bottom",  
                    y=1.05,  
                    xanchor="center",  
                    x=0.5  
                )  
            )

            st.plotly_chart(fig)



    with sociotab:
        logistic_data = load_DBfile("logit_reg_gap.csv", format = 'csv')

        logistic_data['female_lower'] = logistic_data['female'] - 1.96*logistic_data['female_se']
        logistic_data['female_upper'] = logistic_data['female'] + 1.96*logistic_data['female_se']
        logistic_data['urban_lower']  = logistic_data['urban'] - 1.96*logistic_data['urban_se']
        logistic_data['urban_upper'] = logistic_data['urban'] + 1.96*logistic_data['urban_se']
        logistic_data['no_hs_lower'] = logistic_data['no_hs'] - 1.96*logistic_data['no_hs_se']
        logistic_data['no_hs_upper'] = logistic_data['no_hs'] + 1.96*logistic_data['no_hs_se']
        logistic_data['low_es_lower'] = logistic_data['low_es'] - 1.96*logistic_data['low_es_se']
        logistic_data['low_es_upper'] = logistic_data['low_es'] + 1.96*logistic_data['low_es_se']
        logistic_data['less_than_30_lower'] = logistic_data['less_than_30'] - 1.96 * logistic_data['less_than_30_se']
        logistic_data['less_than_30_upper'] = logistic_data['less_than_30'] + 1.96 * logistic_data['less_than_30_se']


        eu_or_country_socio = st.selectbox(
            "Would you like to focus on a specific country or the whole EU? ",
            ["Country", "EU"],
            index = 1
        )

        if eu_or_country_socio == "Country":
        # Step 1: Select Country
            selected_country_socio = st.selectbox(
                "Select a country:",
                logistic_data["country_name_ltn"].unique(),
                index=0  # Default to EU
            )
            # Step 2: Filter Data for Selected Country
            country_data = logistic_data[logistic_data["country_name_ltn"] == selected_country_socio].iloc[0]
        if eu_or_country_socio == "EU":
            country_data = logistic_data[logistic_data["country_name_ltn"] == "EU"].iloc[0]
            selected_country_socio = "EU"

        # Step 3: Reshape Data for Plotly
        effect_data = pd.DataFrame({
            "Characteristic": ["Female", "Urban", "No High School Diploma", "Younger than 30", "Low Economic Status"],
            "AME": [
                country_data["female"],
                country_data["urban"],
                country_data["no_hs"],
                country_data["less_than_30"],
                country_data["low_es"]
            ],
            "Lower Bound": [
                country_data["female_lower"],
                country_data["urban_lower"],
                country_data["no_hs_lower"],
                country_data["less_than_30_lower"],
                country_data["low_es_lower"]
            ],
            "Upper Bound": [
                country_data["female_upper"],
                country_data["urban_upper"],
                country_data["no_hs_upper"],
                country_data["less_than_30_upper"],
                country_data["low_es_upper"]
            ]
        })

        # Step 4: Create the Forest Plot (Horizontal Error Bar Chart)
        fig = go.Figure()

        # Add error bars for confidence intervals
        fig.add_trace(go.Scatter(
            x=effect_data["AME"],
            y=effect_data["Characteristic"],
            mode="markers",
            marker=dict(color="green", size=10),
            error_x=dict(
                type="data",
                symmetric=False,
                array=effect_data["Upper Bound"] - effect_data["AME"],  # Upper CI
                arrayminus=effect_data["AME"] - effect_data["Lower Bound"]  # Lower CI
            ),
            hovertemplate="<b>%{y}: %{x:.2f} p.p.</b><br>" +  # Bold first line with effect value
                  "On average, this attribute changes the probability of being in the justice gap by <b>%{x:.2f}%</b>.<br>" +  
                  "We are 95% confident that the effect is between <b>%{customdata[0]:.2f}</b> and <b>%{customdata[1]:.2f}</b> percentage points.<extra></extra>",
            customdata=effect_data[["Lower Bound", "Upper Bound"]].values  # Pass lower/upper bound for hover text

        ))

        # Add vertical line at 0% (Neutral Effect)
        fig.add_shape(
            type="line",
            x0=0, x1=0,
            y0=-0.5, y1=len(effect_data) - 0.5,
            line=dict(color="pink", width=1.5)
        )

        # Format the layout
        fig.update_layout(
            title=f"Impact of Sociodemographic Characteristics on the Justice Gap ({selected_country_socio})",
            xaxis=dict(title="Average Marginal Effect (p.p.)", range = [-60,60]),
            yaxis=dict(title=""),
            margin=dict(l=100, r=20, t=50, b=50),
            plot_bgcolor="white"
        )

        # Step 5: Display in Streamlit
        st.plotly_chart(fig)




        
