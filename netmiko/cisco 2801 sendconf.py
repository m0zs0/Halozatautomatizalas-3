from netmiko import ConnectHandler

# Eszköz adatok
device = {
    'host': '192.168.1.1',
    'username': 'admin',
    'password': 'admin',
    'secret': 'cisco',
    'device_type': 'cisco_ios'
}

# Csatlakozás
net_connect = ConnectHandler(**device)

#print(net_connect.send_command("show ip int brief"))
net_connect.enable()

net_connect.send_config_set(["hostname ROUTER2"])

# A start.txt fájl tartalmának beolvasása
with open('start.txt', 'r') as f:
    config_commands = f.readlines()

# Konfiguráció küldése
net_connect.send_config_set(config_commands)

# Végződés
net_connect.send_config_set(['end'])

# Kapcsolat bontása
net_connect.disconnect()