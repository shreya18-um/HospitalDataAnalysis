from preswald import text, plotly, table, slider, text_input, get_df
import plotly.express as px
import pandas as pd  # Needed for numeric conversion

# Load the dataset using Preswald's get_df()
df = get_df("hospital_data")

if df is not None and not df.empty:
    text("# 🏥 Hospital Data Analysis Dashboard")
    text("Analyze hospital ratings and emergency services across the USA.")

    # Convert 'Hospital overall rating' to numeric safely
    if "Hospital overall rating" in df.columns:
        df["Hospital overall rating"] = pd.to_numeric(df["Hospital overall rating"], errors="coerce")

    df = df.dropna(subset=["State"])  # Drop missing states to avoid errors

    # Allow users to filter by State (default: CA)
    selected_state = text_input("Enter State (e.g., CA, TX, NY)", default="CA")
    state_filtered_df = df[df["State"].str.upper() == selected_state.upper()] if selected_state else df

    # Filter hospitals by rating
    rating_threshold = slider("Minimum Hospital Rating", min_val=1, max_val=5, default=3)
    filtered_df = state_filtered_df.dropna(subset=["Hospital overall rating"])
    filtered_df = filtered_df[filtered_df["Hospital overall rating"] >= rating_threshold]

    # Show hospitals as a table
    if not filtered_df.empty:
        table(filtered_df[["Hospital Name", "City", "State", "Hospital overall rating", "Emergency Services"]],
              title="Filtered Hospitals")
    else:
        text("⚠️ No hospitals match the selected filters.")

    # Visualizations
    if not df.empty:
        fig1 = px.bar(df.groupby("State")["Hospital Name"].count().reset_index(),
                      x="State", y="Hospital Name", title="Number of Hospitals Per State")
        plotly(fig1)

    if "Hospital overall rating" in df.columns and not df["Hospital overall rating"].dropna().empty:
        fig2 = px.histogram(df.dropna(subset=["Hospital overall rating"]),
                            x="Hospital overall rating",
                            title="Distribution of Hospital Ratings", nbins=5)
        plotly(fig2)

    if "Emergency Services" in df.columns and not df["Emergency Services"].dropna().empty:
        emergency_counts = df["Emergency Services"].value_counts().reset_index()
        emergency_counts.columns = ["Emergency Service Available", "Count"]
        fig3 = px.pie(emergency_counts, names="Emergency Service Available", values="Count",
                      title="Hospitals Offering Emergency Services")
        plotly(fig3)
else:
    text("❌ Error: Dataset could not be loaded. Please check the file path and try again.")
