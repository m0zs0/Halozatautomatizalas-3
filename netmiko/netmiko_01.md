# Netmiko használata - Laborgyakorlat


## I. Teszt


![Rest config net](../PICTURES/Restconf_net.png)

1. lépés: Telepítsd a Python alá a netmiko könyvtárat
```console
pip install netmiko
```
2. lépés:	Kösd össze az Admin PC-t és a Routert konzol kábellel és készítsd el a preconf-ot!
```console
!preconf
hostname R1
enable secret cisco
ip domain-name moriczref.hu
crypto key generate rsa
1024
username admin secret admin
line vty 0 15
login local
transport input ssh

interface FastEthernet0/0
ip address 192.168.1.1 255.255.255.0
no shutdown
```
3. lépés: hozd létre a sendconf.py állományt:
```py
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
```

4. lépés: Hozd létre a sendconf.txt állományt is
```console
hostname ROUTER_1
interface FastEthernet0/1
ip address 192.168.2.1 255.255.255.0
no shutdown
```

5. lépés:	Futtatsd le a py kódot
6. lépés: Ellenőrízd a Routeren, hogy megtörténtek-e a beállítások

