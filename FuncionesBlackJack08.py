import random
import sqlite3

#---------------------------------------------------------------------------------------------
# estoy dejando esta info aca para poder hacer pruebas
palosbaraja=["C","D","E","T"]
numeracionbaraja=['01','02','03','04','05','06','07','08','09','10','11','12','13']
numerodebarajas=2
listacartas=[]
for a in range(numerodebarajas):
    for palo in palosbaraja:
        for numeracion in numeracionbaraja:
            listacartas.append(str(a)+palo+str(numeracion))

listacartasbarajadas=[]
for a in range(numerodebarajas*4*len(numeracionbaraja)):
    carta=random.choice(listacartas)
    listacartasbarajadas.append(carta[1:4])
    listacartas.remove(carta)
#print(listacartasbarajadas)

#---------------------------------------------------------------------------------------------

def valorprimeracarta(listacartas):
    if listacartas[0][1:3] == '01':
        return '01'
    elif listacartas[0][1:3] == '11' or listacartas[0][1:3] == '12' or listacartas[0][1:3] == '13':
        return '10'
    else:
        return listacartas[0][1:3]

def valorsegundacarta(listacartas):
    if listacartas[1][1:3] == '01':
        return '01'
    elif listacartas[1][1:3] == '11' or listacartas[0][1:3] == '12' or listacartas[0][1:3] == '13':
        return '10'
    else:
        return listacartas[1][1:3]

#lista=["C11","C01","T13"]
#print(valorprimeracarta(lista))

def cuentaases(cartas): # cuenta la cantidad de ases en las cartas de alguien
    numerodeases=0
    for carta in cartas:
        if carta[1:3]=="01":
            numerodeases=numerodeases+1
    return numerodeases

def valormano(cartas):
    suma=0
    for carta in cartas:
        if carta[1:3]=='11' or carta[1:3]=='12' or carta[1:3]=='13':
            valorcarta=10
        else:
            valorcarta=int(carta[1:3])
        suma=suma+valorcarta
    a=suma
    b=suma
    numerodeases=0
    for carta in cartas:
        if carta[1:3]=="01":
            numerodeases=numerodeases+1
    if numerodeases>=1:
        b=b+10
    if a>21 and b>21:
        return a
    if a<=21 and b>21:
        return a
    if a<= 21 and b<=21:
        return max(a,b)

# dice si el juego de cartas es soft (hay as que si pides y vuelas puede pasar a ser 1) 
# o hard (hard es cuando no hay un as siendo 11 que pueden pasar a valer uno)
# calcular el valor minimo con as como 1, si es diferente al valor mano, el set de cartas es soft
def tipodemano(cartasjugador):
    tipodemano="H"
    suma=0
    for carta in cartasjugador:
        if carta[1:3]=="11" or carta[1:3]=="12" or carta[1:3]=="13":
            suma=suma + 10
        else:
            suma = suma + int(carta[1:3])
    if suma != valormano(cartasjugador):
        tipodemano="S"
    return tipodemano

# listacartasbarajadas, es una lista con todas las cartas que se han barajado, y el numerodecartasusadasbarajas, dice cuantas
# de esas cartas ya se han usado
def valorcountbaraja(listacartasbarajadas,numerodecartasusadasbaraja):
    valorcuenta=0
    for a in listacartasbarajadas[:numerodecartasusadasbaraja]:
        if int(a[1:3])==1 or int(a[1:3])>=10:
            valorcuenta=valorcuenta-1
        elif int(a[1:3])<=6:
            valorcuenta=valorcuenta+1
        else:
            pass
    return valorcuenta

# probabilidad de ganar si me planto
# es la probabilidad que el dealer quede por debajo del valor mano del jugador 1 mas la probabilidad que el dealer vuele
def probganarjugadormeplantov1(listacartasjugador,listacartasdealer,oddsdealer):
    probganarjugador=0
    probempatarjugador=0
    manojugador=valormano(listacartasjugador)
    for a,b in oddsdealer.items():
        if int(a[0])==int(listacartasdealer[0][1:3]):
            if a[1]=='>=22':
                probganarjugador=probganarjugador+float(b)
            elif int(a[1])<manojugador:
                probganarjugador=probganarjugador+float(b)
            elif int(a[1])==manojugador:
                probempatarjugador=probempatarjugador+float(b)
    probperderjugador=1-probganarjugador-probempatarjugador
    return ["{:.2f}".format(probganarjugador),"{:.2f}".format(probempatarjugador),"{:.2f}".format(probperderjugador)]

# probabilidad de ganar si pido una carta
# en la suma de probabilidades, multiplicacion de probabilidades en cada mano que pueda sacar el jugador 1
# por las probabilidades que el dealer quede por debajo del valor de esa mano mas la probabilida que el dealer vuele
# ejm: prob que la mano del jugador llegue a 15 x ( probdelaer menos de 15 mas prob dealer vuele)
#toma en cuenta la mano inicial del jugador1, y la primera carta del jugador 2
def probganarjugadorpidecartav1(oddsjugador,listacartasdealer,oddsdealer):
    probganarjugador=0
    probempatarjugador=0
    for a,b in oddsjugador.items():
        if a[2] != ">=22":
            for c,d in oddsdealer.items():
                if int(c[0])==int(listacartasdealer[0][1:3]):
                    try:
                        if c[1]=='>=22':
                            probganarjugador=probganarjugador+float(b)*float(d)
                        elif int(c[1])<int(a[2]):
                            probganarjugador=probganarjugador+float(b)*float(d)
                        elif int(c[1])==int(a[2]):
                            probempatarjugador=probempatarjugador+float(b)*float(d)
                    except:
                        pass
    probperderjugador=1-probganarjugador-probempatarjugador
    return ["{:.2f}".format(probganarjugador),"{:.2f}".format(probempatarjugador),"{:.2f}".format(probperderjugador)]


def oddsdealer(listacartasdealer,listacartasbarajadas,numerodecartasusadasbaraja,cantidadsimulaciones):
    resultadosdealer=dict()
    for a in ['C01','C02','C03','C04','C05','C06','C07','C08','C09','C10','C11','C12','C13']:
        listacartasdealer[0]=a     
        for a in range(cantidadsimulaciones):   
            listacartasdealer=[listacartasdealer[0]]
            listacartasxrepartir=[]
            for a in listacartasbarajadas[numerodecartasusadasbaraja:]:
                listacartasxrepartir.append(a)
            manodealer=valormano(listacartasdealer)
            while manodealer <17:
                cartarepartida=random.choice(listacartasxrepartir)
                listacartasdealer.append(cartarepartida)
                manodealer=valormano(listacartasdealer)
                listacartasxrepartir.remove(cartarepartida)    
            if manodealer>21:
                manodealer=">=22"
            resultadosdealer[(listacartasdealer[0][1:3],str(manodealer))]=resultadosdealer.get((listacartasdealer[0][1:3],str(manodealer)),0)+1    
    for mano in resultadosdealer:
            resultadosdealer[mano]="{:.4f}".format(float(resultadosdealer.get(mano,0)/cantidadsimulaciones))
    listaresultadosdealer=[]
    for a,b in resultadosdealer.items():
        listaresultadosdealer.append((a,b))
    listaresultadosdealer.sort()

    # devuelve el diccionario despues de pasar por la lista l que se puede ordenar y se arma el diccionario de nuevo
    #print('Cantidad de Simulaciones por carta: '+str(cantidadsimulacionesdealer))
    oddsdealer=dict()
    for a,b in listaresultadosdealer:
        oddsdealer[a]=b
    return oddsdealer


# si es menos de 12 no se tiene que simular ya que si o si se debe pedir
listacartasjugadorsimulacioneshard=[['C10','C02'],['C10','C03'],['C10','C04'],['C10','C05'],['C10','C06'],['C10','C07'],['C10','C08'],['C10','C09'],['C10','C10']]
listacartasjugadorsimulacionessoft=[['C01','C02'],['C01','C03'],['C01','C04'],['C01','C05'],['C01','C06'],['C01','C07'],['C01','C08'],['C01','C09'],['C01','C10'],['C01','C01']]
#print(listacartasjugadorsimulacionessoft+listacartasjugadorsimulacioneshard)

def oddsjugador(listacartasjugador,listacartasbarajadas,numerodecartasusadasbaraja,cantidadsimulaciones):
# el segundo dato del key es la cantidad e ases para determinar si es hard, sin as, o soft  con as
    valormanoinicialjugador=valormano(listacartasjugador)
    resultadosjugador=dict()        
    for a in range(cantidadsimulaciones):                
        listacartasjugadorcopia=listacartasjugador.copy()
        #print(listacartasjugadorcopia)
        listacartasxrepartir=[]
        for a in listacartasbarajadas[numerodecartasusadasbaraja:]:
            listacartasxrepartir.append(a)
        
        cartarepartida=random.choice(listacartasxrepartir)
        listacartasjugadorcopia.append(cartarepartida)
        manojugador=valormano(listacartasjugadorcopia)
        #manojugador=valormanoinicialjugador+int(cartarepartida[1:3])
        listacartasxrepartir.remove(cartarepartida)   
        
        if manojugador>21:
                manojugador=">=22" 
        
        resultadosjugador[(str(valormanoinicialjugador),str(cuentaases(listacartasjugador)),str(manojugador))]=resultadosjugador.get((str(valormanoinicialjugador),str(cuentaases(listacartasjugador)),str(manojugador)),0)+1
    
    for mano in resultadosjugador:
            resultadosjugador[mano]="{:.4f}".format(float(resultadosjugador.get(mano,0)/cantidadsimulaciones))
    listaresultadosjugador=[]
    for a,b in resultadosjugador.items():
        listaresultadosjugador.append((a,b))
    listaresultadosjugador.sort()
    # devuelve el diccionario despues de pasar por la lista l que se puede ordenar y se arma el diccionario de nuevo
    #print('Cantidad de Simulaciones por carta: '+str(cantidadsimulacionesdealer))
    oddsjugador=dict()
    for a,b in listaresultadosjugador:
        oddsjugador[a]=b
    #print(dictordenadoresultadosjugador)
    return oddsjugador

#print(oddsjugador(['C02','C01'],listacartasbarajadas.copy(),0,1000))

# probabilidad de ganar si me planto
# es la probabilidad que el dealer quede por debajo del valor mano del jugador 1 mas la probabilidad que el dealer vuele
def probganarjugadormeplantov2(listacartasjugador,listacartasdealer,listacartasbarajadas,numerodecartasusadasbaraja,cantidadsimulaciones):
    oddsdealerinterno=oddsdealer(listacartasdealer.copy(),listacartasbarajadas.copy(),numerodecartasusadasbaraja,cantidadsimulaciones)
    probganarjugador=0
    probempatarjugador=0
    manojugador=valormano(listacartasjugador)
    for a,b in oddsdealerinterno.items():
        if int(a[0])==int(listacartasdealer[0][1:3]):
            if a[1]=='>=22':
                probganarjugador=probganarjugador+float(b)
            elif int(a[1])<manojugador:
                probganarjugador=probganarjugador+float(b)
            elif int(a[1])==manojugador:
                probempatarjugador=probempatarjugador+float(b)
    probperderjugador=1-probganarjugador-probempatarjugador
    return ["{:.2f}".format(probganarjugador),"{:.2f}".format(probempatarjugador),"{:.2f}".format(probperderjugador)]

# probabilidad de ganar si pido una carta
# en la suma de probabilidades, multiplicacion de probabilidades en cada mano que pueda sacar el jugador 1
# por las probabilidades que el dealer quede por debajo del valor de esa mano mas la probabilida que el dealer vuele
# ejm: prob que la mano del jugador llegue a 15 x ( probdelaer menos de 15 mas prob dealer vuele)
#toma en cuenta la mano inicial del jugador1, y la primera carta del jugador 2
def probganarjugadorpidecartav2(listacartasjugador,listacartasdealer,listacartasbarajadas,numerodecartasusadasbaraja,cantidadsimulaciones):
    oddsdealerinterno=oddsdealer(listacartasdealer.copy(),listacartasbarajadas.copy(),numerodecartasusadasbaraja,cantidadsimulaciones)
    oddsjugadorinterno=oddsjugador(listacartasjugador.copy(),listacartasbarajadas.copy(),numerodecartasusadasbaraja,cantidadsimulaciones)
    probganarjugador=0
    probempatarjugador=0
    for a,b in oddsjugadorinterno.items():
        if a[2] != ">=22":
            for c,d in oddsdealerinterno.items():
                if int(c[0])==int(listacartasdealer[0][1:3]):
                    try:
                        if c[1]=='>=22':
                            probganarjugador=probganarjugador+float(b)*float(d)
                        elif int(c[1])<int(a[2]):
                            probganarjugador=probganarjugador+float(b)*float(d)
                        elif int(c[1])==int(a[2]):
                            probempatarjugador=probempatarjugador+float(b)*float(d)
                    except:
                        pass
    probperderjugador=1-probganarjugador-probempatarjugador
    return ["{:.2f}".format(probganarjugador),"{:.2f}".format(probempatarjugador),"{:.2f}".format(probperderjugador)]


# hay que darle el input del truecount, debe ser un entero que haya sido truncado 
# considero dos barajas por que el true count es por baraja, y yo cada vez que el count aumenta en 1, le estoy
# aplicando un append y un remove a cada grupo de cartas (altas y bajas) y esto hace que la diferencia sea de 2 por 2 barajas
# equivalente a una true count por una baraja. Esto lo he hecho para evitar el problema de cuando el true count
# es impar, por ejemplo uno, y al agregar un tipo de carta (alta o baja) el maso queda no con 52 sino con 53 cartas y eso
# puede distorsionar los calculos
# maximo input para esta funcion es +-40, en donde solo quedan ya sea las cartas altas o las bajas mas las 12=3*4 cartas medias
def listadecartascontruecount(truecount):
# true count debe ser un entero truncado de la division entre el count y el numero de barajas que faltan repartir
    palosbaraja=["C","D","E","T"]
    numeracionbaraja=['01','02','03','04','05','06','07','08','09','10','11','12','13']
    numerodebarajas=2
    listacartas=[]
    for a in range(numerodebarajas):
        for palo in palosbaraja:
            for numeracion in numeracionbaraja:
                listacartas.append(palo+str(numeracion))
    listacartasbajas=['C02','C03','C04','C05','C06','D02','D03','D04','D05','D06','E02','E03','E04','E05','E06','T02','T03','T04','T05','T06','C02','C03','C04','C05','C06','D02','D03','D04','D05','D06','E02','E03','E04','E05','E06','T02','T03','T04','T05','T06']
    listacartasaltas=['C10','C11','C12','C13','C01','D10','D11','D12','D13','D01','E10','E11','E12','E13','E01','T10','T11','T12','T13','T01','C10','C11','C12','C13','C01','D10','D11','D12','D13','D01','E10','E11','E12','E13','E01','T10','T11','T12','T13','T01']
    #print(listacartas)
    if truecount==0:
        pass
    elif truecount>0:
        for a in range(abs(truecount)):
            cartabaja=random.choice(listacartasbajas)
            cartaalta=random.choice(listacartasaltas)
            listacartas.append(cartaalta)
            listacartas.remove(cartabaja)
            listacartasbajas.remove(cartabaja)
    elif truecount<0:
        for a in range(abs(truecount)):
            cartabaja=random.choice(listacartasbajas)
            cartaalta=random.choice(listacartasaltas)
            listacartas.append(cartabaja)
            listacartas.remove(cartaalta)
            listacartasaltas.remove(cartaalta)
    return listacartas


# calcula las probabilidades y ganancia esperada de plantarse y de pedir una carta
# TrueCount, cartainicial jugador (si se saca de la base va a ser un numero en string), numero de ases jugador1
# y Cartainicial del dealer. Con eso debemos obtener la prob de ganar si me planto , prob de empatar si me planto, y prob de perder si me planto
def probabilidadescartas(TrueCountdef,ValorInicialJugadordef,TipoManodef,ValorInicialDealerdef):
# la carta inicial del dealer es el numero de la carta del dealer, por ejemplo '13' es la K, '11' es la J, y '01' es as
    conndealer=sqlite3.connect('simulacionesdealer01.db')
    cdealer = conndealer.cursor()
    cdealer.execute("SELECT * FROM oddsdealer WHERE TrueCount=:TrueCount AND CartaInicial=:CartaInicial",{'TrueCount':TrueCountdef,'CartaInicial':ValorInicialDealerdef})
    lencdealer=(len(cdealer.fetchall()))
    cdealer.execute("SELECT * FROM oddsdealer WHERE TrueCount=:TrueCount AND CartaInicial=:CartaInicial",{'TrueCount':TrueCountdef,'CartaInicial':ValorInicialDealerdef})
    oddsdealerbase=cdealer.fetchall()
    conndealer.close()


    connjugador=sqlite3.connect('simulacionesjugador02.db')
    cjugador = connjugador.cursor()
    cjugador.execute("SELECT * FROM oddsjugador WHERE TrueCount=:TrueCount AND CartaInicial=:CartaInicial AND TipoMano=:TipoMano",{'TrueCount':TrueCountdef,'CartaInicial':ValorInicialJugadordef,'TipoMano':TipoManodef})
    lencjugador=(len(cjugador.fetchall()))
    cjugador.execute("SELECT * FROM oddsjugador WHERE TrueCount=:TrueCount AND CartaInicial=:CartaInicial AND TipoMano=:TipoMano",{'TrueCount':TrueCountdef,'CartaInicial':ValorInicialJugadordef,'TipoMano':TipoManodef})
    oddsjugadorbase=cjugador.fetchall()
    connjugador.close()

    manojugador=int(ValorInicialJugadordef)
    # calcula las probabilidades de plantarse
    probganarjugadormeplanto=0
    probempatarjugadormeplanto=0
    for a in oddsdealerbase:
        if a[2]==">=22":
            probganarjugadormeplanto=probganarjugadormeplanto+float(a[3])
        elif int(a[2])<manojugador:
            probganarjugadormeplanto=probganarjugadormeplanto+float(a[3])
        elif int(a[2])==manojugador:
            probempatarjugadormeplanto=probempatarjugadormeplanto+float(a[3])
    probperderjugadormeplanto=1-probganarjugadormeplanto-probempatarjugadormeplanto
    gananciaesperadameplanto=probganarjugadormeplanto*1+probempatarjugadormeplanto*0+probperderjugadormeplanto*-1
    

    # calcula las probabilidades de sacar una carta mas
    probganarjugadorpidecarta=0
    probempatarjugadorpidecarta=0

    for j in oddsjugadorbase:
        if j[3] != '>=22':
            for d in oddsdealerbase:
                if d[2]==">=22":
                    probganarjugadorpidecarta=probganarjugadorpidecarta+float(j[4])*float(d[3])
                elif int(d[2])<int(j[3]):
                    probganarjugadorpidecarta=probganarjugadorpidecarta+float(j[4])*float(d[3])
                elif int(d[2])==int(j[3]):
                    probempatarjugadorpidecarta=probempatarjugadorpidecarta+float(j[4])*float(d[3])

    probperderjugadorpidecarta=1-probganarjugadorpidecarta-probempatarjugadorpidecarta
    gananciaesperadapidecarta=probganarjugadorpidecarta*1+probempatarjugadorpidecarta*0+probperderjugadorpidecarta*-1

    resultadosmeplanto=["{:.2f}".format(probganarjugadormeplanto),"{:.2f}".format(probempatarjugadormeplanto),"{:.2f}".format(probperderjugadormeplanto),"{:.2f}".format(gananciaesperadameplanto)]
    resultadospidecarta=["{:.2f}".format(probganarjugadorpidecarta),"{:.2f}".format(probempatarjugadorpidecarta),"{:.2f}".format(probperderjugadorpidecarta),"{:.2f}".format(gananciaesperadapidecarta)]
    decision="PEDIR CARTA"
    
    if gananciaesperadameplanto>gananciaesperadapidecarta:
        decision="ME PLANTO"

    if lencdealer==0 or lencjugador==0:
        return ["No se Encontró Data Suficiente","",""]
    else:
        return [resultadosmeplanto,resultadospidecarta,decision]

    #print(oddsjugadorbase)
    #print(oddsdealerbase)
  
#probabilidadescartas('0','12','0','06')
#print(probabilidadescartas('0','17',"S",'11'))

def barajarcartas(numerodebarajas):
    
    palosbaraja = ["C", "D", "E", "T"]
    numeracionbaraja = ['01', '02', '03', '04', '05', '06', '07', '08',
                        '09', '10', '11', '12', '13']
    # numeracionbaraja=['01','04','06']

    listacartas = []
    for a in range(numerodebarajas):
        for palo in palosbaraja:
            for numeracion in numeracionbaraja:
                listacartas.append(str(a)+palo+str(numeracion))

    listacartasbarajadas = []
    for a in range(numerodebarajas*4*len(numeracionbaraja)):
        carta = random.choice(listacartas)
        listacartasbarajadas.append(carta[1:4])
        listacartas.remove(carta)

    return listacartasbarajadas


    
