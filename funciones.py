import numpy as np
import pandas as pd
from math import isnan
import scipy.stats as stats
import os
import shutil

def trans(tabla):
    tabla = [[j for j in i] for i in tabla]
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

def leer_tabla(ruta , nombre = 'tabla 1'):
    if type(ruta) == str:
        tablas = pd.read_excel(ruta, sheet_name=None)
        # Iterar sobre las hojas
        nombres_hojas = []
        all_tablas = []
        for nombre_hoja, dataframe in tablas.items():
            nombres_hojas.append(nombre_hoja.replace('-',' ').replace('_',' '))
            all_tablas.append(dataframe)
        return [nombres_hojas, all_tablas]
    
    if type(ruta) == pd.DataFrame:
        tabla = ruta
        col = [i for i in tabla.columns]
        new_tabla = []
        for lis in tabla.values:
            new_tabla.append([])
            for val in lis:
                try:
                    val_str = str(val).replace(',','.')
                    new_val = float(val_str)
                    new_tabla[-1].append(new_val)
                except:
                    new_tabla[-1].append(val)
        return [[nombre],[pd.DataFrame(dict(zip(col,trans(new_tabla))))]]

def val_significativa(val,cifras_sig, separador_decimales = '.'):
    val_str = str(val).replace(',','.')
    new_val = float(val_str)
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
    texto_tabla += '\t\\end{tabular}\n\t\\caption{' + nombre_cap + '}\n\t\\label{tab:' + nombre_cap.replace(' ','-').replace('_','-') + '}\n\\end{table}\n\n\n'


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

\addto\captionsspanish{\renewcommand{\tablename}{Tabla}}'''
    with open(ruta_carpeta + '/' + 'comandos.tex', 'w', encoding='utf-8') as archivo:
        archivo.write(texto)

def crear_include(ruta_carpeta, texto):
    if type(texto) == list:
        texto = '\n'.join(texto)

    with open(ruta_carpeta + '/' + texto.replace(' ','_').replace('-',' ') +'.tex', 'w', encoding='utf-8') as archivo:
        archivo.write('\\section{' + texto.replace('-',' ').replace('_', ' ') + '} \\label{sec:' + texto.replace(' ','-').replace('_', '-') +'}\n')
    return '\\include{' + texto.replace(' ','_').replace('-',' ') + '}'

def crear_input(ruta_carpeta, texto):
    if type(texto) == list:
        texto = '\n'.join(texto)

    with open(ruta_carpeta + '/' + texto.replace(' ','_').replace('-',' ') +'.tex', 'w', encoding='utf-8') as archivo:
        archivo.write('\\section{' + texto.replace('-',' ').replace('_', ' ') + '} \\label{sec:' + texto.replace(' ','-').replace('_', '-') +'}\n')
    return '\\input{' + texto.replace(' ','_').replace('-',' ') + '}'

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
    n = len(new_lista)
    mean = np.mean(new_lista)
    std_dev = np.std(new_lista, ddof=1)  # Desviación estándar muestral
    
    # Calcular el estadístico de Grubbs

    G_max = max([abs(i - mean) / std_dev for i in new_lista])
    val_g_max = [i for i in new_lista if abs(i - mean) / std_dev == G_max][0]
    
    # Calcular el valor crítico de Grubbs
    t_dist = stats.t.ppf(1 - alpha/(2*n), n-2)  # distribucion t
    G_critical = ((n-1) / np.sqrt(n)) * np.sqrt(t_dist**2 / (n-2 + t_dist**2))
    print(str(G_max) + ' < ' + str(G_critical))
    print(std_dev)
    if std_dev == 0:
        return False, val_g_max
    return G_max > G_critical, val_g_max

def grubbs_multiple(data, alpha=0.05):
    outliers = []
    while True:
        G_max, G_critical = grubbs_test(data, alpha)
        if G_max > G_critical:
            outlier = np.max(np.abs(data - np.mean(data)))
            outliers.append(outlier)
            data.remove(outlier)  # Eliminar el outlier detectado
        else:
            break
    return outliers

def ejercicio_blanca(ruta, confianza = 0.95, cifras_sig = 3, separador_decimales = '.', left = '', center = '', right = '\\today'):

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

        return new_col,new_valores



    nombre_archivo = '.'.join((ruta.split('/')[-1].replace('%20',' ').replace(' ','_')).split('.')[:-1])
    carpeta_latex = crear_carpeta(ruta = '', nombre_carpeta = nombre_archivo)
    crear_carpeta(ruta = carpeta_latex, nombre_carpeta = 'carpeta_img')
    comandos_latex(carpeta_latex)
    texto_main = ''
    texto_main += crear_input(carpeta_latex, 'Objetivo y principio de la práctica') + '\n'
    texto_main += crear_input(carpeta_latex, 'Muestra papel')+ '\n'
    texto_main += crear_input(carpeta_latex, 'Normas a considerar')+ '\n'
    texto_main += crear_input(carpeta_latex, 'Aparatos utilizados')+ '\n'
    texto_main += crear_input(carpeta_latex, 'Condiciones ambientales')+ '\n'
    texto_main += crear_input(carpeta_latex, 'Medidas')+ '\n'
    

    nombres,tablas = leer_tabla(ruta)
    if type(cifras_sig) == list:
        if len(cifras_sig)<len(nombres):
            cifras_sig = [3 for i in nombres]
    elif type(cifras_sig) == str:
        cifras_sig = [3 for i in nombres]
    elif type(cifras_sig) == int or type(cifras_sig) == float:
        cifras_sig = [int(cifras_sig) for i in nombres]
    else:
        return print('Error en el formato de cifras')

    for pos_tab,tabla in enumerate(tablas):
        print(nombres[pos_tab])
        nombre_inicio = nombres[pos_tab] + ' inicio'
        tabla_t =trans(acondicionar_tabla(tabla.values, separador_decimales = separador_decimales, cifras_sig = cifras_sig[pos_tab]))
        tabla_latex = pd.DataFrame(dict(zip(['muestras'] + [i for i in tabla.columns],[['muetra '+str(i+1) for i in range(len(trans(tabla_t)))]] + tabla_t)))
        texto = tabla2latex(tabla_latex, nombre_cap = nombre_inicio , cifras_sig = cifras_sig[pos_tab], separador_decimales = separador_decimales)
        texto_main += '\\input{' + nombre_inicio.replace(' ','_') +'}\n'
        with open(carpeta_latex + '/' + nombre_inicio.replace(' ','_')+'.tex', 'w', encoding='utf-8') as archivo:
            archivo.write(texto)
        display(tabla_latex)
        tabla_in = tabla
        bucle_end = []
        contador = 0
        while True:
            if contador == 0:
                nombre_tb = nombres[pos_tab]
            else:
                nombre_tb = nombres[pos_tab] + ' Grubbs '+str(contador)
            new_col,new_valores = tabla_def(tabla_in)
            medias = []
            val_std = []
            val_max = []
            val_min = []
            intervalo_confianza_mes_menys = []
            intervalo_confianza = []
            for lista in new_valores:
                lista_def = [i for i in lista if not isnan(i)]
                media = np.mean(lista_def)
                v_std = np.std(lista_def)
                medias.append(media) 
                val_std.append(v_std)
                val_max.append(max(lista_def))
                val_min.append(min(lista_def))
                n = len(lista_def)

                # Definir el intervalo de confianza (por ejemplo, 95%)
                
                alfa = 1 - confianza

                # Calcular el valor crítico para el intervalo de confianza deseado (distribución normal)
                valor_critico = stats.norm.ppf(1 - alfa / 2)

                # Definir el intervalo de confianza usando la fórmula correcta
                mes_menys = valor_critico * (v_std / np.sqrt(n))
                limite_inferior = media - mes_menys
                limite_superior = media + mes_menys
                intervalo_confianza_mes_menys.append(str(val_significativa(val = media, cifras_sig = cifras_sig[pos_tab],separador_decimales = separador_decimales)) + ' +- ' + str(val_significativa(val = v_std, cifras_sig = cifras_sig[pos_tab],separador_decimales = separador_decimales)))
                intervalo_confianza.append(str(val_significativa(val = limite_inferior, cifras_sig = cifras_sig[pos_tab],separador_decimales = separador_decimales)) + ' - ' + str(val_significativa(val = limite_superior, cifras_sig = cifras_sig[pos_tab],separador_decimales = separador_decimales)))
            new_valores_t = trans(new_valores)
            tabla_latex = pd.DataFrame(dict(zip(['muestras']+new_col,[['muetra '+str(i+1) for i in range(len(new_valores_t))] + ['medias','Desviacion estandard','valor maximo','valor minimo', 'Intervalo de confianza', 'Intervalo']] + acondicionar_tabla(trans(new_valores_t+[medias, val_std, val_max, val_min, intervalo_confianza_mes_menys, intervalo_confianza]),separador_decimales = separador_decimales, cifras_sig = cifras_sig[pos_tab]))))
            display(tabla_latex)
            print(3*'\n')
            for pos, lista in enumerate(new_valores):
                print(val_std[pos])
                if val_std[pos] != 0:
                    condicion_G, val_g_max = grubbs_test(lista = lista, alpha = alfa)
                    bucle_end.append(condicion_G)
                    if condicion_G:
                        new_valores[pos] = [np.nan if ls == val_g_max else ls for ls in lista]
                else:
                    bucle_end.append(False)

            if True not in bucle_end:
                break

            tabla_in = pd.DataFrame(dict(zip(new_col,new_valores)))
            texto_main += '\\input{' + nombre_tb.replace(' ','_') +'}\n'
            texto = tabla2latex(tabla_latex, nombre_cap = nombre_tb , cifras_sig = cifras_sig[pos_tab], separador_decimales = separador_decimales)
            with open(carpeta_latex + '/' + nombre_tb.replace(' ','_')+'.tex', 'w', encoding='utf-8') as archivo:
                archivo.write(texto)
            contador += 1
        tabla_in = pd.DataFrame(dict(zip(new_col,new_valores)))
        texto_main += '\\input{' + nombre_tb.replace(' ','_') +'}\n'
        texto = tabla2latex(tabla_latex, nombre_cap = nombre_tb , cifras_sig = cifras_sig[pos_tab], separador_decimales = separador_decimales)
        with open(carpeta_latex + '/' + nombre_tb.replace(' ','_')+'.tex', 'w', encoding='utf-8') as archivo:
            archivo.write(texto)
    texto_main += crear_input(carpeta_latex, 'Otros alumnos')+ '\n'
    texto_main += crear_input(carpeta_latex, 'Observaciones')+ '\n'
    crear_main_latex(carpeta_latex, texto_main, left = left, center = center, right = right)


    

    # Crear el archivo ZIP
    shutil.make_archive(os.path.basename(carpeta_latex), 'zip', carpeta_latex)


def ejercicio_cristina(ruta, cifras_sig = 3, separador_decimales = '.', left = '', center = '', right = '\\today'):

    nombre_archivo = '.'.join((ruta.split('/')[-1].replace('%20',' ').replace(' ','_')).split('.')[:-1])
    carpeta_latex = crear_carpeta(ruta = '', nombre_carpeta = nombre_archivo)
    crear_carpeta(ruta = carpeta_latex, nombre_carpeta = 'carpeta_img')
    comandos_latex(carpeta_latex)
    texto_main = ''
    texto_main += crear_input(carpeta_latex, 'Introducción teórica') + '\n'
    texto_main += crear_input(carpeta_latex, 'Objetivo de la práctica')+ '\n'
    texto_main += crear_input(carpeta_latex, 'Materiales y métodos')+ '\n'
    texto_main += crear_input(carpeta_latex, 'Resultados')+ '\n'
    # texto_main += crear_input(carpeta_latex, 'Condiciones ambientales')+ '\n'
    # texto_main += crear_input(carpeta_latex, 'Medidas')+ '\n'
    

    nombres,tablas = leer_tabla(ruta)
    if type(cifras_sig) == list:
        if len(cifras_sig)<len(nombres):
            cifras_sig = [3 for i in nombres]
    elif type(cifras_sig) == str:
        cifras_sig = [3 for i in nombres]
    elif type(cifras_sig) == int or type(cifras_sig) == float:
        cifras_sig = [int(cifras_sig) for i in nombres]
    else:
        return print('Error en el formato de cifras')

    for pos_tab,tabla in enumerate(tablas):
        print(nombres[pos_tab])
        nombre_inicio = nombres[pos_tab]
        tabla_t =trans(acondicionar_tabla(tabla.values, separador_decimales = separador_decimales, cifras_sig = cifras_sig[pos_tab]))
        tabla_latex = pd.DataFrame(dict(zip([i for i in tabla.columns], tabla_t)))
        texto = tabla2latex(tabla_latex, nombre_cap = nombre_inicio , cifras_sig = cifras_sig[pos_tab], separador_decimales = separador_decimales)
        texto_main += '\\input{' + nombre_inicio.replace(' ','_') +'}\n'
        with open(carpeta_latex + '/' + nombre_inicio.replace(' ','_')+'.tex', 'w', encoding='utf-8') as archivo:
            archivo.write(texto)
        display(tabla_latex)
    texto_main += crear_input(carpeta_latex, 'Discusión de Resultados')+ '\n'
    texto_main += crear_input(carpeta_latex, 'Conclusiones')+ '\n'
    crear_main_latex(carpeta_latex, texto_main, left = left, center = center, right = right)


    

    # Crear el archivo ZIP
    shutil.make_archive(os.path.basename(carpeta_latex), 'zip', carpeta_latex)


def ejercicio_oriol(ruta, cifras_sig = 3, separador_decimales = '.', left = '', center = '', right = '\\today'):

    nombre_archivo = '.'.join((ruta.split('/')[-1].replace('%20',' ').replace(' ','_')).split('.')[:-1])
    carpeta_latex = crear_carpeta(ruta = '', nombre_carpeta = nombre_archivo)
    crear_carpeta(ruta = carpeta_latex, nombre_carpeta = 'carpeta_img')
    comandos_latex(carpeta_latex)
    texto_main = ''
    texto_main += crear_input(carpeta_latex, 'Objetivo de la práctica')+ '\n'
    texto_main += crear_input(carpeta_latex, 'Material utilizado')+ '\n'
    texto_main += crear_input(carpeta_latex, 'Normativa aplicable o a tener en cuenta')+ '\n'
    texto_main += crear_input(carpeta_latex, 'Datos experimentales obtenidos (medidas directas obtenidas en el laboratorio)')+ '\n'
    # texto_main += crear_input(carpeta_latex, 'Medidas')+ '\n'
    

    nombres,tablas = leer_tabla(ruta)
    if type(cifras_sig) == list:
        if len(cifras_sig)<len(nombres):
            cifras_sig = [3 for i in nombres]
    elif type(cifras_sig) == str:
        cifras_sig = [3 for i in nombres]
    elif type(cifras_sig) == int or type(cifras_sig) == float:
        cifras_sig = [int(cifras_sig) for i in nombres]
    else:
        return print('Error en el formato de cifras')

    for pos_tab,tabla in enumerate(tablas):
        print(nombres[pos_tab])
        nombre_inicio = nombres[pos_tab]
        tabla_t =trans(acondicionar_tabla(tabla.values, separador_decimales = separador_decimales, cifras_sig = cifras_sig[pos_tab]))
        tabla_latex = pd.DataFrame(dict(zip([i for i in tabla.columns], tabla_t)))
        texto = tabla2latex(tabla_latex, nombre_cap = nombre_inicio , cifras_sig = cifras_sig[pos_tab], separador_decimales = separador_decimales)
        texto_main += '\\input{' + nombre_inicio.replace(' ','_') +'}\n'
        with open(carpeta_latex + '/' + nombre_inicio.replace(' ','_')+'.tex', 'w', encoding='utf-8') as archivo:
            archivo.write(texto)
        display(tabla_latex)
    texto_main += crear_input(carpeta_latex, 'Resultados (Incluyendo factores de conversión y justificando la eliminación de valores discrepantes)')+ '\n'
    texto_main += crear_input(carpeta_latex, 'Análisis, discusión de los resultados y conclusiones')+ '\n'
    crear_main_latex(carpeta_latex, texto_main, left = left, center = center, right = right)


    

    # Crear el archivo ZIP
    shutil.make_archive(os.path.basename(carpeta_latex), 'zip', carpeta_latex)