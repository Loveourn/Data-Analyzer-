import streamlit as st
import pandas as pd
import io
from lyzr import DataAnalyzr

def main():
    st.title("lyzr AI- Excel Analyzer")

    # Create a file uploader widget
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)

        # Display the uploaded CSV file as a DataFrame
        st.write("Uploaded CSV file:")
        st.write(df)

        # Checkbox to select all columns
        if st.checkbox('Select all columns'):
            selected_columns = df.columns.tolist()
        else:
            # Allow user to select columns for analysis
            selected_columns = st.multiselect("Select columns for analysis", df.columns.tolist(), default=df.columns.tolist())

        # Allow user to input analysis query
        user_input = st.text_input("Enter your analysis query:")

        if st.button("Predict"):
            # Filter DataFrame based on selected columns
            selected_df = df[selected_columns]

            # Initialize DataConnector and DataAnalyzr
            data_analyzr = DataAnalyzr(df=selected_df, api_key='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')

            # Get analysis insights
            with st.spinner("Analyzing..."):
                try:
                    analysis = data_analyzr.analysis_insights(user_input=user_input)
                    st.write("Analysis Insights:")
                    st.write(analysis)
                except Exception as e:
                    st.error(f"An error occurred during analysis: {e}")


            with st.spinner("Visualizing..."):
                try:
                    # The visualizations function returns a dictionary of image titles to their byte content
                    visualizations = data_analyzr.visualizations(user_input=user_input)
                    
                    # Loop through the returned dictionary, converting byte content to images and display
                    for image_name, image_bytes in visualizations.items():
                        image = io.BytesIO(image_bytes)  # Convert byte content to a stream
                        st.image(image, use_column_width=True) 

                except Exception as e:
                    st.error(f"An error occurred during visualization: {e}")


            # Get dataset description
            description = data_analyzr.dataset_description()
            st.write("Dataset Description:")
            st.write(description)

            # Get recommended analysis queries
            queries = data_analyzr.ai_queries_df()
            st.write("Recommended Analysis Queries:")
            st.write(queries)

            # Get analysis recommendations
            analysis_recommendation = data_analyzr.analysis_recommendation()
            st.write("Analysis Recommendations:")
            st.write(analysis_recommendation)

            # Get strategic recommendations
            recommendations = data_analyzr.recommendations(user_input=user_input)
            st.write("Strategic Recommendations:")
            st.write(recommendations)

            # Get tasks for analysis
            tasks = data_analyzr.tasks(user_input=user_input)
            st.write("Tasks for Analysis:")
            st.write(tasks)

if __name__ == "__main__":
    main()