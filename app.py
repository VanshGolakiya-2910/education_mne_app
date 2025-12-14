import streamlit as st
import pandas as pd
import tempfile

from validators.schema import validate_schema_df
from validators.quality import run_quality_checks
from validators.cleaning import clean_dataset
from validators.severity import compute_severity_score
from indicators.derive import derive_all_indicators
from visuals.plots import (
    plot_overview_completion,
    plot_fragility_and_gender
)
from reports.qa_pdf import generate_qa_pdf

# =========================================================
# PAGE CONFIG (MUST BE FIRST)
# =========================================================

st.set_page_config(page_title="Education M&E Pipeline", layout="wide")

st.title("Education Monitoring & Evaluation Pipeline")
st.write("Upload a partner dataset to validate, clean, and analyze education indicators.")

# =========================================================
# FILE UPLOAD
# =========================================================

uploaded_file = st.file_uploader(
    "Upload education monitoring dataset (CSV or Excel)",
    type=["csv", "xlsx"]
)

if uploaded_file:
    # =====================================================
    # LOAD FILE
    # =====================================================
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("File uploaded successfully.")
    st.write("Preview of uploaded data:")
    st.dataframe(df.head())

    # =====================================================
    # STEP 1: SCHEMA VALIDATION
    # =====================================================
    schema_errors = validate_schema_df(df)

    if schema_errors:
        st.error("Schema validation failed.")
        for err in schema_errors:
            st.write(f"- {err}")
        st.stop()
    else:
        st.success("Schema validation passed.")

    # =====================================================
    # STEP 2: DATA QUALITY CHECKS
    # =====================================================
    qa_report = run_quality_checks(df)

    st.subheader("Data Quality Report")
    st.json(qa_report)

    # =====================================================
    # STEP 3: CLEANING
    # =====================================================
    clean_df, audit_log = clean_dataset(df)

    st.success("Data cleaning completed.")
    st.write("Corrections applied:", len(audit_log))

    st.download_button(
        "Download Clean Dataset",
        clean_df.to_csv(index=False),
        file_name="clean_dataset.csv"
    )

    st.download_button(
        "Download Audit Log",
        audit_log.to_csv(index=False),
        file_name="audit_log.csv"
    )

    # =====================================================
    # STEP 4: INDICATORS
    # =====================================================
    indicators = derive_all_indicators(clean_df)

    st.subheader("Derived Indicators")
    for name, table in indicators.items():
        st.write(f"### {name}")
        st.dataframe(table)

    # =====================================================
    # STEP 5: VISUAL INSIGHTS
    # =====================================================
    st.subheader("Key Visual Insights")

    st.pyplot(plot_overview_completion(clean_df))
    st.pyplot(plot_fragility_and_gender(clean_df))

    # =====================================================
    # STEP 6: SEVERITY SCORING
    # =====================================================
    severity = compute_severity_score(qa_report)

    st.subheader("Data Quality Severity")
    st.write(f"Severity level: **{severity}**")

    if severity == "HIGH":
        st.error("Dataset not suitable for analysis. Partner resubmission recommended.")
    elif severity == "MEDIUM":
        st.warning("Proceed with caution.")
    else:
        st.success("Dataset suitable for analysis.")

    # =====================================================
    # STEP 7: QA PDF REPORT
    # =====================================================
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        generate_qa_pdf(tmp.name, qa_report, severity)
        st.download_button(
            "Download QA Report (PDF)",
            open(tmp.name, "rb"),
            file_name="QA_Report.pdf"
        )
        
    # =====================================================
    # SAVE OUTPUT FILES IN MEMORY
    # =====================================================

    output_files = {}

    # Clean data
    output_files["Clean Dataset"] = (
        "clean_dataset.csv",
        clean_df.to_csv(index=False).encode("utf-8")
    )

    # Audit log
    output_files["Audit Log"] = (
        "audit_log.csv",
        audit_log.to_csv(index=False).encode("utf-8")
    )

    # Indicator tables
    for name, table in indicators.items():
        filename = name.lower().replace(" ", "_") + ".csv"
        output_files[name] = (
            filename,
            table.to_csv(index=False).encode("utf-8")
        )

    # QA PDF
    output_files["QA Report (PDF)"] = (
        "QA_Report.pdf",
        open(tmp.name, "rb").read()
    )

    # =====================================================
    # FINAL DOWNLOAD CENTER
    # =====================================================

    st.divider()
    st.subheader("Download Center")

    download_rows = []

    for label, (filename, _) in output_files.items():
        download_rows.append({
            "File": filename,
            "Description": label
        })

    download_df = pd.DataFrame(download_rows)
    st.dataframe(download_df, use_container_width=True)

    for label, (filename, data) in output_files.items():
        st.download_button(
            label=f"Download {filename}",
            data=data,
            file_name=filename,
            mime="application/octet-stream"
        )

    # =====================================================
    # DOWNLOAD ALL AS ZIP
    # =====================================================

    import zipfile
    import io

    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for _, (filename, data) in output_files.items():
            zip_file.writestr(filename, data)

    st.download_button(
        label="Download All Files (ZIP)",
        data=zip_buffer.getvalue(),
        file_name="education_mne_outputs.zip",
        mime="application/zip"
    )
