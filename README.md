# Airflow ETL Pipeline with PostgreSQL and OpenWeather API

## 📌 Project Overview
This project implements an **ETL (Extract, Transform, Load) pipeline** using **Apache Airflow** to:
- Extract weather data from the **OpenWeather API**.
- Transform the data for preprocessing.
- Load the processed data into a **PostgreSQL database**.

The project follows the **Astro CLI structure** (`astro dev init`).

---

## 🏗 Project Structure
```
.
├── dags/                # Airflow DAGs (Pipeline definitions)
│   ├── etl_pipeline.py  # Main ETL workflow
│   ├── utils.py         # Utility functions (API calls, transformations)
│
├── include/             # Additional files (SQL scripts, configurations)
│
├── plugins/             # Custom Airflow plugins (if needed)
│
├── tests/               # Unit tests for DAGs
│
├── Dockerfile           # Airflow Docker setup
├── requirements.txt     # Python dependencies
├── airflow_settings.yaml # Airflow configurations
├── README.md            # Project documentation
└── .astro/              # Astro CLI configurations
```

---

## 🛠️ Tools Used
### **Apache Airflow**
- A powerful workflow orchestration tool for scheduling and managing data pipelines.
- Provides DAGs (Directed Acyclic Graphs) to define ETL workflows.

### **PostgreSQL**
- A robust, open-source relational database system.
- Used to store the transformed weather data.

### **OpenWeather API**
- Provides real-time and historical weather data.
- Free access available with API key registration.

---

## ⚙️ Prerequisites
- **Docker & Docker Compose** installed
- **Astro CLI** installed (`pip install astro-cli`)
- **PostgreSQL Database** (running locally or on cloud)
- **OpenWeather API Key** (Get from [OpenWeather](https://openweathermap.org/api))

---

## 🚀 Getting Started
### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/ETL-pipeline-airflow-to-postgres.git
cd ETL-pipeline-airflow-to-postgres
```

### 2️⃣ Start Airflow
```bash
astro dev start
```

### 3️⃣ Set up PostgreSQL Connection in Airflow UI
1. Open Airflow UI (`http://localhost:8080`)
2. Go to **Admin → Connections**
3. Create a **Postgres Connection** with:
   - Conn ID: `postgres_db`
   - Conn Type: `Postgres`
   - Host: `localhost`
   - Schema: `your_database`
   - Login: `your_user`
   - Password: `your_password`

### 4️⃣ Add OpenWeather API Key
- Store your **API key** in Airflow Variables:
  ```bash
  airflow variables set openweather_api_key "YOUR_API_KEY"
  ```

### 5️⃣ Trigger the DAG
1. Open Airflow UI (`http://localhost:8080`)
2. Enable and run the DAG `etl_pipeline`

---

## 🔧 Key Components
- **DAG (`etl_pipeline.py`)**: Defines the ETL workflow.
- **Task 1 - Extract**: Fetches weather data from OpenWeather API.
- **Task 2 - Transform**: Cleans and processes data.
- **Task 3 - Load**: Inserts data into PostgreSQL.

---

## 📜 License
MIT License

---

## 📬 Contact
For questions or contributions, reach out via [GitHub Issues](https://github.com/your-username/ETL-pipeline-airflow-to-postgres/issues).

