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
```console
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
login local
transport input ssh
```
5. lépés:	Állítsd be a RESTConf használatát
```console
ip http secure-server
restconf
```
6. lépés:	Kösd össze a Client PC-t a Router0-val, a GigabitEthernet0/0/0 porton egy Switch-en keresztül
7. lépés:	Állítsd be a Client PC IP címét 192.168.1.10/24-re, és az átjárót is.

## II. Adatlekérdezés a Routertől
1. lépés:	Nyisd meg a `Visual Studio Code`-ot, majd annak `Thunder Client` bűvítményét! Hozz létre egy `New Request`-et! 
2. lépés:	A kérés típusánál válaszd a `GET`-et, majd a mezőbe írd be: 
```
https://192.168.1.1/restconf/data/ietf-interfaces:interfaces
```
3. lépés:	Az URL mező alatti `Auth` tab-on válaszd `Basic`-et, majd írd be a felhasználónevet és a jelszót! (admin, cisco123!)
4. lépés:	Ezután válaszd a `Headers` tab-ot! Adj meg egy kulcsot `Content-Type` névvel, és `application/yang-data+json` értékkel, illetve egy `Accept` kulcsot szintén `application/yang-data+json` értékkel.
5. lépés:	A `Send` gombra kattintva az alábbi eredményt -*Response*- látod: 
```
{
    "ietf-interfaces:interface": {
          "name": "GigabitEthernet0",
		    "enabled": true,
          "ietf-ip:ipv4": {
            "address": [
                "ip": "192.168.1.1",
                "netmask": "255.255.255.0"
            ]
          },
        {
          "name": "GigagbitEthernet1",
          "enabled": false
        }
}
```

## III. Konfigurációmódosítás a Routeren
1. lépés:	Hozz létre egy `New Request`-et! Ezúttal a `PUT` kérést válaszd, majd a mezőbe írd be a következő sort: 
```
https://192.168.1.1/restconf/data/ietf-interfaces:interfaces
```
2. lépés:	Az URL mező alatti `Auth` tab-on válaszd `Basic`-et, majd írd be a felhasználónevet és a jelszót! (admin, cisco123!)
3. lépés:	Ezután válaszd a `Headers` tab-ot! Adj meg egy kulcsot `Content-Type` névvel, és `application/yang-data+json` értékkel, illetve egy `Accept` kulcsot szintén `application/yang-data+json` értékkel.
4. lépés:	Válaszd ki a `Body/JSON` tab-ot! Másold be ide az előbbi kérésnél kapott *Response* tartalmat! 
5. lépés:	Módosítsd a kódot úgy, hogy a `GigabitEthernet0/0/1` interfészének az `enable` értékét `true`-ra állítod, valamint beállítod az interface IP címét `192.168.2.1/24`-re.
6. lépés:	Kattints a `Send` gombra!
7. lépés:	Ellenőrzés: A `GET`-el és/vagy az Admin PC-vel ellenőrizd le, hogy sikeres volt-e a konfiguráció!
```
{
    "ietf-interfaces:interface": {
          "name": "GigabitEthernet0",
		    "enabled": true,
          "ietf-ip:ipv4": {
            "address": [
                "ip": "192.168.1.1",
                "netmask": "255.255.255.0"
            ]
          },
        { 
          "name": "GigabitEthernet1",
		    "enabled": true,
          "ietf-ip:ipv4": {
            "address": [
                "ip": "192.168.2.1",
                "netmask": "255.255.255.0"
            ]
        }
}
```
