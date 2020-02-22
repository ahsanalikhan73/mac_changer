#!/usr/bin/env python
import subprocess
import argparse
import re
from colorama import init, Fore		# for fancy/colorful display

class MAC_Changer:
    def __init__(self):
        # initialize colorama
        init()
        # define colors
        self.GREEN = Fore.GREEN
        self.RED = Fore.RED
        self.Cyan = Fore.CYAN
        self.Yellow = Fore.YELLOW
        self.Blue = Fore.BLUE
        self.RESET = Fore.RESET

    def arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', '--interface', dest='interface', help='Interface to change its MAC Address')
        parser.add_argument('-m', '--mac', dest='new_mac', help='New MAC Address')
        values = parser.parse_args()
        if not values.interface:
            parser.error('\n{}[-] Please Specify The Interface {}'.format(self.Cyan, self.RESET))
        if not values.new_mac:
            parser.error('\n{}[-] Please Specify The New MAC Address {}'.format(self.Yellow, self.RESET))
        return values

    def change_mac(self, interface, mac):
        print('\n\t{}[+] Changing MAC Address ...{}'.format(self.Blue, self.RESET))
        subprocess.call(['ifconfig', interface, 'down'])
        subprocess.call(['ifconfig', interface, 'hw', 'ether', mac])
        subprocess.call(['ifconfig', interface, 'up'])

    def get_mac(self, interface):
        output = subprocess.check_output(['ifconfig', interface])
        current_mac = re.search('\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', output)
        if current_mac:     # Because lo interface in linux doesn't have a MAC address
            return current_mac.group(0)
        else:
            print('\n\t{}[-] Could Not Read MAC Address {}'.format(self.RED, self.RESET))

    def start(self):
        option = self.arguments()
        subprocess.call(['clear'])

        print('{}\n\n\t\t\t\t\t\t#########################################################{}'.format(self.Cyan, self.RESET))
        print('\n{}\t\t\t\t\t\t#\t           M A C Address Changer\t\t#\n{}'.format(self.Cyan, self.RESET))
        print('{}\t\t\t\t\t\t#########################################################{}\n\n'.format(self.Cyan, self.RESET))

        print('\n\n[+] MAC Spoofing ...')
        current_MAC = self.get_mac(option.interface)
        print('\n\n\t{}Current MAC : '.format(self.Yellow) + str(current_MAC) + '{}'.format(self.RESET))
        self.change_mac(option.interface, option.new_mac)    # Changing MAC Address
        current_MAC = self.get_mac(option.interface)         # updata the variable
        if current_MAC == option.new_mac:
            print('\n\t{}[+] MAC Address Successfully Changed To '.format(self.GREEN) + str(current_MAC) + '{}\n\n'.format(self.RESET))
        else:
            print('\n\t{}[-] MAC Address Did Not Get Changed ...{}\n'.format(self.RED, self.RESET))

if __name__ == "__main__":
    mac = MAC_Changer()
    mac.start()