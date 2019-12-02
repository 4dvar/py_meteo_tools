#!/usr/bin/env python

import numpy as np
import sys


H = float(sys.argv[1])
F = float(sys.argv[2])
M = float(sys.argv[3])



class pod_far_csi_bias:
    """
    PURPOSE:
        calculate evaluation metrics from given hits, false and misses
    """

    def __init__(self,H,F,M):
        self.hits = H
        self.false = F
        self.misses = M
        
    
    def pod(self):
        """
        PURPOSE:
            calc probability of detection (pod)
        """
        pod_a = self.hits / (self.hits+self.misses)
        return pod_a


    def far(self):
        """
        PURPOSE:
            calc false alarm rate (far)
        """
        far_a = self.false / (self.false+self.hits)
        return far_a


    def csi(self):
        """
        PURPOSE:
            calc critical success rate (csi)
        """
        csi_a = self.hits / (self.hits + self.misses + self.false)
        return csi_a


    def bias(self):
        """
        PURPOSE:
            calc bias
        """
        bias_a = (self.hits+self.false) / (self.hits+self.misses)
        return bias_a


    def print_out_in_line(self):
        """
        PUROPOSE:
            print all metrics in one line
            e.g. can be used for automatic processing for a large number of input data (H F M)
        """
        return str(self.pod()) + '  ' + str(self.far()) + '  ' + str(self.csi()) + '  ' + str(self.bias())


    def latex_out(self):
        """
        PUROPOSE:
            print all metrics in latex format
        """
        return '& $ ' + self.format_numbers(self.pod()) + ' $ & $ ' + self.format_numbers(self.far()) + ' $ & $ ' + self.format_numbers(self.csi()) + ' $ & $ ' + self.format_numbers(self.bias()) + ' $ \\'


    def print_metrics(self):
        print('POD: '+str(self.format_numbers(self.pod())))
        print('FAR: '+str(self.format_numbers(self.far())))
        print('CSI: '+str(self.format_numbers(self.csi())))
        print('BIAS: '+str(self.format_numbers(self.bias())))
        return


    def format_numbers(self,nr):
        """
        PURPOSE:
            format numbers and output as string
        """
        return str(round(nr,3))



if __name__ == '__main__':

    # USAGE:
    # python pod_far_csi_bias.py H F M
    # e.g. python pod_far_csi_bias.py 100 20 10


    obj = pod_far_csi_bias(H,F,M)
    obj.print_metrics()