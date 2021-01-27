import os
import math

class RSSI_Tools:
    def __init__(self):
        self.__measured_power = {}
        self.__enviromental = {}

    '''
        Reads RSSI of a given MAC address
    '''
    def __read_RSSI(self,MAC:str):
        raw_input = os.popen('sudo btmgmt find').read()

        input_list = raw_input.splitlines()

        beacon_rssi = None
        for s in input_list:
            if MAC in s:
                s_split = s.split(' ')
                beacon_rssi = s_split[s_split.index('rssi') + 1]

        if beacon_rssi is None:
            return None
        return int(beacon_rssi)


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
        for i in range(10):
            RSSI = self.__read_RSSI(MAC)
            sum = sum + RSSI
            print(sum)
        return sum / 10

    '''
        calculates also the standard deviation
    '''
    def __calculate_standard_dev(self,MAC:str):
        li = []
        sum = 0
        for i in range(10):
            RSSI = self.__read_RSSI(MAC)
            if RSSI is None:
                print('MAC Not Found')
                return
            li.append(RSSI) #populates a list with RSSI readings
            sum = sum + RSSI
            
        mean = sum / 10 
        self.__measured_power[MAC] = mean
        print('Measured Power Set: '+mean)

        sum_of_squares = 0
        for i in range(100):
            sum_of_squares = pow((li[i] - mean),2)
        
        variance = sum_of_squares / 9
        print('Standard Deviation: '+math.sqrt(sum_of_squares))


    def __calobrate_enviromental(self,MAC):
        sum_of_n = 0
        for i in range(2,10):
            print('Place Beacon '+i+'m away')
            input('Press enter to continue:')
            RSSI = self.get_mean_RSSI(MAC)
            sum_of_n = sum_of_n + (self.__measured_power[MAC] - RSSI)/(10*math.log(i,10))
        self.__enviromental[MAC] = sum_of_n/10



        
tools = RSSI_Tools()

while True:
    mac = input('Enter MAC Address: ')
    tools.get_distance(mac)



