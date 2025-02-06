# RESTconf használata 2 - Laborgyakorlat

## 0. API dokumentáció: 

https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/prog/configuration/166/b_166_programmability_cg/restconf_prog_int.pdf

## 1. Hostname lekérdezése

```console
GET
https://192.168.1.1/restconf/data/Cisco-IOS-XE-native:native/hostname
Auth/Basic/Username: "admin"
Auth/Basic/Password: "cisco123!"
Headers/Content-Type: "application/yang-data+json"
Headers/Accept: "application/yang-data+json"
```

## 2. Hostname beállítása
```console
PUT
https://192.168.1.1/restconf/data/Cisco-IOS-XE-native:native/hostname
Auth/Basic/Username: "admin"
Auth/Basic/Password: "cisco123!"
Headers/Content-Type: "application/yang-data+json"
Headers/Accept: "application/yang-data+json"
Body/JSON:
{
    "Cisco-IOS-XE-native:hostname": "NewRouterName"
}
```

## 3. GigabitEthernet 0/0/0 IP címzésének lekérdezése
```console
GET
https://192.168.1.1/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet0%2F0%2F0
Auth/Basic/Username: "admin"
Auth/Basic/Password: "cisco123!"
Headers/Content-Type: "application/yang-data+json"
Headers/Accept: "application/yang-data+json"
```

## 4. GigabitEthernet 0/0/0 felkapcsolási állapotának lekérdezése
```console
GET
https://192.168.1.1/restconf/data/ietf-interfaces:interfaces-state/interface=GigabitEthernet0%2F0%2F0
Auth/Basic/Username: "admin"
Auth/Basic/Password: "cisco123!"
Headers/Content-Type: "application/yang-data+json"
Headers/Accept: "application/yang-data+json"
```

## 5. GigabitEthernet 0/0/0 IP címzése és felkapcsolása
```console
PUT
https://192.168.1.1/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet0/0/0
Auth/Basic/Username: "admin"
Auth/Basic/Password: "cisco123!"
Headers/Content-Type: "application/yang-data+json"
Headers/Accept: "application/yang-data+json"
Body/JSON:
{
    "ietf-interfaces:interface": {
        "name": "GigabitEthernet0/0/0",
        "enabled": true,
        "ietf-ip:ipv4": {
            "address": [
                {
                    "ip": "192.168.1.1",
                    "netmask": "255.255.255.0"
                }
            ]
        }
    }
}
```

## 6. Banner lekérdezése
```console
GET
https://192.168.1.1/restconf/data/Cisco-IOS-XE-native:native/banner/motd
Auth/Basic/Username: "admin"
Auth/Basic/Password: "cisco123!"
Headers/Content-Type: "application/yang-data+json"
Headers/Accept: "application/yang-data+json"
```

## 7. Banner beállítása
```console
PUT
https://192.168.1.1/restconf/data/Cisco-IOS-XE-native:native/banner/motd
Auth/Basic/Username: "admin"
Auth/Basic/Password: "cisco123!"
Headers/Content-Type: "application/yang-data+json"
Headers/Accept: "application/yang-data+json"
Body/JSON:
{
    "Cisco-IOS-XE-native:banner": {
        "login": {
            "banner": "#Welcome to the router!#"
        }
    }
}
```

## 8. Jelszavak lekérdezése
```console
GET
https://192.168.1.1/restconf/data/Cisco-IOS-XE-native:native/username
Auth/Basic/Username: "admin"
Auth/Basic/Password: "cisco123!"
Headers/Content-Type: "application/yang-data+json"
Headers/Accept: "application/yang-data+json"
```

## 9. Jelszavak beállítása
```console
PUT
https://192.168.1.1/restconf/data/Cisco-IOS-XE-native:native/username
Auth/Basic/Username: "admin"
Auth/Basic/Password: "cisco123!"
Headers/Content-Type: "application/yang-data+json"
Headers/Accept: "application/yang-data+json"
Body/JSON:
{
    "Cisco-IOS-XE-native:username": [
        {
            "name": "admin",
            "privilege": 15,
            "password": {
                "password": "newpassword"
            }
        }
    ]
}
```
