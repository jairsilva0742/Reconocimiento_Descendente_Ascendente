# Acá se ingresa la Tabla LL, se usa como ejemplo una gramática dada en clase
Titulo=["    "," +  "," -  "," *  "," /  "," (  "," )  ","num "," id "," $  "]
UnidadGramatical=["+","-","*","/","(",")","num","id","$"]
FuncionSintactica=["E","E'","T","T'","F"]
TablaLL=[[" E  ","    ","    ","    ","    ","TE' ","    ","TE' ","TE' ","    "],
         [" E' ","+TE'","-TE'","    ","    ","    "," h  ","    ","    "," h  "],
         [" T  ","    ","    ","    ","    ","FT' ","    ","FT' ","FT' ","    "],
         [" T' "," h  "," h  ","*FT'","/FT'","    "," h  ","    ","    "," h  "],
         [" F  ","    ","    ","    ","    ","(E) ","    ","num ","id  ","    "]]

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

#Acá se imprime la tabla    
for pos in Titulo:
    print(pos,end=" ")

for x in range(0,len(TablaLL)):
    print(" ")
    for y in range(0,len(TablaLL[x])):
        print(TablaLL[x][y],end=" ")

#Se ingresa la cadena a revisar
#cadena="num+id*num$"
cadena="id*(id+num*id)$"
pila=[]
apilar(pila,UnidadGramatical[8]) # Se apila la primer Funcion Sintáctica
apilar(pila,FuncionSintactica[0]) # Se apila la primer Funcion Sintáctica
print("Pila Inicial ",end="")
print(pila)
print("Cadena ",end="")
print(cadena)

continuar=True
while(continuar):

    
    z=recorrer(cadena) #En z está la variable encontrada de Udades Gramaticales  
    if pila[len(pila)-1]!="h":#Solo se hace la parte del recorrido de la pila si el ultimo valor no es h (lambda)
        pos=recorrer2(pila[len(pila)-1])

    if pila[len(pila)-1]==z[0]:
        print(" Se Elimina Dato ",end="") 
        print(z[0])
        #Acá se eliminará la palabra en caso de que sea igual la de la cadena a la apilada, tanto en la pila como en la cadena
        desapilar(pila,len(pila)-1)
        cadena=cadena[z[1]::]
        
    elif pila[len(pila)-1]=="h":
        #Si es h se desapila para omitir su busqueda
        desapilar(pila,len(pila)-1)
    else:
        #Si no son iguales el valor de la PILA con el de la cadena, entonces se apilara el nuevo valor
        a=TablaLL[pos[2]][z[2]+1] # se halla l valor que se cruza entre primer udad grmatical y la F sintactica

        Nuevaletra=["XX","",""]
        pilaCar=[]
        while Nuevaletra[0]!="NOENCONTRADO": # Se recorre el parametro encontrado en la tabla
            Nuevaletra=recorrer2(a)
            if Nuevaletra[0]!="NOENCONTRADO":
                apilar(pilaCar,Nuevaletra[0])                
                a=a[Nuevaletra[1]::]
        desapilar(pila,len(pila)-1)       
        for z in reversed(pilaCar):
            apilar(pila,z)
    print("Pila Actual ",end="")
    print(pila)
    print("Cadena ",end="")
    print(cadena)
    if len(pila)==1: #Este if es para finalizar la busqueda y definir si la cadena corresponde a la gramática
        print(pila[0])
        if pila[0]==cadena:
            continuar=False
            print("La cadena corresponde a la gramática")
        else:
            continuar=False
            print("La cadena NO corresponde a esta gramática")  

