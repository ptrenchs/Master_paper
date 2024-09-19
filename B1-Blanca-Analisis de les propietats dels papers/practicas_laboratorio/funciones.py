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

def leer_tabla(ruta):
    if type(ruta) == str:
        tabla = pd.read_excel(ruta)
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
    return pd.DataFrame(dict(zip(col,trans(new_tabla))))

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
    
    tabla = leer_tabla(tabla)
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
    for i in trans(datos):
        fila = [str(j) for j in i]
        fila_def += '\t\t'+' & '.join(fila) + ' \\\\ \n'
    texto_tabla += fila_def
    texto_tabla += '\t\t\\hline\n\t\\end{tabular}\n\t\\caption{' + nombre_cap + '}\n\t\\label{tab:' + nombre_cap.replace(' ','-').replace('_','-') + '}\n\\end{table}'


    print(texto_tabla)
