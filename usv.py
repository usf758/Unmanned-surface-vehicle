#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dronekit import connect
import time
from automission_utils import automission, new_waypoint

# Load configuration data
with open("Data.txt", "r") as data:
    for ln in data:
        if ln.startswith("home_lat"):
            home_lat = float(ln.split(" ")[2])
        elif ln.startswith("home_long"):
            home_long = float(ln.split(" ")[2])
        elif ln.startswith("home_ASL"):
            home_ASL = float(ln.split(" ")[2])
        elif ln.startswith("Bearing"):
            main_bearing = float(ln.split(" ")[2])
        elif ln.startswith("Take_off_angle"):
            takeoff_angle = float(ln.split(" ")[2])
        elif ln.startswith("Take_off_alt"):
            takeoff_alt = float(ln.split(" ")[2])
        elif ln.startswith("waypoints_file"):
            waypoints_file = ln.split(" ")[2].replace('"', '').strip()

# Connect to vehicle
connection_string = '127.0.0.1:14551'
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)

# Wait for vehicle to initialize
while not vehicle.is_armable:
    print("Waiting for vehicle to initialize...")
    time.sleep(1)

# Create mission
mission = automission('plane')

# Add takeoff command
lat, lon = new_waypoint(home_lat, home_long, 1, main_bearing)
mission.takeoff(takeoff_angle, lat, lon, takeoff_alt)

# Add waypoints
with open(waypoints_file + '.txt') as file:
    lines = file.readlines()[2:]  # Skip headers
    for line in lines:
        lat, lon, alt = line.split()[8:11]
        mission.waypoint(float(lat), float(lon), float(alt))

# Write mission to file
mission.write()

# Upload mission to vehicle
import_mission_filename = "Output.txt"
print(f"Uploading mission from {import_mission_filename}...")
mission.upload_mission(import_mission_filename, vehicle)

# Close vehicle connection
print("Mission uploaded successfully. Closing vehicle connection.")
vehicle.close()
