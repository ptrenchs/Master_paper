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

def schopper_corr(tabla,nombre,ruta):
    x_masa = 2
    nombre_arch_spe = ('.'.join(os.path.basename(ruta).split('.')[:-1])).replace('_',' ').replace('-',' ')
    nombre_arch_sub_bar = nombre_arch_spe.replace(' ','_')
    nombre_spe = nombre.replace('_',' ').replace('-',' ')
    nombre_sub_bar = nombre_spe.replace(' ','_')
    nombre_arch_spe_t = ' '.join([i for i in nombre_arch_spe.split(' ')if not str.isdigit(i)])

    col_,datos_ = tabla.columns,tabla.values
    if len(tabla.values) == 0:
        return tabla
    pos_y = [i for i in range(len(col_)) if 'schopper' in col_[i].lower()]
    # print(pos_y)
    if len(pos_y) == 0:
        return tabla

    tabla_gr = pd.read_csv('https://raw.githubusercontent.com/ptrenchs/Master_paper/main/B1-Oriol-Tecnologia%20de%20la%20fabricacio%20de%20paper/practicas_laboratorio/tablas_grafica_oriol.csv')
    col_gr,datos = tabla_gr.columns,trans(tabla_gr.values)
    pos_x = [i for i,c in enumerate(col_gr) if 'x' in c.lower()][0]
    x_in = np.array(datos[pos_x])
    all_y = [d for i,d in enumerate(datos) if i != pos_x]
    new_reg = []
    plt.figure(figsize=(10,6))
    plt.title(nombre_arch_spe_t + '-' + nombre_spe)
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
        new_tab = []
        for i in range(len(datos_)):
            new_tab.append([j for j in datos_[i]] + [y_masa_corregida_list[i]])
        return pd.DataFrame(dict(zip(new_col,trans(new_tab))))
    else:
        return tabla

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

def val_significativa(val,cifras_sig, separador_decimales = '.'):
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
            return (signe + val_tot_str + abs(len(val_tot_str)-1 - cifras_sig) * '0').replace('.',separador_decimales)
        else:
            return signe + val_tot_str.replace('.',separador_decimales)
    else:
        # if int(val_tot[-2:])z0:
        return (signe + val_sin_e + val_e).replace('.',separador_decimales)


def acondicionar_tabla(tabla, cifras_sig = 3, separador_decimales = '.'):
    tabla= [[j for j in i] for i in tabla]
    new_tabla = []
    if type(cifras_sig) == list and len(cifras_sig) >= len(tabla):
        cifras_sig = [int(cifras_sig[i]) for i in range(len(tabla))]
        for pos,lis in enumerate(tabla):
            new_tabla.append([])
            for val in lis:
                try:
                    new_tabla[-1].append(val_significativa(val,cifras_sig[pos], separador_decimales))
                except:
                    if type(val) == str:
                        new_tabla[-1].append(val)
                    elif isnan(val):
                        new_tabla[-1].append('')
                    else:
                        new_tabla[-1].append(val)
    elif type(cifras_sig) == int or type(cifras_sig) == float or len(cifras_sig) < len(tabla):
        if type(cifras_sig) == list:
            cifras_sig = 3
        cifras_sig = int(cifras_sig)
        for lis in tabla:
            new_tabla.append([])
            for val in lis:
                try:
                    new_tabla[-1].append(val_significativa(val,cifras_sig, separador_decimales))
                except:
                    if type(val) == str:
                        new_tabla[-1].append(val)
                    elif isnan(val):
                        new_tabla[-1].append('')
                    else:
                        new_tabla[-1].append(val)

    return new_tabla




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
            passar_str_num(tabla = dataframe).to_csv(new_ruta_carpeta + '/' + str(n) + '_' + nombre_hoja + '.csv',index = False)
            n += 1


def tabla2latex(tabla, nombre_cap = 'tabla 1', cifras_sig = 3, separador_decimales = '.'):
    
    _, tabla = leer_tabla(tabla)
    tabla = tabla[0]
    # display(tabla)
    columnas, datos = tabla.columns, acondicionar_tabla(tabla.values, cifras_sig, separador_decimales)

    texto_tabla = '''
\\begin{table}[H]
\t\\centering
    '''
    texto_tabla += '\t\\begin{tabular}{|'+'|'.join(['m{'+str(round(float(0.9 * 1/len(columnas)),2))[:5]+'\\textwidth}'for i in columnas])+'|}'

    texto_tabla += '''
\t\t\\hline\n\t\t'''
    col = []
    for i in columnas:
        col.append('\\multicolumn{1}{|m{'+str(round(float(0.9 * 1/len(columnas)),2))[:5]+'\\textwidth}|}{\\textbf{'+ i +r'}}')

    texto_tabla += ' & '.join(col)

    texto_tabla += '\n\t\t\\\\ \\hline\n'

    fila_def = ''
    for i in datos:
        fila = [str(j) for j in i]
        fila_def += '\t\t'+' & '.join(fila) + ' \\\\ \\hline\n'
    texto_tabla += fila_def
    texto_tabla += '\t\\end{tabular}\n\t\\caption{' + nombre_cap + '}\n\t\\label{tab:' + nombre_cap.replace(' ','_').replace('-','_').replace('\t','_') + '}\n\\end{table}\n\n\n'


    return texto_tabla


def crear_carpeta(nombre_carpeta,ruta = ''):
    if ruta != '':
        ruta_carpeta = ruta + '/' + nombre_carpeta
    else:
        ruta_carpeta = nombre_carpeta
    if not os.path.exists(ruta_carpeta):
        os.mkdir(ruta_carpeta)
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

def crear_include_or_input(texto, posicion = '', ruta_carpeta = '', tipo = 'include'):
    if type(texto) == list:
        texto = ' '.join(texto)

    tex_label = texto.replace(' ','_').replace('-','_').replace('\t','_')
    if posicion != '':
        nombre_archivo = str(posicion) + '_' + tex_label
    if ruta_carpeta != '':
        nombre_archivo = ruta_carpeta + '/' +  nombre_archivo
    texto_include = nombre_archivo.split('/')
    if 1 < len(texto_include):
        texto_include = '/'.join(texto_include[1:])

    with open(nombre_archivo +'.tex', 'w', encoding='utf-8') as archivo:
        archivo.write('\\section{' + tex_label.replace('_', ' ') + '} \\label{sec:' + tex_label +'}\n')
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
    if 1 <= n: 
        std_dev = np.std(new_lista, ddof=1)  # Desviación estándar muestral
    elif n == 1:
        std_dev = np.std(new_lista)
    
    # Calcular el estadístico de Grubbs

    G_max = max([abs(i - mean) / std_dev for i in new_lista])
    val_g_max = [i for i in new_lista if abs(i - mean) / std_dev == G_max][0]
    # Calcular el valor crítico de Grubbs
    t_dist = stats.t.ppf(1 - alpha/(2*n), n-2)  # distribucion t
    G_critical = ((n-1) / np.sqrt(n)) * np.sqrt(t_dist**2 / (n-2 + t_dist**2))
    # print(str(G_max) + ' < ' + str(G_critical))
    
    if std_dev == 0:
        return False, [np.nan if val_g_max == i else i for i in lista]
    return G_max > G_critical, [np.nan if val_g_max == i else i for i in lista]

def estadisticos(tabla, confianza = 95, cifras_sig = 3, separador_decimales = '.'):
    confianza = abs(confianza)
    if 1<confianza:
        confianza = confianza / 100
    alfa = 1 - confianza
    
    datos = trans(tabla.values)
    
    
    if len([i for i in datos[0] if type(i) ==str]) != len(datos[0]):
        # tabla = schopper_corr(tabla = tabla,)
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
                    std.append(np.std(dato))
                else:
                    std.append(np.std(dato,ddof=1))
                max_.append(max(dato))
                min_.append(min(dato))
                media_mas_menos.append(f'{val_significativa(val = medias[-1] - stats.norm.ppf(1 - alfa / 2) * (std[-1] / np.sqrt(len(dato))), cifras_sig = cifras_sig, separador_decimales = separador_decimales)} - {val_significativa(val = medias[-1] + stats.norm.ppf(1 - alfa / 2) * (std[-1] / np.sqrt(len(dato))), cifras_sig = cifras_sig, separador_decimales = separador_decimales)}')
                intervalo.append(f'{val_significativa(val = medias[-1] - stats.norm.ppf(1 - alfa / 2) * (std[-1] / np.sqrt(len(dato))), cifras_sig = cifras_sig, separador_decimales = separador_decimales)} - {val_significativa(val = medias[-1] + stats.norm.ppf(1 - alfa / 2) * (std[-1] / np.sqrt(len(dato))), cifras_sig = cifras_sig, separador_decimales = separador_decimales)}')
        
        return pd.DataFrame(dict(zip(col,trans(trans(datos) + [medias, std, max_, min_, media_mas_menos, intervalo]))))
    else:
        return tabla


ruta = "/home/pol-trenchs/Escritorio/Trabajo/3_Resultados/1_Popiedades_fisicomecanicas/1_Inicial_y_refino/3_Refino_5000.csv"
# excel_to_csv(ruta)
tabla = pd.read_csv(ruta)
print(tabla)
tabla = tabla_def(tabla)
print(estadisticos(tabla))

datos = trans(tabla.values)


