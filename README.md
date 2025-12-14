
# Education Monitoring & Evaluation (M&E) Pipeline

## Overview

This project implements an **end-to-end education Monitoring & Evaluation (M&E) analytics pipeline**, inspired by real-world workflows used by organizations such as **UNICEF** and **Education Cannot Wait (ECW)**.

The system allows users to **upload partner-reported education datasets** (CSV or Excel) and automatically performs data validation, quality assurance, indicator derivation, visualization, and reporting. The focus of the project is on **data governance, auditability, and policy-relevant analysis**, rather than predictive modeling.

---

## Key Features

### 1. Upload-Based Data Ingestion
- Supports CSV and Excel (`.xlsx`) files
- Designed for partner data submissions
- No hardcoded datasets

### 2. Schema Validation
- Verifies required columns and data types
- Validates categorical fields (education level, gender, wealth quintile, etc.)
- Blocks analysis if schema requirements are not met

### 3. Data Quality Assurance (QA)
- Missing value assessment
- Out-of-range value detection
- Logical consistency checks (e.g., completion rate ≤ attendance rate)
- Generates a structured QA report

### 4. Auditable Data Cleaning
- Applies bounded corrections where necessary
- Preserves original values in an audit log
- Ensures transparency and traceability of changes

### 5. Data Quality Severity Scoring
- Classifies datasets as **LOW**, **MEDIUM**, or **HIGH** risk
- Supports go/no-go decisions for analysis
- Mirrors real M&E decision workflows

### 6. Indicator Derivation
Derived indicators commonly used in education reporting:
- Education transition drop-off (Primary → Lower Secondary → Higher Secondary)
- Gender Parity Index (GPI)
- Rural–Urban completion gap
- Fragility-related completion gaps

### 7. Analytical Visualizations
Automatically generated plots include:
- Completion rate trends by education level
- Gender and fragility comparisons
- Structural inequality insights

Visuals are designed for **policy analysis and reporting**, not decorative dashboards.

### 8. Download Center
Users can download:
- Cleaned dataset
- Audit log
- Derived indicator tables
- PDF Data Quality Assurance report

### 9. QA Report (PDF)
- Automatically generated, human-readable QA summary
- Suitable for documentation, reporting, or donor review

---

## Tech Stack

- **Python**
- **Streamlit** (interactive web interface)
- **Pandas / NumPy** (data processing)
- **Matplotlib** (analytical visualization)
- **ReportLab** (PDF report generation)

---

## Project Structure

education-mne-pipeline/  
├── app.py # Main Streamlit application  
├── requirements.txt # Project dependencies  
│  
├── validators/  
│ ├── schema.py # Schema validation logic  
│ ├── quality.py # Data quality checks  
│ ├── cleaning.py # Data cleaning and audit logging  
│ └── severity.py # Severity scoring  
│  
├── indicators/  
│ └── derive.py # Indicator derivation logic  
│  
├── visuals/  
│ └── plots.py # Analytical visualization functions  
│  
├── reports/  
│ └── qa_pdf.py # PDF QA report generator  
│  
└── README.md

---

## How to Run Locally

### 1. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate       # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
streamlit run app.py
```

The app will be available at:
```bash
http://localhost:8501
```


## Deployment

The application is designed to be deployed on **Streamlit Community Cloud** using direct GitHub integration.

No additional server configuration or Docker setup is required for standard deployment.

----------

## Intended Use Case

This project demonstrates:

-   Education data governance practices
    
-   Monitoring & Evaluation (M&E) workflows
    
-   Data quality assurance pipelines
    
-   Policy-relevant education analytics
    

It is suitable as:

-   A technical portfolio project
    
-   An applied M&E analytics example
    
-   A learning tool for education data systems
    

----------

## Notes

-   The system can be used with real or synthetic datasets.
    
-   It is designed to generalize across countries, regions, and development contexts.
    
-   Emphasis is placed on **data quality, interpretability, and accountability**.
    

----------

## License

This project is licensed under the **MIT License**.

