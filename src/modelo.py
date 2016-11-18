# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os

#Dividiremos en dos clases: una que se encargue del tema del GStreamer y otra para el tema del árbol de directorios (esta última necesita de un árbol n-ario).
class Bosque(object):
    '''
    Bosque usado para la estructura de ArbolEneario.
    '''
    def __init__(self):
        '''
        Constructor
        '''
        #Lista de ArbolEneario.
        self.listBosque = []
        
    def anyadirNuevoArbol(self, arbol):
        '''
        Añade un nuevo hijo (ArbolEneario) a la lista de hijos.
        '''
        self.listBosque = self.listBosque + [arbol]
   
    def setListBosque(self, nuevaListBosque):
        self.listBosque = listBosque
   
    def getListBosque(self):
        return self.listBosque
        
    def getListHijosByElemento(self, elemento):
        res = None
        for elem in self.listBosque:
            if elem.getElemento() == elemento:
                res = elem.getHijos()
        return res
   
    def getIndexHijosByElemento(self, elemento):
        res = -1
        count = 0
        for elem in self.listBosque:
            if elem.getElemento() == elemento:
                res = count
            count = count + 1
        return res
        
    def getArbolByIndex(self, index):
        return self.listBosque[index]
        
    def isBosqueVacio(self):
        return len(self.listBosque) == 0
        
    def lenBosque(self):
        return len(self.listBosque)
   

class ArbolEneario(object):
    '''
    Estructura de Árbol n-rio, cada elemento será un bosque.
    '''
    def __init__(self):
        '''
        Constructor
        '''
        #Elemento que llevará el objeto a guardar en este nodo del árbol.
        self.elemento = None
        #Objeto de la clase Bosque con los hijos del árbol.
        self.hijos = Bosque()
        
    def setElemento(self, elem):
        self.elemento = elem
   
    def getElemento(self):
        return self.elemento
        
    def getHijos(self):
        return self.hijos
    
    def setHijos(self, newHijos):
        self.hijos = newHijos
    
    def addHijo(self, elem):
        '''
        Añade un nuevo hijo, el hijo puede ser, por ejemplo, de tipo cadena.
        '''
        newHijo = ArbolEneario()
        newHijo.setElemento(elem)
        self.hijos.anyadirNuevoArbol(newHijo)
        
    def addHijoArbolEneario(self, elem):
        '''
        Añade un nuevo hijo, el hijo sólo puede ser un árbol n-ario.
        '''
        self.hijos.anyadirNuevoArbol(elem)
        
    def isSinHijos(self):
        return self.hijos.isBosqueVacio()
        
    def isVacio(self):
        return self.elemento == None
    


class ArbolDeFicherosYDirectorios(object):
    '''
    Trata todo el tema del árbol de directorios. Dada una carpeta guarda ese árbol en una estructura (lista de listas) y luego 
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        self.arbolDirectorios = ArbolEneario()
        self.rutaDirectorioRaiz = None
    
    def setRutaDirectorioRaiz(self, ruta):
        self.rutaDirectorioRaiz = ruta
    
    def getRutaDirectorioRaiz(self):
        return self.rutaDirectorioRaiz
        
    def refleshArbolDirectorios(self):
        def createArbolDirectorios(rutaDirectorioRaiz):
            arbol = ArbolEneario()
            if rutaDirectorioRaiz != None:
                listSubDirectorios = None
                try:
                    listSubDirectorios = os.listdir(rutaDirectorioRaiz)
                except:
                    listSubDirectorios = []
                listaFicheros = []
                listaDirectorios = []
                thePath = rutaDirectorioRaiz + "/"
                for element in listSubDirectorios:
                    isFile = True
                    try:
                        fich = open(element, 'r')
                        fich.close()
                    except:
                        isFile = False
                    
                    if isFile:
                        listaFicheros = listaFicheros + [thePath + element]
                    else:
                        #print "thePath: ", thePath
                        #print "element: ", element
                        listaDirectorios = listaDirectorios + [thePath + element]
                # Aquí tendré dos listas, una para ficheros y otra para directorios, ambas con sus rutas absolutas.
                # Quedaría asignar la raíz y hacer un árbol para todos los directorios.
                arbol.setElemento(rutaDirectorioRaiz)
                # Primero añado al árbol los ficheros.
                for element in listaFicheros:
                    arbol.addHijo(element)
                # Luego añado los directorios.
                for element in listaDirectorios:
                    # Añado el árbol del directorio
                    arbol.addHijoArbolEneario(createArbolDirectorios(element))
                
            return arbol
                
        self.arbolDirectorios = createArbolDirectorios(self.rutaDirectorioRaiz)
        
    def __iter__(self):
        return IteradorDeArbolEneario(self.arbolDirectorios)
        
    def __str__(self):
        c = ""
        for elem in self:
            c = c + elem + "\n"
        # Devolver la cadena sin el enter final.
        return c[:-1]
   
    def toLista(self):
        c = []
        for elem in self:
            c = c + [elem]
        return c
        
        
class IteradorDeArbolEneario(object):
    """
    Clase iteradora del árbol general, cuyo método next devuelve el elemento actual.
    """
    def __init__(self, arbolN):
        self.isUltimoNodo = arbolN.isVacio()
        self.arbolN = arbolN
        self.ultimoNodo = arbolN #Tipo ArbolEneario, referencia del nodo actual.
        self.listaBacktracking = [] #Lista de los bosques por los que vamos pasando en cada nodo, el último es el del nodo actual, si se ha llegado al final de un bosque, se elimina de la lista.
        #bosqueSiguiente = self.ultimoNodo.getHijos()
        #if not self.ultimoNodo.isSinHijos():
        #    # Sólo añadir nuevo bosque a la lista de backtracking si su longitud es mayor que uno.
        #    #if bosqueSiguiente.lenBosque() > 1:
        #        #self.listaBacktracking = [[bosqueSiguiente, 1]]
        
    def next(self):
        """
        Método que realiza una iteración en el árbol n-ario.
        """
        if self.isUltimoNodo:
            raise StopIteration
        else:
            # Devolver el nodo.
            res = self.ultimoNodo.getElemento()
            # Ir al siguiente nodo antes de terminar o dejarlo todo listo para parar la iteración.
            bosqueSiguiente = self.ultimoNodo.getHijos()
            if not self.ultimoNodo.isSinHijos():
                # Sólo añadir nuevo bosque a la lista de backtracking si su longitud es mayor que uno.
                if bosqueSiguiente.lenBosque() > 1:
                    self.listaBacktracking = self.listaBacktracking + [[bosqueSiguiente, 1]]
                self.ultimoNodo = bosqueSiguiente.getArbolByIndex(0)
            else:
                # Mirar si se puede hacer backtracking.
                if len(self.listaBacktracking) > 0:
                    # Pillamos el último elemento.
                    self.ultimoNodo = self.listaBacktracking[-1][0].getArbolByIndex(self.listaBacktracking[-1][1])
                    self.listaBacktracking[-1][1] = self.listaBacktracking[-1][1] + 1
                    # Miro si se puede seguir haciendo backtracking en este bosque (var backtracking).
                    if self.listaBacktracking[-1][1] >= (self.listaBacktracking[-1][0]).lenBosque():
                        # No se puede seguir haciendo backtracking en este bosque, luego lo elimino de la lista.
                        self.listaBacktracking = self.listaBacktracking[:-1]
                else:
                    # Hemos llegado al final.
                    self.isUltimoNodo = True
        return res
        
        
class MegaSuperUltraConversor(object):
    """
    Clase que maneja el conversor de música que voy a hacer (no funciona con carpetas con puntos, si tiene algún punto la contaremos como fichero).
    """
    def __init__(self):
        self.arbolDeDirectorios = ArbolDeFicherosYDirectorios()
        self.miPath = ""
        
    def setPath(self, newPath):
        self.miPath = newPath
        self.arbolDeDirectorios.setRutaDirectorioRaiz(newPath)
        self.arbolDeDirectorios.refleshArbolDirectorios()
    
    def getPath(self):
        self.miPath
        
    def convertirMp3s(self, nuevoPath, bitrate):
        '''
        Devuelve la lista de mp3s a convertir y una lista de comandos para convertirlos. Ejecutará automáticamente el copiaEstructura (nota: 192 es el bitrate (tasa de bits) a minimizar (128 es calidad semi cd, 96 calidad radio FM)).
        '''
        listaPosiblesNuevosMp3 = self.copiaEstructura(nuevoPath)
        listaPosiblesMp3Creados = self.arbolDeDirectorios.toLista()
        listaPosiblesMp3Creados.sort()
        listaMp3ACrear = []
        listaMp3Creados = []
        i = 0
        for elemento in listaPosiblesNuevosMp3:
            if elemento[-4:] == ".mp3":
                listaMp3ACrear = listaMp3ACrear + [elemento]
                listaMp3Creados = listaMp3Creados + [listaPosiblesMp3Creados[i]]
            i = i + 1
        
        i = 0
        listaDeOrdenes = []
        for elemento in listaMp3ACrear:
            nuevaOrden = 'gst-launch -v filesrc location=\"' + listaMp3Creados[i] + '\" ! decodebin ! audioconvert ! audioresample ! lame bitrate=' + bitrate + ' ! id3v2mux ! filesink location=\"' + elemento + '\"'            
            listaDeOrdenes = listaDeOrdenes + [nuevaOrden]
            i = i + 1
        return listaMp3Creados, listaDeOrdenes

    def copiaEstructura(self, nuevoPath):
        '''
        Copia la estructura del directorios (carpetas) actual a un nuevo directorio, no tendrá en cuenta los ficheros.
        '''
        listaDirectoriosACrear = []
        listaDirectoriosACreados = []
        c = self.miPath
        finCadena = len(c[:(-1*len(c.split("/")[-1]))])
        for elemento in self.arbolDeDirectorios:
            listaDirectoriosACreados = listaDirectoriosACreados + [elemento]
            res = ""
            if len(elemento) == finCadena:
                res = nuevoPath
            else:
                res = nuevoPath + "/" + elemento[finCadena:]
            listaDirectoriosACrear = listaDirectoriosACrear + [res]
        
        # Hay que ordenar la listaDirectoriosACrear
        listaDirectoriosACrear.sort()
        listaDirectoriosACreados.sort()
        # Una carpeta sin ficheros no la copiaremos (haremos como si fuera un fichero).
        j = 0
        nuevaLista = []
        for elemento in listaDirectoriosACrear:
            isFile = True
            try:
                fich = open(element, 'r')
                fich.close()
            except:
                isFile = False
            
            if not isFile:
                # Si es directorio comprobar que contiene ficheros mp3s o carpetas.
                listSubDirectorios = None
                try:
                    listSubDirectorios = os.listdir(listaDirectoriosACreados[j])
                except:
                    listSubDirectorios = []
                
                contieneMp3OCarpetas = False
                i = 0
                end = len(listSubDirectorios)
                while (i < end) and (not contieneMp3OCarpetas):
                    nomFile = listSubDirectorios[i]
                    # Si tiene algún punto lo contaremos como fichero.
                    contieneMp3OCarpetas = (nomFile.count(".") == 0) or (nomFile[-4:] == ".mp3")
                    i = i + 1
                # Si la carpeta no está vacía y contiene mp3s u otras carpetas entrará en el siguiente if
                if contieneMp3OCarpetas:
                    #Crear directorio (elemento). Al haberse ordenado antes se creará siempre un directorio padre antes que un directorio hijo.
                    if elemento != nuevoPath:
                        os.mkdir(elemento)
            j = j + 1
        return listaDirectoriosACrear

