# Pizza Bolis Delivery Distance Calculator
This repository contains a web application that helps to predict delivery times and routes for Pizza Bolis, a popular pizza chain in the US. It uses the Google Maps API to calculate distances and routes, and a simple linear regression model trained on historical data to predict delivery times.

The application is written in Python using the Flask web framework, and is intended to be run on a server. It provides a simple web interface for entering orders and drivers, and assigns orders to drivers based on their predicted delivery times and routes.

# Features
Distance Calculation: Calculates the distance from the Pizza Bolis location to the customer's location using the Google Maps API.

Direction Determination: Determines the general direction (North, South, East, or West) from the Pizza Bolis location to the customer's location.

Delivery Time Prediction: Uses a linear regression model to predict the delivery time based on the calculated distance. The model is trained on historical delivery data.

Order Assignment: Assigns orders to drivers based on their predicted delivery times and routes. It tries to balance the load among available drivers.

Interface: Provides a simple web interface for entering orders and drivers.

# Usage
Clone the repository to your local machine.
Install the required Python packages using pip.
Run the application using Flask.
Open your web browser and navigate to the URL of your local server (usually http://localhost:5000).
Enter the addresses of the orders and the names of the drivers, then click "Assign orders".
The application will assign the orders to the drivers and display the assignments, along with the distances, predicted delivery times, and directions.
# Requirements
Python 3.6 or later
Flask
pandas
scikit-learn
googlemaps Python client
# Contributions
Contributions are welcome! Please feel free to submit a Pull Request.

# Disclaimer
This application uses the Google Maps API, which is a paid service. You will need to provide your own API key and bear the costs associated with its use. Also, the application is intended for educational and demonstration purposes only. It may not be suitable for production use without further modifications. Use at your own risk.

# License
This project is licensed under the MIT License. See the LICENSE file for more details.
