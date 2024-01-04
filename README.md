# Honolulu Climate Analysis Project

## Overview
This project is designed to assist in planning a vacation in Honolulu, Hawaii, by providing a climate analysis based on available data. The project consists of two main parts: 

### Part 1: Analyze and Explore Climate Data
In this section, Python, SQLAlchemy, Pandas, and Matplotlib are utilized to perform a basic climate analysis and explore the climate database. The following tasks are carried out:
- Connecting to the SQLite database using SQLAlchemy.
- Reflecting tables into classes using SQLAlchemy's automap_base() function.
- Conducting precipitation and station analysis:
  - Precipitation Analysis: Retrieving the previous 12 months of precipitation data, summarizing statistics, and visualizing the results in a plot.
  - Station Analysis: Determining the total number of stations, finding the most-active stations, and analyzing temperature data for the most-active station.

### Part 2: Design Your Climate App
Upon completion of the initial analysis, a Flask API is designed based on the developed queries. The API includes the following routes:
- `/`: Homepage displaying available routes.
- `/api/v1.0/precipitation`: Returns JSON representation of the last 12 months of precipitation data.
- `/api/v1.0/stations`: Returns a JSON list of stations available in the dataset.
- `/api/v1.0/tobs`: Returns a JSON list of temperature observations for the previous year from the most-active station.
- `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`: Returns a JSON list of minimum, average, and maximum temperatures for a specified start date or start-end range.
- `/api/v1.0/start_end`: Interactive user interface that returns a list of temperature observations for a specific start and (optional) end date of interest.

## Instructions for Use
To utilize this project:
1. Access the provided files (`climate_starter.ipynb` and `hawaii.sqlite`) for conducting the climate analysis.
2. Execute the Python notebook to run the analysis and generate visualizations.
3. Utilize the Flask API routes to retrieve specific climate data for further analysis or integration into applications.

Please remember to close the session after completing the analysis.

For detailed step-by-step instructions, refer to the provided documentation within the `climate_starter.ipynb` notebook.

## Important Notes
- Ensure that Python, SQLAlchemy, Pandas, and Matplotlib are installed to execute the analysis.
- Review the provided notebook for comprehensive guidance on conducting the climate analysis.
- Modify the Flask API routes as needed to suit specific data retrieval requirements.
