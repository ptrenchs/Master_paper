import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import isnan
import scipy.stats as stats
import os
import shutil


# --------------------------------------------------------

class  Directorio:

    def __init__(self, rutas):
        if type(rutas)==str:
             rutas = (rutas.replace(' ','').replace('\t','')).split(',')
        self.rutas = rutas

    def ordenar_lista_num(lista):
        lista_ordenada = []
        lista_no_ordenada = [i for i in lista]
        if lista == []:
            return []
        for orde in [str(i) for i in range(len(lista) + 1)]:
            for lso in lista:
                if '/' in lso:
                    nombre_carp = os.path.basename(lso).replace(' ','_').replace('-','_')
                    if '.' in nombre_carp:
                        nombre_carp = '.'.join(nombre_carp.split('.')[:-1])
                else:
                    nombre_carp = lso.replace(' ','_').replace('-','_')
                if nombre_carp.split('_')[0] == orde or nombre_carp.split('_')[-1] == orde:
                    # print(lista)
                    # print(lso)
                    lista_ordenada.append(lso)
                    lista_no_ordenada.remove(lso)
        return lista_ordenada + lista_no_ordenada

    def archivos(ruta):
        if os.path.isdir(ruta):
            return Directorio.ordenar_lista_num([os.path.join(ruta, item) for item in os.listdir(ruta) if os.path.isfile(os.path.join(ruta, item))])
        else:
            return []
    
    def carpetas(ruta):
        if os.path.isdir(ruta):
            return Directorio.ordenar_lista_num([os.path.join(ruta, item) for item in os.listdir(ruta) if os.path.isdir(os.path.join(ruta, item))])
        else:
            return []
    
    def all_archivos(self):
        archivos_all = []
        lista = []
        rutas = [i for i in self.rutas]
        while rutas != []:
            for ruta in rutas:
                archivos_all += Directorio.archivos(ruta=ruta)
                lista += Directorio.carpetas(ruta=ruta)
            rutas = lista
            lista = []
        return archivos_all
    
    def all_carpetas(self):
        carpetas_all = []
        lista = []
        rutas = [i for i in self.rutas]
        while rutas != []:
            for ruta in rutas:
                lista += Directorio.carpetas(ruta=ruta)
            rutas = lista
            carpetas_all += lista
            lista = []
        return carpetas_all
    
class Filtros_formato:
    def __init__(self, rutas, formatos= ''):
        if type(rutas)==str:
             rutas = (rutas.replace(' ','').replace('\t','')).split(',')
        self.rutas = rutas
        if type(formatos)==str:
             formatos = (formatos.replace(' ','').replace('\t','').replace('.','')).split(',')
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
             carpetas = (carpetas.replace(' ','').replace('\t','')).split(',')
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

                if '/' + carpeta +'/' not in ruta:
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
    

def informacion_ruta(ruta):
    carpeta = '/'.join(ruta.split('/')[:-1])
    nombre = '.'.join(os.path.basename(ruta).split('.')[:-1])
    extension = os.path.basename(ruta).split('.')[-1]
    return carpeta,nombre,extension.lower()
# --------------------------------------------------------


def trans(tabla_original):
    tabla = [[j for j in i] for i in tabla_original]
    if tabla == []:
        return tabla
    tabla_trans = []
    len_list = max([len(i) for i in tabla])
    new_tabla = []
    for i in tabla:
        new_tabla.append(i+[np.nan]*(len_list-len(i)))
    for i in range(len(new_tabla[0])):
        for j in range(len(tabla)):
            if j == 0:
                tabla_trans.append([new_tabla[j][i]])
            else:
                tabla_trans[i].append(new_tabla[j][i])
    return tabla_trans

    

def schopper_corr(tabla,ruta,palabra_clave = 'Carpeta_latex'):
    x_masa = 2
    nombre = '.'.join(os.path.basename(ruta).split('.')[:-1])
    nombre_spe = nombre.replace('_',' ').replace('-',' ')
    nombre_sub_bar = nombre_spe.replace(' ','_')
    ruta_carp = '/'.join(ruta.split('/')[:-1])
    

    col_,datos_ = tabla.columns,tabla.values
    if len(tabla.values) == 0:
        return tabla,''
    pos_y = [i for i in range(len(col_)) if 'schopper' in col_[i].lower()]
    # print(pos_y)
    if len(pos_y) == 0:
        return tabla,''

    tabla_gr = pd.read_csv('https://raw.githubusercontent.com/ptrenchs/Master_paper/main/B1-Oriol-Tecnologia%20de%20la%20fabricacio%20de%20paper/practicas_laboratorio/tablas_grafica_oriol.csv')
    col_gr,datos = tabla_gr.columns,trans(tabla_gr.values)
    pos_x = [i for i,c in enumerate(col_gr) if 'x' in c.lower()][0]
    x_in = np.array(datos[pos_x])
    all_y = [d for i,d in enumerate(datos) if i != pos_x]
    new_reg = []
    plt.figure(figsize=(10,6))
    # plt.title(nombre_arch_spe_t + '-' + nombre_spe)
    for y_in in all_y:
        y = np.array([i for i in y_in if not isnan(i)])
        # len_y = len(y)
        # print(y)
        # x_in
        x = x_in[:len(y)]
        n = 1
        while True:
            coef = np.polyfit(x,y,deg = n)
            y_ajustado = np.polyval(coef,x)

            ss_res = np.sum((y - y_ajustado) ** 2)

            # SS_tot es la suma total de los cuadrados (respecto a la media de y)
            ss_tot = np.sum((y - np.mean(y)) ** 2)

            # R^2
            r2 = 1 - (ss_res / ss_tot)

            if 0.9985 < r2 and 0 < r2:
                break
            n += 1
        new_reg.append(coef)
        # plt.scatter(x,y,label=col_gr)
        new_x = np.linspace(min(x), max(x), 100)
        new_y = np.polyval(coef,new_x)
        # plt.plot(new_x,new_y,label=col_gr)
        plt.plot(new_x,new_y)

    y_masa_corregida_list = []
    pos_x = [i for i in range(len(col_)) if 'mas' in col_[i].lower()]
    for num,punt in enumerate(datos_):
        x = punt[pos_x[0]]
        y = punt[pos_y[0]]
        if x == 0 or y == 0:
            pass
        else:
            new_reg_min = [new_reg[i] for i in range(len(new_reg))]
            dist_1 = [np.polyval(coef,x) - y for coef in new_reg_min]
            pos_min = [abs(i) for i in dist_1].index(min(np.abs(dist_1)))
            y_min = np.polyval(new_reg_min[pos_min],x)
            new_reg_max = [new_reg[i] for i in range(len(new_reg)) if i != pos_min]
            dist_2 = [np.polyval(coef,x) - y for coef in new_reg_max]
            # print(dist)
            pos_max = [abs(i) for i in dist_2].index(min(np.abs(dist_2)))
            y_max = np.polyval(new_reg_max[pos_max],x)
            # print(y_min,y_max)
            y_min_masa = np.polyval(new_reg_min[pos_min],x_masa)
            y_max_masa = np.polyval(new_reg_max[pos_max],x_masa)
            # print(y_max, y_min,y)
            y_masa_corregida = y_max_masa - (y_max - y) / (y_max - y_min) * (y_max_masa - y_min_masa)# (y_max - y) / (y_max - y_min) = (y_max_masa - y_masa_corregida) / (y_max_masa - y_min_masa)
            # print(y_masa_corregida)
            y_masa_corregida_list.append(y_masa_corregida)
            plt.scatter(x,y,label=f'muestra {num+1}')
            plt.scatter(x_masa,y_masa_corregida,label=f'muestra {num+1} corregido')
    plt.xlabel(col_[pos_x[0]])
    plt.ylabel(col_[pos_y[0]])
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    
    new_col = [j for j in col_] + ['Schopper corregido']
    # print(new_col)
    if y_masa_corregida_list != []:
        ruta_img = crear_carpeta(nombre_carpeta = 'Carpeta_img',ruta = ruta_carp) + '/' + nombre_sub_bar + '.png'
        new_tab = []
        for i in range(len(datos_)):
            new_tab.append([j for j in datos_[i]] + [y_masa_corregida_list[i]])
        plt.savefig(ruta_img)    
        return pd.DataFrame(dict(zip(new_col,trans(new_tab)))), figure_latex(ruta_img = ruta_img, ruta_carp_tex=ruta_carp,palabra_clave = palabra_clave)
    else:
        return tabla, ''

def tabla_def(tabla):
    col = [i for i in tabla.columns]
    sec_float = []
    new_valores = []
    new_col = []
    for co in col:
        palabra = co.replace('-',' ').replace('\t',' ').replace('_',' ')
        while True:
            if palabra[0] == ' ':
                palabra = palabra[1:]
            if palabra[-1] == ' ':
                palabra = palabra[:-1]
            if 2*' ' in palabra:
                palabra = palabra.replace(2*' ',' ')
            if palabra[0] != ' ' and palabra[-1] != ' ' and '  ' not in palabra:
                break
        palabra = palabra.split(' ')
        isfloat = False
        for i in range(len(palabra)):
            try:
                int(palabra[i])
                isfloat = True
                pal_antic = ' '.join(palabra[:-1])
                break
            except:
                isfloat = False
        if isfloat:
            sec_float.append([val for val in tabla[co]])
        else:
            if len(sec_float) != 0:
                sec_float = trans(sec_float)
                sec_float = [np.mean(valores) for valores in sec_float]
                new_valores.append(sec_float)
                new_col.append(pal_antic)
                

            new_col.append(co)
            new_valores.append([val for val in tabla[co]])
            sec_float = []

    if isfloat and len(sec_float) != 0:
        sec_float = trans(sec_float)
        sec_float = [np.mean(valores) for valores in sec_float]
        new_valores.append(sec_float)
        new_col.append(pal_antic)

    return pd.DataFrame(dict(zip(new_col,new_valores)))

def passar_str_num(tabla):
    new_tabla = []
    for lis in [[i for i in tabla.columns]] + [i for i in tabla.values]:
        new_tabla.append([])
        for val in lis:
            try:
                val_str = str(val).replace(',','.')
                new_val = float(val_str)
                new_tabla[-1].append(new_val)
            except:
                new_tabla[-1].append(val)
    return pd.DataFrame(dict(zip(new_tabla[0],trans(new_tabla[1:]))))

def leer_tabla(ruta , nombre = 'tabla 1'):
    nombres_hojas = []
    all_tablas = []

    if type(ruta) == str:
        tablas = pd.read_excel(ruta, sheet_name=None)
        
        for nombre_hoja, dataframe in tablas.items():
            nombres_hojas.append(nombre_hoja.replace('-',' ').replace('_',' '))
            tabla = ruta
            all_tablas.append(passar_str_num(dataframe))
        return [nombres_hojas, all_tablas]
    
    if type(ruta) == pd.DataFrame:
        tabla = ruta
        nombres_hojas.append(nombre)
        all_tablas.append(passar_str_num(tabla))
        return [nombres_hojas, all_tablas]

def val_significativa(val,cifras_sig, separador_decimales = '.', cient = True):
    val_str = str(val).replace(',','.')
    new_val = float(val_str)
    # if isnan(new_val):
    #     return new_val
    if new_val < 0:
        signe = '-'
    else:
        signe = ''
    new_val = abs(new_val)   
    val_str = str(f"{new_val:.20f}")
    val_str_int = val_str.split('.')[0]
    val_str_dec = val_str.split('.')[-1]
    if int(val_str_dec) == 0 and int(val_str_int) == 0:
        val_sin_e = '0' + '.' + cifras_sig * '0'
        val_e = 'e+0'
    if int(val_str_dec) == 0 and int(val_str_int) != 0:
        val_sin_e = val_str_int[0] + '.' + val_str_int[1:][:cifras_sig]
        val_e = 'e+' + str(len(val_str_int) - 1)
        val_sig = val_sin_e + 'e+' + str(len(val_str_int) - 1)

    if int(val_str_int) == 0 and int(val_str_dec) != 0:
        for i in range(len(val_str_dec)):
            if val_str_dec[i] != '0':
                break
        val_sin_e = val_str_dec[i] + '.' + val_str_dec[i+1:][:cifras_sig]
        val_e = 'e-' + str(i+1)
        val_sig = val_sin_e + 'e-' + str(i+1)

    if int(val_str_int) != 0 and int(val_str_dec) != 0:
        if len(val_str_int)>cifras_sig:
            val_sin_e = val_str_int[0] + '.' + val_str_int[1:][:cifras_sig-1]
            val_e = 'e+' + str(len(val_str_int) - 1)
            
        else:
            if len(val_str_int) + len(val_str_dec) > cifras_sig:
                val_sin_e = val_str_int[0] + '.' + val_str_int[1:] + val_str_dec[:cifras_sig+1-len(val_str_int)]
                val_e = 'e+' + str(len(val_str_int) - 1)
                val_sig = val_sin_e + 'e+' + str(len(val_str_int) - 1)
            else:
                val_sin_e = val_str_int + '.' + val_str_dec
                val_e = 'e+' + str(len(val_str_int) - 1)

    val_sin_e = str(round(float(val_sin_e),cifras_sig-1))
    # print(val_sin_e)
    val_sin_e = val_sin_e + abs(len(val_sin_e)-1 - cifras_sig) * '0'
    val_tot = val_sin_e + val_e
    if int(val_tot[-2:])<3 and int(val_tot[-2:])>=0:
        val_tot_str = str(float(val_tot))
        if len(val_tot_str)-1<cifras_sig:
            if cient:
                return (signe + val_tot_str + abs(len(val_tot_str)-1 - cifras_sig) * '0').replace('.',separador_decimales)
            else:
                return str(float(signe + val_tot_str + abs(len(val_tot_str)-1 - cifras_sig) * '0')).replace('.',separador_decimales)
        else:
            if cient:
                return signe + val_tot_str.replace('.',separador_decimales)
            else:
                return str(float(signe + val_tot_str)).replace('.',separador_decimales)
    else:
        # if int(val_tot[-2:])z0:
        if cient:
            return (signe + val_sin_e + val_e).replace('.',separador_decimales)
        else:
            return str(float(signe + val_sin_e + val_e)).replace('.',separador_decimales)


def acondicionar_tabla(tabla, cifras_sig = 3, separador_decimales = '.', cient = True):
    datos = tabla.values
    datos = [[j for j in i] for i in datos]
    new_tabla = []
    if type(cifras_sig) == list and len(cifras_sig) >= len(datos):
        cifras_sig = [int(cifras_sig[i]) for i in range(len(datos))]
        for pos,lis in enumerate(datos):
            new_tabla.append([])
            for val in lis:
                try:
                    new_tabla[-1].append(val_significativa(val,cifras_sig[pos], separador_decimales, cient = cient))
                except:
                    if type(val) == str:
                        new_tabla[-1].append(val)
                    elif isnan(val):
                        new_tabla[-1].append('')
                    else:
                        new_tabla[-1].append(val)
    elif type(cifras_sig) == int or type(cifras_sig) == float or len(cifras_sig) < len(datos):
        if type(cifras_sig) == list:
            cifras_sig = 3
        cifras_sig = int(cifras_sig)
        for lis in datos:
            new_tabla.append([])
            for val in lis:
                try:
                    new_tabla[-1].append(val_significativa(val,cifras_sig, separador_decimales, cient = cient))
                except:
                    if type(val) == str:
                        new_tabla[-1].append(val)
                    elif isnan(val):
                        new_tabla[-1].append('')
                    else:
                        new_tabla[-1].append(val)

    return pd.DataFrame(dict(zip(tabla.columns,trans(new_tabla))))




def excel_to_csv(ruta):
    ruta_carpeta = '/'.join(ruta.split('/')[:-1])
    archivo = os.path.basename(ruta)
    formato = archivo.split('.')[-1]
    nombre = '.'.join(archivo.split('.')[:-1])
    if formato.lower() in 'xlsx':
        n = 1
        tablas = pd.read_excel(ruta, sheet_name = None)
        new_ruta_carpeta = crear_carpeta(ruta = ruta_carpeta,nombre_carpeta=nombre)
        for nombre_hoja, dataframe in tablas.items():
            nombre_hoja = nombre_hoja.replace(' ','_').replace('-','_')
            if [i for i in dataframe.columns] != [] and [i for i in dataframe.values] != []:
                print([i for i in dataframe.columns])
                passar_str_num(tabla = dataframe).to_csv(new_ruta_carpeta + '/' + str(n) + '_' + nombre_hoja + '.csv',index = False)
            n += 1

def escribir_doc(ruta_archivo, texto):
    ruta_carp, _, _ = informacion_ruta(ruta_archivo)
    crear_carpeta(ruta = ruta_carp)
    if type(texto) == list:
        texto = '\n'.join(texto)
    with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
        archivo.write(texto)

def corregir_ruta(ruta, palabra_clave = 'Carpeta_latex'):
    ruta_split = ruta.split('/')
    ruta_split = ruta_split[::-1]
    for i,rs in enumerate(ruta_split):
        if palabra_clave in rs:
            return '/'.join(ruta_split[:i][::-1])
    return ruta

def corregir_nombre(nombre):
    # print(nombre)
    for nm in nombre:
        for car in ' \t-_':
            if nm == car:
                break
        if nm == car:
            break
    if nm == car:
        nombre_sp = nombre.split(car)
    else:
        nombre_sp = nombre
    if str.isnumeric(nombre_sp[0]):
        return car.join(nombre_sp[1:])
    else:
        return nombre

def figure_latex(ruta_img, ruta_carp_tex, tipo = 'input', palabra_clave = 'Carpeta_latex'):
    nombre = '.'.join(os.path.basename(ruta_img).split('.')[:-1])
    new_ruta = '/'.join(ruta_img.split('/')[:-1])
    nombre_label = nombre.replace(' ','_').replace('-','_')
    nombre_cap = nombre_label.replace('_',' ')
    texto = ''
    texto += '\n\\begin{figure}[H]\n'
    texto += '\t\\centering\n'
    texto += '\t\\includegraphics[width=\\textwidth]{' + corregir_ruta(ruta = ruta_img, palabra_clave = palabra_clave) + '}\n'
    texto += '\t\\caption{' + corregir_nombre(nombre_cap) + '}\n'
    texto += '\t\\label{fig:' + corregir_ruta(ruta = new_ruta, palabra_clave = palabra_clave).replace(' ','_').replace('-','_').replace('/','_') + '_' + nombre_label + '}\n'
    texto += '\\end{figure}\n'
    escribir_doc(ruta_archivo = ruta_carp_tex + '/' + nombre_label + '_img.tex', texto = texto)

    return '\\' + tipo + '{' + corregir_ruta(ruta = ruta_carp_tex, palabra_clave = palabra_clave) + '/' + nombre_label + '}'

def tabla2latex(tabla, ruta, cifras_sig = 3, separador_decimales = '.',cient = True, tipo = 'input', palabra_clave = 'Carpeta_latex'):
    # print(ruta)
    nombre = '.'.join(os.path.basename(ruta).split('.')[:-1])
    new_ruta = '/'.join(ruta.split('/')[:-1])
    nombre_label = nombre.replace(' ','_').replace('-','_')
    nombre_cap = nombre_label.replace('_',' ')
    # print(tabla)
    tab = acondicionar_tabla(tabla, cifras_sig = cifras_sig, separador_decimales = separador_decimales, cient = cient)
    columnas, datos = tab.columns, tab.values


    texto_tabla = '''
\\begin{table}[H]
\t\\centering
    '''
    texto_tabla += '\t\\begin{tabularx}{\\textwidth}{|'+'|'.join(['X'for i in columnas])+'|}'

    texto_tabla += '''
\t\t\\hline\n\t\t'''


    texto_tabla += ' & '.join(['\\textbf{' + i + '}}' for i in columnas])

    texto_tabla += '\n\t\t\\\\ \\hline\n'

    fila_def = ''
    for i in datos:
        fila = [str(j) for j in i]
        fila_def += '\t\t'+' & '.join(fila) + ' \\\\ \\hline\n'
    texto_tabla += fila_def
    texto_tabla += '\t\\end{tabularx}\n\t\\caption{' + corregir_nombre(nombre_cap) + '}\n\t\\label{tab:' + corregir_ruta(ruta = new_ruta, palabra_clave = palabra_clave).replace(' ','_').replace('-','_').replace('/','_') + '_' + nombre_label + '}\n\\end{table}\n\n\n'



    escribir_doc(ruta_archivo = new_ruta + '/' + nombre_label + '.tex', texto = texto_tabla)

    return '\\' + tipo + '{' + corregir_ruta(ruta = new_ruta, palabra_clave = palabra_clave) + '/' + nombre_label + '}'


def crear_carpeta(nombre_carpeta = '',ruta = ''):
    if nombre_carpeta == '':
        if ruta == '':
            raise ValueError(f"Error")
            
        else:
            ruta_carpeta = ruta
    else:
        if ruta == '':
            ruta_carpeta = nombre_carpeta
        else:
            ruta_carpeta = ruta + '/' + nombre_carpeta
            
    # print(ruta_carpeta)
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta, exist_ok=True)
        while True:
            if os.path.exists(ruta_carpeta):
                break
    return ruta_carpeta



def comandos_latex(ruta_carpeta):
    texto = '''\\usepackage[utf8]{inputenc}
\\usepackage[spanish]{babel}
\\usepackage{graphicx}
\\usepackage{geometry}
\\usepackage{float}
\\usepackage[dvipsnames]{xcolor}
\\usepackage{imakeidx}
\\usepackage{tabularx}
\\usepackage{hyperref}
\\usepackage{fancyhdr}
\\usepackage{setspace}
\\usepackage{parskip}
\\usepackage{wrapfig}
\\usepackage{vmargin}
\\usepackage{ragged2e}
\\usepackage{array}
\\usepackage{lipsum} % Para generar texto de ejemplo
\\setpapersize{A4}
\\setmargins{2.2cm}          % marge esquerre
{0cm}                       % marge superior
{16cm}                    % amplada del text
{23.57cm}                   % altura del text
{55pt}                      % altura capçaleres
{1.25cm}                    % espai entre el text i les capçaleres
{1pt}                       % altura del peu de pàgina
{1.5cm}                     % espai entre el text i el peu de pàgina
%% FI MARGES

\\spacing{1.5}

\\addto\\captionsspanish{\\renewcommand{\\tablename}{Tabla}}'''
    with open(ruta_carpeta + '/' + 'comandos.tex', 'w', encoding='utf-8') as archivo:
        archivo.write(texto)

def crear_include_or_input(ruta, texto='', posicion = '', ruta_carpeta = '', tipo = 'input'):
    if type(texto) == list:
        texto = ' '.join(texto)
    if os.path.isdir(ruta):
        nombre = os.path.basename(ruta)
    if os.path.isfile(ruta):
        nombre = '.'.join(os.path.basename(ruta).split('.')[:-1])
    nombre_archivo = nombre.replace(' ','_').replace('-','_')
    nombre_label = nombre.replace(' ','_').replace('-','_').replace('\t','_')
    if posicion != '':
        nombre_archivo = str(posicion) + '_' + nombre_archivo
    if ruta_carpeta != '':
        nombre_archivo = ruta_carpeta + '/' +  nombre_archivo
    texto_include = nombre_archivo.split('/')
    for i,ti in enumerate(texto_include):
        if 'Carpeta_latex' in ti:
            break
    texto_include = '/'.join(texto_include[i:])

    with open(nombre_archivo +'.tex', 'w', encoding='utf-8') as archivo:
        archivo.write('\\section{' + '_'.join(nombre_label.split('_')[1:]).replace('_', ' ') + '} \\label{sec:' + nombre_label +'}\n' + texto)
    return '\\' + tipo + '{' + texto_include + '}'


def crear_main_latex(ruta_carpeta,texto_medio, left = '', center = '', right = '\\today'):
    if type(texto_medio) == list:
        texto_medio = '\n'.join(texto_medio)
    texto = '\\documentclass{article}\n'
    texto += '\\include{comandos}\n'
    texto += '\\fancyhead[L]{'+ left +'}\n'
    texto += '\\fancyhead[C]{'+ center +'}\n'
    texto += '\\fancyhead[R]{'+ right +'}\n'
    texto += '\\fancyfoot[C]{\\thepage}\n'
    texto += '\\begin{document}\n'
    texto += '\\pagestyle{fancy}\n\n'
    texto += texto_medio
    texto += '\n\\end{document}'
    with open(ruta_carpeta + '/' + 'main.tex', 'w', encoding='utf-8') as archivo:
        archivo.write(texto)


def grubbs_test(lista, alpha=0.05):
    new_lista = [i for i in lista if not isnan(i)]
    if new_lista == []:
        return False, lista
    n = len(new_lista)
    mean = np.mean(new_lista)
    if 1 < n: 
        std_dev = np.std(new_lista, ddof=1)  # Desviación estándar muestral
    else:
        std_dev = np.std(new_lista)
    if std_dev == 0:
        return False, new_lista
    # Calcular el estadístico de Grubbs
    
    G_s = [abs(i - mean) / std_dev for i in new_lista]
    G_max = max([abs(i - mean) / std_dev for i in new_lista])
    pos_max = G_s.index(G_max)
    val_g_max = [i for i in new_lista][pos_max]
    # Calcular el valor crítico de Grubbs
    t_dist = stats.t.ppf(1 - alpha/(2*n), n-2)  # distribucion t
    G_critical = ((n-1) / np.sqrt(n)) * np.sqrt(t_dist**2 / (n-2 + t_dist**2))
    # print(str(G_max) + ' < ' + str(G_critical))
    
    
    return G_max > G_critical, [np.nan if val_g_max == i else i for i in lista]

def estadisticos_y_grubbs(tabla, ruta, confianza = 95, cifras_sig = 3, separador_decimales = '.', cient = True, palabra_clave = 'Carpeta_latex'):
    
    list_inputs = []

    # print(acondicionar_tabla(tabla, cifras_sig = cifras_sig, separador_decimales = separador_decimales, cient = cient))
 
    list_inputs.append(tabla2latex(tabla, ruta, cifras_sig = cifras_sig, separador_decimales = separador_decimales, cient = cient, tipo = 'input', palabra_clave = palabra_clave))

    confianza = abs(confianza)
    if 1<confianza:
        confianza = confianza / 100
    alfa = 1 - confianza
    
    datos = trans(tabla.values)
    
    
    if len([i for i in datos[0] if type(i) ==str]) != len(datos[0]):
        tabla, tx = schopper_corr(tabla = tabla, ruta= ruta, palabra_clave = palabra_clave)
        list_inputs.append(tx)
        datos = trans(tabla.values)
        for i in range(len(datos)):
            while True:
                condi, dat = grubbs_test(datos[i],alpha=alfa)
                if not condi:
                    break
                datos[i] = dat
        col = ['Muestras'] + [i for i in tabla.columns]
        datos = [[f'Muestra {i}' for i in range(len(datos[0]))]] + datos
        medias = ['Medias'] 
        std = ['Std']
        max_ = ['Min']
        min_ = ['Max']
        media_mas_menos = ['int. conf']
        intervalo = ['Intervalo']
        for dat in datos[1:]:
            dato = [i for i in dat if not isnan(i)]
            if dato ==[]:
                medias.append(np.nan)
                std.append(np.nan)
                max_.append(np.nan)
                min_.append(np.nan)
                media_mas_menos.append(np.nan)
                intervalo.append(np.nan)
            else:
                medias.append(np.mean(dato))
                if 1 < len(dato):
                    std.append(np.std(dato,ddof=1))
                else:
                    std.append(np.std(dato))
                max_.append(max(dato))
                min_.append(min(dato))
                media_mas_menos.append(f'{val_significativa(val = medias[-1] - stats.norm.ppf(1 - alfa / 2) * (std[-1] / np.sqrt(len(dato))), cifras_sig = cifras_sig, separador_decimales = separador_decimales, cient = cient)} - {val_significativa(val = medias[-1] + stats.norm.ppf(1 - alfa / 2) * (std[-1] / np.sqrt(len(dato))), cifras_sig = cifras_sig, separador_decimales = separador_decimales, cient = cient)}')
                intervalo.append(f'{val_significativa(val = medias[-1] - stats.norm.ppf(1 - alfa / 2) * (std[-1] / np.sqrt(len(dato))), cifras_sig = cifras_sig, separador_decimales = separador_decimales, cient = cient)} - {val_significativa(val = medias[-1] + stats.norm.ppf(1 - alfa / 2) * (std[-1] / np.sqrt(len(dato))), cifras_sig = cifras_sig, separador_decimales = separador_decimales, cient = cient)}')
        tabla_def = pd.DataFrame(dict(zip(col,trans(trans(datos) + [medias, std, max_, min_, media_mas_menos, intervalo]))))
        carp_ruta = '/'.join(ruta.split('/')[:-1])
        nomb = '.'.join(os.path.basename(ruta).split('.')[:-1])
        formato = os.path.basename(ruta).split('.')[-1]
        new_ruta = carp_ruta + '/' + nomb + '_definitiva' + '.' + formato
        list_inputs.append(tabla2latex(tabla = tabla_def, ruta = new_ruta, cifras_sig = cifras_sig, separador_decimales = separador_decimales, cient = cient, tipo = 'input',palabra_clave = palabra_clave))
        return pd.DataFrame(dict(zip(col,trans(trans(datos) + [medias, std, max_, min_, media_mas_menos, intervalo])))), '\n'.join(list_inputs)
    else:
        return tabla,''


# ruta = "/home/pol-trenchs/Escritorio/Trabajo/3_Resultados/1_Popiedades_fisicomecanicas/1_Inicial_y_refino/3_Refino_5000.csv"
# ruta_ini = "/home/pol-trenchs/Escritorio/Trabajo/"
ruta_ini = "/home/ptrenchs/Escritorio/Trabajo"
confianza = 95
cifras_sig = 3
separador_decimales = '.'
cient = False
palabra_clave = 'latex'

if str.endswith(ruta_ini,'/'):
    ruta_ini = ruta_ini[:-1]

ob_dir = Directorio(rutas=ruta_ini)
exc_arch = Filtros_formato(ob_dir.all_archivos(), 'xlsx').elejir()
# print(exc_arch)
for ea in exc_arch:
    excel_to_csv(ea)
titulo_1 = os.path.basename(ruta_ini)
ob_dir = Directorio(rutas=ruta_ini)


carpetas = []
lista_dic = []
# archivos = []
n = 0
rutas = [i for i in [ruta_ini]]
while True:
    all_sub = []
    sub_lista = []
    for ruta in rutas:
        carp = Directorio.carpetas(ruta=ruta)
        arch = Filtros_formato(Directorio.archivos(ruta=ruta),'csv,tex').elejir()
        all_ = Directorio.ordenar_lista_num(arch + carp)
        sub_lista.append(all_)
        all_sub += all_
        carpetas += carp

    lista_dic.append(dict(zip(rutas ,sub_lista)))
    rutas = carpetas
    if rutas == [] or n == 3:
        break
    carpetas = []
    n += 1

new_carpeta = os.path.basename(ruta_ini)

lista_dic = lista_dic[::-1]
new_text = []
for i,ld in enumerate(lista_dic):  
    for clave, valor in ld.items():
        texto_list = []
        # print(clave)
        for val in valor:
            if i < 3:
                texto_list.append('\\' + (n - i -1) * 'sub' + 'section{' + corregir_nombre(os.path.basename(val).replace('_',' ').replace('-',' ')) + '}')
                print(i * '\t' + '\\' + (n - i -1) * 'sub' + 'section{' + corregir_nombre(os.path.basename(val).replace('_',' ').replace('-',' ')) + '}')
            else:
                texto_list.append('\\' + 'capitulo{' + corregir_nombre(os.path.basename(val).replace('_',' ').replace('-',' '))+ '}')
                print(i * '\t' + '\\' + 'capitulo{' + corregir_nombre(os.path.basename(val).replace('_',' ').replace('-',' '))+ '}')
            new_val = val.replace('/' + titulo_1 + '/', '/' + titulo_1 + '_' + palabra_clave + '/')
            print(val)
            if os.path.isfile(val):
                carp_,nomb_,forma_ = informacion_ruta(ruta = val)
                if forma_ == 'csv':
                    tabla = pd.read_csv(val)
                    _,lista_inputs = estadisticos_y_grubbs(tabla = pd.read_csv(val), ruta = new_val, confianza = confianza, cifras_sig = cifras_sig, separador_decimales = separador_decimales, cient = cient, palabra_clave = palabra_clave)
                    texto_list.append(lista_inputs)
                else:
                    pass
            if os.path.isdir(val):
                texto_list.append('\\include{' + corregir_ruta(ruta = new_val + '/' + os.path.basename(new_val) + '_branch', palabra_clave =palabra_clave)+'}')
                
                
                # new_val = '/'.join(new_val.split('/')[:-1]) + '/' + os.path.basename(new_val)
            print(i * '\t' + os.path.basename(new_val))
            # print(val)
            # print(new_val)
        if i<len(lista_dic) -1:
            new_clave = clave.replace('/' + titulo_1 + '/', '/' + titulo_1 + '_' + palabra_clave + '/')
            ruta_new_clave = new_clave + '/' + os.path.basename(new_clave) + '_branch.tex'
        else:
            new_clave = clave.replace('/' + titulo_1 , '/' + titulo_1 + '_' + palabra_clave )
            ruta_new_clave = new_clave + '/' + 'main.tex'
        escribir_doc(ruta_archivo = ruta_new_clave,texto = texto_list)
        print('\n'.join(texto_list))
        print('\n')
    print('\n')
    # print(ld)
lista_dic[-1]

# if n == 3:
#     for i,ld in enumerate(lista_dic[::-1]):
#         if i == len(lista_dic)-1:
#             print('creacion del main')
#             for clave, valor in ld.items():
#                 for val in valor:
#                     new_val = val.replace('/' + titulo_1 + '/', '/' + titulo_1 + '_latex/')
#                     if os.path.basename(new_val).split('.')[-1].lower() == 'xlsx':
#                         new_val = '/'.join(new_val.split('/')[:-1]) + '/' + '.'.join(os.path.basename(new_val).split('.')[:-1]) + '_main'
#                     else:
#                         new_val = '/'.join(new_val.split('/')[:-1]) + '/' + os.path.basename(new_val) + '_main'
#                     print(i * '\t' + os.path.basename(new_val))
#             # print([[os.path.basename(i) for i in valor] for clave, valor in ld.items()])
#         elif i == len(lista_dic)-2:
#             print('Creacion de los ' + 'capitulo')
#             for clave, valor in ld.items():
#                 for val in valor:
#                     new_val = val.replace('/' + titulo_1 + '/', '/' + titulo_1 + '_latex/')
#                     if os.path.basename(new_val).split('.')[-1].lower() == 'xlsx':
#                         new_val = '/'.join(new_val.split('/')[:-1]) + '/' + '.'.join(os.path.basename(new_val).split('.')[:-1]) + '_main'
#                     else:
#                         new_val = '/'.join(new_val.split('/')[:-1]) + '/' + os.path.basename(new_val) + '_main'
#                     print(i * '\t' + os.path.basename(new_val))
#         else:
#             print('Creacion de los ' + (i-2) * 'sub' + 'section')
#             for clave, valor in ld.items():
#                 for val in valor:
#                     new_val = val.replace('/' + titulo_1 + '/', '/' + titulo_1 + '_latex/')
#                     if os.path.basename(new_val).split('.')[-1].lower() == 'xlsx':
#                         new_val = '/'.join(new_val.split('/')[:-1]) + '/' + '.'.join(os.path.basename(new_val).split('.')[:-1]) + '_main'
#                     else:
#                         new_val = '/'.join(new_val.split('/')[:-1]) + '/' + os.path.basename(new_val) + '_main'
#                     print(i * '\t' + os.path.basename(new_val))





#         for clave, valor in ld.items():
#             print(i * '\t'+ os.path.basename(clave))


# else:
#     for i,ld in enumerate(lista_dic):
#         if i == 0:
#             print('creacion del main')
#         else:
#             print('Creacion de los ' + (i-2) * 'sub' + 'section')
#         for clave, valor in ld.items():
#             print(i * '\t'+ os.path.basename(clave))


# confianza = 95
# cifras_sig = 3
# separador_decimales = '.'
# cient = False
# palabra_clave = 'Carpeta_latex'
# tabla = pd.read_csv(ruta)

# tabla = tabla_def(tabla)
# ruta_guardar = '/'.join(ruta.split('/')[:-1])
# nombre = os.path.basename(ruta)
# estadisticos_y_grubbs(tabla = tabla, ruta_guardar = ruta_guardar, nombre = nombre, confianza = confianza, cifras_sig = cifras_sig, separador_decimales = separador_decimales, cient = cient)


