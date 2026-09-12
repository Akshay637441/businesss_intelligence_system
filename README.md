# Multi-Industry Business Intelligence and Opportunity Analysis System

### Live Application

**[Open the Business Insights
Application](https://business-intelligence-system.streamlit.app/)**

A Big Data--driven business intelligence system built using the **Yelp
Open Dataset**, Hadoop/HDFS, Apache Spark, NLP, machine learning,
SQLite, and Streamlit.

------------------------------------------------------------------------

## 1. Project Overview

The **Multi-Industry Business Intelligence and Opportunity Analysis
System** transforms large-scale Yelp business and review data into
actionable business insights.

Instead of presenting only conventional dashboards, the system allows
users to:

-   Select a business industry.
-   Search for an individual business.
-   Evaluate its overall business health.
-   Analyze customer feedback and sentiment.
-   Identify strengths and customer concerns.
-   Examine category-specific customer experience aspects.
-   Estimate business decline risk.
-   Discover promising city--industry market opportunities.

The system focuses on four industries:

-   **Restaurant**
-   **Grocery**
-   **Healthcare**
-   **Auto Repair**

The underlying business dataset is not restricted to these four
categories; the full Yelp business dataset is retained, while these four
categories are used as the application's focus industries.

------------------------------------------------------------------------

## 2. Problem Statement

Large business-review datasets contain valuable information about
customer satisfaction, business performance, demand, and market
conditions. However, extracting useful business intelligence from
millions of reviews requires scalable data-processing techniques.

This project addresses the problem of converting large-scale Yelp
business and review data into understandable business-level and
market-level insights using a Big Data processing pipeline.

------------------------------------------------------------------------

## 3. Objectives

1.  Process large Yelp business and review datasets using Hadoop and
    Apache Spark.
2.  Clean and prepare business and review data for analysis.
3.  Perform review-based sentiment analysis.
4.  Calculate an interpretable Business Health Score.
5.  Identify potential business decline risk.
6.  Perform category-specific aspect analysis.
7.  Generate business strengths and customer concerns.
8.  Identify city--industry combinations with higher market opportunity.
9.  Store processed web-application data in SQLite.
10. Provide an interactive web interface using Streamlit.

------------------------------------------------------------------------

## 4. Dataset

The project uses the **Yelp Open Dataset**, including Yelp business and
review information.

### Dataset scale used in the project

  Data                          Records
  ------------------------- -----------
  Businesses                    150,346
  Reviews                     6,990,280
  Focus industries                    4
  Business-aspect records       399,950

The review dataset spans multiple years and contains millions of
customer reviews, making it suitable for demonstrating distributed Big
Data processing.

------------------------------------------------------------------------

## 5. Big Data Architecture

``` text
                    Yelp Open Dataset
                           |
                           v
                 +-------------------+
                 |   Hadoop / HDFS   |
                 |   Raw Data Store  |
                 +-------------------+
                           |
                           v
                 +-------------------+
                 |    Apache Spark   |
                 | Data Processing   |
                 +-------------------+
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
        NLP / Sentiment  Business     Opportunity
          Analysis       Health &       Analysis
                         Risk
             |             |             |
             +-------------+-------------+
                           |
                           v
                 +-------------------+
                 |   SQLite Database |
                 |  Web-ready Data   |
                 +-------------------+
                           |
                           v
                 +-------------------+
                 |     Streamlit     |
                 |   Web Application |
                 +-------------------+
```

------------------------------------------------------------------------

## 6. Technology Stack

### Big Data

-   Hadoop HDFS
-   Apache Spark
-   PySpark

### Data Processing and Analysis

-   Python
-   Pandas
-   NumPy
-   Scikit-learn
-   NLP preprocessing
-   TF-IDF
-   Logistic Regression
-   Random Forest

### Database

-   SQLite

### Visualization and Web Application

-   Streamlit
-   Plotly
-   Matplotlib
-   HTML/CSS styling

### Deployment

-   GitHub
-   Streamlit Community Cloud

------------------------------------------------------------------------

## 7. Major Features

### 7.1 Business Search and Discovery

Users can select one of the four focus industries and search for a
specific business.

The application presents:

-   Business name
-   Location
-   Industry
-   Yelp rating
-   Review activity

------------------------------------------------------------------------

### 7.2 Business Health Score

The system calculates an overall health score on a **0--100 scale**.

The score combines:

-   Rating score --- **50%**
-   Review activity --- **30%**
-   Operating status --- **20%**

The resulting health status is categorized as:

-   **Healthy**
-   **Moderate**
-   **At Risk**

This provides a compact indicator of the business's current position
based on available Yelp-derived indicators.

------------------------------------------------------------------------

### 7.3 Customer Feedback and Sentiment

Customer reviews are analyzed to classify feedback into:

-   Positive
-   Neutral
-   Negative

The project also includes a TF-IDF and Logistic Regression sentiment
model.

### Sentiment model evaluation

  Metric                 Result
  -------------------- --------
  Accuracy               79.49%
  Weighted Precision     77.93%
  Weighted Recall        79.49%
  Weighted F1            77.79%

The model was trained and evaluated using a sampled review dataset.

------------------------------------------------------------------------

### 7.4 Strengths and Problems

The application automatically identifies important customer experience
areas.

**Strengths** are derived from aspects with the highest positive
customer perception.

**Problems/concerns** are derived from aspects with the highest negative
customer perception.

This helps turn review data into concise business intelligence rather
than requiring users to manually inspect thousands of reviews.

------------------------------------------------------------------------

### 7.5 Category-Specific Aspect Analysis

Different industries have different customer experience dimensions.

The project therefore uses category-specific aspects.

  -----------------------------------------------------------------------
  Industry                            Example aspects
  ----------------------------------- -----------------------------------
  Restaurant                          Food, Service, Staff, Price,
                                      Quality, Ambience

  Grocery                             Product Quality, Variety, Price,
                                      Service, Staff, Cleanliness

  Healthcare                          Doctors, Quality of Care, Service,
                                      Staff, Wait Time, Cleanliness

  Auto Repair                         Repair Quality, Service, Staff,
                                      Price, Parts, Wait Time
  -----------------------------------------------------------------------

The system generated **399,950 business-aspect records** across the four
focus industries.

> **Note:** Aspect sentiment is derived from the review-rating sentiment
> associated with aspect mentions. It should be interpreted as
> rating-derived aspect feedback rather than a direct human-annotated
> text-sentiment label.

------------------------------------------------------------------------

### 7.6 Business Risk / Early Warning

The system calculates a risk score using:

-   Business health
-   Negative customer feedback

Businesses are classified into:

-   Low Risk
-   Medium Risk
-   High Risk

This provides an early-warning indicator for businesses that may require
closer attention.

------------------------------------------------------------------------

### 7.7 Business Health Prediction

A Random Forest model is also included for business health-status
prediction.

### Model evaluation

  Metric       Result
  ---------- --------
  Accuracy     97.26%

The model uses business and customer-feedback features such as:

-   Stars
-   Review count
-   Operating status
-   Positive percentage
-   Negative percentage
-   Business category

The health-status target is based on the project's engineered Business
Health Score categories, so the prediction result should be understood
as prediction of the project's defined health-status framework rather
than an externally validated business-failure label.

------------------------------------------------------------------------

### 7.8 Market Opportunity Analysis

The application also evaluates **city + industry** combinations to
identify promising markets.

The opportunity score combines:

-   **Review demand --- 60%**
-   **Inverse business competition --- 40%**

Review demand is normalized using review volume, while competition is
represented by the number of businesses in the corresponding
city--industry combination.

The result is an **Opportunity Score** used to rank market
opportunities.

> The opportunity score is a market-ranking indicator, not a guarantee
> of business success.

------------------------------------------------------------------------

## 8. Results

Some important project outputs include:

### Business Health

  Health Status     Businesses
  --------------- ------------
  Healthy               52,820
  Moderate              66,930
  At Risk               30,596

### Review Rating Distribution

    Rating     Reviews
  -------- -----------
         1   1,069,561
         2     544,240
         3     691,934
         4   1,452,918
         5   3,231,627

### Rating-derived sentiment

  Sentiment       Reviews   Approx. share
  ----------- ----------- ---------------
  Positive      4,684,545           67.0%
  Neutral         691,934            9.9%
  Negative      1,613,801           23.1%

------------------------------------------------------------------------

## 9. Project Structure

``` text
businesss_intelligence/
│
├── app/
│   └── streamlit_app.py
│
├── big_data/
│   ├── create_business_aspects.py
│   ├── create_web_database.py
│   ├── load_business_aspects.py
│   ├── spark_features.py
│   ├── spark_processing.py
│   └── spark_reviews.py
│
├── data/
│   └── business_insights.db.zip
│
├── data_analysis/
│   ├── category_analysis.py
│   ├── opportunity_analysis.py
│   ├── sentiment_analysis.py
│   └── trend_analysis.py
│
├── visualisations/
│   ├── opportunities.py
│   ├── ratings.py
│   ├── sentiment.py
│   ├── trends.py
│   └── generated charts
│
├── check_data.py
├── requirements.txt
├── .gitignore
└── README.md
```

The original Yelp raw dataset, local virtual environment, uncompressed
SQLite database, and processed temporary data are excluded from the Git
repository because of their size and deployment requirements.

------------------------------------------------------------------------

## 10. Running the Application Locally

### Clone the repository

``` bash
git clone https://github.com/Akshay637441/businesss_intelligence_system.git
cd businesss_intelligence_system
```

### Create a virtual environment

``` bash
python -m venv venv
```

Activate it on Windows:

``` powershell
venv\Scripts\activate
```

### Install dependencies

``` bash
pip install -r requirements.txt
```

### Run Streamlit

``` bash
streamlit run app/streamlit_app.py
```

The application will open in the browser.

------------------------------------------------------------------------

## 11. Big Data Processing Workflow

The project processing workflow is:

``` text
Raw Yelp JSON
      ↓
HDFS Storage
      ↓
Spark Data Cleaning
      ↓
Business & Review Processing
      ↓
Sentiment / NLP Analysis
      ↓
Feature Engineering
      ↓
Business Health
      ↓
Risk Analysis
      ↓
Aspect Analysis
      ↓
Opportunity Analysis
      ↓
SQLite Web Database
      ↓
Streamlit Application
```

------------------------------------------------------------------------

## 12. Deployment

The Streamlit application is deployed using **Streamlit Community
Cloud**.

### Live application

**https://business-intelligence-system.streamlit.app/**

The web application uses the compressed SQLite database stored in the
repository and automatically extracts the database when required by the
deployed application.

------------------------------------------------------------------------

## 13. Future Scope

Possible extensions include:

-   Time-series business decline forecasting.
-   More advanced transformer-based sentiment analysis.
-   Review-topic modeling.
-   Competitor comparison.
-   Geographic visualization using business coordinates.
-   More sophisticated market-demand estimation.
-   External economic and demographic data integration.
-   Automated recommendations for business owners.
-   Real-time review monitoring when live data sources are available.

------------------------------------------------------------------------

## 14. Academic Significance

This project demonstrates how a large-scale dataset can be transformed
into an end-to-end Big Data application.

It combines:

**Big Data Storage → Distributed Processing → NLP → Machine Learning →
Business Intelligence → Web Deployment**

rather than limiting the project to a conventional data visualization
dashboard.

------------------------------------------------------------------------

## 15. Disclaimer

This project is an academic/business-intelligence prototype based on the
Yelp Open Dataset.

Business Health Scores, Risk Scores, Opportunity Scores, and related
classifications are analytical indicators designed for this project.
They should not be interpreted as guaranteed predictions of business
success, failure, financial performance, or investment outcomes.

Sentiment and aspect results are derived from the project's defined
processing methodology and should be interpreted within that context.

------------------------------------------------------------------------

## Live Demo

### [Launch Business Insights →](https://business-intelligence-system.streamlit.app/)
