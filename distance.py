#First success, optimising with distance
#This code needs the following things to be fully ready
#1. The cities should be taken as input and not be static
#2 Possibly use the google maps API to get the distance between the cities
#3. This should be made the backend for the actual use case of the website, frontend repo to start soon


import requests
import json
import itertools


def create_data_model(city):
   """Stores the data for the problem."""
   data = {}

   # List of cities
   cities = city
   place_ids = {}
   cities_coordinates={}


   for city in cities:
       url1 = f'https://nominatim.openstreetmap.org/search?q={city}&format=json'

       response = requests.get(url1)
       result = response.json()

       if result:
           place_id = result[0]['place_id']
           #print(place_id, city)
           place_ids[city] = place_id
           url=f'https://nominatim.openstreetmap.org/details?place_id={place_id}&format=json'

           response = requests.get(url)
           result = response.json()
           cities_coordinates[city]=result['centroid']['coordinates']
           long=result['centroid']['coordinates'][0]
           lat=result['centroid']['coordinates'][1]
           #print(long,lat)

   # Initialize the distance matrix
   data["distance_matrix"] = []


   # Fetch the distance between each pair of cities
   for origin in cities:
       origin_coordinates = cities_coordinates[origin]
       row = []
       for destination in cities:
           destination_coordinates = cities_coordinates[destination]
           url = 'https://api.openrouteservice.org/v2/directions/driving-car'
           headers = {
               'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
               'Authorization': '5b3ce3597851110001cf62485e20e7a960f64e1e90f631af07a27df8',
               'Content-Type': 'application/json; charset=utf-8'
           }
           body = {"coordinates":[
                       [origin_coordinates[0], origin_coordinates[1]],
                       [destination_coordinates[0], destination_coordinates[1]]
                   ],"radiuses":[-1],"units":"m"}
           response = requests.post(url, headers=headers, json=body)
           result = response.json()
           # Extract the distance value from the API response
           distance = result['routes'][0]['segments'][0]['distance']
           #print(f"Distance between {origin} and {destination} is {distance} meters")
           row.append(distance)
       data["distance_matrix"].append(row)

   data["num_vehicles"] = 1
   data["depot"] = 0
   #print(data)
   return data


#distance_matrix = data["distance_matrix"]

def total_distance(path, distance_matrix):
   """
   Calculate the total distance of a given path based on the distance matrix.
   """
   total = 0
   for i in range(len(path) - 1):
       total += distance_matrix[path[i]][path[i + 1]]
   return total

def brute_force_tsp(starting_point, distance_matrix):
   """
   Find the optimal route using brute-force approach.
   """
   num_cities = len(distance_matrix)
   cities = list(range(num_cities))
   cities.remove(starting_point) # Remove starting point from the cities list
   min_distance = float('inf')
   optimal_route = None

   for perm in itertools.permutations(cities):
       # Construct full path starting from the starting point
       path = [starting_point] + list(perm)
       path_distance = total_distance(path, distance_matrix)
       if path_distance < min_distance:
           min_distance = path_distance
           optimal_route = path

   # Add starting point at the end to complete the route
   optimal_route.append(starting_point)

   return optimal_route


starting_point = 0 # Starting point index

#optimal_route = brute_force_tsp(starting_point, distance_matrix)

# Print the optimal route
#print("Optimal route:", "->".join(map(str, optimal_route)))
#print(create_data_model()['distance_matrix'])
# Print the total distance of the optimal route
