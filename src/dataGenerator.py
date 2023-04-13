#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  5 13:01:23 2021
mock data generator stream. 
[x_vib,y_vib,z_vib,tilt,power]
x_vib = prone to failure x > 0.6 & y_vib > 0.8, or prone to failure x > 0.4 & z_vib > 0.3 (vibs go 0-1)
y_vib = prone to failure y > 0.45 & z_vib > 0.4, or prone to failure y_vib > 0.8 & x_vib > 0.6
z_vib = prone to failure z > 0.3 and x_vib > > 0.4, or y_vib > 0.3 & z_vib > 0.4
tilt = not a factor in failure
power = failure at power less than 35 (0-100)


TODO:
    Need to add capability for data drift (perhaps x_vib starts to become more common?)
@author: nicolenlama
"""

import pandas as pd
from sys import getsizeof
# import numpy as np
import random
import argparse


class Generator():
    def __init__(self,size=1,reason='training',failureRate=1):
        self.size = size
        self.reason = reason
        self.iters = self.convertSizeToIters()
        self.failureRate = failureRate
        self.generatorFunctions = [self.generateXYFailure,self.generateYZFailure,self.generateXZFailure,self.generatePowerFailure,self.generateHealthySample]
        self.failureFunctions = [self.generateXYFailure,self.generateYZFailure,self.generateXZFailure,self.generatePowerFailure]
        self.generateDataSet()

    def convertSizeToIters(self):
        iters = round(self.size * 9000)
        return iters
    def healthy_x_vals(self):
        return random.uniform(0, 0.4)
    def healthy_y_vals(self):
        return random.uniform(0, 0.45)
    def healthy_z_vals(self):
        return random.uniform(0, 0.3)
    def healthy_tilt_vals(self):
        return random.uniform(0, 0.1)
    def healthy_power_vals(self):
        return random.uniform(35, 100)
    
    def isTraining(self):
        if self.reason=='training':
            return True
        else:
            return False
        
    def generateXYFailure(self):
        X = random.uniform(0.6, 1)
        Y = random.uniform(0.8, 1)
        sample = [X,Y,self.healthy_z_vals(),self.healthy_tilt_vals(),self.healthy_power_vals()]

        return sample
    
    def generateYZFailure(self):
        Z = random.uniform(0.4, 1)
        Y = random.uniform(0.45, 1)
        sample = [self.healthy_x_vals(),Y,Z,self.healthy_tilt_vals(),self.healthy_power_vals()]

        return sample
    
    def generateXZFailure(self):
        X = random.uniform(0.6, 1)
        Z = random.uniform(0.8, 1)
        sample = [X,self.healthy_y_vals(),Z,self.healthy_tilt_vals(),self.healthy_power_vals()]

        return sample
   
    def generatePowerFailure(self):
        power = random.uniform(0, 35)
        sample = [self.healthy_x_vals(),self.healthy_y_vals(),self.healthy_z_vals(),self.healthy_tilt_vals(),power]

        return sample   
    
    def generateHealthySample(self):
        sample =[self.healthy_x_vals(),self.healthy_y_vals(),self.healthy_z_vals(),self.healthy_tilt_vals(),self.healthy_power_vals()]
        return sample

    def generateDataSet(self):
        data = []
        print(self.isTraining())
        if self.isTraining():
            for x in range(self.iters):
                decision = random.choice(['healthy','failure'])
                if decision == 'healthy':
                    sample = self.generateHealthySample()
                    sample.append("Healthy")
                else:
                    func = random.choice(self.failureFunctions)
                    sample = func()
                    sample.append("Failure")
                data.append(sample)
            data = pd.DataFrame(data, columns=['rpm','tool_wear','process_temperature','torque','air_temperature','label'])
        else: 
            for x in range(self.iters):
                number = random.randint(1, 100)
                if number <= self.failureRate:
                    func = random.choice(self.failureFunctions)
                else:
                    func = self.generateHealthySample
                sample = func()
                data.append(sample) 
            data = pd.DataFrame(data, columns=['rpm','tool_wear','process_temperature','torque','air_temperature'])
        self.data = data 
                

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Data')
    parser.add_argument('--size', metavar='MB', type=int,
                        help='size of data set in MBs. Note: This is not exact')
    parser.add_argument('--reason', type=str, choices=['training','stream'],
                        help='choose training for training data set and stream for stream')
    parser.add_argument('--failureRate', type=int, nargs='+', default = 1,
                        help='failure rate 0-100')
    parser.add_argument('--fileName', type=str, default = "data.json",
                    help='filename of output data')

    args = parser.parse_args()
    dataObj = Generator(args.size,args.reason,args.failureRate)
    data = dataObj.data
    print(data)
    # b = getsizeof(data)
    # mb = b/1024/1024
    data.to_json("./{0}".format(args.fileName),'records')
    print("{0} has been generated".format(args.fileName))
