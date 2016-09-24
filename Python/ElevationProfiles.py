import googlemaps
import pandas as pd
import simplejson as sj
import urllib as urllib

carreteras_df = pd.read_csv('Carreteras.csv', encoding='UTF-8', delimiter=',')
carreteras_coord = carreteras_df.st_Y.astype(str).str.cat(carreteras_df.st_X.astype(str), sep=',')
carreteras_coord = carreteras_coord.values.tolist()
elevation_table = {}
elevationArray = []
distance_table = []
distance_table.append(0)
for n in range(len(carreteras_coord)-1):
    if carreteras_coord[n] == carreteras_coord[n+1]:
        print "coordenada repetida"
    else:
        pathStr = carreteras_coord[n] + "|" + carreteras_coord[n+1]
        print pathStr
        origin = carreteras_coord[n]
        destination = carreteras_coord[n+1]
        url_e = "https://maps.googleapis.com/maps/api/elevation/json?path="+pathStr+"&samples=10&key=AIzaSyAh2PIcLDrPecSSR36z2UNubqphdHwIw7M"
        response_e = sj.load(urllib.urlopen(url_e))
        url_d = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="+origin+"&destinations="+destination+"&mode=driving&key=AIzaSyAh2PIcLDrPecSSR36z2UNubqphdHwIw7M"
        response_d = sj.load(urllib.urlopen(url_d))
        distance_table.append(distance_table[n]+ 0.001 * (response_d['rows'][0]['elements'][0]['distance']['value']))
        for resultset in response_e['results']:
            elevationArray.append(resultset['elevation'])

f = open('carreteras_distance.dat', 'w')
f.write(str(distance_table))
f.close()


f = open('carreteras_elevation.dat', 'w')
f.write(str(elevationArray))
f.close()
