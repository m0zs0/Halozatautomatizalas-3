# Netmiko használata - Laborgyakorlat


## I. Csatlakozás több eszközhöz egymás után (sorosan)

```py
from netmiko import ConnectHandler

# Több eszköz adatai listában
devices = [
    {'host': '192.168.1.1', 'username': 'admin', ...},
    {'host': '192.168.1.2', 'username': 'admin', ...},
    {'host': '192.168.1.3', 'username': 'admin', ...}
]

# Csatlakozás minden eszközhöz
for device in devices:
    net_connect = ConnectHandler(**device)
    output = net_connect.send_command('show version')
    print(output)
    net_connect.disconnect()
```

## II. Csatlakozás több eszközhöz egyszerre (párhuzamosan)

```py
from concurrent.futures import ThreadPoolExecutor
from netmiko import ConnectHandler

# ... (eszközök listája)

def connect_device(device):
    net_connect = ConnectHandler(**device)
    output = net_connect.send_command('show version')
    print(output)
    net_connect.disconnect()

with ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(connect_device, devices)

```

## III. Konfigurációs parancsok küldése
```py
from netmiko import ConnectHandler

# ... (eszköz adatai)

# Csatlakozás
net_connect = ConnectHandler(**device)

# Konfigurációs parancsok küldése
config_commands = [
    'interface GigabitEthernet0/1',
    'ip address 192.168.2.1 255.255.255.0',
    'no shutdown'
]
net_connect.send_config_set(config_commands)

# Kapcsolat lezárása
net_connect.disconnect()

```

## IV. Konfigurációs fájl feltöltése
```py
from netmiko import ConnectHandler

# Eszköz adatai
device = {
    'host': '192.168.1.1',
    'username': 'admin',
    'password': 'password',
    'device_type': 'cisco_ios'
}

# Csatlakozás
net_connect = ConnectHandler(**device)

# Konfigurációs fájl feltöltése
net_connect.send_config_from_file('new_config.txt')

# Kapcsolat lezárása
net_connect.disconnect()

```

## V. Dinamikus konfigurációk Jinja2-vel
```py
from netmiko import ConnectHandler
from jinja2 import Template

# Eszköz adatai
device = {
    # ...
}

# Konfigurációs sablon
template = Template("""
interface GigabitEthernet0/{{ interface_number }}
  ip address {{ ip_address }} 255.255.255.0
  no shutdown
""")

# Változók
variables = {
    'interface_number': '1',
    'ip_address': '192.168.2.1'
}

# Konfiguráció generálása
config_commands = template.render(variables)

# ... (csatlakozás és konfiguráció küldése)

```
Ha a konfigurációkban változó részeket szeretnél kezelni, a Jinja2 templating engine-t használhatod.

## VI. save_config() metódus meghívásával elmentjük a futó konfigurációt az eszköz flash memóriájába
```py
from netmiko import ConnectHandler

# Eszköz adatai
device = {
    'host': '192.168.1.1',
    'username': 'admin',
    'password': 'password',
    'device_type': 'cisco_ios'
}

# Csatlakozás
net_connect = ConnectHandler(**device)

# Konfigurációs módosítások (ha szükségesek)
# ...

# Konfiguráció mentése
net_connect.save_config()

# Kapcsolat lezárása
net_connect.disconnect()
```

## VII. Konfigurációk összehasonlítása
```py
# ... (csatlakozás és konfiguráció módosítása)

# Régi konfiguráció lekérése
old_config = net_connect.send_command('show running-config')

# Új konfiguráció mentése és lekérése
net_connect.save_config()
new_config = net_connect.send_command('show running-config')

# Összehasonlítás (pl. diff eszköz segítségével)
# ...

```

## VIII. A kapott kimenetek feldolgozása reguláris kifejezések segítségével

IP cím kinyerése egy show ip interface brief parancs kimenetéből
```py
import re
from netmiko import ConnectHandler

# Eszköz adatai
device = {
    # ...
}

# Csatlakozás
net_connect = ConnectHandler(**device)

# Parancs végrehajtása és kimenetet tárolása
output = net_connect.send_command('show ip interface brief')

# Reguláris kifejezés az IP címek keresésére
ip_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"

# IP címek kinyerése és kiíratása
ip_addresses = re.findall(ip_regex, output)
print(ip_addresses)

#Interfész állapotának ellenőrzése:

interface_status_regex = r"GigabitEthernet0/1\s+is\s+(\w+)"

#Hibaüzenetek keresése:

error_regex = r"Error: (\w+)"

##Konfigurációs paraméterek értékének kinyerése:

ip_address_regex = r"ip address (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"


```
További lehetőségek:

XML vagy JSON formátum: Egyes eszközök XML vagy JSON formátumban adják vissza a kimenetet. Ezekben az esetekben a megfelelő könyvtárakkal (pl. xml.etree.ElementTree, json) könnyebben elemezhetjük az adatokat.

Hiba kezelés: Kivételek kezelése, hibaüzenetek kezelése.
A Netmiko send_config_set metódusa valóban egy listát ad vissza, amelyben minden elem egy tuple. Ez a tuple két elemből áll:

Parancs: A küldött konfigurációs parancs.
Eredmény: Egy boolean érték, ami True, ha a parancs sikeresen végrehajtódott, vagy False, ha hiba történt.

```py
from netmiko import ConnectHandler

# ... (eszköz adatai)

# Csatlakozás
net_connect = ConnectHandler(**device)

# Konfigurációs parancsok
config_commands = [
    'interface GigabitEthernet0/1',
    'ip address 192.168.2.1 255.255.255.0',
    'no shutdown'
]

# Konfiguráció küldése és hiba kezelés
result = net_connect.send_config_set(config_commands)

# Eredmények kiértékelése
for command, success in result:
    if not success:
        print(f"A következő parancs végrehajtása sikertelen volt: {command}")

# Kapcsolat lezárása
net_connect.disconnect()

```

Részletesebb hibaüzenetek
```py
# ... (előző kód)

for command, success in result:
    if not success:
        output = net_connect.send_command('show errors')
        print(f"A következő parancs végrehajtása sikertelen volt: {command}")
        print(f"Hibaüzenet: {output}")
```

YAML: Konfigurációs fájlok kezeléséhez hasznos.

YAML (YAML Ain't Markup Language) egy emberi olvashatóságot és egyszerűséget szem előtt tartó adatserializálási nyelv. A hálózati eszközök konfigurációinak kezelésében gyakran használják, mivel könnyen szerkeszthető és olvasható konfigurációs fájlokat lehet vele létrehozni.

Miért előnyös a YAML a konfigurációs fájlokhoz?

Olvashatóság: A YAML szintaxisa egyszerű és logikus, így könnyen érthető még bonyolultabb konfigurációk esetén is.

Flexibilitás: Támogatja a különböző adattípusokat (számok, szövegek, listák, szótárak), így sokféle konfigurációt képes reprezentálni.
Szerkeszthetőség: A YAML fájlok egyszerű szövegfájlok, így bármilyen szövegszerkesztővel módosíthatók.
Példa egy YAML konfigurációs fájlra (egy router konfigurációja):

YAML
```yaml
devices:
  router1:
    host: 192.168.1.1
    username: admin
    password: mypassword
    device_type: cisco_ios
    commands:
      - interface GigabitEthernet0/1
      - ip address 192.168.100.1 255.255.255.0
      - no shutdown
  router2:
    # ... hasonló beállítások ...
```
használata
```yaml
import yaml
from netmiko import ConnectHandler

# YAML fájl betöltése
with open('devices.yaml') as f:
    devices = yaml.safe_load(f)

# Csatlakozás az első routerhez és konfiguráció módosítása
for device_name, device_config in devices.items():
    net_connect = ConnectHandler(**device_config)
    net_connect.send_config_set(device_config['commands'])
    net_connect.disconnect()
```

Jinja2: Dinamikus sablonok létrehozásához.

A Jinja2 egy erős, Python alapú sablonmotor, amelyet webfejlesztésben és más területeken is széles körben használnak. Kiválóan alkalmas dinamikus sablonok létrehozására, amelyekkel testreszabható kimeneteket generálhatunk különböző adatok alapján

Miért hasznos a Jinja2 a hálózati automatizálásban?

Dinamikus konfigurációk: A Jinja2 segítségével olyan konfigurációs fájlokat hozhatunk létre, amelyekben változók és vezérlő struktúrák szerepelnek. Ez lehetővé teszi, hogy azonos alapsablonból különböző eszközökhöz testreszabott konfigurációkat generáljunk.

Paraméterezhető szkriptek: A szkripteinket is paraméterezhetjük Jinja2 sablonokkal, így például egyetlen szkriptet használhatunk különböző hálózati eszközök konfigurálására.

Olvashatóság: A Jinja2 szintaxisa egyszerű és logikus, így a sablonok könnyen olvashatók és karbantarthatók.

Példa: Egy router konfigurációjának generálása Jinja2-vel

```yaml
from jinja2 import Template

# Sablon definiálása
template = Template("""
interface GigabitEthernet0/{{ interface_number }}
  ip address {{ ip_address }} 255.255.255.0
  no shutdown
""")

# Adatok megadása
data = {
    'interface_number': '1',
    'ip_address': '192.168.1.100'
}

# Sablon renderelése
output = template.render(data)

print(output)
```

Bonyolultabb példa:
```yaml
YAML
routers:
  - name: router1
    interfaces:
      - name: GigabitEthernet0/1
        ip_address: 192.168.1.100
      - name: GigabitEthernet0/2
        ip_address: 192.168.2.100
  - name: router2
    # ...
```

```yaml
# ... (YAML fájl betöltése)

for router in data['routers']:
    for interface in router['interfaces']:
        template = Template("""
        interface {{ interface['name'] }}
          ip address {{ interface['ip_address'] }} 255.255.255.0
          no shutdown
        """)
        output = template.render(interface=interface)
        print(output)
```


•  Konfigurációk kezelése: Hogyan töltünk fel konfigurációs fájlokat, hogyan módosítunk konfigurációs paramétereket?
•  Kimenetek elemzése: Hogyan elemezzük a kapott kimeneteket, hogyan vonunk le következtetéseket az adatokból?
•  Best practices: Milyen jó gyakorlatokat érdemes követni a hálózatautomatizálás során?

A hálózati automatizálás egyre nagyobb szerepet játszik az IT infrastruktúrák kezelésében. Azonban a hatékony és megbízható automatizáláshoz fontos bizonyos alapelveket és gyakorlatokat követni.

Átfogó tervezés és moduláris felépítés
Világos célok: Határozzuk meg pontosan, hogy mit szeretnénk automatizálni, és milyen problémákat oldunk meg vele.
Moduláris felépítés: Bontsuk fel az automatizálási feladatokat kisebb, önállóan tesztelhető modulokra.
Verziókövetés: Használjunk verziókövető rendszert (pl. Git), hogy nyomon követhessük a változásokat és könnyebben visszaállíthassuk a korábbi állapotokat.
Konfigurációkezelés
YAML vagy JSON: Használjunk emberi olvasható formátumú konfigurációs fájlokat (YAML, JSON).
Változók használata: Paraméterezhetővé tegyük a konfigurációkat változók segítségével.
Templátok: Alkalmazzunk templating motorokat (pl. Jinja2) dinamikus konfigurációk generálásához.
Tesztelés és hibakezelés
Unit tesztek: Írjunk unit teszteket az egyes modulokhoz, hogy biztosítsuk azok helyes működését.
Integrációs tesztek: Végezzünk integrációs teszteket, hogy ellenőrizzük, hogy a modulok együttesen is jól működnek.
Hibakezelés: Implementáljunk megfelelő hibakezelési mechanizmusokat, hogy a hibák ne okozzanak váratlan leállásokat.
Logolás: Rögzítsük az automatizálás során keletkező eseményeket és hibákat log fájlokban.
Biztonság
Hozzáférés-vezérlés: Korlátozzuk az automatizálási szkriptek hozzáférését a hálózati eszközökhöz.
Titkosítás: Tároljuk biztonságosan a jelszavakat és egyéb érzékeny adatokat.
Input validáció: Ellenőrizzük az automatizálási szkriptekbe bevitt adatokat, hogy elkerüljük a rosszindulatú kódok végrehajtását.
Dokumentáció
Részletes dokumentáció: Készítsünk részletes dokumentációt az automatizálási folyamatokról, hogy más fejlesztők is könnyen megértsék és továbbfejleszthessék azokat.
Kommentek: Használjunk kommenteket a kódban, hogy megmagyarázzuk a bonyolultabb részeket.
Eszközök és technológiák
Ansible: Egy egyszerű és hatékony eszköz hálózati automatizáláshoz.
Netmiko: Python könyvtár hálózati eszközökkel való kommunikációhoz.
Paramiko: Python könyvtár SSH protokoll használatához.
Nagios: Hálózati monitorozó eszköz.
További tippek
Kezdj kicsiben: Ne akarjunk mindent egyszerre automatizálni. Kezdjünk egy egyszerű feladattal, majd fokozatosan bővítsük az automatizálási környezetet.
Ismételhetőség: Az automatizálási folyamatoknak reprodukálhatónak kell lenniük.
Folyamatos fejlesztés: Az automatizálási rendszereket folyamatosan fejleszteni kell, hogy lépést tartsanak a változó követelményekkel.
Összefoglalva: A hálózati automatizálás hatékony és megbízható végrehajtásához fontos a tervezés, a moduláris felépítés, a tesztelés, a biztonság és a dokumentáció. A megfelelő eszközök és technológiák kiválasztásával jelentősen egyszerűsíthetjük az automatizálási feladatokat.

