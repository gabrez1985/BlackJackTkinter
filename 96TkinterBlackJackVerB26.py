from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import tkinter.font as font
import random
from FuncionesBlackJack08 import *
import sqlite3
import math
import time

root = Tk()
root.title(" BlackJack")
root.iconbitmap("IconoBlackJack32.ico")
root.geometry("900x600")
root.config(background="green")

FramePuntajes=LabelFrame(root, text="",padx=0, pady=0,bg="green")
FramePuntajes.pack(fill='both')

FrameCartasJuego=LabelFrame(root, text="",padx=0, pady=0,bg="green")
FrameCartasJuego.pack(fill='both')

FrameBotonesJuego=LabelFrame(root, text="",padx=5, pady=5,bg="green")
FrameBotonesJuego.pack(fill="both", padx=0, pady=0,expand=True)

FrameStatusBar=LabelFrame(root,text="")
FrameStatusBar.pack(fill='both')

statusestadisticas='NO'

def HabilitarEstadisticas():
    global LabelTipDerecha
    global HabilitarEstadisticasBoton
    global DeshabilitarEstadisticasBoton
    global statusestadisticas
    HabilitarEstadisticasBoton['state']=DISABLED
    DeshabilitarEstadisticasBoton['state']=NORMAL
    LabelTipDerecha.grid(row=4,column=2,padx=0,pady=(30,0),sticky=NW)
    statusestadisticas='SI'
    
def DeshabilitarEstadisticas():
    global LabelTipDerecha
    global HabilitarEstadisticasBoton
    global DeshabilitarEstadisticasBoton
    global statusestadisticas
    HabilitarEstadisticasBoton['state']=NORMAL
    DeshabilitarEstadisticasBoton['state']=DISABLED
    LabelTipDerecha.grid_remove()
    statusestadisticas='NO'
    

def MePlanto(): # solo es necesario declarar como variables globales las que se modifican dentro de la funcion que se esta definiendo
    global IniciarManoBoton
    global PedirCartaBoton
    global MePlantoBoton
    global LabelImagenDealerCartaNueva
    global puntajejugador1
    global puntajedealer
    global manodealer
    global LabelResultadoMano
    global LabelResultadoAcumulado
    global numerodecartasusadasbaraja
    global LabelCartasUsadas
    global ImageImagenCartasDealer
    global ImageImagenCartasJugador1
    global ImagenCartaDealer
    global LabelTipDerecha
    global LabelManoJugador1
    global LabelManoDealer
    global truecount
    global EntryApuestaJugador1
    global apuestajugador1
    global LabelFichasJugador1
    global fichasjugador1

    LabelManoJugador1=Label(FrameCartasJuego,text="Mano Jugador: " +str(manojugador1),anchor=S)
    LabelManoJugador1['font']=font.Font(family="Century Gothic",size=12,weight='bold')
    LabelManoJugador1.grid(row=3,column=1,padx=0,sticky=S)
    LabelManoJugador1.config(background="green")

    EntryApuestaJugador1= Entry(FrameBotonesJuego, width=10,bg='blue',fg='white',borderwidth=5)
    EntryApuestaJugador1.grid(row=0,column=4,pady=(5,0),padx=(20,0))
    EntryApuestaJugador1.insert(0,apuestajugador1)
    EntryApuestaJugador1.configure(justify='center')

    ImagenCartasDealer=ListaBasesCartas[13]
    ImagenCartasDealer.paste(Image.open('resize150Base14Cartas.png'),areabase)
    for a in range(len(listacartasdealer)):
        ImagenCartasDealer.paste(Image.open('resize150'+listacartasdealer[a]+'.png'),ListaAreasBasesCartas[a])
    ImagenCartasDealer.save('resize150ImagenCartasDealer.png')
    ImageImagenCartasDealer=ImageTk.PhotoImage(Image.open('resize150ImagenCartasDealer.png'))
    LabelImagenCartasDealer=Label(FrameCartasJuego,image=ImageImagenCartasDealer)
    LabelImagenCartasDealer.grid(row=2,column=0,padx=5,sticky=W)

    LabelCartasUsadas.grid_forget()
    try:
        LabelTipDerecha.grid_forget()
    except:
        pass
    
    PedirCartaBoton['state']=DISABLED
    MePlantoBoton['state']=DISABLED

    IniciarManoBoton=Button(FrameBotonesJuego,text="Iniciar Mano",padx=5,pady=10,fg="orange",bg="black",command= IniciarMano) 
    IniciarManoBoton['font']=font.Font(family="Helvetica",size=10,weight='bold')
    IniciarManoBoton.grid(row=0,column=1,padx=(400,0),pady=0)

    while manodealer <17:
        listacartasdealer.append(listacartasbarajadas[numerodecartasusadasbaraja])
        manodealer=valormano(listacartasdealer[0:len(listacartasdealer)])

        ImagenCartasDealer=ListaBasesCartas[13]
        ImagenCartasDealer.paste(Image.open('resize150Base14Cartas.png'),areabase)

        for a in range(len(listacartasdealer)):
            ImagenCartasDealer.paste(Image.open('resize150'+listacartasdealer[a]+'.png'),ListaAreasBasesCartas[a])
        ImagenCartasDealer.save('resize150ImagenCartasDealer.png')
        ImageImagenCartasDealer=ImageTk.PhotoImage(Image.open('resize150ImagenCartasDealer.png'))
        LabelImagenCartasDealer=Label(FrameCartasJuego,image=ImageImagenCartasDealer)
        LabelImagenCartasDealer.grid(row=2,column=0,padx=5,sticky=W)
    
        numerodecartasusadasbaraja=numerodecartasusadasbaraja+1
        



    LabelResultadoMano=Label(FramePuntajes,text="Mano Dealer: "+str(manodealer)+"\n"+"Mano Jugador: "+str(manojugador1),fg="black", bg="green",pady=10, anchor=E)
    LabelResultadoMano['font']=font.Font(family="Century Gothic",size=15)
    LabelResultadoMano.grid(row=0,column=4,padx=100)

    LabelManoDealer=Label(FrameCartasJuego,text="Mano Dealer: " +str(manodealer),anchor=SW)
    LabelManoDealer['font']=font.Font(family="Century Gothic",size=12,weight='bold')
    LabelManoDealer.grid(row=1,column=1,padx=3,sticky=SW)
    LabelManoDealer.config(background="green")

    if manojugador1>21:
        puntajedealer=puntajedealer+1
        fichasjugador1=fichasjugador1-int(apuestajugador1)
    elif manodealer>21:
        puntajejugador1=puntajejugador1+1
        fichasjugador1=fichasjugador1+int(apuestajugador1)
    elif manojugador1==manodealer:
        pass
    elif manojugador1>manodealer:
        puntajejugador1=puntajejugador1+1
        fichasjugador1=fichasjugador1+int(apuestajugador1)
    else:
        puntajedealer=puntajedealer+1
        fichasjugador1=fichasjugador1-int(apuestajugador1)

    LabelResultadoAcumulado=Label(FramePuntajes,text="Puntaje Dealer: "+str(puntajedealer)+"\n"+"Puntaje Jugador: "+str(puntajejugador1),anchor=W,fg="black", bg="green",pady=10)
    LabelResultadoAcumulado['font']=font.Font(family="Century Gothic",size=15)
    LabelResultadoAcumulado.grid(row=0,column=1,sticky=W,columnspan=3,padx=(280,0))

    LabelFichasJugador1=Label(FramePuntajes,text="Fichas Jugador1: "+str(fichasjugador1),anchor=W,fg="black", bg="green",pady=10)
    LabelFichasJugador1['font']=font.Font(family="Century Gothic",size=15,weight='bold')
    LabelFichasJugador1.grid(row=0,column=0,sticky=W,columnspan=3,padx=(10,0))
    
    count=valorcountbaraja(listacartasbarajadas,numerodecartasusadasbaraja)
    barajasrestantes='{:.1f}'.format((52*numerodebarajas-numerodecartasusadasbaraja)/52)
    truecount=math.trunc(count/float(barajasrestantes))
    
    LabelTipDerecha=Label(FrameCartasJuego,anchor=CENTER,text="Count: "+str(count)+"\n"+"Bajaras Restantes: "+str(barajasrestantes)+"\n\n"+"TrueCount: "+str(truecount))
    LabelTipDerecha['font']=font.Font(family="Century Gothic",size=12,weight='bold')
    if statusestadisticas=='SI':
        LabelTipDerecha.grid(row=4,column=2,padx=0,pady=50,sticky=NW)
    LabelTipDerecha.config(background="green")


    

    #print (count)
    #print(52*numerodebarajas-numerodecartasusadasbaraja)
    #print(truecount)

def PedirCarta():  # solo es necesario declarar como variables globales las que se modifican dentro de la funcion que se esta definiendo
    # por ejemplo listaimagenescartasjugador1 se usa en PedirCarta() pero no se modifica, por lo que no es necesario declararla como global
    global LabelImagenJugador1CartaNueva
    global manojugador1
    global numerodecartasusadasbaraja
    global LabelCartasUsadas
    global ImageImagenCartasDealer
    global ImageImagenCartasJugador1
    global LabelTipDerecha
    global LabelManoJugador1
    global apuestajugador1

    LabelCartasUsadas.grid_forget()
    LabelManoJugador1.grid_forget()
    LabelTipDerecha.grid_forget()

    listacartasjugador1.append(listacartasbarajadas[numerodecartasusadasbaraja])
    numerodecartasusadasbaraja=numerodecartasusadasbaraja+1
    manojugador1=valormano(listacartasjugador1[0:len(listacartasjugador1)])

    ImagenCartasJugador1=ListaBasesCartas[13]
    for a in range(len(listacartasjugador1)):
        ImagenCartasJugador1.paste(Image.open('resize150'+listacartasjugador1[a]+'.png'),ListaAreasBasesCartas[a])
    ImagenCartasJugador1.save('resize150ImagenCartasJugador1.png')
    ImageImagenCartasJugador1=ImageTk.PhotoImage(Image.open('resize150ImagenCartasJugador1.png'))
    LabelImagenCartasJugador1=Label(FrameCartasJuego,image=ImageImagenCartasJugador1)
    LabelImagenCartasJugador1.grid(row=4,column=0,padx=5,sticky=W)


    try:
        LabelManoJugador1.grid_forget()
        #LabelManoJugador1.destroy()
    except:
        pass

    if manojugador1>21:
        PedirCartaBoton['state']=DISABLED
        MePlanto()
    else:
        LabelManoJugador1=Label(FrameCartasJuego,text="Mano Jugador: " +str(manojugador1),anchor=S)
        LabelManoJugador1['font']=font.Font(family="Century Gothic",size=12,weight='bold')
        LabelManoJugador1.grid(row=3,column=1,padx=3,sticky=S)
        LabelManoJugador1.config(background="green")    
        
        if valormano(listacartasjugador1)<=11:
            tipcartas="PEDIR CARTA - no es posible volar la mano"
            LabelTipDerecha=Label(FrameCartasJuego,anchor=NW,text=tipcartas)
            LabelTipDerecha['font']=font.Font(family="Century Gothic",size=12,weight='bold')
            if statusestadisticas=='SI':
                LabelTipDerecha.grid(row=4,column=2,padx=0,pady=60,sticky=NW)
            LabelTipDerecha.config(background="green")
        else:
            valorcartadealer=str((listacartasdealer[0][1:3]))
            if valorcartadealer=='01':
                valorcartadealer=='11'
            elif valorcartadealer=='11' or valorcartadealer=='12' or valorcartadealer=='13':
                valorcartadealer =='10'
            tipcartas=probabilidadescartas('0',str(valormano(listacartasjugador1.copy())),tipodemano(listacartasjugador1.copy()),str(valorcartadealer))
            tipcartastruecount=probabilidadescartas(str(truecount),str(valormano(listacartasjugador1.copy())),tipodemano(listacartasjugador1.copy()),str(valorcartadealer))
            if tipcartas[0]=="No se Encontró Data Suficiente":
                LabelTipDerecha=Label(FrameCartasJuego,anchor=CENTER,text="")
                LabelTipDerecha['font']=font.Font(family="Century Gothic",size=12,weight='bold')
                if statusestadisticas=='SI':
                    LabelTipDerecha.grid(row=4,column=2,padx=0,sticky=NW,pady=60)
                LabelTipDerecha.config(background="green")
            else:    
                LabelTipDerecha=Label(FrameCartasJuego,anchor=CENTER,text="Probabilidades con True Count 0"+"\n"+"Me Planto [g,e,p,ge]: "+str(tipcartas[0])+"\n"+"Pedir Carta [g,e,p,ge]: " + str(tipcartas[1])+"\n"+str(tipcartas[2])\
                    +"\n\n"+"Probabilidades con True Count Actual: "+str(truecount)+"\n"+"Me Planto [g,e,p,ge]: "+str(tipcartastruecount[0])+"\n"+"Pedir Carta [g,e,p,ge]: " + str(tipcartastruecount[1])+"\n"+str(tipcartastruecount[2]))
                LabelTipDerecha['font']=font.Font(family="Century Gothic",size=11,weight='bold')
                if statusestadisticas=='SI':
                    LabelTipDerecha.grid(row=4,column=2,padx=0,pady=(30,0),sticky=NW)
                LabelTipDerecha.config(background="green")
        
        #print(tipcartas)



def IniciarMano():
    global EmpezarJuegoBoton
    global IniciarManoBoton
    global PedirCartaBoton
    global MePlantoBoton
    global listacartasjugador1
    global listacartasdealer
    global listaimagenescartasjugador1
    global listaimagenescartasdealer
    global manojugador1
    global manodealer
    global LabelResultadoMano
    global listacartas
    global numerodecartasusadasbaraja
    global LabelCartasUsadas
    global ImageImagenCartasDealer
    global ImageImagenCartasJugador1
    global LabelBarajas
    global LabelTipDerecha
    global LabelManoJugador1
    global HabilitarEstadisticasBoton
    global DeshabilitarEstadisticasBoton
    global apuestajugador1
    global EntryApuestaJugador1
    
    for widget in FrameCartasJuego.winfo_children():
        widget.destroy()

    listacartasjugador1=[]
    listacartasdealer=[]
    
    listacartasjugador1.append(listacartasbarajadas[numerodecartasusadasbaraja])
    numerodecartasusadasbaraja=numerodecartasusadasbaraja+1
    listacartasdealer.append(listacartasbarajadas[numerodecartasusadasbaraja])
    numerodecartasusadasbaraja=numerodecartasusadasbaraja+1
    listacartasjugador1.append(listacartasbarajadas[numerodecartasusadasbaraja])
    numerodecartasusadasbaraja=numerodecartasusadasbaraja+1
    listacartasdealer.append(listacartasbarajadas[numerodecartasusadasbaraja])
    numerodecartasusadasbaraja=numerodecartasusadasbaraja+1
    manojugador1=valormano(listacartasjugador1[0:len(listacartasjugador1)])
    manodealer=valormano(listacartasdealer[0:len(listacartasdealer)])
    
    listaimagenescartasjugador1=[]
    listaimagenescartasdealer=[]

    listaimagenescartasjugador1.append(ImageTk.PhotoImage(Image.open(filelocation+listacartasjugador1[0]+'.png')))
    listaimagenescartasjugador1.append(ImageTk.PhotoImage(Image.open(filelocation+listacartasjugador1[1]+'.png')))
    listaimagenescartasdealer.append(ImageTk.PhotoImage(Image.open(filelocation+listacartasdealer[0]+'.png')))
    listaimagenescartasdealer.append(ImageTk.PhotoImage(Image.open(filelocation+listacartasdealer[1]+'.png')))

    EmpezarJuegoBoton=Button(FrameBotonesJuego,text="Barajar",padx=5,pady=15,fg="black",bg='#2719A2',command= EmpezarJuego)
    EmpezarJuegoBoton['font']=font.Font(family="Helvetica",size=10,weight='bold')
    EmpezarJuegoBoton.grid(row=1,column=0,padx=10,pady=(70,5))

    try:
        IniciarManoBoton['state']=DISABLED
    except:
        IniciarManoBoton=Button(FrameBotonesJuego,text="Iniciar Mano",padx=5,pady=10,fg="orange",bg="black", state=DISABLED) 
        IniciarManoBoton['font']=font.Font(family="Helvetica",size=10,weight='bold')
        IniciarManoBoton.grid(row=0,column=1,padx=(400,0),pady=0)

    try:
        apuestajugador1=int(EntryApuestaJugador1.get())
        #print("Entro")
    except:
        apuestajugador1=10

    print(apuestajugador1)

    EntryApuestaJugador1.destroy()
    LabelApuestaInicial.destroy()
    
    EntryApuestaJugador1= Entry(FrameBotonesJuego, width=10,bg='blue',fg='white',borderwidth=5)
    EntryApuestaJugador1.grid(row=0,column=4,pady=(5,0),padx=(20,0))
    EntryApuestaJugador1.insert(0,apuestajugador1)
    EntryApuestaJugador1.configure(justify='center')

    LabelApuestaJugador1=Label(FrameBotonesJuego,text="Colocar Apuesta en el recuadro de la izquierda")
    LabelApuestaJugador1['font']=font.Font(family="Century Gothic",size=8)
    LabelApuestaJugador1.grid(row=0,column=5,padx=0,pady=(5,0))
    LabelApuestaJugador1.config(background='green')

    EntryApuestaJugador1.config(state='disabled')

    PedirCartaBoton=Button(FrameBotonesJuego,text="Pedir Carta",padx=5,pady=12,fg="orange",bg="black",command=PedirCarta)
    PedirCartaBoton['font']=font.Font(family="Helvetica",size=10,weight='bold')
    PedirCartaBoton.grid(row=0,column=2,padx=2,pady=0)
    
    MePlantoBoton=Button(FrameBotonesJuego,text="Me Planto",padx=5,pady=10,fg="orange",bg="black",command=MePlanto)
    MePlantoBoton['font']=font.Font(family="Helvetica",size=10,weight='bold')
    MePlantoBoton.grid(row=0,column=3,padx=0,pady=0)

    if statusestadisticas=='SI':
        HabilitarEstadisticasBoton=Button(FrameBotonesJuego,text="Habilitar"+"\n"+"Estadisticas",padx=0,pady=0,fg='orange',bg="black",command=HabilitarEstadisticas)
        HabilitarEstadisticasBoton['font']=font.Font(family="Helvetica",size=8,weight='bold')
        HabilitarEstadisticasBoton.grid(row=0,column=6,padx=(100,0),pady=0)
        HabilitarEstadisticasBoton['state']=DISABLED

        DeshabilitarEstadisticasBoton=Button(FrameBotonesJuego,text="Deshabilitar"+"\n"+"Estadisticas",padx=0,pady=0,fg="orange",bg="black",command=DeshabilitarEstadisticas,anchor=W)
        DeshabilitarEstadisticasBoton['font']=font.Font(family="Helvetica",size=8,weight='bold')
        DeshabilitarEstadisticasBoton.grid(row=0,column=7,padx=(10,0),pady=0,sticky=W)

    else:
        HabilitarEstadisticasBoton=Button(FrameBotonesJuego,text="Habilitar"+"\n"+"Estadisticas",padx=0,pady=0,fg="orange",bg="black",command=HabilitarEstadisticas)
        HabilitarEstadisticasBoton['font']=font.Font(family="Helvetica",size=8,weight='bold')
        HabilitarEstadisticasBoton.grid(row=0,column=6,padx=(100,0),pady=0)

        DeshabilitarEstadisticasBoton=Button(FrameBotonesJuego,text="Deshabilitar"+"\n"+"Estadisticas",padx=0,pady=0,fg="orange",bg="black",command=DeshabilitarEstadisticas,anchor=W)
        DeshabilitarEstadisticasBoton['font']=font.Font(family="Helvetica",size=8,weight='bold')
        DeshabilitarEstadisticasBoton.grid(row=0,column=7,padx=(10,0),pady=0,sticky=W)
        DeshabilitarEstadisticasBoton['state']=DISABLED

    LabelJugador1=Label(FrameCartasJuego,text="Jugador - 1",anchor=W,fg="black", bg="green")
    LabelJugador1['font']=font.Font(family="Century Gothic",size=15,weight='bold')
    LabelJugador1.grid(row=3,column=0,sticky=W,pady=(30,5))

    LabelDealer=Label(FrameCartasJuego,text="Dealer",anchor=W,fg="black", bg="green")
    LabelDealer['font']=font.Font(family="Century Gothic",size=15,weight='bold')
    LabelDealer.grid(row=1,column=0,sticky=W,pady=(10,5))

    LabelCartasUsadas=Label(FrameBotonesJuego,text="Se han usado "+str(numerodecartasusadasbaraja)+" cartas de un total de "+str(len(listacartasbarajadas)) +" cartas barajadas",anchor=W,fg="black", bg="green")
    LabelCartasUsadas['font']=font.Font(family="Century Gothic",size=10)
    LabelCartasUsadas.grid(row=1,column=1,sticky=W,pady=(70,5))
    
    LabelBarajas.destroy()
    LabelBarajas=Label(FrameBotonesJuego,text='Para cambiar la cantidad de barajas a usar completa el recuadro de la izquierda y pulsa el boton Barajar',anchor=W,fg="black", bg='green')
    LabelBarajas['font']=font.Font(family="Century Gothic",size=10)
    LabelBarajas.grid(row=2,column=1,sticky=W,pady=(7,5),columnspan=5)
    
    ImagenCartasJugador1=ListaBasesCartas[13]
    ImagenCartasJugador1.paste(Image.open('resize150Base14Cartas.png'),areabase)
    for a in range(len(listacartasjugador1)):
        ImagenCartasJugador1.paste(Image.open('resize150'+listacartasjugador1[a]+'.png'),ListaAreasBasesCartas[a])
    ImagenCartasJugador1.save('resize150ImagenCartasJugador1.png')
    ImageImagenCartasJugador1=ImageTk.PhotoImage(Image.open('resize150ImagenCartasJugador1.png'))
    LabelImagenCartasJugador1=Label(FrameCartasJuego,image=ImageImagenCartasJugador1)
    LabelImagenCartasJugador1.grid(row=4,column=0,padx=5,sticky=W)
    
    ImagenCartasDealer=ListaBasesCartas[13]
    ImagenCartasDealer.paste(Image.open('resize150Base14Cartas.png'),areabase)

    ImagenCartasDealer.paste(Image.open('resize150'+listacartasdealer[0]+'.png'),ListaAreasBasesCartas[0])
    ImagenCartasDealer.paste(Image.open('resize150CardBack.png'),ListaAreasBasesCartas[1])
      
    ImagenCartasDealer.save('resize150ImagenCartasDealer.png')
    ImageImagenCartasDealer=ImageTk.PhotoImage(Image.open('resize150ImagenCartasDealer.png'))
    LabelImagenCartasDealer=Label(FrameCartasJuego,image=ImageImagenCartasDealer)
    LabelImagenCartasDealer.grid(row=2,column=0,padx=5,sticky=W)

    try:
        LabelResultadoMano.destroy()
    except:
        pass
    
    if numerodecartasusadasbaraja>len(listacartasbarajadas)-30:# si quedan menos de 30 cartas por repartir, se debe volver a barajar
        messagebox.showinfo(
            " Información","No quedan muchas cartas por repartir. Se deben volver a barajar las cartas."
            +"\n\n"+"Para seguir jugando baraje las cartas con el boton de la esquina inferior izquierda")
        IniciarManoBoton['state']=DISABLED
        PedirCartaBoton['state']=DISABLED
        MePlantoBoton['state']=DISABLED
        EntryApuestaJugador1.config(state='normal')
    
    #print("Probabilidadades si me Planto")
    #print(probganarjugadormeplantov2(listacartasjugador1.copy(),listacartasdealer.copy(),listacartasbarajadas.copy(),numerodecartasusadasbaraja,1000))
    #print("Probabilidadades si pido Carta")
    #print(probganarjugadorpidecartav2(listacartasjugador1.copy(),listacartasdealer.copy(),listacartasbarajadas.copy(),numerodecartasusadasbaraja,1000))
    
    if valormano(listacartasjugador1)<=11:
        tipcartas="PEDIR CARTA - no es posible volar la mano"
        LabelTipDerecha=Label(FrameCartasJuego,anchor=CENTER,text=tipcartas)
        LabelTipDerecha['font']=font.Font(family="Century Gothic",size=12,weight='bold')
        if statusestadisticas=='SI':
            LabelTipDerecha.grid(row=4,column=2,padx=0,pady=60,sticky=NW)
        LabelTipDerecha.config(background="green")
    else:
        valorcartadealer=str((listacartasdealer[0][1:3]))
        if valorcartadealer=='01':
            valorcartadealer=='11'
        elif valorcartadealer=='11' or valorcartadealer=='12' or valorcartadealer=='13':
            valorcartadealer =='10'
        tipcartas=probabilidadescartas('0',str(valormano(listacartasjugador1.copy())),tipodemano(listacartasjugador1.copy()),str(valorcartadealer))
        tipcartastruecount=probabilidadescartas(str(truecount),str(valormano(listacartasjugador1.copy())),tipodemano(listacartasjugador1.copy()),str(valorcartadealer))
        LabelTipDerecha=Label(FrameCartasJuego,anchor=CENTER,text="Probabilidades con True Count 0"+"\n"+"Me Planto [g,e,p,ge]: "+str(tipcartas[0])+"\n"+"Pedir Carta [g,e,p,ge]: " + str(tipcartas[1])+"\n"+str(tipcartas[2])\
            +"\n\n"+"Probabilidades con True Count Actual: "+str(truecount)+"\n"+"Me Planto [g,e,p,ge]: "+str(tipcartastruecount[0])+"\n"+"Pedir Carta [g,e,p,ge]: " + str(tipcartastruecount[1])+"\n"+str(tipcartastruecount[2]))
        LabelTipDerecha['font']=font.Font(family="Century Gothic",size=11,weight='bold')
        if statusestadisticas=='SI':
            LabelTipDerecha.grid(row=4,column=2,padx=0,pady=(30,0),sticky=NW)
        LabelTipDerecha.config(background="green")

    
    LabelManoJugador1=Label(FrameCartasJuego,text="Mano Jugador: " +str(manojugador1),anchor=S)
    LabelManoJugador1['font']=font.Font(family="Century Gothic",size=12,weight='bold')
    LabelManoJugador1.grid(row=3,column=1,padx=3,sticky=S)
    LabelManoJugador1.config(background="green")

    valorprimeracartadealer=int(listacartasdealer[0][1:3])
    if valorprimeracartadealer==11 or valorprimeracartadealer==12 or valorprimeracartadealer==13:
        valorprimeracartadealer=10
    elif valorprimeracartadealer==1:
        valorprimeracartadealer=11
    else:
        pass

    LabelManoDealer=Label(FrameCartasJuego,text="Mano Dealer: " +str(valorprimeracartadealer),anchor=SW)
    LabelManoDealer['font']=font.Font(family="Century Gothic",size=12,weight='bold')
    LabelManoDealer.grid(row=1,column=1,padx=0,sticky=SW)
    LabelManoDealer.config(background="green")


def EmpezarJuego():
    global EmpezarJuegoBoton
    global numerodebarajas
    global listacartas
    global listacartasbarajadas
    global listaimagenescartasbarajadas
    global numerodecartasusadasbaraja
    global puntajejugador1
    global puntajedealer
    global LabelCartasUsadas
    global EntryNumeroBarajas
    global LabelImagenDerecha
    global LabelManoJugador1
    global truecount
    global apuestajugador1
    global EntryApuestaJugador1
    global fichasjugador1

    try:
        LabelCartasUsadas.grid_forget()
    except:
        pass

    try:
        numerodebarajas=int(EntryNumeroBarajas.get())
    except:
        numerodebarajas=4
    listacartas=[]
    for a in range(numerodebarajas):
        for palo in palosbaraja:
            for numeracion in numeracionbaraja:
                listacartas.append(str(a)+palo+str(numeracion))

    truecount=0

    listacartasbarajadas=[]
    listaimagenescartasbarajadas=[]
    for a in range(numerodebarajas*4*len(numeracionbaraja)):
        carta=random.choice(listacartas)
        listacartasbarajadas.append(carta[1:4])
        listacartas.remove(carta)
        listaimagenescartasbarajadas.append(ImageTk.PhotoImage(Image.open(filelocation+carta[1:4]+'.png')))

    #print(listacartasbarajadas)

    numerodecartasusadasbaraja=0
    try:
        EmpezarJuegoBoton.destroy()
    except:
        pass

    ReiniciarBoton=Button(FrameBotonesJuego,text="Reiniciar",padx=5,pady=10,fg="orange",bg="black",command=IniciarPrograma)
    ReiniciarBoton['font']=font.Font(family="Helvetica",size=10,weight='bold')
    ReiniciarBoton.grid(row=2,column=7,padx=10,pady=(0,0))

    IniciarMano()


def IniciarPrograma():
    global puntajejugador1
    global puntajedealer
    global apuestajugador1
    global fichasjugador1
    global EntryApuestaJugador1
    global EntryNumeroBarajas
    global LabelBarajas
    global LabelApuestaInicial
    global EmpezarJuegoBoton
    global LabelResultadoAcumulado
    global LabelFichasJugador1
    
    puntajejugador1=0
    puntajedealer=0

    apuestajugador1=10
    fichasjugador1=500

    EntryNumeroBarajas= Entry(FrameBotonesJuego, width=10,bg='blue',fg='white',borderwidth=5)
    EntryNumeroBarajas.grid(row=2,column=0,pady=(5,0))
    EntryNumeroBarajas.insert(0,'4')
    EntryNumeroBarajas.configure(justify='center')

    EntryApuestaJugador1= Entry(FrameBotonesJuego, width=10,bg='blue',fg='white',borderwidth=5)
    EntryApuestaJugador1.grid(row=3,column=0,pady=(5,0))
    EntryApuestaJugador1.insert(0,apuestajugador1)
    EntryApuestaJugador1.configure(justify='center')

    LabelBarajas=Label(FrameBotonesJuego,text='Para cambiar la cantidad de barajas a usar llene el recuadro de la izquierda y pulse el boton Empezar Juego',anchor=W,fg="black", bg='green')
    LabelBarajas['font']=font.Font(family="Century Gothic",size=10)
    LabelBarajas.grid(row=2,column=1,sticky=W,pady=(7,5),columnspan=5)

    LabelApuestaInicial=Label(FrameBotonesJuego,text='Ingresar apuesta para primera mano en el recuadro de la izquierda',anchor=W,fg="black", bg='green')
    LabelApuestaInicial['font']=font.Font(family="Century Gothic",size=10)
    LabelApuestaInicial.grid(row=3,column=1,sticky=W,pady=(7,5),columnspan=5)


    EmpezarJuegoBoton=Button(FrameBotonesJuego,text="Empezar Juego",padx=5,pady=10,fg="orange",bg="black",command= EmpezarJuego)
    EmpezarJuegoBoton['font']=font.Font(family="Helvetica",size=10,weight='bold')
    EmpezarJuegoBoton.grid(row=0,column=0,padx=5,pady=10)

    LabelResultadoAcumulado=Label(FramePuntajes,text="Puntaje Dealer: "+str(0)+"\n"+"Puntaje Jugador: "+str(0),anchor=W,fg="black", bg="green",pady=10)
    LabelResultadoAcumulado['font']=font.Font(family="Century Gothic",size=15)
    LabelResultadoAcumulado.grid(row=0,column=1,sticky=W,columnspan=3,padx=(280,0))

    LabelFichasJugador1=Label(FramePuntajes,text="Fichas Jugador1: "+str(fichasjugador1),anchor=W,fg="black", bg="green",pady=10)
    LabelFichasJugador1['font']=font.Font(family="Century Gothic",size=15,weight='bold')
    LabelFichasJugador1.grid(row=0,column=0,sticky=W,columnspan=3,padx=(10,0))

    EmpezarJuego()


messagebox.showinfo(
    " Reglas BlackJack","El objetivo del juego es competir contra el dealer, ganando el que más se acerque a 21."
    +"\n\n"+"Si pasas los 21, vuelas y pierdes la mano. Igualmente si tú no vuelas y el dealer pasa los 21, ganas la mano."
    +"\n\n"+"Ojo que las cartas J,Q,K tienen un valor de 10 y no de 11, 12 y 13."
    +"\n\n"+"El As tiene un valor de 1 u 11, el que convenga más en cada mano"
    +"\n\n"+"Recuerda que por reglas de la casa, el dealer deja de sacar cartas cuando llega a 17 o más."
    +"\n\n"+"Para empezar a jugar completa el recuadro que aparecerá con la cantidad de barajas con las que quieres jugar. El estándar en los casinos es de 4 a 6."
    +"\n\n¡Suerte!")

ListaBasesCartas=[]
ListaAreasBasesCartas=[]
for a in range(14):
    ListaBasesCartas.append(Image.open('resize150Base'+str(a+1)+'Cartas.png'))
    area=(a*30,0,150+a*30,229)
    ListaAreasBasesCartas.append(area)

areabase=(0,0,540,229) # sirve para resetear la base donde se ponen las cartas

   
filelocation="resize150"
palosbaraja=["C","D","E","T"]
#numeracionbaraja=['01','04','06']
numeracionbaraja=['01','02','03','04','05','06','07','08','09','10','11','12','13']

carta2dealervolteada=ImageTk.PhotoImage(Image.open(filelocation+'CardBack.png'))


StatusLabel=Label(FrameStatusBar,text="BlackJackGRVer02",bd=1,relief=SUNKEN,anchor=E)
StatusLabel.pack(fill='x')

IniciarPrograma()


root.mainloop()
