import os
import math
from bluepy.btle import Scanner

class RSSI_Tools:
    def __init__(self):
        self.__measured_power = {}
        self.__enviromental = {}

    '''
        Reads RSSI of a given MAC address
    '''
    def __read_RSSI(self,MAC:str):
        ble_list = Scanner().scan(4.0)
        for dev in ble_list:
            print(dev.addr)
            if dev.addr == MAC.lower():
                return dev.rssi
        return None


    '''
        returns the distance of beacon
    '''
    def get_distance(self,MAC)->float:
        if MAC in self.__measured_power:
            RSSI = self.get_mean_RSSI(MAC)
            return pow(10,(self.__measured_power[MAC] - RSSI)/(10*self.__enviromental[MAC]))
        
        print('Place Beacon at 1m from PI')
        input('Press enter to continue')

        self.__calculate_standard_dev(MAC)
        self.__calobrate_enviromental(MAC)



    def get_mean_RSSI(self,MAC:str):
        sum = 0
        for i in range(5):
            RSSI = self.__read_RSSI(MAC)
            if RSSI is None:
                return None
            sum = sum + RSSI
            print(sum)
        return sum / 5

    '''
        calculates also the standard deviation
    '''
    def __calculate_standard_dev(self,MAC:str):
        li = []
        sum = 0
        for i in range(5):
            RSSI = self.__read_RSSI(MAC)
            if RSSI is None:
                print('MAC Not Found')
                return
            li.append(RSSI) #populates a list with RSSI readings
            sum = sum + RSSI
            
        mean = sum / 4 
        self.__measured_power[MAC] = mean
        print('Measured Power Set: '+str(mean))

        sum_of_squares = 0
        for i in range(5):
            sum_of_squares = pow((li[i] - mean),2)
        
        variance = sum_of_squares / 4
        print('Standard Deviation: '+str(math.sqrt(sum_of_squares)))


    def __calobrate_enviromental(self,MAC):
        sum_of_n = 0
        for i in range(2,10):
            print('Place Beacon '+str(i)+'m away')
            input('Press enter to continue:')
            RSSI = self.get_mean_RSSI(MAC)
            sum_of_n = sum_of_n + (self.__measured_power[MAC] - RSSI)/(10*math.log(i,10))
        self.__enviromental[MAC] = sum_of_n/10



        
tools = RSSI_Tools()

while True:
    mac = input('Enter MAC Address: ')
    tools.get_distance(mac)



