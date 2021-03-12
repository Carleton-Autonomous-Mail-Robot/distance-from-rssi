#!/usr/bin/env python

import os
import math
from bluepy.btle import Scanner

class RSSI_Tools:
    def __init__(self):
        self.__measured_power = -59
        self.__enviromental = {}

    '''
        Reads RSSI of a given MAC address
    '''
    def __read_RSSI(self,MAC):
        ble_list = Scanner().scan(0.5)
        for dev in ble_list:
            #print(dev.addr)
            if dev.addr == MAC.lower():
                return dev.rssi
        return None


    '''
        returns the distance of beacon
    '''
    def get_enviromental(self,MAC):
        self.__calobrate_enviromental(MAC)



    def get_mean_RSSI(self,MAC):
        sum = 0
        samples = 10
        rng = 10
        for i in range(rng):
            RSSI = self.__read_RSSI(MAC)
            if RSSI is None:
                samples = samples - 1
                continue
            sum = sum + RSSI
            #print(sum)
        return sum / samples



    def __calobrate_enviromental(self,MAC):
        sum_of_n = 0
        for i in range(2,10):
            print('Place Beacon '+str(i)+'m away')
            raw_input('Press enter to continue:')
            RSSI = self.get_mean_RSSI(MAC)
            sum_of_n = sum_of_n + (self.__measured_power - RSSI)/(10*math.log(i,10))
        self.__enviromental[MAC] = sum_of_n/8
        print("Enviromental Factor: " + str(sum_of_n/8))
        
    
    '''
        Reads RSSI of a given MAC address
    '''
    def read_RSSI(self,MAC):
        ble_list = Scanner().scan(1)
        for dev in ble_list:
            if dev.addr == MAC.lower():
                print(dev.addr)
        return None

        
tools = RSSI_Tools()


while True:
    mac = raw_input('Enter MAC Address: ')
    tools.get_enviromental(mac)



