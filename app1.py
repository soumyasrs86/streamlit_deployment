import streamlit as st
import pandas as pd
from io import BytesIO

st.write("Hi doctor")

# Input fields for user details
name = st.text_input("Name")
age = st.text_input("Age")
gender = st.selectbox("Gender", ["Male", "Female", "Other"])

# Input fields for favorite movies
movie1 = st.text_input("Movie 1")
movie2 = st.text_input("Movie 2")
movie3 = st.text_input("Movie 3")

# Multiselect for favorite colors
options = st.multiselect(
    "What are your favorite colors",
    ["Green", "Yellow", "Red", "Blue"],
    ["Yellow", "Red"]
)

# Create DataFrames
df_user = pd.DataFrame({"Name": [name], "Age": [age], "Gender": [gender]})
df_movies = pd.DataFrame({"Favorite Movies": [movie1, movie2, movie3]})
df_colors = pd.DataFrame({"Favorite Colors": options})  # Each color in a separate row

# Display the DataFrames
st.write("User Details:")
st.dataframe(df_user)
st.write("Favorite Movies:")
st.dataframe(df_movies)
st.write("Favorite Colors:")
st.dataframe(df_colors)

# Convert DataFrames to Excel with all in a single sheet
def to_excel(user_df, movies_df, colors_df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        # Write each DataFrame to the same sheet with a space in between
        user_df.to_excel(writer, index=False, sheet_name="Selections", startrow=0)
        movies_df.to_excel(writer, index=False, sheet_name="Selections", startrow=len(user_df) + 2)
        colors_df.to_excel(writer, index=False, sheet_name="Selections", startrow=len(user_df) + len(movies_df) + 4)
    output.seek(0)
    return output

# Add download button
st.download_button(
    label="Download selections as Excel",
    data=to_excel(df_user, df_movies, df_colors),
    file_name="selections.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
