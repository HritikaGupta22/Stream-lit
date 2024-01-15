# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
    st.title("File Upload Dashboard")

    # User input choice
    upload_option = st.radio("Choose Data Source:", ["Upload a File"])

    if upload_option == "Upload a File":
        # File uploader widget
        uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

        if uploaded_file is not None:
            # Display uploaded file
            st.subheader("Uploaded File:")
            st.write(uploaded_file.name)

            # Read the data from the uploaded CSV file
            df = pd.read_csv(uploaded_file)

            # Display the DataFrame
            st.subheader("Data Preview:")
            st.dataframe(df)

            # Add blocks for average values
            add_average_blocks(df)

            # Add visualizations
            create_visualizations(df)

def add_average_blocks(df):
    st.sidebar.subheader("Average Values of India:")
    
    # Average Life Expectancy of India
    india_avg_life_expectancy = df[df['Country Name'] == 'India']['Life Expectancy World Bank'].mean()
    st.sidebar.write(f"Avg. Life Expectancy of India: {india_avg_life_expectancy:.2f} years")

    # Average CO2 Emissions of India
    india_avg_co2_emissions = df[df['Country Name'] == 'India']['CO2'].mean()
    st.sidebar.write(f"Avg. CO2 Emissions of India: {india_avg_co2_emissions:.2f} metric tons per capita")

    # Average Health Expenditure % of India
    india_avg_health_expenditure = df[df['Country Name'] == 'India']['Health Expenditure %'].mean()
    st.sidebar.write(f"Avg. Health Expenditure % of India: {india_avg_health_expenditure:.2f}%")

    # Average Education Expenditure % of India
    india_avg_education_expenditure = df[df['Country Name'] == 'India']['Education Expenditure %'].mean()
    st.sidebar.write(f"Avg. Education Expenditure % of India: {india_avg_education_expenditure:.2f}%")

def create_visualizations(df):
    # Sidebar for multifilter slicer
    st.sidebar.subheader("Filter Data:")
    selected_regions = st.sidebar.multiselect("Select Regions", df['Region'].unique())
    selected_income_groups = st.sidebar.multiselect("Select Income Groups", df['IncomeGroup'].unique())

    # Create year slicer
    selected_years = st.sidebar.slider("Select Year Range", min_value=2001, max_value=2019, value=(2001, 2019), step=1)

    # Filter data based on slicer selections
    filtered_data = df[
        (df['Region'].isin(selected_regions)) &
        (df['IncomeGroup'].isin(selected_income_groups)) &
        (df['Year'].between(selected_years[0], selected_years[1]))
    ]
  
    
    # Visualizations
    st.subheader("Visualizations:")

    # Graph 1: Bar Plot - Region-wise Unemployment
    st.subheader("Graph 1: Region-wise Unemployment")
    region_unemployment = filtered_data.groupby("Region")["Unemployment"].mean()
    st.bar_chart(region_unemployment)

    # Graph 2: Bar Plot - Region-wise Life Expectancy and Line Plot - Prevalence of Undernourishment
    st.subheader("Graph 2: Region-wise Life Expectancy and Prevalence of Undernourishment")
    fig, ax1 = plt.subplots(figsize=(10, 6))
    df1 = filtered_data.groupby("Region")[["Life Expectancy World Bank", "Prevelance of Undernourishment"]].mean().reset_index()
    ax1.bar(df1['Region'], df1['Life Expectancy World Bank'], color='blue', alpha=0.7, label='Life Expectancy')
    ax1.set_xlabel('Region')
    ax1.set_ylabel('Life Expectancy', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax2 = ax1.twinx()
    ax2.plot(df1['Region'], df1['Prevelance of Undernourishment'], color='red', marker='o', label='Prevalence of Undernourishment')
    ax2.set_ylabel('Prevalence of Undernourishment', color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    st.pyplot(fig)

    # Graph: Scatter Plot - Relationship between CO2 Emissions and Life Expectancy
    st.subheader("Graph 3: Scatter Plot: Relationship between CO2 Emissions and Life Expectancy")

    # Create scatter plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(filtered_data['CO2'], filtered_data['Life Expectancy World Bank'], alpha=0.7)
    ax.set_xlabel('Carbon Dioxide Emissions (kiloton)')
    ax.set_ylabel('Life Expectancy')
    ax.set_title('Relationship between CO2 Emissions and Life Expectancy')

    # Display the plot using Streamlit
    st.pyplot(fig)



    # Graph 4: Scatter Plot - Impact of Expenditure on Health and Education on Life Expectancy
    st.subheader("Graph 4: Impact of Expenditure on Life Expectancy")
    fig, ax = plt.subplots(figsize=(10, 6))
    # Group by 'Year Range' and calculate the mean for each group
    grouped = filtered_data.groupby("Country Name").agg({
        'Health Expenditure %': 'mean',
        'Education Expenditure %':'mean',
        'Life Expectancy World Bank': 'mean'
    }).reset_index()
    scatter = ax.scatter(grouped['Health Expenditure %'], grouped['Life Expectancy World Bank'], c=grouped['Education Expenditure %'], cmap='viridis', alpha=0.7)
    ax.set_xlabel('Health Expenditure %')
    ax.set_ylabel('Life Expectancy World Bank')
    ax.set_title('Impact of Expenditure on Life Expectancy')
    ax.legend(*scatter.legend_elements(), title='Education Expenditure %')
    st.pyplot(fig)

    # Graph 5: Pie Plot - Region-wise Corruption
    st.subheader("Graph 5: Region-wise Corruption")

    # Create a copy of the filtered data to avoid modifying the original DataFrame
    filtered_data_copy = filtered_data.copy()

    # Convert 'Corruption' column to numeric (in case it's not already)
    filtered_data_copy['Corruption'] = pd.to_numeric(filtered_data_copy['Corruption'], errors='coerce')

    # Drop rows with missing values in 'Corruption' column
    filtered_data_copy = filtered_data_copy.dropna(subset=['Corruption'])

    # Create the pie plot using matplotlib
    fig, ax = plt.subplots(figsize=(8, 8))
    region_corruption = filtered_data_copy.groupby("Region")["Corruption"].mean()
    ax.pie(region_corruption, labels=region_corruption.index, autopct='%1.1f%%', startangle=90)
    ax.set_title('Region-wise Corruption')

    # Display the plot using Streamlit
    st.pyplot(fig)


    # Graph 6: Line Plot - Income Group-wise Life Expectancy
    st.subheader("Graph 6: Income Group-wise Life Expectancy World Bank")
    fig, ax = plt.subplots(figsize=(10, 6))
    income_group_education = filtered_data.groupby("IncomeGroup")["Life Expectancy World Bank"].mean()
    ax.plot(income_group_education.index, income_group_education.values, marker='o', linestyle='-', color='purple')
    ax.set_xlabel('Income Group')
    ax.set_ylabel('Life Expectancy World Bank %')
    ax.set_title('Income Group-wise Life Expectancy World Bank')
    st.pyplot(fig)

    # Graph 7: Multiline Plot - Effect of Communicable and Non-Communicable Diseases on Life Expectancy (Grouped by Year)
    st.subheader("Graph 7 : Multiline Plot: Effect of Communicable and Non-Communicable Diseases on Life Expectancy (Grouped by Year)")
    fig, ax = plt.subplots(figsize=(12, 8))

    # Group by 'Year' and calculate the mean for each group
    grouped_data = filtered_data.groupby("Year").agg({
        'Communicable': 'mean',
        'NonCommunicable': 'mean',
        'Life Expectancy World Bank': 'mean'
    }).reset_index()

    # Plot the mean values
    ax.plot(grouped_data['Communicable'], grouped_data['Life Expectancy World Bank'], marker='o', label='Communicable Diseases')
    ax.plot(grouped_data['NonCommunicable'],grouped_data['Life Expectancy World Bank'], marker='o', label='Non-Communicable Diseases')
    ax.set_ylabel('Life Expectancy')
    ax.set_title('Effect of Communicable and Non-Communicable Diseases on Life Expectancy (Grouped by Year)')
    ax.legend()
    st.pyplot(fig)


if __name__ == "__main__":
    main()