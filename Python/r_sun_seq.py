###################################################################
#Comando de inicialización del mapset, desde la consola de comandos de GRASS, remover el símbolo # para ejecutarlos
#Además debe cambiarse la ruta del comando r.in.gdal, ahí se debe colocar el mapa de elevaciones según se encuentre en su computadora
###################################################################
#r.in.gdal input=C:\Users\ARGUELLO-PC\Desktop\ConsultoriaMINAE\GRASS_GIS\BaseGISCostaRica\MED30CR\med30crtm\w001001.adf output=w001001 -o
#g.rename raster=w001001,elevacion
#r.slope.aspect elevation=elevacion slope=pendiente aspect=orientacion





###################################################################
#Comandos desde la consola Python que pueden cambiarse con cada ejecución
###################################################################

#Definiciones de usuario###########################################
start_day=1 #Día inicial del análisis 1  32 60 91  121 152 182 213 244 274 305 335
end_day=31 #Día final del análisis     31 59 90 120 151 181 212 243 273 304 334 365
start_hour=0 #Hora inicial del análisis
end_hour=23 #Hora final del análisis
year=2015
linke_value=5.75 #Valor promedio de la turbidez atmosférica en Costa Rica. OJO PARA CADA MES CAMBIA
albedo_value=0.1 #Valor promedio del albedo en Costa Rica
step=0.5 #Mapea cada media hora, pero acumula cada hora
tipo_consulta='global' #Seleccionar una de las 3 opciones 'global', 'directa', 'difusa'
savepath='C:\Users\ARGUELLO-PC\Desktop\ConsultoriaMINAE\GRASS_GIS\CostaRicaMapsetTest1000x1000\Resultados_mensuales_horarios\\'
coordpath='C:\Users\ARGUELLO-PC\Desktop\ConsultoriaMINAE\GRASS_GIS\CoordenadasMedidas.csv'
x=540108.289999999 #longitud de consulta en crtm05
y=1034401.64 #latitud de consulta en crtm05
####################################################################





###################################################################
#Comandos desde la consola Python que solo se escriben solo una vez
###################################################################

#Inicialización#####################################################
def inicializacion(start_day, end_day, start_hour, end_hour):
	import grass.script.core as gcore #OJO, creo que puede correr sin esto
	import os #OJO, creo que puede correr sin esto
	if(start_day>end_day):
		aux=start_day
		start_day=end_day
		end_day=aux
	if(start_hour>end_hour):
		aux=start_hour
		start_hour=end_hour
		end_hour=aux
	if(start_day<=0):
		start_day=1
	if(end_day>365):
		end_day=365
	if(start_hour<0):
		start_hour=0
	if(end_hour>24):
		end_hour=24		
	return start_day, end_day+1, start_hour, end_hour+1
####################################################################

#Turbidez Atmosférica mensual#######################################
def linke_mes(day):
	if(day>=1 and day<=31):
		linke_value=5.75
		return linke_value
	if(day>=32 and day<=59):
		linke_value=5.75
		return linke_value
	if(day>=60 and day<=90):
		linke_value=6
		return linke_value
	if(day>=91 and day<=120):
		linke_value=6
		return linke_value
	if(day>=121 and day<=151):
		linke_value=6.3
		return linke_value
	if(day>=152 and day<=181):
		linke_value=6.3
		return linke_value
	if(day>=182 and day<=212):
		linke_value=6.3
		return linke_value
	if(day>=213 and day<=243):
		linke_value=6.3
		return linke_value		
	if(day>=244 and day<=273):
		linke_value=6.3
		return linke_value
	if(day>=274 and day<=304):
		linke_value=6.3
		return linke_value		
	if(day>=305 and day<=334):
		linke_value=6
		return linke_value
	if(day>=335 and day<=365):
		linke_value=5.75
		return linke_value	
####################################################################

#Calculadora de mapas de irradiancia################################
def r_sun_AAG(start_day, end_day, start_hour, end_hour, year, albedo_value, step):
	Init=inicializacion(start_day, end_day, start_hour, end_hour)
	start_day=Init[0]
	end_day=Init[1]
	start_hour=Init[2]
	end_hour=Init[3]
	for day in range(start_day, end_day, 1):
		for time in range(start_hour, end_hour, 1):
			suffix=''
			if (time>9):
				if(day>9):
					suffix='_h' + str(time) + '_d' + str(day) + '_a' + str(year)
				else:
					suffix='_h' + str(time) + '_d0' + str(day) + '_a' + str(year)
			else:
				if(day>9):
					suffix='_h0' + str(time) + '_d' + str(day) + '_a' + str(year)
				else:
					suffix='_h0' + str(time) + '_d0' + str(day) + '_a' + str(year)
			params={}
			params.update({'linke_value': linke_mes(day)})
			params.update({'albedo_value': albedo_value})
			params.update({'beam_rad': 'dire_rad' + suffix})
			params.update({'diff_rad': 'difu_rad' + suffix})
			params.update({'glob_rad': 'glob_rad' + suffix})
			grass.run_command('r.sun', elevation='elevacion', aspect='orientacion', slope='pendiente', day=day, time=time, step=step, overwrite=grass.overwrite(), quiet=True, **params)
####################################################################
				
#Consultador de mapas de irradiancia################################
def r_what_AAG(start_day, end_day, start_hour, end_hour, year, tipo_consulta, x, y):
	for day in range(start_day, end_day+1, 1):
		for time in range(start_hour, end_hour+1, 1):
			suffix=''
			if (time>9):
				if(day>9):
					suffix='_h' + str(time) + '_d' + str(day) + '_a' + str(year)
				else:
					suffix='_h' + str(time) + '_d0' + str(day) + '_a' + str(year)
			else:
				if(day>9):
					suffix='_h0' + str(time) + '_d' + str(day) + '_a' + str(year)
				else:
					suffix='_h0' + str(time) + '_d0' + str(day) + '_a' + str(year)
			with open(savepath + tipo_consulta + '_x' + str(x) + '_y' + str(y)+ '.csv', 'a') as csvfile:
				data=str(grass.raster_what(tipo_consulta + suffix, [[x,y]]))+'\n'
				csvfile.write(data)		
####################################################################		

#Ciclo de consulta de mapas#########################################		
def r_what_cicle():
	for i in range(0, len(CoordenadasMedidores) ,1):
		x=float(CoordenadasMedidores[i][0])
		y=float(CoordenadasMedidores[i][1])
		r_what_AAG(start_day, end_day, start_hour, end_hour, year, tipo_consulta, x, y)
###################################################################
		
		
		
		
		
###################################################################
#Comandos desde la consola Python para crear los mapas y consultarlos
###################################################################
								
#Creación de mapas##################################################		
r_sun_AAG(start_day, end_day, start_hour, end_hour, year, albedo_value, step)
####################################################################

#Consulta de mapas##################################################
import csv
import numpy as np
CoordenadasMedidores = np.genfromtxt (coordpath, delimiter=",")
vect_consulta=['global', 'directa', 'difusa']
#inicializacion(start_day, end_day, start_hour, end_hour)
for i in range(0,len(vect_consulta),1):
	tipo_consulta=vect_consulta[i]
	r_what_cicle()
	return tipo_consulta
#end_day=end_day-1
#end_hour=end_hour-1
####################################################################
				