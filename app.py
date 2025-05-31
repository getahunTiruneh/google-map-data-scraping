# app.py

import streamlit as st
import os
import subprocess

st.set_page_config(page_title="Google Maps Scraper", layout="centered")

st.title("🗺️ Google Maps Data Extractor")

business_type = st.text_input("Business Type", placeholder="e.g., Dentist")
location = st.text_input("Location", placeholder="e.g., London")
total_results = st.number_input("Number of Results", min_value=1, max_value=500, value=20)

if st.button("Extract"):
    if not business_type or not location:
        st.warning("Please enter both business type and location.")
    else:
        search_query = f"{business_type.strip()} {location.strip()}"
        st.info(f"Running extraction for: {search_query}")

        command = f"python data-extractor.py -s \"{search_query}\" -t {total_results}"
        with st.spinner("Extracting data..."):
            result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            st.success("✅ Extraction completed!")

            filename_base = f"google_maps_data_{search_query.replace(' ', '_')}"
            excel_path = f"output/{filename_base}.xlsx"
            csv_path = f"output/{filename_base}.csv"

            if os.path.exists(excel_path):
                with open(excel_path, "rb") as f:
                    st.download_button("📥 Download Excel", f, file_name=os.path.basename(excel_path))

            if os.path.exists(csv_path):
                with open(csv_path, "rb") as f:
                    st.download_button("📥 Download CSV", f, file_name=os.path.basename(csv_path))
        else:
            st.error("❌ An error occurred during extraction.")
            st.code(result.stderr)
