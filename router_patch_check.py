# -*- coding: utf-8 -*-
"""
Created on Wed Dec 10 18:37:08 2016

@author: Titilayo
"""
import sys, re
from collections import Counter


noRE = re.compile(',no,', re.I)                 # Regular expression that checks for no in the csv file
line_list = []                                  # List store of the lines of the csv file from routers of OS 12 and above which have not been patched
ip_list = []                                    # List store of the ip's in the csv file from routers of OS 12 and above which have not been patched
host_name_list = []                             # List store of the host names in the csv file that do not have the same ip address from routers of OS 12 and above which have not been patched
unique_ip_routers = []                          # list store of the routers of hostnames in host_name_list

with open(sys.argv[1], 'r') as infs:
    num = 0
    for line in infs:
        if num > 0:
            if noRE.search(line):
                if float(line.split(",")[3]) >= 12:
                    line_list.append(line)
                    ip_list.append(line.split(",")[1])
        num += 1

    unique_ip = [ip for ip, count in Counter(ip_list).items() if
                 count == 1]                                                         # remove re-occuring ip addresses in ip_list

    for router in range(len(line_list)):
        l = [line_list[router] for item in unique_ip if
             item in line_list[router]]                                              # List of a router that does not share ip addresses
        if l != []:
            unique_ip_routers.append(l[0])

            host_name_list.append(l[0].split(",")[0].lower())

            unique_ip_host_name_list = [ip for ip, count in Counter(host_name_list).items() if
                                        count == 1]                                         # remove re-occuring hostnames in host_name_list

    for router in range(len(unique_ip_routers)):
        l = [unique_ip_routers[router] for item in unique_ip_host_name_list if item in unique_ip_routers[
            router]]                                                                        # list of a router in unique_ip_router that do not share the same hostname
        if l != []:
             print((l[0]).split(",")[0]),                                                   # hostname
             print("(" + (l[0]).split(",")[1] + "),"),                                      # (IP Address)
             print("OS version " + (l[0]).split(",")[3]),                                   # OS version

             if (l[0]).split(",")[4] != '\r\n':
                print("[" + (l[0]).split(",")[4].join([l[0].split(",")[4].strip() + "]"]))  # Notes

             else:
               print((l[0]).split(",")[4].strip('\n'))
