import pandas as pd
import math

#Metodo que analiza la cadena de forma ascendente
def analizar(pila,pilaAcciones,cadena,TablaM,Producciones):
    continuar=True
    contador=0
    exito=False
    try:
        while continuar:
            contador+=1
            resultadoBusqueda=recorrer(cadena)
            estado=pila[len(pila)-1]     #El estado se encuentra en la cima de la pila
            
            #esta parte del código se usa para imprimir el estado actual de la pila y de la cadena ingresada
            print("Cadena Actual: ",end="")    
            print(cadena)
            print("Numero iteraciones: ",end="")    
            print(contador)
            print("Pila Actual: ",end="")
            for a in pila:     
                print(a,end=" ")
            print("")
            
            if resultadoBusqueda[0]=="NOENCONTRADO":#Si no se encuentra el token, entonces se finalia el programa
                
                continuar=False
            else:
                token=resultadoBusqueda[0]     #este es el token o palabra encontrada
                posToken=resultadoBusqueda[2]  # esta es la posicion token
                Accion=TablaM[estado][posToken]
                if type(Accion)==str:
                    NuevaAccion=Accion[0]      #esta parte define la accion que puede ser 'S', 'R' o 'a'
                if NuevaAccion=="S": #Accion de Shift o cambio
                    
                    apilar(pila,token)
                    apilar(pila,int(Accion[1::]))
                    cadena=cadena[resultadoBusqueda[1]::]
                    Operacion="Cambio "+Accion
                    apilar(pilaAcciones,Operacion) #Se acumulan las operaciones previas
                    
                elif NuevaAccion=="R": #Accion de reduce o reducción
                    #con numero se busca No de produccion y beta son los tokens o simbolos de esta produccion
                    Dosbeta=2*int(Producciones[int(Accion[1])][1])
                    for a in range(0,Dosbeta):
                        desapilar(pila,len(pila)-1)
                        
                    Operacion="Reduccion "+Accion
                    apilar(pilaAcciones,Operacion)
                    
                    # Se busca el numero de producción de acuerdo a la acción
                    sintactica=recorrer2(Producciones[int(Accion[1])][0])
                    
                    # Se obtiene el valor del GOTO de acuerdo al estado de la pila asi como la variable sintáctica
                    GoTo=TablaM[pila[len(pila)-1]][sintactica[2]+12]
                    
                    apilar(pila,sintactica[0])                
                    apilar(pila,int(GoTo))
                    
                elif NuevaAccion=="a": #estado de aceptación de la gramática
                    exito=True
                    continuar=False
                else:
                    
                    continuar=False
                    
            
    except:
        print("Fin del programa, Gramática No aceptada")
    resultado=[pilaAcciones,exito]
    return resultado
#Metodo para comparar cadena con unidades gramaticales
def recorrer(cadena):
    cadena=cadena
    NuevaCadena=""
    encontrado=False
    for x in range(0,len(cadena)):
        if encontrado==True:
            break
        caracter=cadena[x]
        NuevaCadena=NuevaCadena+caracter
        
        for y in range(0,len(UnidadGramatical)):
            
            if NuevaCadena==UnidadGramatical[y]:
                encontrado=True                
                break
    if encontrado==False:
        NuevaCadena="NOENCONTRADO"
    return [NuevaCadena,x,y]

#Este método recorre funciones sintacticas y posteriormente udades. Gramaticales
def recorrer2(cadena):
    
    cadena=cadena
    NuevaCadena=""
    encontrado=False
    for x in range(0,len(cadena)):
        if encontrado==True:
            break
        caracter=cadena[x]
        NuevaCadena=NuevaCadena+caracter
        
        for y in range(0,len(FuncionSintactica)):
            
            if NuevaCadena==FuncionSintactica[y]:
                if len(cadena)>1 and cadena[x+1]=="'":
                    NuevaCadena=NuevaCadena+cadena[x+1]
                    y=y+1
                encontrado=True                    
                break                                           
                
            elif NuevaCadena==" h":
                print("FOUND H")
                NuevaCadena="h"
                encontrado=True                
                break       
            
    if encontrado==False:
        NuevaCadena=recorrer(cadena)[0]
        x=recorrer(cadena)[1]
        y=recorrer(cadena)[2]
    return [NuevaCadena,x,y]


#Funciones para apilar y desapilar elementos
def apilar(pila, x):
    if x!=" ":
        pila.append(x)       
    
def desapilar(pila, x):
    pila.pop(x)   

#Función para imprimir la Tabla M
def imprimirTablaM(TablaM,Titulo):
    for t in Titulo:
        print(t,end="|")
    for a in TablaM:
        print("")
        for b in a:
            if type(b)==int:
                if b<10:
                    print("",end=" ")
                    print(b,end=" | ")
                else:
                    print(b,end=" | ")
                
            if type(b)==str:
                if len(b)<3:
                    print("",end=" ")
                    print(b,end=" | ")
                    
                else:
                    print(b,end=" | ")
                    
            elif type(b)==float:
                if not math.isnan(b):
                    b=int(b)
                    if b<10:
                        print(" ",end=" ")
                        print(b,end=" | ")
                        
                    else:
                        print("",end=" ")
                        print(b,end=" | ")
                        
                else:
                    print("   ",end=" | ")  
                    
                    
#########################################################################################################
#Empieza el MAIN 
# se lee de excel la tabla M donde estan las accion y los GOTO    
archivo = 'TablaM.xlsx'
  
df = pd.read_excel(archivo, sheet_name='Hoja1')
df2 = pd.read_excel(archivo, sheet_name='Hoja2')
#Se pasan a arreglos Numpy la tabla M como las reglas de Producción
TablaM=df.to_numpy()
Producciones=df2.to_numpy()

Titulo=["Edo"," id  ","  =  ","  ;  ","  +  ","  -  "  ,  "  *  ","  /  "," num ","  (  ","  )  ","  $  ","  A  ","  E  ","  T  ","  F  "]
UnidadGramatical=["","id","=",";","+","-","*","/","num","(",")","$"]
FuncionSintactica=["A","E","T","F"]


imprimirTablaM(TablaM,Titulo)

print("\nListado de Reglas de Producción")
for b in Producciones:
    print("")
    print(b[0],end=" ")
                
#ingreso de cadena por Consola
cad=input("\nPor favor ingrese la cadena a buscar: ")
cadena=cad+"$"

pilaAcciones=[]
pila=[]
estado=0
apilar(pila,estado)

resultado=analizar(pila,pilaAcciones,cadena,TablaM,Producciones)
print("")       
print("Resumen de Operaciones:")   
for c in resultado[0]:
    print(c)

if resultado[1]:
    print("")
    print("ESTADO DE ACEPTACIÓN: la cadena pertenece a la gramática")   
else:
    print("")
    print("Error: la cadena No pertenece a la gramática")    
        
