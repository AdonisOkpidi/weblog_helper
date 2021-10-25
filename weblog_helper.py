#!/usr/bin/env python
import argparse
import ipaddress
import requests
import os
import re

def get_logs():
    url = ("https://s3.amazonaws.com/syseng-challenge/public_access.log.txt")
    all_log_info = requests.get(url)
    log_info = all_log_info.text

    write_log = open("./weblog_output.txt", "a")
    write_log.write(log_info)
    write_log.close()

def open_logs():
    open_log = open('./weblog_output.txt', "r")
    logs = open_log.readlines()

    return logs

def validate_ip_address(ip_address):
    try:
        ip = ipaddress.ip_network(ip_address)
        print("IP address {} is valid. The object returned is {}".format(ip_address, ip))
    except ValueError:
        print("IP address {} is not valid".format(ip_address))
        exit

def get_cidr_range(ip_address, logs):
    for ip in ipaddress.IPv4Network(ip_address):
        for log in logs:
            if re.search(rf'{str(ip)}\b', log):
                print(log)

def get_ipv4(ip_address, logs):
    for log in logs:
        if ip_address in log:
            print(log)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Get log information about IP address.')
    parser.add_argument('--ip', type=str, required=True, help='IP address to search Ex: --ip \'127.0.0.1\'')
    args = parser.parse_args()

    ip_address = args.ip
    slash = "/"

    #Check for web
    if not os.path.isfile('./weblog_output.txt'):
        get_logs()
    else:
        logs = open_logs()

        if slash in args.ip:
            validate_ip_address(args.ip)
            get_cidr_range(ip_address, logs)
        else:
            validate_ip_address(args.ip)
            get_ipv4(ip_address, logs)
