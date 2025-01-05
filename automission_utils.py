#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math

R = 6371000.0  # Earth radius in meters

class automission:
    def __init__(self, vehicle_type):
        assert vehicle_type == 'plane'
        self.mlist = []  # each element of the array represents a command, i.e., waypoint, with its parameters
        self.counter = 1
        self.mlist.append(f"QGC WPL 110\n0\t1\t0\t16\t0\t0\t0\t0\t{home_lat}\t{home_long}\t{home_ASL}\t1\n")  # Current Home Location

    def param_to_mcommand(self, *args):
        string = str(self.counter) + '\t'
        self.counter += 1
        for i in args:
            string += str(i) + '\t'
        string = string.rstrip('\t') + '\n'
        self.mlist.append(string)

    def waypoint(self, lat, lon, alt, delay=0):
        waypoint_id = 16
        self.param_to_mcommand(0, 3, waypoint_id, delay, 0, 0, 0, lat, lon, alt, 1)

    def takeoff(self, angle, lat, lon, alt):
        takeoff_id = 22
        self.param_to_mcommand(0, 3, takeoff_id, angle, 0, 0, 0, lat, lon, alt, 1)

    def write(self, name='Output'):
        with open(str(name) + ".txt", "w") as text_file:
            for i in self.mlist:
                print(i)
                text_file.write(i)

def new_waypoint(lat1, long1, d, brng):
    brng = brng * (math.pi / 180)
    lat1_r, long1_r = Convert(lat1, long1)
    lat2_r = math.asin(math.sin(lat1_r) * math.cos(d / R) + math.cos(lat1_r) * math.sin(d / R) * math.cos(brng))
    long2_r = long1_r + math.atan2((math.sin(brng) * math.sin(d / R) * math.cos(lat1_r)),
                                   (math.cos(d / R) - math.sin(lat1_r) * math.sin(lat2_r)))
    lat2, long2 = ReConvert(lat2_r, long2_r)
    return lat2, long2

def Convert(lat, lon):
    return float(lat) * math.pi / 180, float(lon) * math.pi / 180

def ReConvert(lat, lon):
    return float(lat) * 180 / math.pi, float(lon) * 180 / math.pi
