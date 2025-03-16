from preswald import text, plotly, table, slider, text_input
import pandas as pd
import plotly.express as px
import os

# Step 1: Define the dataset path manually
dataset_path = "C:/Users/MacBook Pro/hospital/hospital_project/data/HospInfo_reduced.csv"





# Step 2: Load the dataset manually
if os.path.exists(dataset_path):
    df = pd.read_csv(dataset_path)
else:
    text("❌ Error: Dataset not found at " + dataset_path)
    df = None

if df is not None:
    # Display Dashboard Title
    text("# 🏥 Hospital Data Analysis Dashboard")
    text("Analyze hospital ratings and emergency services across the USA.")

    # Convert 'Hospital overall rating' to numeric for analysis
    df["Hospital overall rating"] = pd.to_numeric(df["Hospital overall rating"], errors="coerce")

    # Allow users to filter by State (without default argument)
    selected_state = text_input("Enter State (e.g., CA, TX, NY)")
    if selected_state:
        state_filtered_df = df[df["State"].str.upper() == selected_state.upper()]
    else:
        state_filtered_df = df  # Show all states if input is empty

    # Allow users to filter by minimum hospital rating
    rating_threshold = slider("Minimum Hospital Rating", min_val=1, max_val=5, default=3)
    filtered_df = state_filtered_df.dropna(subset=["Hospital overall rating"])
    filtered_df = filtered_df[filtered_df["Hospital overall rating"] >= rating_threshold]

    # Display filtered hospitals as a table
    table(filtered_df[["Hospital Name", "City", "State", "Hospital overall rating", "Emergency Services"]],
          title="Filtered Hospitals")

    # Visualization - Number of hospitals per state
    hospital_count_per_state = df.groupby("State")["Hospital Name"].count().reset_index()
    fig1 = px.bar(hospital_count_per_state, x="State", y="Hospital Name", title="Number of Hospitals Per State")
    plotly(fig1)

    # Visualization - Hospital Ratings Distribution
    fig2 = px.histogram(df.dropna(subset=["Hospital overall rating"]), 
                        x="Hospital overall rating", 
                        title="Distribution of Hospital Ratings", nbins=5)
    plotly(fig2)

    # Show emergency service availability
    emergency_counts = df["Emergency Services"].value_counts().reset_index()
    emergency_counts.columns = ["Emergency Service Available", "Count"]
    fig3 = px.pie(emergency_counts, names="Emergency Service Available", values="Count", 
                  title="Hospitals Offering Emergency Services")
    plotly(fig3)
else:
    text("⚠️ The dataset could not be loaded. Please check the file path and try again.")
