# Générateur de certificat de déplacement

## Développer

### Installer le projet

```console
git clone https://github.com/ataumo/genattest.git
```

#### Installation des paquets necessaires :
```console
pip3 install pdfrw
pip3 install reportlab
pip3 install datetime
pip3 install getopt
```

## Initialiser

Completer les informations du fichier ``genattest.py``

### Completer les informations
```
firstname="Emmanuel"
lastname="Macron"
birthday="09/05/1972"
placeofbirth="Paris"
address="20 rue du Caire"
zipcode="75666"
city="Paris"
ccity="Paris"
```

### Générer l'attestation 

```
python3 genattest.py
```

## Utilisation

`option` : raison

`-t` : "Déplacements entre le domicile et le lieu d’exercice de l’activité professionnelle ou un établissement d’enseignement ou de formation, déplacements professionnels ne pouvant être différés, déplacements pour un concours ou un examen."

`-a` : "Déplacements pour effectuer des achats de fournitures nécessaires à l'activité professionnelle, des achats de première nécessité3 dans des établissements dont les activités demeurent autorisées, le retrait de commande et les livraisons à domicile."

`-s` : "Déplacements brefs, dans la limite d'une heure quotidienne et dans un rayon maximal d’un kilomètre autour du domicile,  liés à l’activité physique individuelle des personnes, à l’exclusion de toute pratique sportive collective et de toute proximité avec d’autres personnes, soit à la promenade avec les seules personnes regroupées dans un même domicile, soit aux besoins des animaux de compagnie."

```
python3 genattest.py -t
```
