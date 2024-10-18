import os
import shutil

class  Directorio:

    def __init__(self, ruta):
        self.ruta = ruta

    def archivos(self):
        return [os.path.join(self.ruta, item) for item in os.listdir(self.ruta) if os.path.isfile(os.path.join(self.ruta, item))]
    
    def carpetas(self):
        return [os.path.join(self.ruta, item) for item in os.listdir(self.ruta) if os.path.isdir(os.path.join(self.ruta, item))]
    
    def all_archivos(self):
        if type(self.ruta)==str:
            rutas = (self.ruta.replace(' ','').replace('\t','')).split(',')
        archivos_all = []
        carpetas_finales = []
        while rutas != []:
            for ruta in rutas:
                archivos_all += Directorio(ruta=ruta).archivos()
                carpetas_finales += Directorio(ruta=ruta).carpetas()
            rutas = carpetas_finales
            carpetas_finales = []
        return archivos_all
    
    def all_carpetas(self):
        if type(self.ruta)==str:
            rutas = (self.ruta.replace(' ','').replace('\t','')).split(',')
        carpetas_all = []
        carpetas_finales = []
        while rutas != []:
            for ruta in rutas:
                carpetas_finales += Directorio(ruta=ruta).carpetas()
            rutas = carpetas_finales
            carpetas_all += carpetas_finales
            carpetas_finales = []
        return carpetas_all
    
class Filtros_formato:
    def __init__(self, rutas, formatos= ''):
        self.rutas = rutas
        self.formatos = formatos
    

    def elejir(self):
        new_lista = []
        if self.formatos == '':
            return new_lista
        else:
            for ruta in self.rutas:
                for formato in (self.formatos.replace(' ','')).split(','):
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
                for formato in (self.formatos.replace(' ','')).split(','):
                    formato_ruta = ruta.split('.')[-1]
                    if formato_ruta.lower() == formato.lower():
                        break
                if not (formato_ruta.lower() == formato.lower()):
                    new_lista.append(ruta)
            return new_lista


class Filtros_carpetas:

    def __init__(self, rutas, carpetas = ''):
        self.rutas = rutas
        self.carpetas = carpetas


    def elejir(self):
        new_lista = []
        if self.carpetas == '':
            return self.rutas
        else:
            for ruta in self.rutas:
                for carpeta in (self.carpetas.replace(' ','')).split(','):
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
                for carpeta in (self.carpetas.replace(' ','')).split(','):
                    if '/' + carpeta +'/' in ruta:
                        break

                if not ('/' + carpeta +'/' in ruta):
                    new_lista.append(ruta)
            return new_lista
        
    
        
class Filtros_archivos:

    def __init__(self, rutas, archivos = '', archivos_eliminados = ''):
        self.rutas = rutas
        self.archivos = archivos

    def elejir(self):
        new_lista = []
        if self.archivos == '':
            return new_lista
        else:
            for ruta in self.rutas:
                for arch in (self.archivos.replace(' ','')).split(','):
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
                for arch in (self.archivos.replace(' ','')).split(','):
                    nombre_archivo = '.'.join(os.path.basename(ruta).split('.')[:-1])
                    if nombre_archivo == arch:
                        break
                if not (nombre_archivo == arch):
                    new_lista.append(ruta)
            return new_lista

class ordenar_directorio:
    def __init__(self,rutas):
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