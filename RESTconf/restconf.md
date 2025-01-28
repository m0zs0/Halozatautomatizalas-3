# RESTconf használata - Laborgyakorlat


## I. Hálózat kialakítása

**Fontos**: A RESTConf használatához szükséges, hogy a router IOS-XE verziója legalább 16.6 legyen (Alkalmas routerek: Cisco ISR4221 vagy ISR4321 router)!

![Rest config net](../PICTURES/Restconf_net.png)

1. lépés:	Kösd össze az Admin PC-t és a Routert konzol kábellel!
2. lépés:	Ellenőrízd a IOS-XE verziószámát:
```console
show version
```
3. lépés:	Állítsd be az alap IP konfigurációt
```bash
interface GigabitEthernet0/0/0
ip address 192.168.1.1 255.255.255.0 
no shutdown
```
4. lépés:	Állítsd be az SSH-t (a felhasználó neve cisco, jelszava cisco123! legyen)
```console
username admin privilege 15 secret cisco123! 
ip domain-name moriczref.hu 
crypto key generate rsa general-keys modulus 1024 
ip ssh version 2 
line vty 0 4 
login local transport input ssh
```
5. lépés:	Állítsd be a RESTConf használatát
