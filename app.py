import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(page_title="Data Visualizer", layout="wide")

# App title
st.title("📊 Easy Data Visualizer")
st.write("Upload your dataset and create multiple visualizations effortlessly!")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Read dataset
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.stop()

    st.success("✅ File uploaded successfully!")

    # Show preview
    st.subheader("🔍 Data Preview")
    st.dataframe(df.head())

    # Sidebar options
    st.sidebar.header("⚙️ Visualization Settings")

    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

    if len(numeric_cols) == 0:
        st.warning("No numeric columns found for plotting.")
    else:
        # Visualization choices
        plot_type = st.sidebar.multiselect(
            "Choose Visualization Types",
            ["Histogram", "Scatter Plot", "Box Plot", "Correlation Heatmap"],
            default=["Histogram", "Scatter Plot"]
        )

        # Generate plots
        st.subheader("📈 Visualizations")

        if "Histogram" in plot_type:
            st.write("### Histogram")
            col = st.selectbox("Select numeric column for Histogram", numeric_cols, key="hist_col")
            fig, ax = plt.subplots()
            sns.histplot(df[col], kde=True, ax=ax)
            st.pyplot(fig)

        if "Scatter Plot" in plot_type and len(numeric_cols) >= 2:
            st.write("### Scatter Plot")
            x_axis = st.selectbox("Select X-axis", numeric_cols, key="scatter_x")
            y_axis = st.selectbox("Select Y-axis", numeric_cols, key="scatter_y")
            fig, ax = plt.subplots()
            sns.scatterplot(x=df[x_axis], y=df[y_axis], ax=ax)
            st.pyplot(fig)

        if "Box Plot" in plot_type and len(numeric_cols) > 0 and len(categorical_cols) > 0:
            st.write("### Box Plot")
            x_cat = st.selectbox("Select categorical column", categorical_cols, key="box_x")
            y_num = st.selectbox("Select numeric column", numeric_cols, key="box_y")
            fig, ax = plt.subplots()
            sns.boxplot(x=df[x_cat], y=df[y_num], ax=ax)
            st.pyplot(fig)

        if "Correlation Heatmap" in plot_type and len(numeric_cols) > 1:
            st.write("### Correlation Heatmap")
            fig, ax = plt.subplots(figsize=(8,6))
            sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)

else:
    st.info("👆 Upload a file to get started")
