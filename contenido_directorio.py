import os
import shutil

class  Directorio:

    def __init__(self, rutas):
        if type(rutas)==str:
             rutas = (rutas.replace(' ','').replace('\t','')).split(',')
        self.rutas = rutas


    def archivos(ruta):
        return [os.path.join(ruta, item) for item in os.listdir(ruta) if os.path.isfile(os.path.join(ruta, item))]
    
    def carpetas(ruta):
        return [os.path.join(ruta, item) for item in os.listdir(ruta) if os.path.isdir(os.path.join(ruta, item))]
    
    def all_archivos(self):
        archivos_all = []
        carpetas_finales = []
        rutas = [i for i in self.rutas]
        while rutas != []:
            for ruta in rutas:
                archivos_all += Directorio.archivos(ruta=ruta)
                carpetas_finales += Directorio.carpetas(ruta=ruta)
            rutas = carpetas_finales
            carpetas_finales = []
        return archivos_all
    
    def all_carpetas(self):
        carpetas_all = []
        carpetas_finales = []
        rutas = [i for i in self.rutas]
        while rutas != []:
            for ruta in rutas:
                carpetas_finales += Directorio.carpetas(ruta=ruta)
            rutas = carpetas_finales
            carpetas_all += carpetas_finales
            carpetas_finales = []
        return carpetas_all
    
class Filtros_formato:
    def __init__(self, rutas, formatos= ''):
        if type(rutas)==str:
             rutas = (rutas.replace(' ','').replace('\t','')).split(',')
        self.rutas = rutas
        if type(formatos)==str:
             formatos = (formatos.replace(' ','').replace('\t','')).split(',')
        self.formatos = formatos
    

    def elejir(self):
        new_lista = []
        if self.formatos == '':
            return new_lista
        else:
            for ruta in self.rutas:
                for formato in self.formatos:
                    formato_ruta = ruta.split('.')[-1]
                    if formato_ruta.lower() == formato.lower():
                        new_lista.append(ruta)
                        break
            return new_lista
    
    def eliminar(self):
        new_lista = []
        if self.formatos == '':
            return new_lista
        else:
            for ruta in self.rutas:
                for formato in self.formatos:
                    formato_ruta = ruta.split('.')[-1]
                    if formato_ruta.lower() == formato.lower():
                        break
                if not (formato_ruta.lower() == formato.lower()):
                    new_lista.append(ruta)
            return new_lista


class Filtros_carpetas:

    def __init__(self, rutas, carpetas = ''):
        if type(rutas)==str:
             rutas = (rutas.replace(' ','').replace('\t','')).split(',')
        self.rutas = rutas
        if type(carpetas)==str:
             rutas = (carpetas.replace(' ','').replace('\t','')).split(',')
        self.carpetas = carpetas


    def elejir(self):
        new_lista = []
        if self.carpetas == '':
            return self.rutas
        else:
            for ruta in self.rutas:
                for carpeta in self.carpetas:
                    if '/' + carpeta +'/' in ruta:
                        new_lista.append(ruta)
                        break
            return new_lista
        
    def eliminar(self):
        new_lista = []
        if self.carpetas == '':
            return self.rutas
        else:
            for ruta in self.rutas:
                for carpeta in self.carpetas:
                    if '/' + carpeta +'/' in ruta:
                        break

                if not ('/' + carpeta +'/' in ruta):
                    new_lista.append(ruta)
            return new_lista
        
    
        
class Filtros_archivos:

    def __init__(self, rutas, archivos = ''):
        if type(rutas)==str:
             rutas = (rutas.replace(' ','').replace('\t','')).split(',')
        self.rutas = rutas
        if type(archivos)==str:
             archivos = (archivos.replace(' ','').replace('\t','')).split(',')
        self.archivos = archivos

    def elejir(self):
        new_lista = []
        if self.archivos == '':
            return new_lista
        else:
            for ruta in self.rutas:
                for arch in self.archivos:
                    nombre_archivo = '.'.join(os.path.basename(ruta).split('.')[:-1])
                    if nombre_archivo == arch:
                        new_lista.append(ruta)
                        break
            return new_lista
    
    def eliminar(self):
        new_lista = []
        if self.archivos == '':
            return new_lista
        else:
            for ruta in self.rutas:
                for arch in self.archivos:
                    nombre_archivo = '.'.join(os.path.basename(ruta).split('.')[:-1])
                    if nombre_archivo == arch:
                        break
                if not (nombre_archivo == arch):
                    new_lista.append(ruta)
            return new_lista

class ordenar_directorio:
    def __init__(self,rutas):
        if type(rutas)==str:
             rutas = (rutas.replace(' ','').replace('\t','')).split(',')
        self.rutas = rutas

    def ordenar(self):
        new_lista = []
        for ruta in self.rutas:
            formato = ruta.split('.')[-1]
            carpeta_archivo = ruta.split('/')[-2]
            carpeta_formato = 'Carpeta_' + formato
            if carpeta_archivo != carpeta_formato:
                archivo = os.path.basename(ruta)
                old_ruta_carp = '/'.join(ruta.split('/')[:-1])
                new_ruta_carp = old_ruta_carp + '/' + carpeta_formato
                os.makedirs(new_ruta_carp, exist_ok=True)
                shutil.move(old_ruta_carp + '/' + archivo,new_ruta_carp + '/' + archivo)
                new_lista.append(new_ruta_carp + '/' + archivo)
            else:
                new_lista.append(ruta)
        return new_lista