from flask import Flask, render_template, request, jsonify
from sklearn.linear_model import LinearRegression
import googlemaps
import math
import pandas as pd
from datetime import datetime
#Initialize Model
model=LinearRegression()
app = Flask(__name__)

# Replace YOUR_API_KEY with your actual Google Maps API key
gmaps = googlemaps.Client(key='AIzaSyAyKdn3-PtAIaqpOiowekVvaARC9yH8nbY')
# Assume we have some historical delivery data
# In reality, you would load this data from a database or a CSV file
data = pd.DataFrame({
    'distance': [5, 10, 15, 20, 25],  # distances in km
    'delivery_time': [15, 20, 30, 40, 50]  # delivery times in minutes
})

# Train model
X = data[['distance']]
y = data['delivery_time']
model.fit(X, y)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        address = request.form['address']
        distance = calculate_distance(address)
        return render_template('index.html', distance=distance)
    return render_template('index.html')

@app.route('/assign', methods=['POST'])
def assign_order():
    data = request.get_json()
    orders = data['orders']
    drivers = data['drivers']
    
    # Calculate distances for each order
    distances_directions = [calculate_distance_and_direction(order) for order in orders]
    distances = [dist[0] for dist in distances_directions]
    directions = [dist[1] for dist in distances_directions]

    # Assign orders to drivers
    assignments = assign_orders_to_drivers(orders, drivers, distances, directions)

    return jsonify(assignments)

def predict_delivery_time(distance):
    # Predict delivery time based on distance
    delivery_time = model.predict([[distance]])
    return round(delivery_time[0], 2)

def assign_orders_to_drivers(orders, drivers, distances, directions):
    orders_with_info = zip(orders, distances, directions)
    sorted_orders = sorted(orders_with_info, key=lambda x: (x[2], x[1]))

    assignments = []

    for i, (order, distance, direction) in enumerate(sorted_orders):
        driver = drivers[i % len(drivers)]
        #Predict delivery time
        delivery_time=predict_delivery_time(distance)
        order_received_time=datetime.now() #store the current time
        time_remaining = 35 - delivery_time  # calculate time remaining
          # Determine delivery lateness
        if delivery_time <= 20:
            delivery_lateness = "green"
        elif delivery_time <= 30:
            delivery_lateness = "yellow"
        else:
            delivery_lateness = "red"

        assignments.append({'driver': driver, 'order': order, 'distance': distance, 'direction': direction, 'predicted_delivery_time':str(delivery_time), 'order_received_time':order_received_time.strftime("%H:%M:%S"),'time_remaining': str(time_remaining) if time_remaining > 0 else '0' })


    return assignments

def get_direction(order_location, store_location):
    lat1, lng1 = math.radians(order_location[0]), math.radians(order_location[1])
    lat2, lng2 = math.radians(store_location[0]), math.radians(store_location[1])
    dLng = lng2 - lng1

    x = math.cos(lat2) * math.sin(dLng)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dLng)

    bearing = math.degrees(math.atan2(x, y))
    bearing = (bearing + 360) % 360

    if 45 <= bearing < 135:
        return 'East'
    elif 135 <= bearing < 225:
        return 'South'
    elif 225 <= bearing < 315:
        return 'West'
    else:
        return 'North'

def calculate_distance_and_direction(address):
    pizza_bolis_location = (38.917038, -77.036527)
    geocode_result = gmaps.geocode(address)
    lat_lng = geocode_result[0]['geometry']['location']
    location = (lat_lng['lat'], lat_lng['lng'])

    distance_result = gmaps.distance_matrix(pizza_bolis_location, location, mode='driving')
    distance = float(distance_result['rows'][0]['elements'][0]['distance']['text'].split(' ')[0])

    direction = get_direction(location, pizza_bolis_location)

    return distance, direction



if __name__ == '__main__':
    app.run(debug=True)
