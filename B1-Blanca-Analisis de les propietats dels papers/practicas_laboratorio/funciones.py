import numpy as np
import pandas as pd
from math import isnan

def trans(tabla):
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
    val_str = str(f"{new_val:.20f}")
    val_str_int = val_str.split('.')[0]
    val_str_dec = val_str.split('.')[-1]
    if int(val_str_dec) == 0 and int(val_str_int) == 0:
        val_sig = '0' + '.' + cifras_sig * '0'

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
    val_sin_e = val_sin_e + abs(len(val_sin_e)-1 - cifras_sig) * '0'
    val_tot = val_sin_e + val_e
    if int(val_tot[-2:])<3 and int(val_tot[-2:])>=0:
        val_tot_str = str(float(val_tot))
        if len(val_tot_str)-1<cifras_sig:
            return (val_tot_str + abs(len(val_tot_str)-1 - cifras_sig) * '0').replace('.',separador_decimales)
        else:
            return val_tot_str.replace('.',separador_decimales)
    else:
        # if int(val_tot[-2:])z0:
        return (val_sin_e + val_e).replace('.',separador_decimales)


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
    texto_tabla += '\t\\begin{tabular}{|'+'|'.join(['m{'+str(round(float(1/len(columnas)),3))+'\\textwidth}'for i in columnas])+'|}'

    texto_tabla += '''
\t\t\\hline\n\t\t'''
    col = []
    for i in columnas:
        col.append('\\multicolumn{1}{|c|}{\\textbf{'+ i +r'}}')

    texto_tabla += ' & '.join(col)

    texto_tabla += '\n\t\t\\\\\\hline\n'

    fila_def = ''
    for i in datos:
        fila = [str(j) for j in i]
        fila_def += '\t\t'+' & '.join(fila) + ' \\\\ \n'
    texto_tabla += fila_def
    texto_tabla += '\t\t\\hline\n\t\\end{tabular}\n\t\\caption{' + nombre_cap + '}\n\t\\label{tab:' + nombre_cap.replace(' ','-').replace('_','-') + '}\n\\end{table}\n\n\n'


    return texto_tabla

def ejercicio_blanca(ruta, cifras_sig = 3, separador_decimales = '.'):

    def calculos_medias_std(tabla):
        col = [i for i in tabla.columns]
        medias = []
        val_max = []
        val_min = []
        val_std = []
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
            for i in range(len(palabra)):
                try:
                    float(palabra[i])
                    isfloat = True
                    pal_antic = ' '.join(palabra[:-1])
                except:
                    isfloat = False
            if isfloat:
                sec_float.append(tabla[co])
            else:
                if len(sec_float) > 0:
                    sec_float = np.transpose(sec_float)
                    sec_float = [np.mean(valores) for valores in sec_float]
                    new_valores.append(sec_float)
                    medias.append(np.mean(sec_float))
                    val_std.append(np.std(sec_float,ddof=1))
                    val_max.append(max(sec_float))
                    val_min.append(min(sec_float))
                    new_col.append(pal_antic)
                new_col.append(co)
                new_valores.append([val for val in tabla[co]])
                medias.append(np.mean(tabla[co]))
                val_std.append(np.std(tabla[co],ddof=1))
                val_max.append(max(tabla[co]))
                val_min.append(min(tabla[co]))
                sec_float = []
        return new_col,new_valores,val_std,medias,val_max,val_min


    _,tabla_Grubbs = leer_tabla(ruta = 'https://raw.githubusercontent.com/ptrenchs/Master_paper/main/B1-Blanca-Analisis%20de%20les%20propietats%20dels%20papers/practicas_laboratorio/tabla_Grubbs.xlsx' , nombre = 'tabla 1')
    tabla_Grubbs = tabla_Grubbs[0]
    for pos in (tabla_Grubbs['Number of Observations']):
        if pos == 10:
            break
    num_g = tabla_Grubbs['Upper 2.5% Significance: Level'][pos]

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
        display(tabla)
        display([i for i in tabla.values])
        tabla_latex = pd.DataFrame(zip([i for i in tabla.columns], acondicionar_tabla([i for i in tabla.values],separador_decimales = separador_decimales, cifras_sig = cifras_sig[pos_tab])))
        texto = tabla2latex(tabla_latex, nombre_cap = nombre_inicio , cifras_sig = cifras_sig[pos_tab], separador_decimales = separador_decimales)
        with open(nombre_inicio.replace(' ','_')+'.tex', 'w', encoding='utf-8') as archivo:
            archivo.write(texto)
        display(tabla_latex)
        tabla_in = tabla
        bucle = True
        bucle_end = True
        contador = 0
        while True:
            if contador == 0:
                nombre_tb = nombres[pos_tab]
            else:
                nombre_tb = nombres[pos_tab] + ' '+str(contador)
            new_col,new_valores,val_std,medias,val_max,val_min = calculos_medias_std(tabla_in)
            new_valores_t = trans(new_valores)
            tabla_latex = pd.DataFrame(dict(zip(['muestras']+new_col,[['muetra '+str(i+1) for i in range(len(new_valores_t))] + ['medias','Desviacion estandard','valor maximo','valor minimo']] + acondicionar_tabla(trans(new_valores_t+[medias,val_std,val_max,val_min]),separador_decimales = separador_decimales, cifras_sig = cifras_sig[pos_tab]))))
            display(tabla_latex)
            print(3*'\n')
            for pos, lista in enumerate(new_valores):
                val_provis = [ls for ls in lista if abs(ls-medias[pos])/val_std[pos] < num_g  or isnan(ls)] # or not isnan(abs(ls-medias[pos])/val_std[pos])
                if len(val_provis) != len(new_valores[pos]) and bucle:
                    new_valores[pos] = [ls if abs(ls-medias[pos])/val_std[pos] < num_g else np.nan for ls in lista]
                    bucle_end = False
            if bucle_end:
                break
            tabla_in = pd.DataFrame(dict(zip(new_col,new_valores)))
            texto = tabla2latex(tabla_latex, nombre_cap = nombre_tb , cifras_sig = cifras_sig[pos_tab], separador_decimales = separador_decimales)
            with open(nombre_tb.replace(' ','_')+'.tex', 'w', encoding='utf-8') as archivo:
                archivo.write(texto)
            contador += 1
        tabla_in = pd.DataFrame(dict(zip(new_col,new_valores)))
        texto = tabla2latex(tabla_latex, nombre_cap = nombre_tb , cifras_sig = cifras_sig[pos_tab], separador_decimales = separador_decimales)
        with open(nombre_tb.replace(' ','_')+'.tex', 'w', encoding='utf-8') as archivo:
            archivo.write(texto)
