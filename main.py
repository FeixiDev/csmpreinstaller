#! /usr/bin/env python3

import argparse
from log_record import Logger
from csmpreinstaller import Csmpreinstaller

# 安装 docker
def install_docker(csm):
    csm.modify_fstab_file()
    csm.add_key()
    csm.install_()
    csm.start_docker()

# 安装 Kubernetes 相关软件
def install_kubernetes(csm):
    csm.install_kubernetes()

def display_version():
    print("version: v1.0.0")

def main():
    parser = argparse.ArgumentParser(description='None')
    parser.add_argument('-d', '--install_docker', action='store_true',
                        help='install docker')
    parser.add_argument('-k', '--install_kubernetes', action='store_true',
                        help='install Kubernetes')
    parser.add_argument('-v', '--version', action='store_true',
                        help='Show version information')
    args = parser.parse_args()

    logger = Logger("log")
    csm = Csmpreinstaller(logger)
    
    if args.install_docker:
        install_docker(csm)
    elif args.install_kubernetes:
        install_kubernetes(csm)
    elif args.version:
        display_version()
    else:
        install_docker(csm)
        install_kubernetes(csm)
        
if __name__ == '__main__':
    main()
