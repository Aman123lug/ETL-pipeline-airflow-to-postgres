from airflow import DAG
# from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.decorators import task, dag
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
import json
import os
import requests
import pendulum


with DAG(
   dag_id="openWeatherAPI",
   description="openWeatherAPI",
   start_date=pendulum.today("UTC").add(days=-1),
   schedule="@daily"
   
) as dag:
    
   # step:1 create table if not exists
   @task
   def create_table():
      #initialize PostgresHook
      postgres_hook = PostgresHook(postgres_conn_id="my_postgres_connection" )
      
      create_table_query="""
      CREATE TABLE weather_data (
         id SERIAL PRIMARY KEY,
         city VARCHAR(100) NOT NULL,
         region VARCHAR(100),
         country VARCHAR(100) NOT NULL,
         localtime TIMESTAMP NOT NULL,
         temperature_c NUMERIC(5, 2) NOT NULL,
         temperature_f NUMERIC(5, 2) NOT NULL,
         condition TEXT NOT NULL,
         humidity INT NOT NULL,
         )
      
      """
      postgres_hook.run(create_table_query)
   # step: 2 Extract the OpenWeather API data 
      url = "http://api.weatherapi.com/v1/current.json?key=2f986dba45bd45a4a8092627250402&q=India&aqi=yes"
      API_KEY = "2f986dba45bd45a4a8092627250402"  # Replace with your actual API key
      COUNTRY_NAME = "India"  # Replace with your desired city
      BASE_URL = "http://api.weatherapi.com/v1/current.json"

      # Parameters for the API request
      params = {
         "q": COUNTRY_NAME,
         "key": API_KEY,
         "aqi": "yes"  # Use "imperial" for Fahrenheit
      }

      # Send GET request to the API
      response = requests.get(BASE_URL, params=params)

      # Check if the request was successful
      if response.status_code == 200:
         # Parse the JSON response
         data = response.json()
         # print(data)
      return data
       
       
   # step: 3 Transform the data (select info that i need to save)  
   @task
   def transform_data(response):
      location = response['location']
      city = location['name']
      region = location['region']
      country = location['country']
      localtime = location['localtime']

      # Extract current weather information
      current = response['current']
      temperature_c = current['temp_c']
      temperature_f = current['temp_f']
      condition = current['condition']['text']
      humidity = current['humidity']
      
      data = {
         "city": city,
         "region": region,
         "country": country,
         "localtime": localtime,
         "temperature_c": temperature_c,
         "temperature_f": temperature_f,
         "condition": condition,
         "humidity": humidity
         
      }
      return data
   # step: 4 Load into PostgreSQL      
   @task
   def load_into_postgres(apo_data):
      postgres_hook = PostgresHook(postgres_conn_id="my_postgres_connection")
      insert_query = """
      
      INSERT INTO weather_data (
         city, region, country, localtime,
         temperature_c, temperature_f, condition,
         humidity
      ) VALUES (
         %s, %s, %s, %s, %s, %s, %s, %s 
      )
      
      """
      
      postgres_hook.run(insert_query, parameters=(
         apo_data['city'], 
         apo_data['region'],
         apo_data['country'],
         apo_data['localtime'],
         apo_data['temperature_c'],
         apo_data['temperature_f'],
         apo_data['condition'],
         apo_data['humidity']     
                        ))
      
      
         
      # step: 5 verify the all things everything is working good or not.
      # step: 6 Add all dependency 
   extracted_data = create_table()
   #transform
   transformed_data = transform_data(extracted_data)
   #load
   load_into_postgres(transformed_data)
   
      
      
      
      
    
    
    
    