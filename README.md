# End-to-End Real-Time Streaming Pipeline with Kafka, S3, and Databricks DLT

## Overview

This project demonstrates a **real-time data engineering pipeline** that simulates banking transaction data, ingests it via **Kafka**, persists raw events to **Amazon S3**, and processes them in **Databricks using Delta Live Tables (DLT)** following the **Medallion Architecture (Bronze, Silver, Gold)**.

The goal is to showcase:
- Event streaming with Kafka
- Micro-batch ingestion to S3
- Streaming ETL using Databricks DLT
- Clean separation of raw, refined, and analytics-ready data
- Production-style data engineering patterns

---

## High-Level Architecture 
![image alt](https://github.com/kapardireddy/Kafka_S3_Databricks/blob/10ef66ba8c71890d8a3f1404e713a1edd7442567/Project%20Architecture.png)
***Note : Image Generated using ChatGPT*** (Working on Prompt Engineering)

*Actual DLT Pipeline graph of the Medallion Architecture is below* 


**Flow Summary:**

1. **Kafka Producer (Python)**
   - Generates realistic fake transaction data
   - Publishes messages to Kafka topic `transaction_logs`

2. **Kafka Consumer (Python)**
   - Consumes messages from Kafka
   - Writes raw JSON files to S3 at configurable intervals
   - Mimics real-world banking transaction capture

3. **Databricks Delta Live Tables (DLT) Pipeline**
   - Reads raw JSON from S3 (Bronze)
   - Cleans, normalizes, and structures data (Silver)
   - Produces analytics-ready aggregates and metrics (Gold)

---

## Sample Transaction Event


```json
{
  "transaction_id": "88a0d88f-50c3-4e36-a3ce-37ae1dbe71fb",
  "user": {
    "user_id": 39,
    "name": "Brandy Chavez",
    "email": "umatthews@example.org",
    "country": "Turks and Caicos Islands",
    "city": "Penafort",
    "address": "53773 Garcia Spur Suite 850\nHillville, PR 60101",
    "age": 64,
    "payment_method": "credit_card",
    "device_type": "mobile",
    "ip_address": "77.147.36.70"
  },
  "amount": 496.23,
  "currency": "GBP",
  "timestamp": "2026-01-21T00:39:04.153833Z",
  "category": "travel",
  "items": [
    {
      "item_id": "e6d52ebc-59f3-4b6c-81af-c24928a3d0cd",
      "name": "Train Pass",
      "price": 151.12,
      "quantity": 1
    },
    {
      "item_id": "46983792-6050-4ec3-8c36-8faa9d331832",
      "name": "Flight Ticket",
      "price": 345.11,
      "quantity": 1
    }
  ]
}
```
## Repository Structure
```yaml
KAFKA_S3_DATABRICKS/
│
├── Transactions pipeline/
│ ├── explorations/
│ │ └── sample_exploration.py
│ │
│ ├── transformations/
│ │ ├── bronze/
│ │ │ └── bronze_transactions_ingestion.py
│ │ │
│ │ ├── silver/
│ │ │ ├── silver_transactions.py
│ │ │ ├── silver_users.py
│ │ │ └── silver_items.py
│ │ │
│ │ └── gold/
│ │ ├── gold_daily_metrics.py
│ │ ├── gold_product_summary.py
│ │ └── gold_user_summary.py
│
├── utilities/
│
├── producer.py
├── consumer.py
├── docker-compose.yml
├── requirements.txt
├── README.md
├── Final_Pipeline_Graph.png
└── Kafka_S3_Databricks.png
```

---

## Medallion Architecture (Delta Live Tables)

This project follows the **Medallion Architecture** using **Databricks Delta Live Tables (DLT)** to progressively refine streaming transaction data.

---

### 🟤 Bronze Layer — Raw Data Ingestion

**Purpose:**  
Raw ingestion of transaction events exactly as received.

**Responsibilities:**
- Reads JSON transaction files from Amazon S3
- Applies schema without transformations
- Preserves raw event fidelity for traceability and replay

**File:**
- bronze/bronze_transactions_ingestion.py

---

### ⚪ Silver Layer — Cleaned & Structured Data

**Purpose:**  
Transform raw data into clean, queryable, and normalized tables.

**Responsibilities:**
- Parses nested JSON structures
- Explodes array fields (e.g., `items`)
- Separates entities into logical tables
- Applies basic data quality and consistency rules

**Files:**
- silver/silver_transactions.py
- silver/silver_users.py
- silver/silver_items.py


---

### 🟡 Gold Layer — Business-Ready Analytics

**Purpose:**  
Provide enriched, aggregated datasets for analytics and reporting.

**Responsibilities:**
- Daily transaction metrics
- User-level aggregations
- Product and category summaries
- Optimized for dashboards and stakeholder consumption

**Files:**
- gold/gold_daily_metrics.py
- gold/gold_user_summary.py
- gold/gold_product_summary.py


---

## Local Setup & Execution

### 1. Start Kafka & Dependencies

```bash
docker-compose up -d
```
This starts:

- Kafka broker
- Zookeeper
- Required networking for producer and consumer services

### 2. Start Kafka Producer

```bash
python producer.py
```
This will:
- Continuously generate realistic fake transaction events
- Publishes events to Kafka topic: transaction_logs

### 3. Start Kafka Consumer

```bash
python consumer.py
```
This will:
- Read messages from transaction_logs
- Write raw JSON files to Amazon S3 (update code to match the details of your bucket in .env file)
- Uses time-based or record-count-based batching
- Mimics real-world banking transaction ingestion

This above Steps can performed on:
-> Local machine
-> EC2 instance
-> Any VM with network access to Kafka and S3

---
## Databricks Setup

1. Upload the Transactions pipeline folder to Databricks
2. Create a Delta Live Tables (DLT) pipeline
3. Set the Bronze ingestion file as the pipeline entry point
4. Run the pipeline

## The DLT streaming pipeline will look like this:

![image alt](https://github.com/kapardireddy/Kafka_S3_Databricks/blob/67c004aed808ffb12ebe608ec23cf7921754476e/Final_Pipeline%20Graph.png)

***Please Note : Output records depend on how long you run the Producer and Consumer (Number of users will always be 50)***

### Configure:
1. S3 access credentials
2. Target database/schema
3. Pipeline storage location
4. Run the pipeline in continuous or triggered mode

### Key Concepts Demonstrated
1. Kafka event streaming
2. Schema-on-read ingestion
3. Micro-batch file landing to S3
4. Delta Live Tables (DLT)
5. Streaming tables
6. Medallion architecture
7. Production-style data modeling
8. Analytics-ready Gold tables

### Future Enhancements (Optional)

- Data quality expectations and constraints in DLT
- Late-arriving data handling
- Fraud detection and anomaly detection features
- Change Data Capture (CDC) simulation
- Dashboard integration (Databricks SQL / Power BI)

---
## Author

Built by a Data Engineer focused on real-time, production-grade data pipelines.  
For questions or collaboration, reach out to **kapardi21@gmail.com**.

---
