# Import the code for the dialog
import os.path
import sys, os
from time import perf_counter
# Importing libs
import numpy as np
from functools import wraps
# import matplotlib as plt
from osgeo import ogr, gdal, gdalconst
# import matplotlib.pyplot as plt
from pathlib import Path
import matplotlib.pyplot as plt
from modulos_files.RDC_variables import RDCVariables
from modulos_files.global_variables import GlobalVariables
import glob

class DesenvolvePlugin():
    '''Criada para testar e desenvolver as funções do módulo hidroPixel'''
    
    def __init__(self):
        # Criando instâncias das classes de criação de variáveis
        self.global_vars = GlobalVariables(0,0)
        self.rdc_vars = RDCVariables(0,0)
        self.alfa, self.delta_t, self.criterio_parada, self.beta = 0,0,0,0
        self.numero_total_pix = 0
        self.num_intervalos = 0
        self.volume_total = 0.0 
        self.quantidade_blocos_chuva = 0
        self.chuva_excedente_calc = 0
        self.blocos_vazao = 0
        self.Pexc = 0
        self.fim, self.inicio = 0,0
        self.diretorio_atual = os.path.dirname(os.path.abspath(__file__))

    def optimize(func):
        '''Esta função utiliza métodos python para otimizar o código, gerando um cache para os resultados do usuário'''
        cache = {}

        @wraps(func)
        def wrapper(*args,**kwargs):
            key = str(args) + str(kwargs)

            if key not in cache:
                cache[key] = func(*args,**kwargs)

            return cache[key]
            
        return wrapper
    def close_gui(self, function):
        '''Está função é usada para torna nulo (limpar) as informações adicionadas nos diferentes objetos das funções do Hidropixel Plugin
           - Function = 1 : Flow travel time
           - Function = 2 : Excess rainfall
           - Function = 3 : Flow routing'''

        if function == 1:
            # Verifica se alguma lineEdit sobreu alteração: modifica a execução da função close
            line_edit_list = [
                self.dlg_flow_tt.le_1_pg1.text(),
                self.dlg_flow_tt.le_5_pg1.text(),
                self.dlg_flow_tt.le_6_pg1.text(),
                self.dlg_flow_tt.le_7_pg1.text(),
                self.dlg_flow_tt.le_8_pg1.text(),
                self.dlg_flow_tt.le_9_pg1.text(),
                self.dlg_flow_tt.le_10_pg1.text(),
                self.dlg_flow_tt.le_11_pg1.text(),
                self.dlg_flow_tt.le_12_pg1.text(),
                self.dlg_flow_tt.le_14_pg1.text(),
                self.dlg_flow_tt.le_15_pg1.text(),
                self.dlg_flow_tt.le_16_pg1.text(),
                self.dlg_flow_tt.le_17_pg1.text(),
                self.dlg_flow_tt.le_18_pg1.text(),
                self.dlg_flow_tt.le_19_pg1.text(),
                self.dlg_flow_tt.le_21_pg1.text(),
                self.dlg_flow_tt.le_1_pg2.text(),
                self.dlg_flow_tt.le_2_pg2.text(),
                self.dlg_flow_tt.le_3_pg2.text(),
                self.dlg_flow_tt.le_4_pg2.text(),
                self.dlg_flow_tt.le_5_pg2.text(),
                self.dlg_flow_tt.le_6_pg2.text(),
                self.dlg_flow_tt.le_8_pg2.text(),
                self.dlg_flow_tt.le_9_pg2.text(),
                self.dlg_flow_tt.le_10_pg2.text(),
                self.dlg_flow_tt.le_6_pg4.text(),
                self.dlg_flow_tt.le_7_pg4.text(),
                self.dlg_flow_tt.le_8_pg4.text(),
                self.dlg_flow_tt.le_9_pg4.text(),
                self.dlg_flow_tt.le_10_pg4.text(),
                self.dlg_flow_tt.le_11_pg4.text()
            ]

            # Verifica se algum elemento da lista de line_edits foi modificado
            if any(item != '' for item in line_edit_list) and self.save_result == False:
                while True:

                    result = "Wait! You did not save your changes. Are you sure you want to close?"
                    reply = QMessageBox.warning(None, "Changes not saved", result, QMessageBox.Ok | QMessageBox.Cancel)
                    if reply == QMessageBox.Cancel:
                        break

                    else: 
                        # Limpando as informações armazenadas: line edit
                        self.dlg_flow_tt.le_1_pg1.clear()
                        self.dlg_flow_tt.le_5_pg1.clear()
                        self.dlg_flow_tt.le_6_pg1.clear()
                        self.dlg_flow_tt.le_7_pg1.clear()
                        self.dlg_flow_tt.le_8_pg1.clear()
                        self.dlg_flow_tt.le_9_pg1.clear()
                        self.dlg_flow_tt.le_10_pg1.clear()
                        self.dlg_flow_tt.le_11_pg1.clear()
                        self.dlg_flow_tt.le_12_pg1.clear()
                        self.dlg_flow_tt.le_13_pg1.clear()
                        self.dlg_flow_tt.le_14_pg1.clear()
                        self.dlg_flow_tt.le_15_pg1.clear()
                        self.dlg_flow_tt.le_16_pg1.clear()
                        self.dlg_flow_tt.le_17_pg1.clear()
                        self.dlg_flow_tt.le_18_pg1.clear()
                        self.dlg_flow_tt.le_19_pg1.clear()
                        self.dlg_flow_tt.le_20_pg1.clear()
                        self.dlg_flow_tt.le_21_pg1.clear()

                        self.dlg_flow_tt.le_1_pg2.clear()
                        self.dlg_flow_tt.le_2_pg2.clear()
                        self.dlg_flow_tt.te_1_pg2.clear()
                        self.dlg_flow_tt.le_3_pg2.clear()
                        self.dlg_flow_tt.le_4_pg2.clear()
                        self.dlg_flow_tt.le_5_pg2.clear()
                        self.dlg_flow_tt.le_6_pg2.clear()
                        # self.dlg_flow_tt.le_7_pg2.clear()
                        self.dlg_flow_tt.le_8_pg2.clear()
                        self.dlg_flow_tt.le_9_pg2.clear()
                        self.dlg_flow_tt.le_10_pg2.clear()

                        self.dlg_flow_tt.le_6_pg4.clear()
                        self.dlg_flow_tt.le_7_pg4.clear()
                        self.dlg_flow_tt.le_8_pg4.clear()
                        self.dlg_flow_tt.le_9_pg4.clear()
                        self.dlg_flow_tt.le_10_pg4.clear()
                        self.dlg_flow_tt.le_11_pg4.clear()

                        # Limpando as informações armazenadas: tables widgets
                        nlin_tb1 = self.dlg_flow_tt.tbw_1_pg2.rowCount()
                        ncol_tb1 = self.dlg_flow_tt.tbw_1_pg2.columnCount()
                        nlin_tb2 = self.dlg_flow_tt.tbw_2_pg2.rowCount()
                        ncol_tb2 = self.dlg_flow_tt.tbw_2_pg2.columnCount()
                        # Primeira tabela
                        for lin in range(nlin_tb1):
                            for col in range(ncol_tb1):
                                item = self.dlg_flow_tt.tbw_1_pg2.item(lin, col)
                                if item is not None:
                                    item.setText('')

                        # Segunda tabela
                        for lin in range(nlin_tb2):
                            for col in range(ncol_tb2):
                                item = self.dlg_flow_tt.tbw_2_pg2.item(lin, col)
                                if item is not None:
                                    item.setText('')
                        self.dlg_flow_tt.ch_1_pg4.setChecked(False)  
                        self.dlg_flow_tt.ch_2_pg4.setChecked(False)  
                        self.dlg_flow_tt.ch_3_pg4.setChecked(False)  
                        self.dlg_flow_tt.ch_4_pg4.setChecked(False)  
                        self.dlg_flow_tt.ch_5_pg4.setChecked(False)  
                        self.dlg_flow_tt.ch_6_pg4.setChecked(False)  
                        self.dlg_flow_tt.ch_7_pg4.setChecked(False)
                        self.dlg_flow_tt.ch_8_pg4.setChecked(False)  
                        self.dlg_flow_tt.ch_9_pg4.setChecked(False)  
                        self.dlg_flow_tt.ch_10_pg4.setChecked(False)  
                        self.dlg_flow_tt.ch_11_pg4.setChecked(False)
                        self.dlg_flow_tt.ch_12_pg4.setChecked(False)  
                        self.dlg_flow_tt.ch_13_pg4.setChecked(False)  
                        self.dlg_flow_tt.ch_14_pg4.setChecked(False)  
                        self.dlg_flow_tt.ch_15_pg4.setChecked(False)  
                        self.dlg_flow_tt.ch_16_pg4.setChecked(False)  
                        self.dlg_flow_tt.ch_17_pg4.setChecked(False)  
                        self.dlg_flow_tt.ch_18_pg4.setChecked(False)
                        self.dlg_flow_tt.ch_19_pg4.setChecked(False)  
                        self.dlg_flow_tt.ch_20_pg4.setChecked(False)  
                        self.dlg_flow_tt.ch_21_pg4.setChecked(False)  
                        self.dlg_flow_tt.ch_22_pg4.setChecked(False)
                        self.dlg_flow_tt.close()

                    # Atualiza as variáveis para a condição de salvamento
                    self.save_result = False
                    break

            # Se não houver moficações nos objetos do plugin, a janela será fechada normalmente
            else:
                self.dlg_flow_tt.close()
                self.save_result = False

        elif function == 2:
            # Verifica se alguma lineEdit sobreu alteração: modifica a execução da função close
            line_edit_list = [
                self.dlg_exc_rain.le_1_pg1.text(),
                self.dlg_exc_rain.le_1_pg_ri.text(),
                self.dlg_exc_rain.le_2_pg_ri.text(),
                self.dlg_exc_rain.le_3_pg_ri.text(),
                self.dlg_exc_rain.le_4_pg_ri.text(),
                self.dlg_exc_rain.le_5_pg_ri.text(),
                self.dlg_exc_rain.le_1_pg2.text(),
                self.dlg_exc_rain.le_2_pg2.text(),
                self.dlg_exc_rain.le_3_pg2.text(),
                self.dlg_exc_rain.le_4_pg2.text(),
                self.dlg_exc_rain.le_1_pg4.text(),
                self.dlg_exc_rain.le_2_pg4.text(),
                self.dlg_exc_rain.le_3_pg4.text(),
                self.dlg_exc_rain.le_4_pg4.text(),
                self.dlg_exc_rain.le_5_pg4.text(),
            ]

            # Verifica se algum elemento da função foi modificado
            if any(item != '' for item in line_edit_list) and self.save_result == False:
                while True:

                    result = "Wait! You did not save your changes. Are you sure you want to close?"
                    reply = QMessageBox.warning(None, "Changes not saved", result, QMessageBox.Ok | QMessageBox.Cancel)
                    if reply == QMessageBox.Cancel:
                        break
                    
                    else:
                        # Limpando os elementos da função excess rainfall
                        self.dlg_exc_rain.le_1_pg1.clear()
                        self.dlg_exc_rain.le_2_pg1.clear()
                        self.dlg_exc_rain.le_3_pg1.clear()
                        self.dlg_exc_rain.le_4_pg1.clear()
                        self.dlg_exc_rain.le_1_pg_ri.clear()
                        self.dlg_exc_rain.le_2_pg_ri.clear()
                        self.dlg_exc_rain.le_3_pg_ri.clear()
                        self.dlg_exc_rain.le_4_pg_ri.clear()
                        self.dlg_exc_rain.le_5_pg_ri.clear()
                        self.dlg_exc_rain.le_1_pg2.clear()
                        self.dlg_exc_rain.le_2_pg2.clear()
                        self.dlg_exc_rain.le_3_pg2.clear()
                        self.dlg_exc_rain.le_4_pg2.clear()
                        self.dlg_exc_rain.le_1_pg4.clear()
                        self.dlg_exc_rain.le_2_pg4.clear()
                        self.dlg_exc_rain.le_3_pg4.clear()
                        self.dlg_exc_rain.le_4_pg4.clear()
                        self.dlg_exc_rain.le_5_pg4.clear()
                        self.dlg_exc_rain.le_6_pg4.clear()     
                        self.dlg_exc_rain.rb_1_pg1.setChecked(False) 
                        self.dlg_exc_rain.rb_2_pg1.setChecked(False) 
                        self.dlg_exc_rain.ch_1_pg4.setChecked(False)  
                        self.dlg_exc_rain.ch_2_pg4.setChecked(False)  
                        self.dlg_exc_rain.ch_3_pg4.setChecked(False)  
                        self.dlg_exc_rain.ch_4_pg4.setChecked(False)  
                        self.dlg_exc_rain.ch_5_pg4.setChecked(False)  
                        self.dlg_exc_rain.ch_6_pg4.setChecked(False)
                        self.dlg_exc_rain.close()

                    # Atualiza as variáveis para a condição de salvamento
                    self.save_result = False
                    break
            else:
                # Se não houver moficações nos objetos do plugin, a janela será fechada normalmente
                self.save_result = False
                self.dlg_exc_rain.close()

        elif function == 3:
            # Verifica se alguma lineEdit sobreu alteração: modifica a execução da função close
            line_edit_list = [
                self.dlg_flow_rout.le_1_pg1.text(),
                self.dlg_flow_rout.le_2_pg1.text(),
                self.dlg_flow_rout.le_3_pg1.text(),
                self.dlg_flow_rout.le_4_pg1.text(),
                self.dlg_flow_rout.le_5_pg1.text(),
                self.dlg_flow_rout.le_1_pg2.text(),
                self.dlg_flow_rout.le_2_pg2.text(),
                self.dlg_flow_rout.le_3_pg2.text(),
                self.dlg_flow_rout.le_4_pg2.text(),
                self.dlg_flow_rout.le_5_pg2.text(),
                self.dlg_flow_rout.le_1_pg4.text(),
                self.dlg_flow_rout.le_2_pg4.text(),
                self.dlg_flow_rout.le_3_pg4.text(),
                self.dlg_flow_rout.le_4_pg4.text(),
                self.dlg_flow_rout.le_5_pg4.text(),
                self.dlg_flow_rout.le_6_pg4.text()
            ]

            # Verifica se algum elemento da função foi modificado
            if any(item != '' for item in line_edit_list) and self.save_result == False:
                while True:

                    result = "Wait! You did not save your changes. Are you sure you want to close?"
                    reply = QMessageBox.warning(None, "Changes not saved", result, QMessageBox.Ok | QMessageBox.Cancel)
                    if reply == QMessageBox.Cancel:
                        break
                    
                    else:
                        # Limpando os elementos da função excess rainfall
                        self.dlg_flow_rout.le_1_pg1.clear()
                        self.dlg_flow_rout.le_2_pg1.clear()
                        self.dlg_flow_rout.le_3_pg1.clear()
                        self.dlg_flow_rout.le_4_pg1.clear()
                        self.dlg_flow_rout.le_5_pg1.clear()
                        self.dlg_flow_rout.le_1_pg2.clear()
                        self.dlg_flow_rout.le_2_pg2.clear()
                        self.dlg_flow_rout.le_3_pg2.clear()
                        self.dlg_flow_rout.le_4_pg2.clear()
                        self.dlg_flow_rout.le_5_pg2.clear()
                        self.dlg_flow_rout.le_1_pg4.clear()
                        self.dlg_flow_rout.le_2_pg4.clear()
                        self.dlg_flow_rout.le_3_pg4.clear()
                        self.dlg_flow_rout.le_4_pg4.clear()
                        self.dlg_flow_rout.le_5_pg4.clear()
                        self.dlg_flow_rout.le_6_pg4.clear()     
                        self.dlg_flow_rout.rb_1_pg1.setChecked(False) 
                        self.dlg_flow_rout.rb_2_pg1.setChecked(False) 
                        self.dlg_flow_rout.rb_3_pg1.setChecked(False)  
                        self.dlg_flow_rout.rb_1_pg4.setChecked(False) 
                        self.dlg_flow_rout.rb_2_pg4.setChecked(False) 
                        self.dlg_flow_rout.rb_3_pg4.setChecked(False) 
                        self.dlg_flow_rout.rb_4_pg4.setChecked(False) 
                        self.dlg_flow_rout.ch_1_pg4.setChecked(False)  
                        self.dlg_flow_rout.ch_2_pg4.setChecked(False)  
                        self.dlg_flow_rout.ch_3_pg4.setChecked(False)  
                        self.dlg_flow_rout.ch_4_pg4.setChecked(False)  
                        self.dlg_flow_rout.ch_5_pg4.setChecked(False)  
                        self.dlg_flow_rout.ch_6_pg4.setChecked(False)
                        self.dlg_flow_rout.close()

                    # Atualiza as variáveis para a condição de salvamento
                    self.save_result = False
                    break
   
            else:
                # Se não houver moficações nos objetos do plugin, a janela será fechada normalmente
                self.save_result = False
                self.dlg_flow_rout.close()


    def leh_bacia(self, file_, function):
        """Esta função é utilizada para ler o arquivo raster da bacia hidrográfica (arquivo .RST)
           funciton == 1: flow travel time
           function == 2: excesse rainfall
           function == 3: flow routing"""

        arquivo = file_
        # Tratamento de erros: verifica se o arquivo foi corretamente enviado
        if arquivo:
            if function == 1:
                # Realizando a abertura do arquivo raster e coletando as informações referentes as dimensões do mesmo
                rst_file_bacia = gdal.Open(arquivo)

                # Lendo os dados raster como um array 
                dados_lidos_bacia = rst_file_bacia.GetRasterBand(1).ReadAsArray()
                
                # Tratamento de erro: verifica se o arquivo foi aberto corretamente
                if rst_file_bacia is not None:
                    
                    # Obtenção da dimensão da imagem raster
                    nlin = rst_file_bacia.RasterYSize             
                    ncol = rst_file_bacia.RasterXSize

                    # Criando instâncias das classes de criação de variáveis
                    self.global_vars = GlobalVariables(nlin,ncol)
                    self.rdc_vars = RDCVariables(nlin,ncol)

                    # atualizando os valores das variáveis para coletar o número de linhas e colunas do arquivo raster lido
                    self.rdc_vars.nlin = nlin               
                    self.rdc_vars.ncol = ncol
                    self.rdc_vars.geotransform = rst_file_bacia.GetGeoTransform()
                    self.rdc_vars.projection = rst_file_bacia.GetProjection()                 
                    # Reorganizando os dados lidos da bacia em uma nova matriz chamada bacia.

                    self.global_vars.bacia = dados_lidos_bacia
                    # Fechando o dataset GDAL

                    rst_file_bacia = None
                    print(f'Qtd pix bacia: {np.count_nonzero(self.global_vars.bacia)}\nÁrea da bacia: {(np.count_nonzero(self.global_vars.bacia))*30**2/1000000} Km²')
                    return self.global_vars.bacia

            elif function == 2 or function == 3:
                # Realizando a abertura do arquivo raster e coletando as informações referentes as dimensões do mesmo
                rst_file_bacia = gdal.Open(arquivo)

                # Lendo os dados raster como um array 
                dados_lidos_bacia = rst_file_bacia.GetRasterBand(1).ReadAsArray()
                
                # Tratamento de erro: verifica se o arquivo foi aberto corretamente
                if rst_file_bacia is not None:
                    
                    # Obtenção da dimensão da imagem raster
                    nlin = rst_file_bacia.RasterYSize               
                    ncol = rst_file_bacia.RasterXSize

                    # Criando instâncias das classes de criação de variáveis
                    self.global_vars = GlobalVariables(nlin,ncol)
                    self.rdc_vars = RDCVariables(nlin,ncol)

                    # atualizando os valores das variáveis para coletar o número de linhas e colunas do arquivo raster lido
                    self.rdc_vars.nlin = nlin               
                    self.rdc_vars.ncol = ncol
                    self.rdc_vars.geotransform = rst_file_bacia.GetGeoTransform()
                    self.rdc_vars.projection = rst_file_bacia.GetProjection()

                    # Reorganizando os dados lidos da bacia em uma nova matriz chamada bacia.
                    self.global_vars.bacia = dados_lidos_bacia

                    # Fechando o dataset GDAL
                    rst_file_bacia = None

                    print(f'Qtd pix bacia: {np.count_nonzero(self.global_vars.bacia)}\nÁrea da bacia: {(np.count_nonzero(self.global_vars.bacia))*100/1000000} Km²')
                    return self.global_vars.bacia

                else:
                    """Caso o arquivo raster apresente erros durante a abertura, ocorrerá um erro"""
                    resulte = f"Failde to open the raster file: {arquivo}"
                    print(resulte)
                    # QMessageBox.warning(None, "ERROR!", resulte)

                # Lê informações do arquivo de metadados (.rdc)
                if '.RST' in arquivo:
                    arquivo_rdc = arquivo.replace('.RST', '.RDC')
                elif '.rst' in arquivo:
                    arquivo_rdc = arquivo.replace('.rst', '.RDC')

                if os.path.exists(arquivo_rdc) and os.path.isfile(arquivo_rdc):
                    arquivo_rdc = arquivo_rdc
                else:
                    arquivo_rdc.replace('.RDC','.rdc')
                    if os.path.exists(arquivo_rdc) and os.path.isfile(arquivo_rdc):
                        arquivo_rdc = arquivo_rdc
                    else:
                        resulte = f"There is no file named {arquivo_rdc} in the same directory as {arquivo}!"
                        print(resulte)
                        # QMessageBox.warning(None, "ERROR!", resulte)                        

                if arquivo_rdc is not None:
                    with open(arquivo_rdc, 'r', encoding='iso-8859-1') as rdc_file:
                        # Separando os dados do arquivo RDC em função das linhas que contém alguma das palavras abaixo
                        k_words = ["columns", "rows", "ref. system", "ref. units", "min. X", "max. X", "min. Y", "max. Y", "resolution"]
                        lines_RDC = [line.strip() for line in rdc_file.readlines() if any(word in line for word in k_words)]
                        
                        # Iterando sobre a lista de lines_rdc para guardas as informações das palavras da lista (k_words) nas ruas respectivas variáveis
                        for line in lines_RDC:
                            # Separando as linhas de acordo com o refencial (:)
                            split_line = line.split(":")
                            # Armazenando o primeiro valor da linha (antes do sinal ":")em uma variável e retirando os espaços (caracter) do inicio e fim da linha repartida
                            key = split_line[0].strip()
                            # Armazenando o segundo valor da linha (antes do sinal ":") em uma variáveis e retirando os espaços (caracter) do inicio e fim da linha repartida
                            value = split_line[-1].strip()

                            # Estrutura condicional para verificar quais são as informações de cada linha e armazenando elas em suas respectivas variáveis
                            if key == "ref. system":
                                self.rdc_vars.sistemaref = value
                            elif key == "ref. units":
                                self.rdc_vars.unidaderef = value
                            elif key == "min. X":
                                self.X_minimo = float(value)
                            elif key == "max. X":
                                self.X_maximo = float(value)
                            elif key == "min. Y":
                                self.Y_minimo = float(value)
                            elif key == "max. Y":
                                self.Y_maximo = float(value)
                            elif key == "resolution":
                                self.global_vars.dx = float(value)
                    # Definição das caracteristicas do pixel
                    self.d_x = (self.X_maximo - self.X_minimo)/self.rdc_vars.ncol
                    self.d_y = (self.Y_maximo - self.Y_minimo)/self.rdc_vars.nlin    
                else:
                    # Arquivo não existente: mostra erro para usuário
                    resulte = f"There is no file named {arquivo_rdc} in the same directory as {arquivo}!"
                    print(resulte)
                    # QMessageBox.warning(None, "ERROR!", resulte)                

        else:
            result ="Nenhum arquivo foi selecionado!"
            print(result)
            # QMessageBox.warning(None, "ERROR!", result)
        
    def leh_caracteristica_dRios(self):
        """Esta função é utilizada para ler as informações acerca da característica dos rios de uma bacia hidrográfica (texto .RST)"""

        # Abrindo o arquivo de texto (.txt) com as informações acerca das classes dos rios
        file = r"c:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\SmallExample\1_TravelTime\Input_binary\caracteristicas_classes_rios.txt"
        with open(file, 'r', encoding='utf-8') as arquivo_txt:
            #  Atualizando as variáveis que dependem
            self.global_vars.nclasses =int(arquivo_txt.readline().strip().split(':')[1])
            arquivo_txt.readline()
            # Inicializando as listas
            j_list = []
            Sclasse_list = []
            Mannclasse_list = []
            Rhclasse_list = []

            # Iterando sobre as linhas do arquivo
            for line in arquivo_txt:
                # Divide a linha nos espaços em branco e converte para float
                indice, Rh, Mann, Scla = map(float, line.split(';'))

                # Adiciona os valores às listas
                j_list.append(indice)
                Sclasse_list.append(Scla)
                Mannclasse_list.append(Mann)
                Rhclasse_list.append(Rh)

        # Convertendo as listas em arrays e armazendo nas respectivas variáveis
        self.global_vars.j = np.array(j_list)
        self.global_vars.Sclasse = np.array(Sclasse_list)
        self.global_vars.Mannclasse = np.array(Mannclasse_list)
        self.global_vars.Rhclasse = np.array(Rhclasse_list)

    def leh_classes_rios(self):
        """Esta função é utilizada para ler as informações acerca da classe dos rios da bacia hidrográfica (arquivo raster -  .RST)"""

        arquivo = r"c:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\SmallExample\input_binary\6_RIVER_SEGMENTS_EXbin.RST"
        # Tratamento de erros: verifica se o arquivo foi corretamente enviado
        if arquivo:
            # Realizando a abertura do arquivo raster e coletando as informações referentes as dimensões do mesmo
            rst_file_claRIO = gdal.Open(arquivo)
            
            # Lendo os dados raste como um array 
            dados_lidos_raster_claRIO = rst_file_claRIO.GetRasterBand(1).ReadAsArray()

            #  Tratamento de erros: verifica se o arquivo raster foi aberto corretamente
            if rst_file_claRIO is not None:
                # Reorganizando os dados lidos em uma nova matriz, essa possui as informações sobre as classes dos rios
                self.global_vars.classerio = dados_lidos_raster_claRIO
                # Fechando o dataset GDAL referente ao arquivo raster
                rst_file_claRIO = None
            else:
                # Caso o arquivo raster apresente erros durante a abertura, ocorrerá um erro
                resulte = f"Failde to open the raster file: {arquivo}"
                # QMessageBox.warning(None, "ERROR!", resulte)
                
        else:
            # Exibe uma mensagem de erro
            result ="Nenhum arquivo foi selecionado!"
            # QMessageBox.warning(None, "ERROR!", result)

    def leh_direcoes_de_fluxo(self, A, B, C, D, E, F, G, H):
        """Esta função é utilizada para ler as informações acerca da direção de escoamento dos rios (arquivo raster - .RST)"""

        # Definindo a numeração das direções &
        # Definindo a posição relativa dos pixels vizinhos
        # lin viz = lin centro + dlin(i)
        # col viz = col centro + dcol(i)
        
        self.global_vars.dlin = {
                            45: -1,
                            90: 0,
                            135: 1,
                            180: 1,
                            225: 1,
                            270: 0,
                            315: -1,
                            360: -1
                            }
        self.global_vars.dcol = {
                            45: 1,
                            90: 1,
                            135: 1,
                            180: 0,
                            225: -1,
                            270: -1,
                            315: -1,
                            360: 0
                            }

       
        # ATENÇÃO PARA O VALOR NUMÉRICO DAS DIRECÕES
        # ---------------------------------------------------------
        # - G  H  A      ArcView:  32 64 128    MGB-IPH:  64  128  1 -
        # - F  *  B                16  *  1               32   *   2 -
        # - E  D  C                 8  4  2               16   8   4 -

        # Recebendo os arquivos necessários
        self.rdc_vars.nomeRST = r"c:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\SmallExample\input_binary\3_DIR_EXbin.RST"
        self.rdc_vars.nomeRDC = r"c:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\SmallExample\input_binary\3_DIR_EXbin.RDC"

        # Abrindo o arquivo RDC
        arquivo = self.rdc_vars.nomeRDC
        with open(arquivo, 'r',encoding ='utf-8') as rdc_file:
            # Separando os dados do arquivo RDC em função das linhas que contém alguma das palavras abaixo
            k_words = ["columns", "rows", "ref. system", "ref. units", "min. X", "max. X", "min. Y", "max. Y", "resolution"]
            lines_RDC = [line.strip() for line in rdc_file.readlines() if any(word in line for word in k_words)]
            
            # Iterando sobre a lista de lines_rdc para guardas as informações das palavras da lista (k_words) nas ruas respectivas variáveis
            for line in lines_RDC:
                # Separando as linhas de acordo com o refencial (:)
                split_line = line.split(":")
                # Armazenando o primeiro valor da linha (antes do sinal ":")em uma variável e retirando os espaços (caracter) do inicio e fim da linha repartida
                key = split_line[0].strip()
                # Armazenando o segundo valor da linha (antes do sinal ":") em uma variáveis e retirando os espaços (caracter) do inicio e fim da linha repartida
                value = split_line[-1].strip()

                # Estrutura condicional para verificar quais são as informações de cada linha e armazenando elas em suas respectivas variáveis
                if key == "rows":
                    self.rdc_vars.nlin = int(value)
                elif key == "columns":
                    self.rdc_vars.ncol = int(value)
                elif key == "ref. system":
                    self.rdc_vars.sistemaref = value
                elif key == "ref. units":
                    self.rdc_vars.unidaderef = value
                elif key == "min. X":
                    self.rdc_vars.xmin = float(value)
                elif key == "max. X":
                    self.rdc_vars.xmax = float(value)
                elif key == "min. Y":
                    self.rdc_vars.ymin = float(value)
                elif key == "max. Y":
                    self.rdc_vars.ymax = float(value)
                elif key == "resolution":
                    self.global_vars.dx = float(value)
        
        # Atualizando algumas variáveis com as informações coletadas do arquivo RDC
        self.global_vars.Xres2 = self.global_vars.dx
        self.global_vars.Xres = float(self.global_vars.Xres2)
        self.global_vars.Yres = self.global_vars.Xres

        # Abrindo o arquivo raster 
        rst_file_dir = gdal.Open(self.rdc_vars.nomeRST)
        # Lendo os dados raster como um array
        dados_lidos_direcoes = rst_file_dir.GetRasterBand(1).ReadAsArray()

        # Tratamento de erros: verifica se o arquivo raster foi aberto corretamente
        if rst_file_dir is not None:
            # Reorganizando os dados lidos na matriz destinadas às informações da drenagem da bacia hidrográfica
            self.global_vars.direcoes = dados_lidos_direcoes

            # Fechando o dataset GDAL referente ao arquivo raster
            rst_file_dir = None
        else:
            """Caso o arquivo raster apresente erros durante a abertura, ocorrerá um erro"""
            resulte = f"Failde to open the raster file: {self.rdc_vars.nomeRST}"
            # QMessageBox.warning(None, "ERROR!", resulte)

        # Verificação do valor da variável maxdir
        self.global_vars.maxdir = np.amax(self.global_vars.direcoes)
        chaves = [A, B, C, D, E, F, G, H]
        valores = [45, 90, 135, 180, 225, 270, 315, 360]
        value_error = [valor for valor in valores if type(valor) != int]

        # Dicionário com as combinações das direções de fluxo
        idrisi_map = {}
        for chave, valor in zip(chaves, valores):
            try:
                idrisi_map[chave] = int(valor) # devem ser diferentes entre si, i+1 != i e i-1
            except ValueError:
                result = f'The value(s) "{value_error}" is(are) not (a) valid integer number(s)!'
                print(result)
                # QMessageBox.warning(None, "ERROR!", result)
        
        for lin in range(self.rdc_vars.nlin):
            for col in range(self.rdc_vars.ncol):
                # Verifica se os valores fornecidos pertencem ao código de direção do plugin, se não, os modifica 
                if self.global_vars.direcoes[lin][col] in idrisi_map:
                    # Atualiza o valor do elemento atual da matriz dir de acordo com os novos valores
                    self.global_vars.direcoes[lin][col] = idrisi_map[self.global_vars.direcoes[lin][col]]

        # Tratamento das direções na borda
        self.global_vars.direcoes[0, :] = 360
        self.global_vars.direcoes[-1, :] = 180
        self.global_vars.direcoes[:, 0] = 270
        self.global_vars.direcoes[:, -1] = 90

    def leh_drenagem(self):
        """Esta função é utilizada para ler as informações acerca da drenagem dos rios (arquivo raster - .RST)"""

        # Obtendo o arquivo referente as calasses dos rios da bacia hidrográfica
        arquivo = r"C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\SmallExample\input_binary\5_DRAINAGE_EX_BIN_2.RST"
        # Abrindo o arquivo raster com as informações acerda do sistema de drenagem da bacia hidrográfica
        rst_file_drenagem = gdal.Open(arquivo)
        
        # Lendo os dados raster como um array
        dados_lidos_drenagem = rst_file_drenagem.GetRasterBand(1).ReadAsArray()

        # Tratamento de erros: verifica se o arquivo raster foi aberto corretamente
        if rst_file_drenagem is not None:
            # Reorganizando os dados lidos na matriz destinadas às informações da drenagem da bacia hidrográfica
            self.global_vars.dren = dados_lidos_drenagem
            print(np.count_nonzero(self.global_vars.dren))
            # Fechando o dataset GDAl referente ao arquivo raster
            rst_file_drenagem = None
        else:
            """Caso o arquivo raster apresente erros durante a abertura, ocorrerá um erro"""
            resulte = f"Failde to open the raster file: {arquivo}"
            # QMessageBox.warning(None, "ERROR!", resulte)


    def leh_modelo_numerico_dTerreno(self):
        """Esta função é utilizada para ler as informações acerca do modelo numérico do terreno (arquivo raster - .RST)"""

        # Obtendo o arquivo referente ao MDE da bacia hidrográfica
        arquivo = r'c:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\SmallExample\input_binary\2_DEM_EXbin.RST'

        # Realizando a abertura do arquivo raster e coletando as informações referentes as dimensões do mesmo
        rst_file_MDE = gdal.Open(arquivo)

        # Lendo os dados raster como um array
        dados_lidos_MDE = rst_file_MDE.GetRasterBand(1).ReadAsArray()

        #  Tratamento de erros: verifica se o arquivo raster foi aberto corretamente
        if rst_file_MDE is not None:
            # Reoganizando os dados lidos em uma nova matriz que possuirá os dados ligados ao MDE da baciaa hidrográfica
            self.global_vars.MDE = dados_lidos_MDE

            # Fechando o dataset GDAL
            rst_file_MDE = None
        else:
            """Caso o arquivo raster apresente erros durante a abertura, ocorrerá um erro"""
            resulte = f"Failde to open the raster file: {arquivo}"
            # QMessageBox.warning(None, "ERROR!", resulte)

    def leh_precipitacao_24h(self):
        """Esta função é utilizada para ler as informações acerca da precipitação das últimas 24 horas, P24 (arquivo texto - .txt)"""

        # Coledando os arquivo fornecido
        arquivo = r'C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\Calcula_Tc_SCS_decliv_indiv_grandesmatrizes_utm_LL\info_P24.txt'

        # lendo os arquivos acerda da precipitação das últimas 24 horas
        with open(arquivo, 'r', encoding = 'utf-8') as arquivo_txt:
            arquivo_txt.readline()
            dados_lidos_P24 = float(arquivo_txt.read()) # considerando que no arquivo só possui um valor de precipitação

        # Armazenando o valor da precipitação de 24 horas em uma variável específica
        self.global_vars.P24 = dados_lidos_P24

    def leh_uso_do_solo(self):
        """Esta função é utilizada para ler as informações acerca do uso do solo (arquivo raster - .RST)"""

        # Obtendo o arquivo raster referente ao uso do solo
        arquivo = r"C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\SmallExample\input_binary\8_LULC_EXbin.RST"

        # Abrindo o arquivo raster com as informações acerda do uso do solo da bacia hidrográfica
        rst_file_usoSolo = gdal.Open(arquivo)

        # Lendo os dados do arquivo raster como um array
        dados_lidos_usoSolo = rst_file_usoSolo.GetRasterBand(1).ReadAsArray()

        # Tratamento de erros: verifica se o arquivo raster foi aberto corretamente
        if rst_file_usoSolo is not None:
            # Reorganizando os dados lidos na matriz destinadas às informações da drenagem da bacia hidrográfica
            self.global_vars.usosolo = dados_lidos_usoSolo

            # Inicializando as variáveis fundamentais
            self.global_vars.Nusomax = np.amax(self.global_vars.usosolo)

        else:
            """Caso o arquivo raster apresente erros durante a abertura, ocorrerá um erro"""
            resulte = f"Failde to open the raster file: {arquivo}"
            # QMessageBox.warning(None, "ERROR!", resulte)


    def leh_uso_manning(self):
        """Esta função é utilizada para ler as informações acerca do uso do solo e o coeficiente de rugosidade de Manning (arquivo texto - .txt)"""

        # Onbtendo o arquivo de texto (.txt) com as informações acerca dos coeficientes De Manning para as zonas da bacia hidrográfica
        arquivo = r'c:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\SmallExample\1_TravelTime\Input_binary\relacao_uso_Manning.txt'

        # Criando variável extra, para armazenar os tipos de uso e coeficente de Manning
        class_id = 0
        uso_manning = []
        coef_maning = []
        coef_K = []
        uso_manning_val = {}
        coef_maning_val = []
        coef_K_val = []

        # Abrindo o arquivo que contém o coeficiente de Manning para os diferentes usos do solo
        with open(arquivo, 'r', encoding='utf-8') as arquivo_txt_csv:
            # Amazena a linha do cabeçalho
            firt_line = arquivo_txt_csv.readline().strip()

            # Lê as informações de uso do solo e coeficiente de Manning 
            for line in arquivo_txt_csv:
                # Coletando as informações de cada linha
                info = line.strip().split(';')
                # Armazenando os valores das linhas nas suas respectivas variáveis
                if info[0] !='' and info[1] !='' and info[2] !='' and info[3]:
                    classe_id_key = int(info[0])
                    uso_manning = str(info[1])
                    coef_maning = float(info[2])
                    coef_K = float(info[3])

                    # Adicionando os valores nas variáveis destinadas
                    coef_maning_val = np.append(coef_maning_val, coef_maning)
                    coef_K_val = np.append(coef_K_val, coef_K)
                    uso_manning_val[classe_id_key] = class_id
                    class_id +=1

        # Adicionando cada valor às suas respectivas variáveis
        self.global_vars.uso_mann = uso_manning_val
        self.global_vars.Mann = coef_maning_val
        self.global_vars.coef_K = coef_K_val
        self.global_vars.n_tipo_uso = len(uso_manning)

    def leh_drainage_area(self):
        """Esta função é utilizada para ler as informações acerca do uso do solo (arquivo raster - .rst)"""

        # Obtendo o arquivo raster referente ao uso do solo
        arquivo = r"C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\SmallExample\input_binary\4_DA_KM2_EXbin.RST"

        # Abrindo o arquivo raster com as informações acerda do uso do solo da bacia hidrográfica
        rst_file_dren_area = gdal.Open(arquivo)

        # Lendo os dados do arquivo raster como um array
        dados_lidos_dren_area = rst_file_dren_area.GetRasterBand(1).ReadAsArray()

        # Tratamento de erros: verifica se o arquivo raster foi aberto corretamente
        if rst_file_dren_area is not None:
            # Reorganizando os dados lidos na matriz destinadas às informações da drenagem da bacia hidrográfica
            self.global_vars.dren_area = dados_lidos_dren_area

        else:
            """Caso o arquivo raster apresente erros durante a abertura, ocorrerá um erro"""
            resulte = f"Failde to open the raster file: {arquivo}"
            # QMessageBox.warning(None, "ERROR!", resulte)

    def project(self,x1, x2, y1,y2,tipo2,dist2,lado2,diagonal2):
        """Esta função calcula as distâncias sobre a superfície considerando o elipsóide WGS84"""
        # Definindo as constantes
        PI = 3.141592
        A = 6378.137 #comprimento do semi eixo maior do elipsóide (km)
        B = 6358.752 #comprimento do semi eixo menor do elipsóide (km)

        # Iniciando os cálulos
        ylat = (y1 + y2) / 2

        # Definição do achatamento do elipsóide
        f = (A - B) / A 
        # Determinando o quadrado da excentricidade
        e2 = (2*f) - (f**2) 
        # Determinando o raio da curvatura da Terra na latitude ylat
        rn = A / ((1 - e2*(np.sin(ylat)))**0.2) 

        # Calculando o raio da circunferência de um círculo determinado pelo plano que corta o elipsóide na latitude ylat
        raio_circ = rn*np.cos(ylat)
        dgx = x2 - x1
        dgy = y1 - y2

        dx = raio_circ*dgx*(PI/180.0)
        dy = rn*dgy*(PI/180.0)

        # Verificando o conteúdo da vairável tipo2 e atualizando a distanância com base nele
        if tipo2 == 1:
            dist2 = dx*lado2
        elif tipo2 == 2:
            dist2 = dy*lado2
        elif tipo2 == 3:
            dist2 = np.sqrt(dx**2+dy**2)*diagonal2/1.414

        self.global_vars.dist_2 = dist2

        return dist2

    def comprimento_acumulado(self):
        """Esta função determina o comprimento dos pixels que fazem partes da rede de drenagem da bacia hidrográfica. Da cabeceira ao exutório em questão"""

        # Define variáveis
        Lfoz = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol))
        self.global_vars.Lfoz= Lfoz
        Lac = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol))
        self.global_vars.Lac = Lac
        Lac = None
        Lfoz = None
        contador = 0
        pixel_atual = 0 
        # Iniciando a iteração para varrer todos os elementos da bacia hidrográfica
        for col in range(self.rdc_vars.ncol):
            for lin in range(self.rdc_vars.nlin):
                # Delimitando apenas os elementos que estão presentes na bacia hidrográfica
                if self.global_vars.bacia[lin][col] == 1:
                    # Coletando as informações referentes ao sistema de drenagem da bacia hidrográfica
                    if self.global_vars.dren[lin][col] == 1:
                        pixel_atual +=1
                        self.global_vars.linaux = lin
                        self.global_vars.colaux = col
                        self.global_vars.caminho = 0
                        self.global_vars.tamcam:float = 0.0
                        self.global_vars.tamfoz:float = 0.0

                        while self.global_vars.caminho == 0:
                            
                            # Criando condição de parada
                            condicao = self.global_vars.linaux < 1 or self.global_vars.linaux > self.rdc_vars.nlin \
                            or self.global_vars.colaux< 1 or self.global_vars.colaux >  self.rdc_vars.ncol \
                            or self.global_vars.bacia[self.global_vars.linaux][self.global_vars.colaux] == 0

                            if condicao:
                                self.global_vars.caminho = 1

                            else:
                                contador +=1
                                # Continuar caminho: determina a contagem das distâncias projetadas (WGS84) e \
                                # determina as coordenadas verticais do pixel

                                self.global_vars.Xesq = self.rdc_vars.xmin + (self.global_vars.colaux - 1) * self.global_vars.Xres
                                self.global_vars.Xdir = self.global_vars.Xesq + self.global_vars.Xres
                                self.global_vars.Yinf = self.rdc_vars.ymax - (self.global_vars.linaux * self.global_vars.Yres)
                                self.global_vars.Ysup = self.global_vars.Yinf + self.global_vars.Yres

                                # Determinando a posição relativa ao pixel anterior
                                condicao2 = self.global_vars.linaux2 == self.global_vars.linaux or self.global_vars.colaux2 == self.global_vars.colaux
                                if condicao2:
                                    if self.global_vars.linaux2 == self.global_vars.linaux:
                                        self.rdc_vars.tipo = 1
                                    else:
                                        self.rdc_vars.tipo = 2
                                else:
                                    self.rdc_vars.tipo = 3

                                # Deteminando a distância incremental projetada
                                if self.global_vars.metro == 0:
                                    self.global_vars.auxdist = self.project(self.global_vars.Xesq,
                                                                        self.global_vars.Xdir,
                                                                        self.global_vars.Ysup,
                                                                        self.global_vars.Yinf,
                                                                        self.rdc_vars.tipo,
                                                                        self.global_vars.auxdist,
                                                                        self.global_vars.lado,
                                                                        self.global_vars.diagonal)
                                    
                                else:
                                    if self.rdc_vars.tipo == 1 or self.rdc_vars.tipo == 2:
                                        self.global_vars.auxdist = self.global_vars.dx * self.global_vars.lado

                                    else:
                                        self.global_vars.auxdist = self.global_vars.dx * self.global_vars.diagonal
                                        
                                # Atualizando o comprimento do rio desde o pixel inicial
                                self.global_vars.tamcam = self.global_vars.tamcam + self.global_vars.auxdist
                                self.global_vars.tamfoz = self.global_vars.tamcam

                                # Condição para verificar se o tamanho do rio é maior que o armazenameto do pixel
                                condicao3 = self.global_vars.tamcam > self.global_vars.Lac[self.global_vars.linaux][self.global_vars.colaux]
                                if condicao3:
                                    # O valor do pixel é armazenado em um novo rio
                                    self.global_vars.Lac[self.global_vars.linaux][self.global_vars.colaux] = self.global_vars.tamcam
                                
                                # Armazena o pixel contabilizado
                                self.global_vars.linaux2 = self.global_vars.linaux
                                self.global_vars.colaux2 = self.global_vars.colaux

                                # determina o próximo píxel do caminho
                                self.global_vars.diraux = self.global_vars.direcoes[self.global_vars.linaux, self.global_vars.colaux]
                                self.global_vars.caminho = 0
                                self.global_vars.linaux += self.global_vars.dlin[self.global_vars.diraux]
                                self.global_vars.colaux += self.global_vars.dcol[self.global_vars.diraux]

                        # Atulizando a variável lfoz
                        self.global_vars.Lfoz[lin][col] = self.global_vars.tamfoz

                        print(f'[{pixel_atual}/{(np.count_nonzero(self.global_vars.bacia))}] ({pixel_atual/(np.count_nonzero(self.global_vars.bacia))*100:.2f}%)', end='\r')

        self.fim = perf_counter()
        print(f'{(self.fim - self.inicio)/60} min')                  
        print('Passou compri_acumulado')

    def numera_pixel(self):
        '''Esta função enumera os píxels presentes na rede de drenagem'''

        # Define variáveis
        self.contadren = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol))
        self.numcabe = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol))
        self.cabeceira = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol))
        self.global_vars.numcabeaux = 0
        pixel_atual: int = 0
        cont:int = 0
        # Enumerando os píxels pertencentes à bacia e à rede de drenagem
        pix_bacia_e_dren = (self.global_vars.bacia == 1) & (self.global_vars.dren == 1)
        for col in range(self.rdc_vars.ncol):
            for lin in range(self.rdc_vars.nlin):
                if self.global_vars.bacia[lin][col] == 1:
                    if self.global_vars.dren[lin][col] == 1:
                        cont +=1
                        self.contadren[lin][col] = cont

        pixel_dren = np.where(pix_bacia_e_dren)
        self.global_vars.lincontadren = np.array(pixel_dren[0])
        self.global_vars.colcontadren = np.array(pixel_dren[1])


        # Numeração dos píxels internos a bacia: São chamados de cabeceira, pois o caminho do fluxo é iniciado a partir de cada um deles
        for col in range(1, self.rdc_vars.ncol - 1):
            for lin in range(1, self.rdc_vars.nlin - 1):
                # Atualizará apenas os píxel que estão na bacia hidrográfica(cabeceira == 1)
                if self.global_vars.bacia[lin][col] == 1:
                    pixel_atual +=1
                    # A priori, todos os píxels serão considerados de cabeceira
                    self.cabeceira[lin][col] = 1
                    # Cria vizinhança 3x3 para estudar a direção de fluxo do píxel central.
                    for colaux in range(col - 1, col + 2):
                        for linaux in range(lin - 1, lin + 2):
                            # Para cada vizinho, verifica a direção de fluxo dela e para qual pixel ele drena
                            self.global_vars.diraux = self.global_vars.direcoes[linaux][colaux]
                            self.global_vars.linaux2 = linaux + self.global_vars.dlin[self.global_vars.diraux]
                            self.global_vars.colaux2 = colaux + self.global_vars.dcol[self.global_vars.diraux]

                            # Se algum vizinho drenar para o central em análise, este não é de cabeceira
                            if self.global_vars.linaux2 == lin and self.global_vars.colaux2 == col:
                                self.cabeceira[lin][col] = 0

                    # Enumera de píxels que são cabeceira
                    if self.cabeceira[lin][col] == 1:
                        self.global_vars.numcabeaux += 1
                        self.numcabe[lin][col] = self.global_vars.numcabeaux

                print(f'[{pixel_atual}/{(np.count_nonzero(self.global_vars.bacia))}] ({pixel_atual/(np.count_nonzero(self.global_vars.bacia))*100:.2f}%)', end='\r')

        # Atualiza variáveis globais
        self.global_vars.numcabe = self.numcabe
        self.global_vars.Ncabe = self.global_vars.numcabeaux

        self.fim = perf_counter()
        print(f'{(self.fim - self.inicio)/60} min') 
        print('Passou numera_pix')

    def dist_drenagem(self):
        """Esta funçao determina a distância incremental percorrida pela água na rede de drenagem,
            assim como a declividade pixel a pixel"""

        # Redimenciona as variáveis necessárias
        dist = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol))
        pixeldren = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol))
        self.global_vars.pixeldren = pixeldren
        pixeldren = None
        Difcota = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol))
        self.global_vars.Difcota = Difcota
        Difcota = None
        DECLIVpixjus = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol))
        self.global_vars.DECLIVpixjus = DECLIVpixjus
        DECLIVpixjus = None
        TSpix = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol))
        self.global_vars.TSpix = TSpix
        TSpix = None
        pixel_atual: int = 0

        # iterando sobre os elementos do arquivo raster
        for col in range(self.rdc_vars.ncol):
            for lin in range(self.rdc_vars.nlin):
                # Realiza as operações no apenas na região da bacia hidográfica
                if self.global_vars.bacia[lin][col] == 1:
                    pixel_atual +=1
                    self.global_vars.linaux: int = lin
                    self.global_vars.colaux: int = col
                    self.global_vars.caminho: int = 0
                    self.global_vars.tamcam: float = 0.0

                    if self.global_vars.dren[lin][col] == 1:
                        self.global_vars.caminho: int = 1

                    else:
                        while self.global_vars.caminho == 0:
                            
                            condicao: bool = (self.global_vars.linaux<= 1
                            or self.global_vars.linaux>=self.rdc_vars.nlin
                            or self.global_vars.colaux<=1 or self.global_vars.colaux>= self.rdc_vars.ncol
                            or self.global_vars.bacia[self.global_vars.linaux][self.global_vars.colaux]==0)

                            # Verificando a resposta da variável condicao
                            if condicao:
                                self.global_vars.caminho = 1
                            
                            else:
                                # Verifica se o pixel atual pertence ao sistema de drenagem da bacia hidrográfica
                                condicao2: bool = self.global_vars.dren[self.global_vars.linaux][self.global_vars.colaux] == 1

                                if condicao2:
                                    # Após alocação do pixel da rede de drenagem: encerra o processo de busca
                                    self.global_vars.caminho = 1
                                    dist[lin][col] = self.global_vars.tamcam
                                    self.global_vars.pixeldren[lin][col] = self.contadren[self.global_vars.linaux][self.global_vars.colaux]
                                else:
                                    self.global_vars.diraux = self.global_vars.direcoes[self.global_vars.linaux][self.global_vars.colaux]
                                    self.global_vars.caminho = 0
                                    self.global_vars.colaux2 = self.global_vars.colaux
                                    self.global_vars.linaux2 = self.global_vars.linaux

                                    self.global_vars.linaux += self.global_vars.dlin[self.global_vars.diraux]
                                    self.global_vars.colaux += self.global_vars.dcol[self.global_vars.diraux]

                                    # Calculando a distância incremental percorrida &
                                    # Contabilizar distancias projetadas (WGS84) &
                                    # Determina coordenadas vertices do pixel
                                    self.global_vars.Xesq = self.rdc_vars.xmin + (self.global_vars.colaux2 - 1) * self.global_vars.Xres
                                    self.global_vars.Xdir = self.global_vars.Xesq + self.global_vars.Xres
                                    self.global_vars.Yinf = self.rdc_vars.ymax - self.global_vars.linaux2 * self.global_vars.Yres
                                    self.global_vars.Ysup = self.global_vars.Yinf + self.global_vars.Yres

                                    # Determina a posição relativa ao píxel anterior
                                    condicao3 = self.global_vars.linaux2 == self.global_vars.linaux or self.global_vars.colaux2 == self.global_vars.colaux
                                    if condicao3:
                                        if self.global_vars.linaux2 == self.global_vars.linaux:
                                            self.rdc_vars.tipo = 1
                                        else:
                                            self.rdc_vars.tipo = 2
                                    else:
                                        self.rdc_vars.tipo = 3

                                    # Determinando a distância incremental projetada
                                    if self.global_vars.metro == 0:
                                        self.global_vars.auxdist = self.project(self.global_vars.Xesq,
                                                           self.global_vars.Xdir,
                                                           self.global_vars.Ysup,
                                                           self.global_vars.Yinf,
                                                           self.rdc_vars.tipo,
                                                           self.global_vars.auxdist,
                                                           self.global_vars.lado,
                                                           self.global_vars.diagonal)
                                    else:
                                        condicao4 = self.rdc_vars.tipo == 1 or self.rdc_vars.tipo == 2
                                        if  condicao4:
                                            self.global_vars.auxdist = self.global_vars.dx * self.global_vars.lado
                                        else:
                                            self.global_vars.auxdist = self.global_vars.dx * self.global_vars.diagonal
                                    
                                    # atualiza o comprimento do rio desde o pixel inicial
                                    self.global_vars.tamcam += self.global_vars.auxdist

                                    # ARPdeclivjus

                                    if self.global_vars.tipo_decliv == 4:
                                        # calcula declividade do pixel relativo ao pixel de jusante (este pixel)
                                        self.global_vars.Lincr = self.global_vars.auxdist
                                        self.global_vars.Difcota = self.global_vars.MDE[self.global_vars.linaux2][self.global_vars.colaux2] - self.global_vars.MDE[self.global_vars.linaux][self.global_vars.colaux]
                                        self.global_vars.DECLIVpixjus[self.global_vars.linaux2][self.global_vars.colaux2] = self.global_vars.Difcota/self.global_vars.Lincr*1000.0
                                        self.global_vars.Streaux = self.global_vars.DECLIVpixjus[self.global_vars.linaux2][self.global_vars.colaux2]
                                        self.global_vars.Ltreaux = self.global_vars.Lincr
                                        self.global_vars.usaux = self.global_vars.usosolo[self.global_vars.linaux2][self.global_vars.colaux2]
                                        self.global_vars.Smin = 10 #em m/km

                                        if self.global_vars.Streaux < self.global_vars.Smin:
                                            self.global_vars.Streaux = self.global_vars.Smin
                                        
                                        self.global_vars.Smax = 600 #em m/km
                                        if self.global_vars.Streaux > self.global_vars.Smax:
                                            self.global_vars.Streaux = self.global_vars.Smax

                                        # JVD: correção da indexação para o python (inicia no zero)
                                        # Calcula o TS por píxel
                                        self.global_vars.TSpix[self.global_vars.linaux2][self.global_vars.colaux2] = 5.474 * ((self.global_vars.Mann[self.global_vars.uso_mann[self.global_vars.usaux]] * self.global_vars.Ltreaux)**0.8) / ((self.global_vars.P24**0.5)*((self.global_vars.Streaux/1000.0)**0.4))
                    
                    print(f'[{pixel_atual}/{(np.count_nonzero(self.global_vars.bacia))}] ({pixel_atual/(np.count_nonzero(self.global_vars.bacia))*100:.2f}%)', end='\r')

        # Atualiza as variáveis globais
        self.global_vars.DIST = dist
        self.fim = perf_counter()
        print(f'{(self.fim - self.inicio)/60} min') 
        print('Passou dist_drenagem')

    def dist_trecho(self):
        ''' Esta função determina o número dos diferentes trechos que existem na bacia hidrográfica estudada'''
        self.global_vars.numtreauxmax = 0
        TREpix = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol))
        self.global_vars.TREpix = TREpix
        TREpix = None
        condicao1 = None
        pixel_atual = 0
        #ARPlidar: loop para contar o número máximo de trechos
        for col in range(1, self.rdc_vars.ncol-1):
            for lin in range(1, self.rdc_vars.nlin-1):
                # Ações realizadas apenas na região da bacia
                if self.global_vars.bacia[lin][col] == 1:

                    # ARPlidar
                    if self.global_vars.numcabe[lin][col] > 0:
                        pixel_atual +=1
                        self.global_vars.numcabeaux = int(self.global_vars.numcabe[lin][col])
                        self.global_vars.linaux = lin
                        self.global_vars.colaux = col
                        self.global_vars.linaux2 = lin
                        self.global_vars.colaux2 = col
                        self.global_vars.linaux3 = lin
                        self.global_vars.colaux3 = col
                        self.global_vars.numtreaux = 0
                        self.global_vars.caminho = 0
                        self.global_vars.usaux = self.global_vars.usosolo[lin][col]
                        self.global_vars.usaux2 = self.global_vars.usaux

                        # ARPlidar
                        # Grava qual trecho o píxel em questão pertence
                        self.global_vars.numtreaux2 = 1

                        while self.global_vars.caminho == 0:
                            self.global_vars.diraux = self.global_vars.direcoes[self.global_vars.linaux][self.global_vars.colaux]
                            self.global_vars.linaux += self.global_vars.dlin[self.global_vars.diraux]
                            self.global_vars.colaux += self.global_vars.dcol[self.global_vars.diraux]


                            condicao1 = self.global_vars.usaux != self.global_vars.usosolo[self.global_vars.linaux][self.global_vars.colaux]
                            condicao2 = self.global_vars.dren[self.global_vars.linaux][self.global_vars.colaux] == 1
                           
                            if condicao1 or condicao2:
                                # Mudou o uso do solo ou alcançou a rede de drenagem,
                                # então terminou um trecho no píxel anterior
                                self.global_vars.numtreaux += 1

                                if self.global_vars.numtreaux > self.global_vars.numtreauxmax:
                                    self.global_vars.numtreauxmax = self.global_vars.numtreaux

                                # ARPlidar: incluindo o teste da bacia
                                condicao3 = self.global_vars.dren[self.global_vars.linaux][self.global_vars.colaux] == 1 or self.global_vars.bacia[self.global_vars.linaux][self.global_vars.colaux] == 0
                                if condicao3:
                                    self.global_vars.caminho = 1
                                else:
                                    # Continua o caminho, porém em um trecho novo
                                    self.global_vars.linaux2 = self.global_vars.linaux
                                    self.global_vars.colaux2 = self.global_vars.colaux
                                    self.global_vars.linaux3 = self.global_vars.linaux
                                    self.global_vars.colaux3 = self.global_vars.colaux
                                    self.global_vars.usaux = self.global_vars.usosolo[self.global_vars.linaux][self.global_vars.colaux]
                                    # ARPdecliv
                                    # Grava qual trecho o píxel em questão pertence
                                    self.global_vars.numtreaux2 += 1
                            else:
                                # Vai continuar caminhando, mas grava o valor do par (lin,col) do último píxel acessado
                                self.global_vars.linaux2 = self.global_vars.linaux
                                self.global_vars.colaux2 = self.global_vars.colaux
                                self.global_vars.usaux = self.global_vars.usosolo[self.global_vars.linaux][self.global_vars.colaux]

                        print(f'[{pixel_atual}/{80493}] ({pixel_atual/80493*100:.2f}%)', end='\r')

        self.global_vars.Ntre = self.global_vars.numtreauxmax + 1

        # Percorrendo o caminho desde as cabeceiras e granvando as distâncias relativas de cada trecho de uso do solo contínuo

        # Redimenciona variáveis necessárias
        cotaini = np.zeros((self.global_vars.Ncabe,self.global_vars.Ntre))
        self.global_vars.cotaini = cotaini
        cotaini = None
        cotafim = np.zeros((self.global_vars.Ncabe,self.global_vars.Ntre))
        self.global_vars.cotafim = cotafim
        cotafim = None
        Ltre = np.zeros((self.global_vars.Ncabe,self.global_vars.Ntre))
        self.global_vars.Ltre = Ltre
        Ltre = None
        Stre = np.zeros((self.global_vars.Ncabe,self.global_vars.Ntre))
        self.global_vars.Stre = Stre
        Stre = None
        usotre = np.zeros((self.global_vars.Ncabe,self.global_vars.Ntre))
        self.global_vars.usotre = usotre
        usotre = None
        DISTult = np.zeros((self.global_vars.Ncabe,self.global_vars.Ntre))
        self.global_vars.DISTult = DISTult
        DISTult = None
        refcabtre  = np.zeros((self.rdc_vars.nlin,self.rdc_vars.ncol))
        self.global_vars.refcabtre = refcabtre
        refcabtre = None
        DISTtre  = np.zeros((self.rdc_vars.nlin,self.rdc_vars.ncol))
        self.global_vars.DISTtre = DISTtre
        DECLIVpix  = np.zeros((self.rdc_vars.nlin,self.rdc_vars.ncol))
        self.global_vars.DECLIVpix = DECLIVpix
        DECLIVpix = None
        CABEpix = np.zeros((self.rdc_vars.nlin,self.rdc_vars.ncol))
        self.global_vars.CABEpix = CABEpix
        CABEpix = None
        numtre = np.zeros(self.global_vars.Ncabe)
        self.global_vars.numtre = numtre
        numtre = None

        pixel_atual = 0
        # Continua o cálculo dos trechos
        for col in range(1, self.rdc_vars.ncol-1):
            for lin in range(1, self.rdc_vars.nlin-1):
                # Verificando os elementos da região da bacia
                if self.global_vars.bacia[lin][col] == 1:
                    if self.global_vars.numcabe[lin][col] > 0:
                        pixel_atual +=1
                        self.global_vars.numcabeaux = int(self.global_vars.numcabe[lin][col])
                        self.global_vars.linaux = lin
                        self.global_vars.colaux = col
                        self.global_vars.linaux2 = lin
                        self.global_vars.colaux2 = col
                        self.global_vars.linaux3 = lin
                        self.global_vars.colaux3 = col
                        self.global_vars.numtreaux = 0
                        self.global_vars.caminho = 0
                        self.global_vars.usaux = self.global_vars.usosolo[lin][col]
                        self.global_vars.usaux2 = self.global_vars.usaux

                        # ARPdecliv
                        # Grava qual trecho o píxel em questão pertence
                        self.global_vars.numtreaux2 = 1
                        self.global_vars.TREpix[self.global_vars.linaux2][self.global_vars.colaux2] = self.global_vars.numcabeaux2

                        while self.global_vars.caminho == 0:
                            self.global_vars.diraux = self.global_vars.direcoes[self.global_vars.linaux][self.global_vars.colaux]
                            self.global_vars.linaux += self.global_vars.dlin[self.global_vars.diraux]
                            self.global_vars.colaux += self.global_vars.dcol[self.global_vars.diraux]

                            condicao1 = self.global_vars.usaux != self.global_vars.usosolo[self.global_vars.linaux][self.global_vars.colaux]
                            condicao2 = self.global_vars.dren[self.global_vars.linaux][self.global_vars.colaux] == 1

                            if condicao1 or condicao2:
                                # Mudou o tipo de uso do solo ou alcançou a rede de drenagem,
                                # então terminou o trecho no píxel anterior
                                self.global_vars.numtreaux += 1
                                self.global_vars.numtre[self.global_vars.numcabeaux-1] = self.global_vars.numtreaux
                                self.global_vars.Ltre[self.global_vars.numcabeaux-1][self.global_vars.numtreaux-1] = self.global_vars.DIST[self.global_vars.linaux3][self.global_vars.colaux3] \
                                                                                                                - self.global_vars.DIST[self.global_vars.linaux][self.global_vars.colaux] 
                                                                                                                
                                # Grava a distância (DIST) do último píxel do trecho
                                self.global_vars.DISTult[self.global_vars.numcabeaux-1][self.global_vars.numtreaux-1] = self.global_vars.DIST[self.global_vars.linaux][self.global_vars.colaux]
                                self.global_vars.cotaini[self.global_vars.numcabeaux-1][self.global_vars.numtreaux-1] = self.global_vars.MDE[self.global_vars.linaux3][self.global_vars.colaux3]
                                self.global_vars.cotafim[self.global_vars.numcabeaux-1][self.global_vars.numtreaux-1] = self.global_vars.MDE[self.global_vars.linaux][self.global_vars.colaux]
                                
                                self.global_vars.Stre[self.global_vars.numcabeaux-1][self.global_vars.numtreaux-1] = (self.global_vars.cotaini[self.global_vars.numcabeaux-1][self.global_vars.numtreaux-1] - self.global_vars.cotafim[self.global_vars.numcabeaux-1][self.global_vars.numtreaux-1]) / self.global_vars.Ltre[self.global_vars.numcabeaux-1][self.global_vars.numtreaux-1]*1000.0

                                self.global_vars.usotre[self.global_vars.numcabeaux-1][self.global_vars.numtreaux-1] = self.global_vars.usaux

                                # ARPlidar: adiciona a bacia como condição; chegar na rede de drenagem ou sair da baica, finaliza while
                                condicao4 = self.global_vars.dren[self.global_vars.linaux][self.global_vars.colaux] == 1 or self.global_vars.bacia[self.global_vars.linaux][self.global_vars.colaux] == 0
                                if condicao4:
                                    self.global_vars.caminho = 1
                                    self.global_vars.refcabtre[self.global_vars.linaux3][self.global_vars.colaux3] = self.global_vars.numtreaux
                                    self.global_vars.refcabtre[self.global_vars.linaux2][self.global_vars.colaux2] = self.global_vars.numtreaux

                                else:
                                    # Vai continuar o caminho, mas em um novo trecho
                                    self.global_vars.refcabtre[self.global_vars.linaux3][self.global_vars.colaux3] = self.global_vars.numtreaux
                                    self.global_vars.refcabtre[self.global_vars.linaux2][self.global_vars.colaux2] = self.global_vars.numtreaux

                                    self.global_vars.linaux3 = self.global_vars.linaux
                                    self.global_vars.colaux3 = self.global_vars.colaux
                                    self.global_vars.linaux2 = self.global_vars.linaux
                                    self.global_vars.colaux2 = self.global_vars.colaux
                                    self.global_vars.usaux = self.global_vars.usosolo[self.global_vars.linaux][self.global_vars.colaux]

                                    # ARPdecliv
                                    # Grava qual trecho o píxel em questão pertence
                                    self.global_vars.numtreaux2 += 1
                                    self.global_vars.TREpix[self.global_vars.linaux2][self.global_vars.colaux2] = self.global_vars.numtreaux2

                            else:
                                # Vai continuar caminhando, mas grava o valor do par (lin,col) do último píxel acessado
                                self.global_vars.refcabtre[self.global_vars.linaux3][self.global_vars.colaux3] = self.global_vars.numtreaux + 1
                                self.global_vars.refcabtre[self.global_vars.linaux2][self.global_vars.colaux2] = self.global_vars.numtreaux + 1
                                
                                self.global_vars.linaux2 = self.global_vars.linaux
                                self.global_vars.colaux2 = self.global_vars.colaux
                                self.global_vars.usaux = self.global_vars.usosolo[self.global_vars.linaux][self.global_vars.colaux]

                                # ARPdecliv
                                # Grava qual trecho o píxel em questão pertence
                                self.global_vars.TREpix[self.global_vars.linaux2][self.global_vars.colaux2] = self.global_vars.numtreaux2

                        print(f'[{pixel_atual}/{80493}] ({pixel_atual/80493*100:.2f}%)', end='\r')
        
        # Percorre novamente o caminho desde às cabeceiras, gravando distancias relativas de cada pixel dentro de cada trecho de uso do solo continuo
        # Percorrendo os elementos da bacia hidrográfica
        pixel_atual = 0
        for col in range(1, self.rdc_vars.ncol-1):
            for lin in range(1, self.rdc_vars.nlin-1):
                # Os cálculos são executados apenas na região da bacia hidrográfica
                if self.global_vars.bacia[lin][col] == 1:
                    # ARPlidar
                    if self.global_vars.numcabe[lin][col] > 0:
                        pixel_atual += 1
                        self.global_vars.numcabeaux = int(self.global_vars.numcabe[lin][col])
                        self.global_vars.linaux = lin
                        self.global_vars.colaux = col
                        self.global_vars.linaux2 = lin
                        self.global_vars.colaux2 = col
                        self.global_vars.linaux3 = lin
                        self.global_vars.colaux3 = col
                        self.global_vars.numtreaux = 0
                        self.global_vars.caminho = 0
                        self.global_vars.usaux = self.global_vars.usosolo[lin][col]
                        self.global_vars.usaux2 = self.global_vars.usaux

                        # Grava a distância do píxel relativo ao trecho
                        self.global_vars.DISTtre[self.global_vars.linaux2][self.global_vars.colaux2] = self.global_vars.DIST[lin][col] - self.global_vars.DISTult[self.global_vars.numcabeaux - 1][1]

                        # ARPdecliv: calcula a declividade do píxel relativo ao último píxel do trecho
                        self.global_vars.DECLIVpix[self.global_vars.linaux2][self.global_vars.colaux2] = (self.global_vars.MDE[self.global_vars.linaux2][self.global_vars.colaux2] - self.global_vars.cotafim[self.global_vars.numcabeaux - 1][1]) / self.global_vars.DISTtre[self.global_vars.linaux2][self.global_vars.colaux2]*1000.0

                        # Grava qual cabeceira o píxel em questão faz parte
                        self.global_vars.CABEpix[self.global_vars.linaux2][self.global_vars.colaux2] = self.global_vars.numcabeaux

                        while self.global_vars.caminho == 0:
                            self.global_vars.diraux = self.global_vars.direcoes[self.global_vars.linaux][self.global_vars.colaux]
                            self.global_vars.linaux += self.global_vars.dlin[self.global_vars.diraux]
                            self.global_vars.colaux += self.global_vars.dcol[self.global_vars.diraux]

                            condicao1 = self.global_vars.usaux != self.global_vars.usosolo[self.global_vars.linaux][self.global_vars.colaux]
                            condicao2 = self.global_vars.dren[self.global_vars.linaux][self.global_vars.colaux] == 1     

                            if condicao1 or condicao2:
                                # Mudou o tipo de uso do solo ou alcançou a rede de drenagem, 
                                # então terminou um trecho no píxel anterior
                                self.global_vars.numtreaux += 1
                                self.global_vars.numtre[self.global_vars.numtreaux-1] = self.global_vars.numtreaux
                                
                                # Grava a distância do píxel relativo ao trecho
                                self.global_vars.DISTtre[self.global_vars.linaux][self.global_vars.colaux] = self.global_vars.DIST[self.global_vars.linaux][self.global_vars.colaux] - self.global_vars.DISTult[self.global_vars.numcabeaux-2][self.global_vars.numtreaux-1]

                                self.global_vars.usotre[self.global_vars.numcabeaux-1][self.global_vars.numtreaux-1] = self.global_vars.usaux

                                # ARPlidar: adiciona a bacia hidrográfica como uma condição
                                condicao5 = self.global_vars.dren[self.global_vars.linaux][self.global_vars.colaux] == 1 or self.global_vars.bacia[self.global_vars.linaux][self.global_vars.colaux] == 0
                                if condicao5:
                                    self.global_vars.caminho = 1

                                else:
                                    # Vai continuar o caminho, porém em um novo trecho
                                    self.global_vars.linaux3 = self.global_vars.linaux
                                    self.global_vars.colaux3 = self.global_vars.colaux
                                    self.global_vars.linaux2 = self.global_vars.linaux
                                    self.global_vars.colaux2 = self.global_vars.colaux
                                    self.global_vars.usaux = self.global_vars.usosolo[self.global_vars.linaux][self.global_vars.colaux]

                                    # Grava qual cabeceira o píxel em questão faz parte
                                    self.global_vars.CABEpix[self.global_vars.linaux2][self.global_vars.colaux2] = self.global_vars.numcabeaux

                                    # ARPdecliv: cálcula a declividade do píxel relativo ao último píxel do trecho
                                    self.global_vars.DECLIVpix[self.global_vars.linaux2][self.global_vars.colaux2] = (self.global_vars.MDE[self.global_vars.linaux2][self.global_vars.colaux2] - self.global_vars.cotafim[self.global_vars.numcabeaux - 2][self.global_vars.numtreaux - 1]) / float(self.global_vars.DISTtre[self.global_vars.linaux2][self.global_vars.colaux2])*1000.0


                            else:                     
                            # Vai continuar caminhando, e grava os valores dos pares (nlin,ncol) do último píxel que passou           
                                self.global_vars.linaux2 = self.global_vars.linaux
                                self.global_vars.colaux2 = self.global_vars.colaux
                                self.global_vars.usaux = self.global_vars.usosolo[self.global_vars.linaux][self.global_vars.colaux]

                                # Grava qual cabeceira o píxel em questão pertence
                                self.global_vars.CABEpix[self.global_vars.linaux2][self.global_vars.colaux2] = self.global_vars.numcabeaux

                                # Grava a DIST do píxel relativo ao trecho
                                self.global_vars.DISTtre[self.global_vars.linaux2][self.global_vars.colaux2] = self.global_vars.DIST[self.global_vars.linaux2][self.global_vars.colaux2] \
                                                                                                                - self.global_vars.DISTult[self.global_vars.numcabeaux - 2][self.global_vars.numtreaux - 1]

                        print(f'[{pixel_atual}/{80493}] ({pixel_atual/80493*100:.2f}%)', end='\r')

        self.fim = perf_counter()
        print(f'{(self.fim - self.inicio)/60} min')                        
        print('Passou dist_trecho')

    def tempo_canal(self):
        '''
        Esta função é responsável por determinar o tempo de viagem/concentração da água da foz até o exutório da bacia hidrográfica
        '''
        # Declara e redemenciona variáveis
        condicao = None
        condicao2 = None
        self.classerio_aux = np.zeros((self.rdc_vars.nlin,self.rdc_vars.ncol))
        TempoRio = np.zeros((self.rdc_vars.nlin,self.rdc_vars.ncol))
        self.global_vars.TempoRio = TempoRio
        TempoRio = None

        for col in range(self.rdc_vars.ncol):
            for lin in range(self.rdc_vars.nlin):
                # O cáclulos são executados apenas na região da bacia
                if self.global_vars.bacia[lin][col] == 1:
                    # ainda, os cálculos acontecerão na rede de drenagem da bacia hidrográfica
                    if  self.global_vars.dren[lin][col] == 1:
                        self.global_vars.linaux = lin
                        self.global_vars.colaux = col
                        self.global_vars.linaux1 = lin
                        self.global_vars.colaux1 = col
                        self.global_vars.linaux2 = lin
                        self.global_vars.colaux2 = col
                        self.global_vars.caminho = 0
                        self.global_vars.Tempoauxac = 0

                        # Guarda as características do tipo de trecho que o píxel em questão faz parte
                        self.classerio_aux = self.global_vars.classerio[lin][col]

                        while self.global_vars.caminho == 0:
                            condicao = self.global_vars.linaux < 1 or self.global_vars.linaux > self.rdc_vars.nlin or self.global_vars.colaux < 1 or self.global_vars.colaux > self.rdc_vars.ncol    
                            
                            if condicao:
                                self.global_vars.caminho = 1

                                # Contabilizando o último trecho
                                self.global_vars.Lfozaux1 = self.global_vars.Lfoz[self.global_vars.linaux1][self.global_vars.colaux1]
                                self.global_vars.Lfozaux2 = self.global_vars.Lfoz[self.global_vars.linaux2][self.global_vars.colaux2]
                                # Determina a diferença entre o píxel do Lfoz inicial e o do final
                                self.global_vars.Laux = self.global_vars.Lfozaux1 - self.global_vars.Lfozaux2
                                
                                # A declividade(Saux), o coeficiente de Manning(naux) e o raio hidráulico(Rhaux) são aqueles do tipo de rio (rede de drenagem)
                                self.global_vars.Saux = self.global_vars.Sclasse[self.classerio_aux]
                                self.global_vars.naux = self.global_vars.Mannclasse[self.classerio_aux]
                                self.global_vars.Rhaux = self.global_vars.Rhclasse[self.classerio_aux]

                                # Determinando a velocidade do percurso
                                condicao1 = self.global_vars.linaux2 == self.global_vars.linaux and self.global_vars.colaux2 == self.global_vars.colaux1
                                if condicao1:
                                    # Significa que não há mudança de pixel, ou seja, o pixel a montante é igual ao de jusante
                                    self.global_vars.Velaux = 0
                                    self.global_vars.Tempoaux = 0
                                else:
                                    # Determina a velocidade por percurso
                                    self.global_vars.Velaux = self.global_vars.Rhaux ** (2.0/3.0)*self.global_vars.Saux**(1.0/2.0)/self.global_vars.naux
                                    
                                    # Calculando o tempo de viagem/concentração do percuso em min
                                    # em que: Laux em metros e Velaux em m/s; resultado em min
                                    self.global_vars.Tempoaux = self.global_vars.Laux / self.global_vars.Velaux / 60.0
                                
                                # O tempo é acocumulado desde o primeiro percurso
                                self.global_vars.Tempoauxac += self.global_vars.Tempoaux
                            
                                # Após o fim do traçado desde o inicío do píxel, o tempo será armazenado e o acumulador zerado
                                self.global_vars.TempoRio[lin][col] = self.global_vars.Tempoauxac
                                self.global_vars.Tempoauxac = 0
                        
                            else:
                                condicao2 = self.global_vars.classerio[self.global_vars.linaux][self.global_vars.colaux] != self.classerio_aux
                                # Checando se o caminho ainda está no trecho de mesma classe
                                if condicao2:
                                    self.global_vars.Lfozaux1 = self.global_vars.Lfoz[self.global_vars.linaux1][self.global_vars.colaux1]
                                    self.global_vars.Lfozaux2 = self.global_vars.Lfoz[self.global_vars.linaux2][self.global_vars.colaux2]

                                    # Determina a diferença entre o píxel do Lfoz inicial e o do final
                                    self.global_vars.Laux = self.global_vars.Lfozaux1 - self.global_vars.Lfozaux2
                                    
                                    # A declividade(Saux), o coeficiente de Manning(naux) e o raio hidráulico(Rhaux) são aqueles do tipo de rio (rede de drenagem)
                                    self.global_vars.Saux = self.global_vars.Sclasse[self.classerio_aux]
                                    self.global_vars.naux = self.global_vars.Mannclasse[self.classerio_aux]
                                    self.global_vars.Rhaux = self.global_vars.Rhclasse[self.classerio_aux]

                                    # Determinando a velocidade do percurso
                                    condicao1 = self.global_vars.linaux2 == self.global_vars.linaux and self.global_vars.colaux2 == self.global_vars.colaux1
                                    if condicao1:
                                        self.global_vars.Velaux = 0
                                        self.global_vars.Tempoaux = 0
                                    else:
                                        self.global_vars.Velaux = self.global_vars.Rhaux ** (2.0/3.0)*self.global_vars.Saux**(1.0/2.0)/self.global_vars.naux
                                        
                                        # Calculando o tempo de viagem/concentração do percuso em min 
                                        # em que: Laux em metros e Velaux em m/s; resultado em min
                                        self.global_vars.Tempoaux = self.global_vars.Laux / self.global_vars.Velaux / 60.0
                                    
                                    # O tempo é acocumulado desde o primeiro percurso
                                    self.global_vars.Tempoauxac += self.global_vars.Tempoaux

                                    # Atualizando o novo ponto de partida
                                    self.global_vars.linaux1 = self.global_vars.linaux
                                    self.global_vars.colaux1 = self.global_vars.colaux
                                    self.classerio_aux = self.global_vars.classerio[self.global_vars.linaux1][self.global_vars.colaux1]
                                
                                # Armazenando o píxel contabilizado
                                self.global_vars.linaux2 = self.global_vars.linaux
                                self.global_vars.colaux2 = self.global_vars.colaux  

                                # Deteminando o próximo píxel do caminho
                                self.global_vars.diraux = self.global_vars.direcoes[self.global_vars.linaux][self.global_vars.colaux]
                                self.global_vars.caminho = 0 
                                self.global_vars.linaux += self.global_vars.dlin[self.global_vars.diraux]
                                self.global_vars.colaux += self.global_vars.dcol[self.global_vars.diraux]

        self.fim = perf_counter()
        print(f'{(self.fim - self.inicio)/60} min') 
        print('passou tempo canal')

    def tempo_sup(self):
        """
        Esta função função determina o tempo de concentração/escoamento para os píxels da superfície da rede de drenagem (aqueles que não são canais)
        """
        # Redimenciona as variáveis necessárias
        lincabe = np.zeros(self.global_vars.numcabeaux)
        self.global_vars.lincabe = lincabe
        lincabe = None
        colcabe = np.zeros(self.global_vars.numcabeaux)
        self.global_vars.colcabe = colcabe
        colcabe = None
        TS = np.zeros((self.global_vars.numcabeaux, self.global_vars.Ntre))
        self.global_vars.TS = TS
        TS = None
        TScabe = np.zeros(self.global_vars.numcabeaux)
        self.global_vars.TScabe = TScabe
        TScabe = None
        TScabe2d = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol))
        self.global_vars.TScabe2d = TScabe2d
        TScabe2d = None
        TSnaocabe2d = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol))
        self.global_vars.TSnaocabe2d = TSnaocabe2d
        TSnaocabe2d = None
        TSpixacum = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol))
        self.global_vars.TSpixacum = TSpixacum
        TSpixacum = None

        for lin in range(self.rdc_vars.nlin):
            for col in range(self.global_vars):
                if self.global_vars.numcabe[lin][col] > 0:
                    self.global_vars.numcabeaux = int(self.global_vars.numcabe[lin][col])
                    self.global_vars.lincabe[self.global_vars.numcabeaux] = lin
                    self.global_vars.colcabe[self.global_vars.numcabeaux] = col


        for item in range(self.global_vars.Ncabec):
            self.global_vars.numtreaux = self.global_vars.numtre[item]
            for t in range(self.global_vars.numtreaux):
                self.global_vars.usaux = self.global_vars.numtre[self.global_vars.numcabeaux][t]
                self.global_vars.Ltreaux = self.global_vars.Ltre[self.global_vars.numcabeaux][t]
                self.global_vars.Streaux = self.global_vars.Stre[self.global_vars.numcabeaux][t] 

                if self.global_vars.Streaux > 0:
                    # Determinando o Ts: tempo de concentração
                    self.global_vars.TS[self.global_vars.numcabeaux][t] = 5.474 * ((self.global_vars.Mann[self.global_vars.usaux]*self.global_vars.Ltreaux)**0.8)/((self.global_vars.P24**0.5)*((self.global_vars.Streaux/1000.0)**0.4))
                else:
                    self.global_vars.TS[self.global_vars.numcabeaux][t] = 0
                
                self.global_vars.TScabe[self.global_vars.numcabeaux] += self.global_vars.TS[self.global_vars.numcabeaux][t]
            
            lin1 = self.global_vars.lincabe[self.global_vars.numcabeaux]
            col1 = self.global_vars.colcabe[self.global_vars.numcabeaux]
            self.global_vars.TScabe2d[lin1][col1] = self.global_vars.TScabe[self.global_vars.numcabeaux]
        
        for lin in range(self.rdc_vars.nlin):
            for col in range(self.rdc_vars.ncol):
                # As ações são baseadas na região da bacia hidrográfica
                if self.global_vars.bacia[lin][col] == 1:
                    self.global_vars.numcabeaux = int(self.global_vars.CABEpix[lin][col])
                    self.global_vars.Taux = 0

                    # Verificando se o píxel é válido; executando cabeceiras
                    if self.global_vars.numcabeaux > 0 and self.global_vars.numcabe[lin][col] == 0:
                        
                        self.global_vars.t = self.global_vars.refcabtre[lin][col]
                        self.global_vars.Ltreaux = self.global_vars.Ltre[self.global_vars.numcabeaux][self.global_vars.t]
                        self.global_vars.Ttreaux = self.global_vars.TS[self.global_vars.numcabeaux][self.global_vars.t]
                        self.global_vars.DISTtreaux = self.global_vars.DISTtre[lin][col]
                        self.global_vars.Taux = self.global_vars.DISTtreaux * self.global_vars.Ttreaux / self.global_vars.Ltreaux

                        # ARPdecliv
                        if self.global_vars.subtipodecliv == 'b':
                            self.global_vars.Streaux = self.global_vars.Stre[self.global_vars.numcabeaux][self.global_vars.t]
                            self.global_vars.usaux = self.global_vars.usotre[self.global_vars.numcabeaux][self.global_vars.t]
                            
                            if self.global_vars.Streaux > 0:
                                self.global_vars.Taux = 5.474 * ((self.global_vars.Mann[self.global_vars.usaux] * self.global_vars.DISTtreaux)**0.8) / ((self.global_vars.P24**0.5)*((self.global_vars.Streaux / 1000.0)**0.4))
                            else:
                                self.global_vars.Taux = 0

                        self.global_vars.numtreaux = self.global_vars.numtre[self.global_vars.numcabeaux]

                        if self.global_vars.t < self.global_vars.numtreaux:
                            tt = self.global_vars.t + 1
                            for tt in range(self.global_vars.numtreaux):
                                self.global_vars.Taux += self.global_vars.TS[self.global_vars.numcabeaux][tt]
                        
                        self.global_vars.TSnaocabe2d[lin][col] = self.global_vars.Taux

        self.global_vars.TStodos2d = self.global_vars.TSnaocabe2d + self.global_vars.TScabe2d

        if self.global_vars.tipo_decliv == 4:

            for col in range(self.rdc_vars.ncol):
                for lin in range(self.rdc_vars.nlin):
                    # Exclindo a região fora da bacia
                    self.global_vars.linaux = lin
                    self.global_vars.colaux = col
                    self.global_vars.caminho = 0 
                    self.global_vars.tempocam = 0.0
                    
                    # Para píxels que representam a rede de drenagem
                    if self.global_vars.dren[lin][col]== 1:
                        self.global_vars.caminho = 1
                    else:
                        while self.global_vars.caminho == 0:
                            condicao = self.global_vars.linaux <= 1 or self.global_vars.linaux >=self.rdc_vars.nlin or self.global_vars.colaux <= 1 or self.global_vars.colaux >=self.rdc_vars.nlin \
                                                                    or self.global_vars.bacia[self.global_vars.colaux][self.global_vars.colaux]==0
                            if condicao:
                                self.global_vars.caminho = 1
                            else:
                                if self.global_vars.dren[self.global_vars.linaux][self.global_vars.colaux]:
                                    # Alcançou a rede de drenagem: encerra a busca
                                    self.global_vars.caminho = 1
                                    self.global_vars.TSpixacum[lin][col] = self.global_vars.tempocam
                                else:
                                    self.global_vars.diraux = self.global_vars.direcoes[self.global_vars.linaux][self.global_vars.colaux]
                                    self.global_vars.caminho = 0

                                    self.global_vars.colaux2 = self.global_vars.colaux
                                    self.global_vars.linaux2 = self.global_vars.linaux

                                    # Calculando a distância incremental percorrida
                                    self.global_vars.linaux += self.global_vars.dlin[self.global_vars.diraux]
                                    self.global_vars.colaux += self.global_vars.dcol[self.global_vars.diraux]

                                    # Atualizando o tempo de escoamento desde o píxel inicial
                                    self.global_vars.tempocam += self.global_vars.TSpix[self.global_vars.linaux2][self.global_vars.colaux2]
        self.fim = perf_counter()
        print(f'{(self.fim - self.inicio)/60} min') 
        print('passou tempo superficie')
        
    def tempo_total_func(self):
        '''
        Esta função determina o tempo total de escoamento/concentração da bacia hidrográfica
        '''
        # Redimenciona as variáveis necessárias
        TempoTot = np.zeros((self.rdc_vars.nlin,self.rdc_vars.ncol))
        self.global_vars.TempoTot = TempoTot
        TempoTot = None

        for col in range(self.rdc_vars.ncol):
            for lin in range(self.rdc_vars.nlin):
                # Os procedimentos são realizados ao longo da bacia hidrográfica
                if self.global_vars.bacia[lin][col] == 1:
                    # Ainda, as verificaçãoes seão baseadas na rede de drenagem
                    if self.global_vars.dren[lin][col] == 1:
                        self.global_vars.TempoTot[lin][col] = self.global_vars.TempoRio[lin][col]
                    else:
                        # ARPlidar: otimização
                        self.global_vars.pixel_ref_dren = self.global_vars.pixeldren[lin][col]
                        if self.global_vars.pixel_ref_dren == 1:
                            self.global_vars.ll = self.global_vars.lincontadren[self.global_vars.pixel_ref_dren]
                            self.global_vars.cc = self.global_vars.colcontadren[self.global_vars.pixel_ref_dren]
                            self.global_vars.auxTempoCanal = self.global_vars.TempoRio[self.global_vars.ll][self.global_vars.cc]
                    # ARPtest
                    if self.global_vars.tipo_decliv == 1 or self.global_vars.tipo_decliv == 2 or self.global_vars.tipo_decliv == 3:
                        self.global_vars.TempoTot[lin][col] = self.global_vars.TStodos2d[lin][col] + self.global_vars.auxTempoCanal

                    if self.global_vars.tipo_decliv == 4:
                        self.global_vars.TempoTot[lin][col] = self.global_vars.TSpixacum[lin][col] + self.global_vars.auxTempoCanal

    def min_max(self):
        """
        Esta função determinar os limites das variáveis varMax e varMin 
        """
        self.rdc_vars.Varmax = -1.0e7
        self.rdc_vars.Varmin = 1.0e7

        if self.rdc_vars.tipoMM == 2:
            for col in range(self.rdc_vars.ncol3):
                for lin in range(self.rdc_vars.nlin3):
                    if self.rdc_vars.VarMM2[lin][col] > self.rdc_vars.Varmax:
                        self.rdc_vars.Varmax = self.rdc_vars.VarMM2[lin][col]
                    
                    elif self.rdc_vars.VarMM2[lin][col] < self.rdc_vars.Varmin:
                        self.rdc_vars.Varmin = self.rdc_vars.VarMM2[lin][col]

        else:
            for col in range(self.rdc_vars.ncol3):
                for lin in range(self.rdc_vars.nlin3):
                    if self.rdc_vars.VarMM3[lin][col][self.rdc_vars.i3] > self.rdc_vars.Varmax:
                        self.rdc_vars.Varmax = self.rdc_vars.VarMM3[lin][col][self.rdc_vars.i3]
                        
                    elif self.rdc_vars.VarMM3[lin][col][self.rdc_vars.i3] < self.rdc_vars.Varmin:
                        self.rdc_vars.Varmin = self.rdc_vars.VarMM3[lin][col][self.rdc_vars.i3]

# Funções para as rotinas Flow Travel Time (versão Dário), Excess rainfall e flow routing
    def tempo_concentracao(self):
        '''Está função calcula o tempo de concentração para a bacia hidrográfica fornecida'''
        # Definição das variáveis
        self.global_vars.Seq = np.zeros((self.rdc_vars.nlin,self.rdc_vars.ncol))
        self.global_vars.decliv_pixel = np.zeros((self.rdc_vars.nlin,self.rdc_vars.ncol))

        # Determinação do Manning do pixel e determinação do parâmetro K para o cálculo do Shallow concentrated flow
        print('Entrou def coef K')
        for col in range(self.rdc_vars.ncol):
            for lin in range(self.rdc_vars.nlin):
                if self.global_vars.bacia[lin,col] == 1:
                    pixel_atual += 1

                    for k in range(self.global_vars.n_tipo_uso):
                        if self.global_vars.usosolo[lin,col] == self.global_vars.usaux[k]:
                            self.global_vars.nSolo[lin,col] = self.global_vars.Mann[k]
                            self.global_vars.coef_k_pixel[lin,col] = self.global_vars.coef_K[k]
                    print(f'[{pixel_atual}/{(np.count_nonzero(self.global_vars.bacia))}] ({pixel_atual/(np.count_nonzero(self.global_vars.bacia))*100:.2f}%)', end='\r')      
                              
        # Determinação do comprimento L ao longo do escoamento dentro do pixel
        print('Verifica direção de escoamento 1')
        for col in range(1, self.rdc_vars.ncol - 1):
            for lin in range(1, self.rdc_vars.nlin - 1):
                if self.global_vars.direcoes[lin,col] == 45:
                    self.global_vars.comp_pixel[lin,col] = self.global_vars.dx * self.global_vars.diagonal

                if self.global_vars.direcoes[lin,col] == 90:
                    self.global_vars.comp_pixel[lin,col] = self.global_vars.dx * self.global_vars.lado

                if self.global_vars.direcoes[lin,col] == 135:
                    self.global_vars.comp_pixel[lin,col] = self.global_vars.dx * self.global_vars.diagonal

                if self.global_vars.direcoes[lin,col] == 180:
                    self.global_vars.comp_pixel[lin,col] = self.global_vars.dx * self.global_vars.lado

                if self.global_vars.direcoes[lin,col] == 225:
                    self.global_vars.comp_pixel[lin,col] = self.global_vars.dx * self.global_vars.diagonal

                if self.global_vars.direcoes[lin,col] == 270:
                    self.global_vars.comp_pixel[lin,col] = self.global_vars.dx * self.global_vars.lado
      
                if self.global_vars.direcoes[lin,col] == 315:
                    self.global_vars.comp_pixel[lin,col] = self.global_vars.dx * self.global_vars.diagonal

                if self.global_vars.direcoes[lin,col] == 360:
                    self.global_vars.comp_pixel[lin,col] = self.global_vars.dx * self.global_vars.lado
                      

        # Determinção da declividade S dos pixels do escoamento em superfície (caso o pixel a jusante tenha uma cota maior que o oixel que se quer estimar a declividade,
        # a rotina sai procurando o pixel com cota menor que esteja a jusante e a declividade é caluclada como sendo a diferença de cotas dividida pela distância percorrida pelo escoamento até o pixel com cota menor)

        print('Determina declividade do pixel')
        pixel_atual = 0

        for lin in range(self.rdc_vars.nlin):
            for col in range(self.rdc_vars.ncol):
                if self.global_vars.bacia[lin,col] == 1:
                    pixel_atual += 1

                    if self.global_vars.direcoes[lin,col] == 45:
                        i_test = lin - 1
                        j_test = col + 1

                    elif self.global_vars.direcoes[lin,col] == 90:
                        i_test = lin
                        j_test = col + 1

                    elif self.global_vars.direcoes[lin,col] == 135:
                        i_test = lin + 1
                        j_test = col + 1

                    elif self.global_vars.direcoes[lin,col] == 180:
                        i_test = lin + 1
                        j_test = col

                    elif self.global_vars.direcoes[lin,col] == 225:
                        i_test = lin + 1
                        j_test = col - 1

                    elif self.global_vars.direcoes[lin,col] == 270:
                        i_test = lin
                        j_test = col - 1

                    elif self.global_vars.direcoes[lin,col] == 315:
                        i_test = lin - 1
                        j_test = col - 1
        
                    elif self.global_vars.direcoes[lin,col] == 360:
                        i_test = lin - 1
                        j_test = col
                    
                    # Determinação da declividade do pixel em questão
                    self.global_vars.decliv_pixel[lin,col] = (self.global_vars.MDE[lin,col] - self.global_vars.MDE[i_test,j_test]) / self.global_vars.comp_pixel[lin,col]

                    if self.global_vars.decliv_pixel[lin,col] <= self.global_vars.Smin:
                        self.global_vars.decliv_pixel[lin,col] = self.global_vars.Smin
                    
                    print(f'[{pixel_atual}/{(np.count_nonzero(self.global_vars.bacia))}] ({pixel_atual/(np.count_nonzero(self.global_vars.bacia))*100:.2f}%)', end='\r')      

        # Identificação dos pixels da rede de drenagem que INICIAM os trechos com características homogêneas. Nesses pixel a variável Divisao_Trecho = 1
        # Existem trechos pré definidos onde já existe informação sobre as seções transversais, esses trechos e a informação sobre eles são carregados pelo usuário e permanecem valendo
        # No entanto, há outras partes da rede de drenagem sem informação sobre a seção transversal. Essas outras partes do rio foram subdividas em trechos homogêneos. O início e o fim desses trechos foram determinados assim:
        # 1) Um trecho pode possuir no máximo um comprimento igual a "Comprimento_Trecho" 
        # 2) Se há o encontro com outro rio o trecho termina e a partir do ponto de encontro começa outro trecho
        # 3) Se há o encontro com uma parte do rio que já possua informação sobre a seção transversal carregada pelo usuário, o trecho termina.
        
        # Identificação dos pixels que iniciam a rede de drenagem
        print('Determinação dos pixels que são cabeceira')
        pixel_atual = 0
        for lin in range(self.rdc_vars.nlin):
            for col in range(self.rdc_vars.ncol):
                if self.global_vars.dren[lin,col] == 1:
                    pixel_atual += 1

                    k = 0
                    if self.global_vars.direcoes[lin-1,col-1] == 135 and self.global_vars.dren[lin-1,col-1] == 1:
                        k+=1
                    elif self.global_vars.direcoes[lin-1,col] == 180 and self.global_vars.dren[lin-1,col] == 1:
                        k+=1
                    elif self.global_vars.direcoes[lin-1,col+1] == 225 and self.global_vars.dren[lin-1,col+1] == 1:
                        k+=1
                    elif self.global_vars.direcoes[lin,col+1] == 270 and self.global_vars.dren[lin,col+1] == 1:
                        k+=1
                    elif self.global_vars.direcoes[lin+1,col+1] == 315 and self.global_vars.dren[lin+1,col+1] == 1:
                        k+=1
                    elif self.global_vars.direcoes[lin+1,col] == 360 and self.global_vars.dren[lin+1,col] == 1:
                        k+=1
                    elif self.global_vars.direcoes[lin+1,col-1] == 45 and self.global_vars.dren[lin+1,col-1] == 1:
                        k+=1
                    elif self.global_vars.direcoes[lin,col-1] == 90 and self.global_vars.dren[lin,col-1] == 1:
                        k+=1                  

                    # Se k > 0 significa que aquele pixel da rede drenagem não inicia a rede de drenagem
                    # Se k = 0 significa que aquele pixel da rede de drenagem inicia a rede de drenagem, ou seja, nenhum outro pixel da rede de drenagem escoa para ele 

                    if k == 0:
                        # Se um pixel da rede de drenagem inicia a rede de drenagem significa que ele inicia um trecho da rede de drenagem e portanto a variável Divisao_Trecho = 1
                        self.global_vars.divisao_trecho[lin,col] = 1
                    
                        # Agora a rotina vai procurar os pixels a jusante desse pixel de início da rede de drenagem que iniciam um outro trecho homogêneo
                        i_atual = lin
                        j_atual = col
                        
                        self.global_vars.comp_total[i_atual, j_atual] = self.global_vars.comp_pixel[lin,col]

                        while self.global_vars.bacia[i_atual,j_atual] == 1:
                            if self.global_vars.direcoes[i_atual, j_atual] == 45:
                                i_test = i_atual - 1
                                j_test = j_atual + 1

                            elif self.global_vars.direcoes[i_atual, j_atual] == 90:
                                i_test = i_atual
                                j_test = j_atual + 1

                            elif self.global_vars.direcoes[i_atual, j_atual] == 135:
                                i_test = i_atual + 1
                                j_test = j_atual + 1

                            elif self.global_vars.direcoes[i_atual, j_atual] == 180:
                                i_test = i_atual + 1
                                j_test = j_atual

                            elif self.global_vars.direcoes[i_atual, j_atual] == 225:
                                i_test = i_atual + 1
                                j_test = j_atual - 1

                            elif self.global_vars.direcoes[i_atual, j_atual] == 270:
                                i_test = i_atual
                                j_test = j_atual - 1

                            elif self.global_vars.direcoes[i_atual, j_atual] == 315:
                                i_test = i_atual - 1
                                j_test = j_atual - 1
                
                            elif self.global_vars.direcoes[i_atual, j_atual] == 360:
                                i_test = i_atual - 1
                                j_test = j_atual     

                            # Quando se chega ao exutório da bacia, a rotina para e é o final do trecho, com Divisao_Trecho = 1
                            if self.global_vars.bacia[i_test, j_test] == 0:
                                self.global_vars.divisao_trecho[i_atual, j_atual] = 1
                            
                            self.global_vars.comp_total[i_test, j_test] = self.global_vars.comp_total[i_atual, j_atual] + self.global_vars.comp_pixel[i_test, j_test]

                            # Inicia um novo trecho caso o trecho em questão já tenha alcançado seu comprimento máximo definido pelo usuário
                            if self.global_vars.comp_total[i_test, j_test] > self.global_vars.max_comp_trecho:
                                self.global_vars.divisao_trecho[i_test, j_test] = 1
                                self.global_vars.comp_total[i_test, j_test] = 0

                            # Inicia outro trecho caso haja o encontro com outro curso d'água 
                            k = 0       
                            if self.global_vars.direcoes[i_test-1,j_test-1] == 135 and self.global_vars.dren[i_test-1,j_test-1] == 1:
                                k +=1
                            elif self.global_vars.direcoes[i_test-1,j_test] == 180 and self.global_vars.dren[i_test-1,j_test] == 1:
                                k+=1
                            elif self.global_vars.direcoes[i_test-1,j_test+1] == 225 and self.global_vars.dren[i_test-1,j_test+1] == 1:
                                k+=1
                            elif self.global_vars.direcoes[i_test,j_test+1] == 270 and self.global_vars.dren[i_test,j_test+1] == 1:
                                k+=1
                            elif self.global_vars.direcoes[i_test+1,j_test+1] == 315 and self.global_vars.dren[i_test+1,j_test+1] == 1:
                                k+=1
                            elif self.global_vars.direcoes[i_test+1,j_test] == 360 and self.global_vars.dren[i_test+1,j_test] == 1:
                                k+=1
                            elif self.global_vars.direcoes[i_test+1,j_test-1] == 45 and self.global_vars.dren[i_test+1,j_test-1] == 1:
                                k+=1
                            elif self.global_vars.direcoes[i_test,j_test-1] == 90 and self.global_vars.dren[i_test,j_test-1] == 1:
                                k+=1   

                            if k>1:
                                self.global_vars.divisao_trecho[i_test,j_test] = 1
                                self.global_vars.comp_total[i_test,j_test] = 0

                            # O trecho termina caso haja o encontro com um trecho pré-definido pelo usuário
                            if self.global_vars.classerio[i_test,j_test] > 0:
                                self.global_vars.divisao_trecho[i_test,j_test] = 1
                                i_atual = i_test
                                j_atual = j_test

                                while self.global_vars.bacia[i_atual,j_atual] == 1 and self.global_vars.classerio[i_atual,j_atual] > 0:
                                    if self.global_vars.direcoes[i_atual, j_atual] == 45:
                                        i_test = i_atual - 1
                                        j_test = j_atual + 1

                                    elif self.global_vars.direcoes[i_atual, j_atual] == 90:
                                        i_test = i_atual
                                        j_test = j_atual + 1

                                    elif self.global_vars.direcoes[i_atual, j_atual] == 135:
                                        i_test = i_atual + 1
                                        j_test = j_atual + 1

                                    elif self.global_vars.direcoes[i_atual, j_atual] == 180:
                                        i_test = i_atual + 1
                                        j_test = j_atual

                                    elif self.global_vars.direcoes[i_atual, j_atual] == 225:
                                        i_test = i_atual + 1
                                        j_test = j_atual - 1

                                    elif self.global_vars.direcoes[i_atual, j_atual] == 270:
                                        i_test = i_atual
                                        j_test = j_atual - 1

                                    elif self.global_vars.direcoes[i_atual, j_atual] == 315:
                                        i_test = i_atual - 1
                                        j_test = j_atual - 1
                        
                                    elif self.global_vars.direcoes[i_atual, j_atual] == 360:
                                        i_test = i_atual - 1
                                        j_test = j_atual    

                                    # Permanece a divisão entre trechos homogêneos definida pela usuário
                                    if self.global_vars.classerio[i_test,j_test] != self.global_vars.classerio[i_atual,j_atual]:
                                        self.global_vars.divisao_trecho[i_test,j_test] = 1

                                    if self.global_vars.bacia[i_test,j_test] == 0:
                                        self.global_vars.divisao_trecho[i_test,j_test] = 1

                                    if self.global_vars.classerio[i_test,j_test] == 0:
                                        self.global_vars.divisao_trecho[i_test,j_test] = 1

                                # Fim while 
                                i_atual = i_test
                                j_atual = j_test

                                self.global_vars.comp_total[i_test,j_test] = 0

                            # fim if
                            i_atual = i_test
                            j_atual = j_test   
                    print(f'[{pixel_atual}/{(np.count_nonzero(self.global_vars.bacia))}] ({pixel_atual/(np.count_nonzero(self.global_vars.bacia))*100:.2f}%)', end='\r')      

        # Cálculo da declividade equivalente e raio hidráulico para os trechos da rede de drenagem que não foram carregados pelo usuário
        print('Cálculo da declividade equivalente e raio hidráulico para os trechos da rede de drenagem que não foram carregados pelo usuário')
        pixel_atual = 0
        
        k = self.global_vars.nclasses
        for lin in range(self.rdc_vars.nlin):
            for col in range(self.rdc_vars.ncol):
                if self.global_vars.bacia[lin,col] == 1:
                    pixel_atual += 1

                    # Identifica o pixel que inicia um trecho sem informação sebre a seção transversal
                    if self.global_vars.divisao_trecho[lin,col] == 1:

                        if self.global_vars.classerio[lin,col] == 0:
                            k +=1
                            self.global_vars.comp_total[lin,col] = self.global_vars.comp_pixel[lin,col]
                            if self.global_vars.direcoes[lin,col] == 45:
                                i_atual = lin - 1
                                j_atual = col + 1

                            elif self.global_vars.direcoes[lin,col] == 90:
                                i_atual = lin
                                j_atual = col + 1

                            elif self.global_vars.direcoes[lin,col] == 135:
                                i_atual = lin + 1
                                j_atual = col + 1

                            elif self.global_vars.direcoes[lin,col] == 180:
                                i_atual = lin + 1
                                j_atual = col

                            elif self.global_vars.direcoes[lin,col] == 225:
                                i_atual = lin + 1
                                j_atual = col - 1

                            elif self.global_vars.direcoes[lin,col] == 270:
                                i_atual = lin
                                j_atual = col - 1

                            elif self.global_vars.direcoes[lin,col] == 315:
                                i_atual = lin - 1
                                j_atual = col - 1
                
                            elif self.global_vars.direcoes[lin,col] == 360:
                                i_atual = lin - 1
                                j_atual = col
                                                                      
                            if self.global_vars.divisao_trecho[i_atual,j_atual] == 1 or self.global_vars.bacia[i_atual,j_atual] == 0:
                                # Definição das características da seção transversal do pixel canal
                                self.global_vars.Seq[lin,col] = self.global_vars.decliv_pixel[lin,col]
                                self.global_vars.area_molhada[lin,col] = self.global_vars.coef_c * (self.global_vars.dren_area[lin,col]**self.global_vars.coef_d)
                                self.global_vars.bankfull_width[lin,col] = self.global_vars.coef_g * (self.global_vars.dren_area[lin,col]**self.global_vars.coef_h)
                                perimetro_molhado = ((((2 * (10 ** (1 / 2))) - 2) / 3) * ((self.global_vars.bankfull_width[lin,col] - (((self.global_vars.bankfull_width[lin,col] ** 2) - ((4 / 3) * self.global_vars.area_molhada[lin,col])) ** (1 / 2))) / (2 / 3))) + self.global_vars.bankfull_width[lin,col]
                                raio_hidraulico = self.global_vars.area_molhada[lin,col] / perimetro_molhado
                                self.global_vars.rh_medio[lin,col] = raio_hidraulico
                                self.global_vars.classerio[lin,col] = k

                            if self.global_vars.divisao_trecho[i_atual,j_atual] != 1 and self.global_vars.bacia[i_atual,j_atual] == 1:
                                self.global_vars.comp_total[i_atual,j_atual] = self.global_vars.comp_total[i_atual,j_atual] + self.global_vars.comp_pixel[i_atual,j_atual]
                                somatorio = (self.global_vars.comp_pixel[lin, col] / (self.global_vars.decliv_pixel[lin, col] ** (1 / 2))) + (self.global_vars.comp_pixel[i_atual,j_atual] / (self.global_vars.decliv_pixel[i_atual,j_atual] ** (1 / 2)))
                                
                                # Definição das características da seção transversal do pixel canal
                                self.global_vars.area_molhada[lin,col] = self.global_vars.coef_c * (self.global_vars.dren_area[lin,col]**self.global_vars.coef_d)
                                self.global_vars.bankfull_width[lin,col] = self.global_vars.coef_g * (self.global_vars.dren_area[lin,col]**self.global_vars.coef_h)
                                perimetro_molhado = ((((2 * (10 ** (1 / 2))) - 2) / 3) * ((self.global_vars.bankfull_width[lin,col] - (((self.global_vars.bankfull_width[lin,col] ** 2) - ((4 / 3) * self.global_vars.area_molhada[lin,col])) ** (1 / 2))) / (2 / 3))) + self.global_vars.bankfull_width[lin,col]
                                raio_hidraulico = self.global_vars.area_molhada[lin,col]/perimetro_molhado
                                self.global_vars.rh_medio[lin,col] = raio_hidraulico       

                                self.global_vars.area_molhada[i_atual,j_atual] = self.global_vars.coef_c * (self.global_vars.dren_area[i_atual,j_atual]**self.global_vars.coef_d)
                                self.global_vars.bankfull_width[i_atual,j_atual] = self.global_vars.coef_g * (self.global_vars.dren_area[i_atual,j_atual]**self.global_vars.coef_h)
                                perimetro_molhado = ((((2 * (10 ** (1 / 2))) - 2) / 3) * ((self.global_vars.bankfull_width[i_atual,j_atual] - (((self.global_vars.bankfull_width[i_atual,j_atual] ** 2) - ((4 / 3) * self.global_vars.area_molhada[i_atual,j_atual])) ** (1 / 2))) / (2 / 3))) + self.global_vars.bankfull_width[i_atual,j_atual]
                                raio_hidraulico = self.global_vars.area_molhada[i_atual,j_atual]/perimetro_molhado
                                self.global_vars.rh_medio[i_atual,j_atual] += raio_hidraulico                                  
                                n = 2

                                # Percorre o caminho de fluxo até encontrar o final do trecho
                                while self.global_vars.divisao_trecho[i_atual,j_atual] != 1 and self.global_vars.bacia[i_atual,j_atual] == 1:
                                    if self.global_vars.direcoes[i_atual, j_atual] == 45:
                                        i_test = i_atual - 1
                                        j_test = j_atual + 1

                                    elif self.global_vars.direcoes[i_atual, j_atual] == 90:
                                        i_test = i_atual
                                        j_test = j_atual + 1

                                    elif self.global_vars.direcoes[i_atual, j_atual] == 135:
                                        i_test = i_atual + 1
                                        j_test = j_atual + 1

                                    elif self.global_vars.direcoes[i_atual, j_atual] == 180:
                                        i_test = i_atual + 1
                                        j_test = j_atual

                                    elif self.global_vars.direcoes[i_atual, j_atual] == 225:
                                        i_test = i_atual + 1
                                        j_test = j_atual - 1

                                    elif self.global_vars.direcoes[i_atual, j_atual] == 270:
                                        i_test = i_atual
                                        j_test = j_atual - 1

                                    elif self.global_vars.direcoes[i_atual, j_atual] == 315:
                                        i_test = i_atual - 1
                                        j_test = j_atual - 1
                        
                                    elif self.global_vars.direcoes[i_atual, j_atual] == 360:
                                        i_test = i_atual - 1
                                        j_test = j_atual    
                                    
                                    if self.global_vars.divisao_trecho[i_test,j_test] == 0:
                                        self.global_vars.area_molhada[lin,col] = self.global_vars.coef_c * (self.global_vars.dren_area[lin,col]**self.global_vars.coef_d)
                                        self.global_vars.bankfull_width[lin,col] = self.global_vars.coef_g * (self.global_vars.dren_area[lin,col]**self.global_vars.coef_h)
                                        perimetro_molhado = ((((2 * (10 ** (1 / 2))) - 2) / 3) * ((self.global_vars.bankfull_width[lin,col] - (((self.global_vars.bankfull_width[lin,col] ** 2) - ((4 / 3) * self.global_vars.area_molhada[lin,col])) ** (1 / 2))) / (2 / 3))) + self.global_vars.bankfull_width[lin,col]
                                        raio_hidraulico = self.global_vars.area_molhada[lin,col]/perimetro_molhado
                                        self.global_vars.rh_medio[lin,col] += raio_hidraulico
                                        n+=1

                                        self.global_vars.comp_total[i_test,j_test] = self.global_vars.comp_total[i_atual,j_atual] + self.global_vars.comp_pixel[i_test,j_test]
                                        somatorio += (self.global_vars.comp_pixel[i_test,j_test] / (self.global_vars.decliv_pixel[i_test,j_test]**(1/2)))
                                    
                                    if self.global_vars.divisao_trecho[i_test,j_test] == 1:
                                        self.global_vars.comp_total[i_test,j_test] = self.global_vars.comp_total[i_atual,j_atual] 

                                    i_atual = i_test
                                    j_atual = j_test

                                # Fim while

                                # A declividade equivalente de cada um desses trechos foi estimada como sendo a média harmônica das declividades obtidas via MDE de cada pixel do trecho 
                                self.global_vars.Seq[lin,col] = (self.global_vars.comp_total[i_test,j_test]/somatorio)**2
                                self.global_vars.classerio[lin,col] = k

                                # O raio hidráulico do trecho é a média do Rh dos pixels que pertencem ao trecho em questão
                                self.global_vars.rh_medio[lin,col] /= n

                                if self.global_vars.direcoes[lin,col] == 45:
                                    i_atual = lin - 1
                                    j_atual = col + 1

                                elif self.global_vars.direcoes[lin,col] == 90:
                                    i_atual = lin
                                    j_atual = col + 1

                                elif self.global_vars.direcoes[lin,col] == 135:
                                    i_atual = lin + 1
                                    j_atual = col + 1

                                elif self.global_vars.direcoes[lin,col] == 180:
                                    i_atual = lin + 1
                                    j_atual = col

                                elif self.global_vars.direcoes[lin,col] == 225:
                                    i_atual = lin + 1
                                    j_atual = col - 1

                                elif self.global_vars.direcoes[lin,col] == 270:
                                    i_atual = lin
                                    j_atual = col - 1

                                elif self.global_vars.direcoes[lin,col] == 315:
                                    i_atual = lin - 1
                                    j_atual = col - 1
                    
                                elif self.global_vars.direcoes[lin,col] == 360:
                                    i_atual = lin - 1
                                    j_atual = col      

                                if self.global_vars.divisao_trecho[i_atual,j_atual] != 1 and self.global_vars.bacia[i_atual,j_atual] == 1:
                                    self.global_vars.Seq[i_atual,j_atual] = self.global_vars.Seq[lin,col]
                                    self.global_vars.classerio[i_atual,j_atual] = k
                                    self.global_vars.rh_medio[i_atual,j_atual] = self.global_vars.rh_medio[lin,col]

                                    while self.global_vars.divisao_trecho[i_atual,j_atual] != 1 and self.global_vars.bacia[i_atual,j_atual] == 1:
                                        if self.global_vars.direcoes[i_atual, j_atual] == 45:
                                            i_test = i_atual - 1
                                            j_test = j_atual + 1

                                        elif self.global_vars.direcoes[i_atual, j_atual] == 90:
                                            i_test = i_atual
                                            j_test = j_atual + 1

                                        elif self.global_vars.direcoes[i_atual, j_atual] == 135:
                                            i_test = i_atual + 1
                                            j_test = j_atual + 1

                                        elif self.global_vars.direcoes[i_atual, j_atual] == 180:
                                            i_test = i_atual + 1
                                            j_test = j_atual

                                        elif self.global_vars.direcoes[i_atual, j_atual] == 225:
                                            i_test = i_atual + 1
                                            j_test = j_atual - 1

                                        elif self.global_vars.direcoes[i_atual, j_atual] == 270:
                                            i_test = i_atual
                                            j_test = j_atual - 1

                                        elif self.global_vars.direcoes[i_atual, j_atual] == 315:
                                            i_test = i_atual - 1
                                            j_test = j_atual - 1
                            
                                        elif self.global_vars.direcoes[i_atual, j_atual] == 360:
                                            i_test = i_atual - 1
                                            j_test = j_atual    

                                        if self.global_vars.divisao_trecho[i_test,j_test] == 0:
                                            self.global_vars.Seq[i_test,j_test] = self.global_vars.Seq[lin,col]
                                            self.global_vars.classerio[i_test,j_test] = k
                                            self.global_vars.rh_medio[i_test,j_test] = self.global_vars.rh_medio[lin,col]
                                        
                                        i_atual = i_test
                                        j_atual = j_test
                    print(f'[{pixel_atual}/{(np.count_nonzero(self.global_vars.bacia))}] ({pixel_atual/(np.count_nonzero(self.global_vars.bacia))*100:.2f}%)', end='\r')      

        self.global_vars.n_total_trechos = k

        # Definição sobre o tipo de escoamento
        # Se a variável TipoEscoamento é igual a 2, significa que o escoamento no pixel é do tipo sheet flow, isto é, a partir do pixel inicial onde se iniciou o escoamento a água percorreu no máximo um valor igual a "sheetflow"
        print('Definição do tipo de escoamento')
        pixel_atual = 0

        for lin in range(self.rdc_vars.nlin):
            for col in range(self.rdc_vars.ncol):
                if self.global_vars.bacia[lin,col] == 1:
                    pixel_atual += 1
                    
                    i_atual = lin
                    j_atual = col

                    self.global_vars.comp_total[i_atual,j_atual] = self.global_vars.comp_pixel[i_atual,j_atual]

                    while self.global_vars.comp_total[i_atual,j_atual] <= self.global_vars.sheet_flow:

                        if self.global_vars.direcoes[i_atual, j_atual] == 45:
                            i_test = lin - 1
                            j_test = col + 1
                            self.global_vars.comp_total[i_test,j_test] = self.global_vars.comp_total[i_atual,j_atual] + self.global_vars.comp_pixel[i_test,j_test]

                        elif self.global_vars.direcoes[i_atual, j_atual] == 90:
                            i_test = lin
                            j_test = col + 1
                            self.global_vars.comp_total[i_test,j_test] = self.global_vars.comp_total[i_atual,j_atual] + self.global_vars.comp_pixel[i_test,j_test]

                        elif self.global_vars.direcoes[i_atual, j_atual] == 135:
                            i_test = lin + 1
                            j_test = col + 1
                            self.global_vars.comp_total[i_test,j_test] = self.global_vars.comp_total[i_atual,j_atual] + self.global_vars.comp_pixel[i_test,j_test]

                        elif self.global_vars.direcoes[i_atual, j_atual] == 180:
                            i_test = lin + 1
                            j_test = col
                            self.global_vars.comp_total[i_test,j_test] = self.global_vars.comp_total[i_atual,j_atual] + self.global_vars.comp_pixel[i_test,j_test]

                        elif self.global_vars.direcoes[i_atual, j_atual] == 225:
                            i_test = lin + 1
                            j_test = col - 1
                            self.global_vars.comp_total[i_test,j_test] = self.global_vars.comp_total[i_atual,j_atual] + self.global_vars.comp_pixel[i_test,j_test]

                        elif self.global_vars.direcoes[i_atual, j_atual] == 270:
                            i_test = lin
                            j_test = col - 1
                            self.global_vars.comp_total[i_test,j_test] = self.global_vars.comp_total[i_atual,j_atual] + self.global_vars.comp_pixel[i_test,j_test]

                        elif self.global_vars.direcoes[i_atual, j_atual] == 315:
                            i_test = lin - 1
                            j_test = col - 1
                            self.global_vars.comp_total[i_test,j_test] = self.global_vars.comp_total[i_atual,j_atual] + self.global_vars.comp_pixel[i_test,j_test]
            
                        elif self.global_vars.direcoes[i_atual, j_atual] == 360:
                            i_test = lin - 1
                            j_test = col    
                            self.global_vars.comp_total[i_test,j_test] = self.global_vars.comp_total[i_atual,j_atual] + self.global_vars.comp_pixel[i_test,j_test]

                        i_atual = i_test
                        j_atual = j_test
                    
                    # Definindo variável do tipo de escoamento
                    self.global_vars.tipo_escoamento[i_atual,j_atual] = 1
                    print(f'[{pixel_atual}/{(np.count_nonzero(self.global_vars.bacia))}] ({pixel_atual/(np.count_nonzero(self.global_vars.bacia))*100:.2f}%)', end='\r')      

        # Definindo variável do tipo de escoamento
        self.global_vars.tipo_escoamento[self.global_vars.tipo_escoamento != 1] = 2

        # Cálculo do tempo de viagem
        print('Cálculo do tempo de viagem')
        pixel_atual = 0

        self.global_vars.P24 = self.global_vars.P24 * 0.0393701 #mudança de unidade
        area_molhada_max = 0
        bank_full_width_max = 0
        r = 0
        for lin in range(self.rdc_vars.nlin):
            for col in range(self.rdc_vars.ncol):
                if self.global_vars.bacia[lin,col] == 1:
                    pixel_atual += 1

                    # Tempo de viagem em superfície
                    if self.global_vars.dren[lin,col] == 0:
                        # Sheet flow
                        if self.global_vars.tipo_escoamento[lin,col] == 2:
                            self.global_vars.tempo_viagem[lin,col] = ((0.007 * ((self.global_vars.nSolo[lin,col] * (self.global_vars.comp_pixel[lin,col] * 3.28084)) ** 0.8)) / ((self.global_vars.P24 ** 0.5) * (self.global_vars.decliv_pixel[lin,col] ** 0.4))) * 60
                        # Shallow flow
                        if self.global_vars.tipo_escoamento[lin,col] == 1:
                            self.global_vars.tempo_viagem[lin,col] = (self.global_vars.comp_pixel[lin,col] / ((self.global_vars.coef_k_pixel[lin,col] * (self.global_vars.decliv_pixel[lin,col] ** 0.5)) * 0.3048)) * (1 / 60)

                    # Tempo de viagem em canal
                    if self.global_vars.dren[lin,col] == 1:

                        # Trechos enviados pelo usuário
                        if self.global_vars.classerio[lin,col] <= self.global_vars.n_total_trechos:
                            for k in range(self.global_vars.n_total_trechos):
                                if self.global_vars.classerio[lin,col] == self.global_vars.id_trechos[k]:
                                    vel_dren = ((self.global_vars.Rhclasse[k] ** (2/3)) * (self.global_vars.Sclasse[k]**(1/2))) / self.global_vars.Mannclasse[k]
                                    self.global_vars.Seq[lin,col] = self.global_vars.Sclasse[k]
                                    self.global_vars.tempo_viagem[lin,col] = (self.global_vars.comp_pixel[lin,col] / vel_dren) / 60

                        # Trechos determinados pela rotina 
                        if self.global_vars.classerio[lin,col] > self.global_vars.n_total_trechos:
                            self.global_vars.area_molhada[lin,col] = self.global_vars.coef_c * (self.global_vars.dren_area[lin,col]**self.global_vars.coef_d)
                            self.global_vars.bankfull_width[lin,col] = self.global_vars.coef_g * (self.global_vars.dren_area[lin,col]**self.global_vars.coef_h)
                            perimetro_molhado = ((((2 * (10 ** (1 / 2))) - 2) / 3) * ((self.global_vars.bankfull_width[lin,col] - (((self.global_vars.bankfull_width[lin,col] ** 2) - ((4 / 3) * self.global_vars.area_molhada[lin,col])) ** (1 / 2))) / (2 / 3))) + self.global_vars.bankfull_width[lin,col]
                            raio_hidraulico = self.global_vars.area_molhada[lin,col] / perimetro_molhado
                            vel_dren = ((raio_hidraulico ** (2/3)) * (self.global_vars.Seq[lin,col] ** (1/2))) / self.global_vars.n_canal
                            self.global_vars.tempo_viagem[lin,col] = (self.global_vars.comp_pixel[lin,col] / vel_dren) / 60
                            if self.global_vars.divisao_trecho[lin,col] == 1:
                                k = self.global_vars.classerio[lin,col]
                                self.global_vars.Rhclasse[k] = self.global_vars.rh_medio[lin,col]
                                self.global_vars.Sclasse[k] = self.global_vars.Seq[lin,col]
                                self.global_vars.Mannclasse[k] = self.global_vars.n_canal

                            if self.global_vars.area_molhada[lin,col] > area_molhada_max:
                                area_molhada_max = self.global_vars.area_molhada[lin,col]

                            if self.global_vars.bankfull_width[lin,col] > bank_full_width_max:
                                bank_full_width_max = self.global_vars.bankfull_width[lin,col]

                    # Tempo de viagem no reservatório
                    if self.global_vars.reservoir[lin,col] == 1:
                        vel_reservatorio = (9.81 * self.global_vars.profundidade_resers)**(1/2)
                        self.global_vars.tempo_viagem[lin,col] = (self.global_vars.comp_pixel[lin,col] / vel_reservatorio) / 60

                    r+=1
                    print(f'[{pixel_atual}/{(np.count_nonzero(self.global_vars.bacia))}] ({pixel_atual/(np.count_nonzero(self.global_vars.bacia))*100:.2f}%)', end='\r')      

        # Determinação da declividade máxima
        decliv_max_rio = np.amax(self.global_vars.Seq[self.global_vars.dren==1])
        decliv_max_sup = np.amax(self.global_vars.decliv_pixel[self.global_vars.dren==0])
        if decliv_max_rio > decliv_max_sup:
            decliv_max = decliv_max_rio
        else:
            decliv_max = decliv_max_sup
        
        # Determiação do tempo máximo em que a água leva para escoar em um pixel
        num_r = r
        Tdmax = np.amax(self.global_vars.tempo_viagem_pixel)

        # Determinação do tempo em que a água leva para ir do pixel até o exutório
        print('Determinação do tempo em que a água leva para ir do pixel até o exutório')
        for lin in range(self.rdc_vars.nlin):
            for col in range(self.rdc_vars.ncol):
                if self.global_vars.bacia[lin,col] == 1:
                    i_atual = lin
                    j_atual = col

                    self.global_vars.ttotal[i_atual,j_atual] = self.global_vars.tempo_viagem[i_atual,j_atual]

                    while self.global_vars.bacia[i_atual, j_atual]  == 1:
                        if self.global_vars.direcoes[i_atual, j_atual] == 45:
                            i_test = lin - 1
                            j_test = col + 1
                            self.global_vars.ttotal[i_test,j_test] = self.global_vars.ttotal[i_atual,j_atual] + self.global_vars.tempo_viagem[i_test,j_test]

                        elif self.global_vars.direcoes[i_atual, j_atual] == 90:
                            i_test = lin
                            j_test = col + 1
                            self.global_vars.ttotal[i_test,j_test] = self.global_vars.ttotal[i_atual,j_atual] + self.global_vars.tempo_viagem[i_test,j_test]

                        elif self.global_vars.direcoes[i_atual, j_atual] == 135:
                            i_test = lin + 1
                            j_test = col + 1
                            self.global_vars.ttotal[i_test,j_test] = self.global_vars.ttotal[i_atual,j_atual] + self.global_vars.tempo_viagem[i_test,j_test]

                        elif self.global_vars.direcoes[i_atual, j_atual] == 180:
                            i_test = lin + 1
                            j_test = col
                            self.global_vars.ttotal[i_test,j_test] = self.global_vars.ttotal[i_atual,j_atual] + self.global_vars.tempo_viagem[i_test,j_test]

                        elif self.global_vars.direcoes[i_atual, j_atual] == 225:
                            i_test = lin + 1
                            j_test = col - 1
                            self.global_vars.ttotal[i_test,j_test] = self.global_vars.ttotal[i_atual,j_atual] + self.global_vars.tempo_viagem[i_test,j_test]

                        elif self.global_vars.direcoes[i_atual, j_atual] == 270:
                            i_test = lin
                            j_test = col - 1
                            self.global_vars.ttotal[i_test,j_test] = self.global_vars.ttotal[i_atual,j_atual] + self.global_vars.tempo_viagem[i_test,j_test]

                        elif self.global_vars.direcoes[i_atual, j_atual] == 315:
                            i_test = lin - 1
                            j_test = col - 1
                            self.global_vars.ttotal[i_test,j_test] = self.global_vars.ttotal[i_atual,j_atual] + self.global_vars.tempo_viagem[i_test,j_test]
            
                        elif self.global_vars.direcoes[i_atual, j_atual] == 360:
                            i_test = lin - 1
                            j_test = col    
                            self.global_vars.ttotal[i_test,j_test] = self.global_vars.ttotal[i_atual,j_atual] + self.global_vars.tempo_viagem[i_test,j_test]
                            
                        i_atual = i_test
                        j_atual = j_test

                    self.global_vars.tempo_viagem_tot[lin,col] = self.global_vars.ttotal[i_atual,j_atual]
                    print(f'[{pixel_atual}/{(np.count_nonzero(self.global_vars.bacia))}] ({pixel_atual/(np.count_nonzero(self.global_vars.bacia))*100:.2f}%)', end='\r')      

        # Determinação do tempo de concentração máximo 
        self.global_vars.tc_max = np.amax(self.global_vars.tempo_viagem_tot)

    def numera_pix_bacia(self):
        '''Esta função enumera e quantifica os píxels presentes na bacia hidrográfica, além de atualizar variáveis inerente ao programa'''
        # Dimensionamento das variáveis
        numero_pixel = 0
        self.numb_pix_bacia = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol))
        # Enumera os pixels presentes na bacia hidrográfica
        for lin in range(self.rdc_vars.nlin):
            for col in range(self.rdc_vars.ncol):
                if self.global_vars.bacia[lin][col] == 1:
                    numero_pixel += 1
                    self.numb_pix_bacia[lin][col] = numero_pixel

        # Computa o número total de pixels que são bacia hidrográfica
        self.numero_total_pix = numero_pixel
        numero_pixel = None

    def leh_CN(self, arquivo):
        '''Esta função lê o arquivo enviado pelo usuário contendo os valores do parametro CURVE-NUMBER (CN) para os diferentes pixels da bacia hidrográfica'''
        # Define variáveis
        self.CN = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol))
        # Tratamento de erros: verifica se o arquivo foi corretamente enviado
        if arquivo:
            # Realizando a abertura do arquivo raster e coletando as informações referentes as dimensões do mesmo
            rst_file_CN = gdal.Open(arquivo)
            
            # Lendo os dados raste como um array
            dados_lidos_raster_CN = rst_file_CN.GetRasterBand(1).ReadAsArray()

            #  Tratamento de erros: verifica se o arquivo raster foi aberto corretamente
            if rst_file_CN is not None:
                # Reorganizando os dados lidos em uma nova matriz, essa possui as informações sobre as classes dos rios
                self.CN = dados_lidos_raster_CN
                # Fechando o dataset GDAL referente ao arquivo raster
                rst_file_CN = None
            else:
                # Caso o arquivo raster apresente erros durante a abertura, ocorrerá um erro
                resulte = f"Failde to open the raster file: {arquivo}"
                # QMessageBox.warning(None, "ERROR!", resulte)
                
        else:
            # Exibe uma mensagem de erro
            result ="Nenhum arquivo foi selecionado!"
            # QMessageBox.warning(None, "ERROR!", result)
        return self.CN 

    
    def leh_tempo_viagem(self, arquivo):
        '''Esta função lê o arquivo contendo o tempo de concentração de cada pixel presente na bacia hidrográfica e o armazena'''

        # Tratamento de erros: verifica se o arquivo foi corretamente enviado
        if arquivo:
            # Realizando a abertura do arquivo raster e coletando as informações referentes as dimensões do mesmo
            rst_file_Tempo_total = gdal.Open(arquivo)
            
            # Lendo os dados raste como um array 
            dados_lidos_raster_Tempo_total = rst_file_Tempo_total.GetRasterBand(1).ReadAsArray()

            #  Tratamento de erros: verifica se o arquivo raster foi aberto corretamente
            if rst_file_Tempo_total is not None:
                # Reorganizando os dados lidos em uma nova matriz, essa possui as informações sobre as classes dos rios
                Tempo_total = dados_lidos_raster_Tempo_total
                # Fechando o dataset GDAL referente ao arquivo raster
                rst_file_Tempo_total = None
            else:
                # Caso o arquivo raster apresente erros durante a abertura, ocorrerá um erro
                resulte = f"Failde to open the raster file: {arquivo}"
                # QMessageBox.warning(None, "ERROR!", resulte)
                
        else:
            # Exibe uma mensagem de erro
            result ="Nenhum arquivo foi selecionado!"
            # QMessageBox.warning(None, "ERROR!", result)

        return Tempo_total    

    def precipitacao_acumulada(self):
        '''Esta função lê o arquivo contendo o tempo de concentração de cada pixel presente na bacia hidrográfica e o armazena'''
        arquivo = r"C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\Bacia_mulugun\hidropixel_files\entrada_hidropixel\entrada_hidropixel\Input_bin\Output_bin\pe_acumulada_pixel.RST"
        # Tratamento de erros: verifica se o arquivo foi corretamente enviado
        if arquivo:
            # Realizando a abertura do arquivo raster e coletando as informações referentes as dimensões do mesmo
            rst_file_chuva_acumulada = gdal.Open(arquivo)
            
            # Lendo os dados raste como um array 
            dados_lidos_raster_chuva_acumulada = rst_file_chuva_acumulada.GetRasterBand(1).ReadAsArray()

            #  Tratamento de erros: verifica se o arquivo raster foi aberto corretamente
            if rst_file_chuva_acumulada is not None:
                # Reorganizando os dados lidos em uma nova matriz, essa possui as informações sobre as classes dos rios
                pe_acumulada_pixel = dados_lidos_raster_chuva_acumulada
                # Fechando o dataset GDAL referente ao arquivo raster
                rst_file_chuva_acumulada = None
            else:
                # Caso o arquivo raster apresente erros durante a abertura, ocorrerá um erro
                resulte = f"Failde to open the raster file: {arquivo}"
                # QMessageBox.warning(None, "ERROR!", resulte)
                
        else:
            # Exibe uma mensagem de erro
            result ="Nenhum arquivo foi selecionado!"
            # QMessageBox.warning(None, "ERROR!", result)

        return pe_acumulada_pixel       

    def leh_parametros(self, arquivo):
        '''Esta função lê o arquivo enviado pelo usuário contento os parâmetros do modelo: abstração inicial, time step, tempo critério de parada e o beta'''
        values = []
        with open(arquivo, 'r') as arquivo_txt:
            # Lê as linhas do arquivo separando por ','
            for line in arquivo_txt:
                split_lines = line.split(',')[1].strip()
                values.append(split_lines)

        # Armazena as informações coletadas
        self.alfa = float(values[0])
        self.delta_t = int(values[1])
        self.criterio_parada = int(values[2])
        self.beta = float(values[3])

    def leh_precip_distribuida(self,arquivo):
        '''Esta função lê o arquivo enviado pelo usuário contento os valores da precipitação destribuidos ao longo dos pixels pertencentes a baica hidrográfica'''
        self.quantidade_blocos_chuva = 0
        # Lê os dados enviados e os armaneza
        with open(arquivo, 'r', encoding = 'utf-8') as arquivo_txt:
            # armazena o cabeçalho (primeira linha)
            lines = arquivo_txt.readline().strip()

            # Sepera as linhas por vígula
            split_lines = lines.split(',')

        self.quantidade_blocos_chuva = len(split_lines) - 1 

    def leh_posto_pluv(self, arquivo):
        '''Esta função é responsável por ler e armazenar as informações dos postos pluviométricos'''
        # Definição das variáveis
        id_postos = []
        latitude = []
        longitude = []
        numero_posto = []
        dict_numero_posto = {}
        w = 0
        with open(arquivo, 'r', encoding = 'utf-8') as arquivo_txt:
            # Armazena cabeçalho
            cabecalho = arquivo_txt.readline().strip()
            # Lê as linhas do arquivo enviado
            for line in arquivo_txt:
                split_lines = line.split(',')
                id_postos.append(int(split_lines[0]))
                latitude.append(float(split_lines[1]))
                longitude.append(float(split_lines[2]))
                dict_numero_posto[w] = id_postos[w]
                w+=1
                numero_posto.append(w)

        # Redimensiona as variáveis globais
        self.quantidade_postos = len(numero_posto)
        self.id_postos = np.array(id_postos)
        self.latitude = np.array(latitude)
        self.longitude = np.array(longitude)
        self.numero_posto = dict_numero_posto

    def leh_arquivo_precipitacao(self, arquivo):
        '''Esta função lê e armazena os valores de precipitação de cada posto ao longo do tempo'''
        # Definição das variáveis
        w = 0
        # Recebe e lê o arquivo
        with open(arquivo, 'r', encoding = 'utf-8') as arquivo_txt:
            # Armazena cabeçalho
            cabecalho = arquivo_txt.readline().strip()

            # Redimenciona variáveis
            linhas = arquivo_txt.readlines()
            self.blocos_chuva = len(linhas)
            self.tempo = np.zeros(self.blocos_chuva)
            self.chuva = np.zeros((self.blocos_chuva,(self.quantidade_postos)))

            # Retira informações do arquivo
            w = 0
            for line in linhas:
                split_line = line.split(',')

                # Armazena tempo
                self.tempo[w] = split_line[0]

                # Armazena chuva
                for c in range(self.quantidade_postos):
                    self.chuva[w][c] = split_line[c+1]
                w +=1
         
    @optimize           
    def rainfall_interpolation(self):
        '''Esta função gera o arquivo com a precipitação por pixel por meio da interpolação dos valores das estações pluviométricas enviadas pelo usuário'''
        # Definição de variáveis
        numero_pixel = 0
        numerador = 0
        denominador = 0
        distancia_y = 0
        distancia_x = 0
        rainfall = 0
        numero_total_pix = np.sum(self.global_vars.bacia[self.global_vars.bacia==1])

        # Gera o arquivo com precipitação interpolada por pixel
        arquivo = r'C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\Bacia_mulugun\hidropixel_files\rainfall_interpolated.txt'
        with open(arquivo, 'w', encoding = 'utf-8') as arquivo_txt:
            # JVD:optimize: Escreve cabeçalho
            arquivo_txt.write('Pixel,')
            arquivo_txt.write(','.join(map(str, self.tempo)) + '\n')

            # JVDoptimize: interpolação da precipitação
            for lin in range(self.rdc_vars.nlin):
                for col in range(self.rdc_vars.ncol):
                    if self.global_vars.bacia[lin][col] == 1:
                        numero_pixel += 1
                        linha = str(numero_pixel)
                        x_pixel = self.X_minimo + (col * self.d_x) + (self.d_x / 2)
                        y_pixel = self.Y_maximo - (lin * self.d_y) - (self.d_y / 2)

                        # Aplicação da fórmula de interpolação
                        for w in range(self.blocos_chuva):
                            numerador = 0
                            denominador = 0
                            for k in range(self.quantidade_postos):
                                for q in range(self.quantidade_postos):
                                    if self.numero_posto[q] == self.id_postos[k]:
                                        distancia_y = self.latitude[k] - y_pixel
                                        distancia_x = self.longitude[k] - x_pixel                                
                                        distancia = ((distancia_x ** 2) + (distancia_y ** 2))**(1/2)
                                        numerador += (float(self.chuva[w][q]) / (distancia**2))
                                        denominador += (1/(distancia**2))
                            rainfall = numerador / denominador
                            linha = linha + ',' + f'{rainfall}'

                        # Escreve informação no arquivo
                        arquivo_txt.write(linha+'\n')
                        # Apenas para visualizar o processamento
                        print(f'[{numero_pixel}/{numero_total_pix}] ({numero_pixel/numero_total_pix*100:.2f}%)', end='\r')
    @optimize
    def rainfall_interpolation_map(self):
        '''Se o botão save maps for clicado: gera os arquivos raster com precipitação interpolada por pixel por duração do evento'''
        # Cria variáveis
        self.chuva_pixel = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol))
        numero_pixel = 0
        numerador = 0
        denonimador = 0
        # Gera um arquivo por evento de precipitação
        for w in range(self.blocos_chuva):
            # Pasta enviada pelo user
            path = r'c:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\resultados_test_modelo'
            arquivo = path + f'\{str(self.tempo[w])}.RST'

            # interpolação da pricipitação para o evento em questão
            for lin in range(self.rdc_vars.nlin):
                for col in range(self.rdc_vars.ncol):
                    if self.global_vars.bacia[lin][col] == 1:
                        numero_pixel += 1
                        numerador = 0
                        denominador = 0
                        for k in range(self.quantidade_postos):
                            for q in range(self.quantidade_postos):
                                if self.numero_posto[q] == self.id_postos[k]:
                                    x_pixel = self.X_minimo + (col * self.d_x) + (self.d_x / 2)
                                    y_pixel = self.Y_minimo - (lin * self.d_y) + (self.d_y / 2)
                                    distancia_y = self.latitude[k] - y_pixel
                                    distancia_x = self.longitude[k] - x_pixel
                                    distancia = ((distancia_x ** 2) + (distancia_y ** 2))**(1/2)
                                    numerador += (self.chuva[w][q] / (distancia**2))
                                    denominador += (1/(distancia**2))
                        
                        # Armazena o valor da pricipitação do pixel
                        rainfall_pix = numerador / denominador
                        self.chuva_pixel[lin][col] = rainfall_pix

            num_pix_max = np.amax(self.chuva_pixel)
            # Escreve arquivo raster (.RST) com a precipitação por pixel em toda bacia para o evento em questão
            dados_chuva_pixel = np.array([[float(self.chuva_pixel[lin][col]) for col in range(self.rdc_vars.ncol)] for lin in range(self.rdc_vars.nlin)])
            tipo_dados = gdalconst.GDT_Float32

            # Obtendo o driver o para escrita do arquivo em GeoTiff
            driver = gdal.GetDriverByName('RST')

            # Cria arquivo final
            dataset = driver.Create(arquivo, self.rdc_vars.ncol, self.rdc_vars.nlin, 1, tipo_dados)

            # Escreve os dados na banda do arquivo
            banda = dataset.GetRasterBand(1)
            banda.WriteArray(dados_chuva_pixel)

            # Fechando o arquivo
            dataset = None
            banda = None
            driver = None
            tipo_dados = None

            # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem
            self.rdc_vars.nlin3 = self.rdc_vars.nlin
            self.rdc_vars.ncol3 = self.rdc_vars.ncol
            self.rdc_vars.tipo_dado = 2
            self.rdc_vars.tipoMM = 2
            self.rdc_vars.VarMM2 = self.chuva_pixel
            self.rdc_vars.i3 = 0 
            self.rdc_vars.Xmin3 = self.X_minimo
            self.rdc_vars.Xmax3 = self.X_maximo
            self.rdc_vars.Ymin3 = self.Y_minimo
            self.rdc_vars.Ymax3 = self.Y_maximo
            self.rdc_vars.Varmax = num_pix_max
            self.rdc_vars.Varmin = 0
            nomeRST = arquivo
            self.global_vars.metrordc = self.global_vars.metro
            self.escreve_RDC(nomeRST)    

    @optimize
    def excess_rainfall(self):
        '''Esta função determina gera os arquivos associados a precipitação excedente de cada pixel presente na baica hidrográfica, fumentando-se no método do SCS-CN'''
        # Definição de variáveis
        pixel_atual = 0
        # JVD: estrutura dos arrays
        self.time = np.zeros(50000)
        self.hacum = np.zeros(50000)
        self.perdas_iniciais = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol))
        self.pe_acumulada_pixel = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol))
        self.chuva_total_pixel = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol))
        self.Spotencial = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol))

        self.hexc_pix = np.zeros((self.numero_total_pix, self.quantidade_blocos_chuva))
        
        # arquivo_precipitacao = r"C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\Bacia_mulugun\hidropixel_files\entrada_hidropixel\entrada_hidropixel\Input_ascii\Output_ascii\rainfall_file_rod1.txt"
        arquivo_precipitacao = r"C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\Bacia_mulugun\hidropixel_files\entrada_hidropixel\entrada_hidropixel\Input_ascii\Output_ascii\rainfall_file_minus377mmET.txt"
        with open(arquivo_precipitacao, 'r', encoding = 'utf-8') as arquivo_txt:
            # Armazena cabeçalho do arquivo
            cabecalho = arquivo_txt.readline().strip()
            for lin in range(self.rdc_vars.nlin):
                for col in range(self.rdc_vars.ncol):
                    if self.global_vars.bacia[lin][col]==1:
                        # Cálculo do potencial de armazenamento do solo por pixel presente na bacia
                        self.Spotencial[lin][col] = (25400/self.CN[lin][col])-254

                        # Cálculo das perdas iniciais por pixel presente na bacia
                        self.perdas_iniciais[lin][col] = self.alfa * self.Spotencial[lin][col]

                        Pacum = 0
                        self.time[0] = 0

                        # Armazena as linha do arquivo de precipitação
                        line = arquivo_txt.readline().strip()
                        split_line = line.split(',')

                        for w in range(1, self.quantidade_blocos_chuva+1):
                            chuva_distribuida = float(split_line[w])
                            self.time[w] = self.time[w-1] + self.delta_t

                            Pacum += chuva_distribuida 

                            # Cálculo da chuva excedente
                            if Pacum <= self.perdas_iniciais[lin][col]:
                                self.hacum[w] = 0
                            else:
                                self.hacum[w] = ((Pacum - self.perdas_iniciais[lin][col])**2) / (Pacum - self.perdas_iniciais[lin][col] + self.Spotencial[lin][col])

                            # precipitação efetiva desacumulada por pixel
                            self.hexc_pix[pixel_atual][w-1] = self.hacum[w] - self.hacum[w-1]

                        # Chuva excedente acumulada do pixel
                        self.pe_acumulada_pixel[lin][col] = self.hacum[self.quantidade_blocos_chuva]

                        # Chuva total no pixel
                        self.chuva_total_pixel[lin][col] = Pacum

                        # Atualiza pixel em questão
                        pixel_atual+=1
                        print(f'[{pixel_atual}/{self.numero_total_pix}] ({pixel_atual/self.numero_total_pix*100:.2f}%)', end='\r')

    @optimize       
    def hidrograma_dlr(self):
        '''Esta função gera o hidrograma-DLR da bacia hidrográfica conforme os dados de precipitação enviados'''
        # Definição das variáveis
        Tmax = 0
        a = 0
        tempo_viagem = r"C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\Bacia_mulugun\hidropixel_files\entrada_hidropixel\entrada_hidropixel\Input_bin\Output_bin\travel_time_rod1_atualizado.rst"
        self.tempo_total = self.leh_tempo_viagem(tempo_viagem)
        self.Spotencial = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol))
        self.volume_total_pix = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol))
        self.vazao_pico = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol))
        self.tempo_pico = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol))
        self.TempoTotal_reclass = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol))
        self.vazao_pixel = np.zeros(50000)
        self.tempo_intervalo = np.zeros(50000)
        time = np.zeros(50000)
        # pe_acumulada_pixel = self.precipitacao_acumulada()
        self.tempo_vazao_pixel = np.zeros(50000)
        self.vazao_amortecida_pixel = np.zeros(50000)
        self.vazao = np.zeros(50000)
        a = 0
        # JVDoptmize: máximo tempo de viagem ao exutório
        tempo_total_bacia = self.tempo_total[self.global_vars.bacia == 1]
        Tmax = np.amax(tempo_total_bacia)
        
        # Reclassificação do tempo de viagem ao exutório para multiplos de delta_t
        w = 0
        self.tempo_intervalo[w] = 0
        while self.tempo_intervalo[w] <= Tmax + self.delta_t:
            self.tempo_intervalo[w + 1] = self.tempo_intervalo[w] + self.delta_t
            w += 1

        # JVD: correção sintaxe de vb to py
        # self.num_intervalos = w - 1
        self.num_intervalos = w
        diferenca = 0
        for lin in range(self.rdc_vars.nlin):
            for col in range(self.rdc_vars.ncol):
                diferenca_minima = 100000000
                if self.global_vars.bacia[lin][col] == 1:
                    a+=1
                    for g in range(self.num_intervalos):
                        if self.tempo_intervalo[g] >= self.tempo_total[lin][col]:
                            diferenca = -(self.tempo_total[lin][col] - self.tempo_intervalo[g])

                        else:
                            diferenca = (self.tempo_total[lin][col] - self.tempo_intervalo[g])

                        if diferenca < diferenca_minima:
                            diferenca_minima = diferenca
                            self.TempoTotal_reclass[lin][col] = float(self.tempo_intervalo[g])
                    print(f'Reclassificando tempo... [{a}/{self.numero_total_pix}] ({a/self.numero_total_pix*100:.2f}%)', end='\r')

        print('Reclassificou o tempo!')
        a = 0
        # Determinação do hidrograma
        # Dados do arquivo de precipitação enviado
        tempo_exutorio = 0
        k = 0
        storage_coefficient = 0
        c_1 = 0
        c_2 = 0
        area_bacia = 0

        # lê hietograma 
        arquivo_precipitacao = r'C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\Bacia_mulugun\hidropixel_files\entrada_hidropixel\entrada_hidropixel\Input_bin\Output_bin\hietograma_pe_minus_ETP.txt'
        with open(arquivo_precipitacao, 'r', encoding = 'utf-8') as arquivo_txt:
            # Armazena cabecalho do arquivo com a precipitação efetiva por pixel
            cabecalho = arquivo_txt.readline().strip()

            for lin in range(self.rdc_vars.nlin):
                for col in range(self.rdc_vars.ncol):
                    if self.global_vars.bacia[lin][col] == 1:
                        a+=1
                        time[0] = 0
                        
                        # Armazena as linha do arquivo de precipitação efetiva
                        line = arquivo_txt.readline().strip()
                        split_line = line.split(',')

                        for h in range(1, self.quantidade_blocos_chuva + 1):
                            self.Pexc = float(split_line[h])
                            time[h] = time[h-1] + self.delta_t

                            if self.Pexc > 0:
                                # Vazão correspondente no exutório
                                self.Pexc = (((self.Pexc/1000) * (self.global_vars.dx ** 2)) / self.delta_t) * (1 / 60)  # Vazão em m³/s

                                # Representação da vazão no exutório (translação)
                                tempo_exutorio = time[h-1] + self.TempoTotal_reclass[lin][col]

                                k = int(tempo_exutorio / self.delta_t)
                                self.vazao_pixel[k] = self.Pexc

                        # Volume de água gerado por pixel
                        # self.volume_total_pix[lin][col] = (pe_acumulada_pixel[lin][col] / (10 ** 3)) * (self.global_vars.dx ** 2)  # em m³

                        # Volume total de água gerada em todo evento
                        # self.volume_total += self.volume_total_pix[lin][col]

                        # Parâmetro para estimativa do armazenamento
                        storage_coefficient = self.tempo_total[lin][col] / ((1 / self.beta) - 1)  # em minutos

                        c_1 = self.delta_t / ((2 * storage_coefficient) + self.delta_t)
                        c_2 = 1 - (2 * c_1)

                        # Amortecimento do hidrograma do pixel
                        k = 0
                        blocos_vazao = 0
                        self.tempo_vazao_pixel[k] = 0
                        self.vazao_amortecida_pixel[k] = c_1 * self.vazao_pixel[k]
                        self.vazao[k] = self.vazao[k] + self.vazao_amortecida_pixel[k]
                        while self.tempo_vazao_pixel[k] <= self.criterio_parada:
                            self.vazao_amortecida_pixel[k+1] = (c_1 * self.vazao_pixel[k+1]) + (c_1 * self.vazao_pixel[k]) + (c_2 * self.vazao_amortecida_pixel[k])
                            self.tempo_vazao_pixel[k+1] = self.tempo_vazao_pixel[k] + self.delta_t
                            k += 1
                            blocos_vazao += 1
                            self.vazao[k] = self.vazao[k] + self.vazao_amortecida_pixel[k]

                        # Determinação da vazão e do tempo de pico do hidrograma-DLR por pixel
                        self.vazao_pico[lin][col] = np.amax(self.vazao)
                        self.blocos_vazao = blocos_vazao

                        # Zera vazão no pixel
                        self.vazao_pixel.fill(0)
                        self.vazao_amortecida_pixel.fill(0)

                        print(f'Calculando vazão... [{a}/{self.numero_total_pix}] ({a/self.numero_total_pix*100:.2f}%)', end='\r')

            # Cálculo da área da bacia
            area_bacia = self.numero_total_pix * (self.global_vars.dx **2) # em m²

            # Chuva excedente calculada
            # self.chuva_excedente_calc = (self.volume_total / area_bacia) * (10**3) #em mm

    def tamanho_numero(self, varaux, num):
        '''
        Esta função a dimensão dos números que serão usados na padronização do documento
        '''
        negativo, nzeros, pp, varaux2, limsup = None, None, None, None, None
        
        if varaux < 0:
            negativo: int = 1
        else:
            negativo: int = 0
        
        varaux2 = np.abs(varaux)
        
        for pp in range(11):
            limsup = 10.0**pp
            if varaux2 < limsup:
                nzeros:int = pp
                break

        # Se o valor for inteiro
        if num == 1:
            if nzeros == 0:
                self.global_vars.tamnum = 1 + negativo
            else:
                self.global_vars.tamnum = nzeros + negativo
        # Se o valor for real
        else:
            if nzeros == 0:
                self.global_vars.tamnum = 8 + 1 + negativo
            else:
                self.global_vars.tamnum = 8 + nzeros + negativo   

        return self.global_vars.tamnum

    def aux_RDC(self, file_name, textoaux, varaux, tamnum):
        """
        Esta função é responsável por formatar as informações dos arquivos de saida do programa
        """
        if tamnum == 1:
            formated_phrase = f'{textoaux:14s}{varaux:1d}\n'
            formated_phrase = str(formated_phrase)
            return formated_phrase
        elif tamnum == 2:
            formated_phrase = f'{textoaux:14s}{varaux:2d}\n'
            formated_phrase = str(formated_phrase)
            return formated_phrase
        elif tamnum == 3:
            formated_phrase = f'{textoaux:14s}{varaux:3d}\n'
            formated_phrase = str(formated_phrase)
            return formated_phrase
        elif tamnum == 4:
            formated_phrase = f'{textoaux:14s}{varaux:4d}\n'
            formated_phrase = str(formated_phrase)
            return formated_phrase
        elif tamnum == 5:
            formated_phrase = f'{textoaux:14s}{varaux:5d}\n'
            formated_phrase = str(formated_phrase)
            return formated_phrase
        elif tamnum == 6:
            formated_phrase = f'{textoaux:14s}{varaux:7d}\n'
            formated_phrase = str(formated_phrase)
            return formated_phrase
        elif tamnum == 8:
            formated_phrase = f'{textoaux:14s}{varaux:8d}\n'
            formated_phrase = str(formated_phrase)
            return formated_phrase
        elif tamnum == 9:
            formated_phrase = f'{textoaux:14s}{varaux:9.7f}\n'
            formated_phrase = str(formated_phrase)
            return formated_phrase
        elif tamnum == 10:
            formated_phrase = f'{textoaux:14s}{varaux:10.7f}\n'
            formated_phrase = str(formated_phrase)
            return formated_phrase
        elif tamnum == 11:
            formated_phrase = f'{textoaux:14s}{varaux:11.7f}\n'
            formated_phrase = str(formated_phrase)
            return formated_phrase
        elif tamnum == 12:
            formated_phrase = f'{textoaux:14s}{varaux:12.7f}\n'
            formated_phrase = str(formated_phrase)
            return formated_phrase
        elif tamnum == 13:
            formated_phrase = f'{textoaux:14s}{varaux:13.7f}\n'
            formated_phrase = str(formated_phrase)
            return formated_phrase
        elif tamnum == 14:
            formated_phrase = f'{textoaux:14s}{varaux:14.7f}\n'
            formated_phrase = str(formated_phrase)
            return formated_phrase
        elif tamnum == 15:
            formated_phrase = f'{textoaux:14s}{varaux:15.7f}\n'
            formated_phrase = str(formated_phrase)
            return formated_phrase
        elif tamnum == 16:
            formated_phrase = f'{textoaux:14s}{varaux:16.7f}\n'
            formated_phrase = str(formated_phrase)
            return formated_phrase
        elif tamnum == 17:
            formated_phrase = f'{textoaux:14s}{varaux:17.7f}\n'
            formated_phrase = str(formated_phrase)
            return formated_phrase
        elif tamnum == 18:
            formated_phrase = f'{textoaux:14s}{varaux:18.7f}\n'
            formated_phrase = str(formated_phrase)
            return formated_phrase
        elif tamnum == 19:
            formated_phrase = f'{textoaux:14s}{varaux:19.7f}\n'
            formated_phrase = str(formated_phrase)
            return formated_phrase
         
    def escreve_RDC(self, nome_RST):
        """
        Esta função constrói os arquivos de saída das diferentes funcionalidades do programa
        """
        # Identifica a posição da extensão no arquivo .RST
        pos_ext = nome_RST.find('.RST')

        # Atribui o nome do arquivo .RST ao novo arquivo .rdc
        nome_rdc = nome_RST[:pos_ext] + '.rdc'

        # Abrindo o arquivo 
        with open(nome_rdc, 'w') as rdc_file:
            # Escreve linha com formato do arquivo
            rdc_file.write(f'file format : IDRISI Raster A.1\n')
            # Escreve linha com o título do arquivo
            rdc_file.write(f'File title  : \n')

            # Escreve linha com tipo de dado
            if self.rdc_vars.tipo_dado == 1:
                rdc_file.write(f'data type   : integer\n')
            elif self.rdc_vars.tipo_dado == 2:
                rdc_file.write(f'data type   : real\n')

            # Escreve a linha com o tipo de arquivo
            rdc_file.write(f'file type   : binary\n')

            # Escreve a linha com o número de colunas
            self.global_vars.varaux = self.rdc_vars.ncol3
            self.rdc_vars.num = 1
            textoaux = 'columns     : ' 
            tamnum = self.tamanho_numero(self.global_vars.varaux, self.rdc_vars.num)
            phrase = self.aux_RDC(rdc_file, textoaux, self.global_vars.varaux, tamnum)
            rdc_file.write(phrase)

            # Escreve a linha com o número de linhas
            self.global_vars.varaux = self.rdc_vars.nlin3
            self.rdc_vars.num = 1 # num = 1 : integer
            textoaux = 'rows        : ' 
            tamnum = self.tamanho_numero(self.global_vars.varaux, self.rdc_vars.num)
            phrase = self.aux_RDC(rdc_file, textoaux, self.global_vars.varaux, tamnum)
            rdc_file.write(phrase)
            # Escreve a linha com o sistema de referência
            rdc_file.write(f'ref. system : {self.rdc_vars.sistemaref}\n')

            # Escreve a linha com a unidade de referência
            if self.global_vars.metro == 1:
                rdc_file.write(f'ref. units  : m\n')
            else:
                rdc_file.write(f'ref. units  : deg\n')
            
            # Escreve linha com distância unitária de referência
            rdc_file.write(f'unit dist.  : {1.0:<9.7f}\n')


            # Escreve linha com coordenada xmin
            self.global_vars.varaux = self.rdc_vars.Xmin3
            self.rdc_vars.num = 2 # num = 2 : real
            textoaux = 'min. X      : '
            tamnum = self.tamanho_numero(self.global_vars.varaux, self.rdc_vars.num)
            phrase = self.aux_RDC(rdc_file, textoaux, self.global_vars.varaux, tamnum)
            rdc_file.write(phrase)

            # Escreve linha com coordenada xmax
            self.global_vars.varaux = self.rdc_vars.Xmax3
            self.rdc_vars.num = 2 # num = 2 : real
            textoaux = 'max. X      : '
            tamnum = self.tamanho_numero(self.global_vars.varaux, self.rdc_vars.num)
            phrase = self.aux_RDC(rdc_file, textoaux, self.global_vars.varaux, tamnum)
            rdc_file.write(phrase)
            
            # Escreve linha com coordenada ymin
            self.global_vars.varaux = self.rdc_vars.Ymin3
            self.rdc_vars.num = 2 # num = 2 : real
            textoaux = 'min. Y      : '
            tamnum = self.tamanho_numero(self.global_vars.varaux, self.rdc_vars.num)
            phrase = self.aux_RDC(rdc_file, textoaux, self.global_vars.varaux, tamnum)
            rdc_file.write(phrase)

            # Escreve linha com coordenada ymax
            self.global_vars.varaux = self.rdc_vars.Ymax3
            self.rdc_vars.num = 2 # num = 2 : real
            textoaux = 'max. Y      : '
            tamnum = self.tamanho_numero(self.global_vars.varaux, self.rdc_vars.num)
            phrase = self.aux_RDC(rdc_file, textoaux, self.global_vars.varaux, tamnum)
            rdc_file.write(phrase)

            # Escreve a linha com o valor do erro dos dados
            rdc_file.write(f"pos'n error : unknown\n")

            # Escreve linha com resolução
            self.global_vars.varaux = self.global_vars.dx
            self.rdc_vars.num = 2 # num = 2 : real
            textoaux = 'resolution  : '
            tamnum = self.tamanho_numero(self.global_vars.varaux, self.rdc_vars.num)
            phrase = self.aux_RDC(rdc_file, textoaux, self.global_vars.varaux, tamnum)
            rdc_file.write(phrase)

            # Escreve a linha com o valor mínimo dos dados 
            self.global_vars.varaux = self.rdc_vars.Varmin
            self.rdc_vars.num = 2 # num = 2 : real
            textoaux = 'min. value  : '
            tamnum = self.tamanho_numero(self.global_vars.varaux, self.rdc_vars.num)
            phrase = self.aux_RDC(rdc_file, textoaux, self.global_vars.varaux, tamnum)
            rdc_file.write(phrase)

            # Escreve a linha com o valor máximo dos dados 
            self.global_vars.varaux = self.rdc_vars.Varmax
            self.rdc_vars.num = 2 # num = 2 : real
            textoaux = 'max. value  : '
            tamnum = self.tamanho_numero(self.global_vars.varaux, self.rdc_vars.num)
            phrase = self.aux_RDC(rdc_file, textoaux, self.global_vars.varaux, tamnum)
            rdc_file.write(phrase)

            # Escreve a linha com o valor mínimo de exebição 
            self.global_vars.varaux = self.rdc_vars.Varmin
            self.rdc_vars.num = 2 # num = 2 : real
            textoaux = 'display min : '
            tamnum = self.tamanho_numero(self.global_vars.varaux, self.rdc_vars.num)
            phrase = self.aux_RDC(rdc_file, textoaux, self.global_vars.varaux, tamnum)
            rdc_file.write(phrase)

            #  Escreve a linha com o valor máximo para exibição 
            self.global_vars.varaux = self.rdc_vars.Varmax
            self.rdc_vars.num = 2 # num = 2 : real
            textoaux = 'display max : '
            tamnum = self.tamanho_numero(self.global_vars.varaux, self.rdc_vars.num)
            phrase = self.aux_RDC(rdc_file, textoaux, self.global_vars.varaux, tamnum)
            rdc_file.write(phrase)

            # Escreve a linha com a unidade dos dados
            rdc_file.write(f'value units : unspecified\n')

            # Escreve a linha com o valor do erro dos dados
            rdc_file.write(f'value error : unknown\n')

            # Escreve linha com sinalizador
            rdc_file.write(f'flag value  : {0:1d}\n')
            
            # Escreve a linha com a definição do sinalizador
            rdc_file.write(f"flag def'n  : none\n")

            # Escreve a linha com o número de categorias da legenda
            rdc_file.write(f'legend cats : {0:1d}\n')

            # Escreve a linha sobre a criação da imagem
            rdc_file.write(f'lineage     : This file was created automatically by Hidropixel Plugin')
        
    def escreve_comprimento_acumulado(self):
        """
        Esta função é responsável por formular os arquivos de saída (tanto o raster (.RST), quanto sua documentação (.rdc))
        para os dados referentes aos comprimentos da rede de drenagem da bacia hidrográfica
        """

        # Abrindo o arquivo(fn : file name) para escrita dos resultados
        file_path = r'C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\resultados_test_modelo'
        fn_comp_acum = file_path  + r'\ComprimAcu.RST'

        # Define os dados a serem escritos
        dados_comp_acum = np.array([[float(self.global_vars.Lac[lin][col]) for col in range(self.rdc_vars.ncol)] for lin in range(self.rdc_vars.nlin)]) #lac n existe
        tipo_dados = gdalconst.GDT_Float32

        # Os arquivos terão formato RST
        driver = gdal.GetDriverByName('RST')

        # Cria arquivo final
        dataset = driver.Create(fn_comp_acum, self.rdc_vars.ncol, self.rdc_vars.nlin, 1, tipo_dados)

        # Escreve os dados na banda do arquivo
        banda = dataset.GetRasterBand(1)
        banda.WriteArray(dados_comp_acum)

        # Fechando o arquivo
        dataset = None
        banda = None
        driver = None
        tipo_dados = None

        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem
        self.rdc_vars.nlin3 = self.rdc_vars.nlin
        self.rdc_vars.ncol3 = self.rdc_vars.ncol
        self.rdc_vars.tipo_dado = 2
        self.rdc_vars.tipoMM = 2
        self.rdc_vars.VarMM2 = self.global_vars.Lac
        self.rdc_vars.i3 = 0 
        self.rdc_vars.Xmin3 = self.rdc_vars.xmin
        self.rdc_vars.Xmax3 = self.rdc_vars.xmax
        self.rdc_vars.Ymin3 = self.rdc_vars.ymin
        self.rdc_vars.Ymax3 = self.rdc_vars.ymax
        nomeRST = fn_comp_acum
        self.global_vars.metrordc = self.global_vars.metro
        self.min_max()
        self.escreve_RDC(nomeRST)

    def escreve_comprimento_acumulado_foz(self):
        """
        Esta função é responsável por formular os arquivos de saída (tanto o raster (.RST), quanto sua documentação (.rdc))
        para os dados referentes aos comprimentos da rede de drenagem da bacia hidrográfica
        """
        # Escrevendo o resultado do comprimento da rede de drenagem
        file_path = r'C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\resultados_test_modelo'
        fn_comp_foz = file_path + r'\ComprimFoz.RST'
               
         # Define os dados a serem escritos
        dados_comp_foz = np.array([[float(self.global_vars.Lfoz[lin][col]) for col in range(self.rdc_vars.ncol)] for lin in range(self.rdc_vars.nlin)])
        tipo_dados = gdalconst.GDT_Float32

        # Os arquivos terão formato RST
        driver = gdal.GetDriverByName('RST')

        # Cria arquivo final
        dataset = driver.Create(fn_comp_foz, self.rdc_vars.ncol, self.rdc_vars.nlin, 1, tipo_dados)

        # Escreve os dados na banda do arquivo
        banda = dataset.GetRasterBand(1)
        banda.WriteArray(dados_comp_foz)

        # Fechando o arquivo
        dataset = None
        banda = None
        driver = None
        tipo_dados = None

        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da foz da bacia hidrográfica
        self.rdc_vars.nlin3 = self.rdc_vars.nlin
        self.rdc_vars.ncol3 = self.rdc_vars.ncol
        self.rdc_vars.tipo_dado = 2
        self.rdc_vars.tipoMM = 2
        self.rdc_vars.VarMM2 = self.global_vars.Lfoz
        self.rdc_vars.i3 = 0 
        self.rdc_vars.Xmin3 = self.rdc_vars.xmin
        self.rdc_vars.Xmax3 = self.rdc_vars.xmax
        self.rdc_vars.Ymin3 = self.rdc_vars.ymin
        self.rdc_vars.Ymax3 = self.rdc_vars.ymax
        nomeRST = fn_comp_foz
        self.global_vars.metrordc = self.global_vars.metro
        self.min_max()
        self.escreve_RDC(nomeRST)

    def escreve_num_pix_dren(self):
        '''Esta função escreve a numeração das cabeceiras'''

        # Definindo o caminho para o arquivo RST
        file_path = r'C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\resultados_test_modelo'
        fn_num_cab = file_path + r'\numb_pixel_drenagem.RST'

        # Definindo os dados a serem escritos
        dados_num_cab = np.array([[float(self.contadren[lin][col]) for col in range(self.rdc_vars.ncol)] for lin in range(self.rdc_vars.nlin)])
        num_pix_max = np.amax(dados_num_cab)
        # Definindo o tipo de dados para Float32
        tipo_dados = gdalconst.GDT_Float32

        # Obtendo o driver para escrita do arquivo em GeoTiff
        driver = gdal.GetDriverByName('RST')

        # Criando o arquivo RST
        dataset = driver.Create(fn_num_cab, self.rdc_vars.ncol, self.rdc_vars.nlin, 1, tipo_dados)

        # Escrevendo os dados na banda do arquivo
        banda = dataset.GetRasterBand(1)
        banda.WriteArray(dados_num_cab)

        # Fechando o arquivo
        dataset = None
        banda = None
        driver = None
        tipo_dados = None

        # Alocando as variáveis para escrita do arquivo rdc para o comprimento da rede de drenagem
        self.rdc_vars.nlin3 = self.rdc_vars.nlin
        self.rdc_vars.ncol3 = self.rdc_vars.ncol
        self.rdc_vars.tipo_dado = 1
        self.rdc_vars.tipoMM = 2
        self.rdc_vars.VarMM2 = self.contadren
        self.rdc_vars.i3 = 0 
        self.rdc_vars.Xmin3 = self.rdc_vars.xmin
        self.rdc_vars.Xmax3 = self.rdc_vars.xmax
        self.rdc_vars.Ymin3 = self.rdc_vars.ymin
        self.rdc_vars.Ymax3 = self.rdc_vars.ymax
        self.rdc_vars.Varmax = num_pix_max
        self.rdc_vars.Varmin = 0
        nomeRST = fn_num_cab
        self.global_vars.metrordc = self.global_vars.metro
        self.escreve_RDC(nomeRST)

    def escreve_conectividade(self):
        """
        Esta função é responsável por formular os arquivos de saída (tanto o raster (.RST), quanto sua documentação (.rdc))
        para os dados referentes ao mapa de conectividade das cabeceiras da bacia hidrográfica
        """
        # Abrindo o arquivo(fn : file name) para escrita dos resultados
        file_path = r'C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\resultados_test_modelo'

        # Escrevendo o resultado do mapa de conectividade dos pixels da superficie a rede de drenagem
        fn_n_conect_dren = file_path + r'\num_conexao_drenagem.RST'
        # Valor máximo
        var_max = np.amax(self.global_vars.pixeldren) 

        # Define os dados a serem escritos
        dados_n_conect_dren = np.array([[float(self.global_vars.pixeldren[lin][col]) for col in range(self.rdc_vars.ncol)] for lin in range(self.rdc_vars.nlin)])

        # Os arquivos terão formato RST
        driver = gdal.GetDriverByName('RST')
        tipo_dados = gdalconst.GDT_Float32

        # Cria arquivo final
        dataset = driver.Create(fn_n_conect_dren, self.rdc_vars.ncol, self.rdc_vars.nlin, 1, tipo_dados)

        # Escreve os dados na banda do arquivo
        banda = dataset.GetRasterBand(1)
        banda.WriteArray(dados_n_conect_dren)

        # Escreve os dados na banda do arquivo
        banda = dataset.GetRasterBand(1)
        banda.WriteArray(dados_n_conect_dren)

        # Fechando o arquivo
        dataset = None
        banda = None
        driver = None
        tipo_dados = None

        # Aloca as variáveis para escrita da documentação do arquivo rdc para o comprimento da foz da bacia hidrográfica
        self.rdc_vars.nlin3 = self.rdc_vars.nlin
        self.rdc_vars.ncol3 = self.rdc_vars.ncol
        self.rdc_vars.tipo_dado = 2
        self.rdc_vars.tipoMM = 2
        self.rdc_vars.VarMM2 = self.global_vars.pixeldren
        self.rdc_vars.i3 = 0 
        self.rdc_vars.Xmin3 = self.rdc_vars.xmin
        self.rdc_vars.Xmax3 = self.rdc_vars.xmax
        self.rdc_vars.Ymin3 = self.rdc_vars.ymin
        self.rdc_vars.Ymax3 = self.rdc_vars.ymax
        self.rdc_vars.Varmax = var_max
        self.rdc_vars.Varmin = 0    
        self.global_vars.metrordc = self.global_vars.metro
        nomeRST = fn_n_conect_dren
        self.escreve_RDC(nomeRST)

    def escreve_dados_trecho(self):
        # Esta função escreve os dados de saída referentes aos diferentes trechos dos canais da bacia hidrográfica
        file_path = r'C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\resultados_test_modelo'
        fn_dados_tre_sup = file_path + r'\dados_trechos_superf.txt'

        with open(fn_dados_tre_sup, 'w', encoding = 'utf-8') as arquivo_txt:
            arquivo_txt.write('{:<10}{:<6}{:<6}{:<10}{:<10}{:<12}{:<6}\n'.format('Cabeceira', 'Trecho', 'L(m)', 'Z_ini(m)', 'Z_fim(m)','Decliv(m/km)', 'Uso'))
            
            for self.global_vars.numcabeaux in range(self.global_vars.Ncabec):
                self.global_vars.numcabeaux = self.global_vars.numtre[self.global_vars.numcabeaux]

            for t in range(self.global_vars.numtreaux):
                if self.global_vars.usotre[self.global_vars.numcabeaux-1][t] == 0:
                        print(f'{t}; {self.global_vars.numcabeaux}  Uso zero')
                        input('Press enter to continue...')
                        pass
                # Escrevendo as linhas do arquivo conforme os valores das variáveis
                arquivo_txt.write('{:<10}{:<6}{:<10.2f}{:<10.2f}{:<10.2f}{:<12.6f}{:<6}\n'.format(self.global_vars.numcabeaux, t, self.global_vars.Ltre[self.global_vars.numcabeaux-1][t], self.global_vars.cotaini[self.global_vars.numcabeaux-1][t], self.global_vars.cotafim[self.global_vars.numcabeaux-1][t],\
                                                                                    self.global_vars.Stre[self.global_vars.numcabeaux-1][t],self.global_vars.usotre[self.global_vars.numcabeaux-1][t]))

    def escreve_decliv_pixel(self):
        '''Esta função gera o mapa de numeração dos pixels da rede de drenagem'''

        # Abrindo o arquivo(fn : file name) para escrita dos resultados
        file_path = r'C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\resultados_test_modelo'
        fn_decli_pix = file_path + r'\decliv_pixel.RST'

        # Define os dados a serem escritos
        dados_decli_pix = np.array([[float(self.global_vars.decliv_pixel[lin][col]) for col in range(self.rdc_vars.ncol)] for lin in range(self.rdc_vars.nlin)])
        tipo_dados = gdalconst.GDT_Float32

        # Obtendo o driver para escrita do arquivo em GeoTiff
        driver = gdal.GetDriverByName('RST')
        # Cria arquivo final
        dataset = driver.Create(fn_decli_pix, self.rdc_vars.ncol, self.rdc_vars.nlin, 1, tipo_dados)

        # Escreve os dados na banda do arquivo
        banda = dataset.GetRasterBand(1)
        banda.WriteArray(dados_decli_pix)

        # Fechando o arquivo
        dataset = None
        banda = None
        driver = None
        tipo_dados = None

        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem
        self.rdc_vars.nlin3 = self.rdc_vars.nlin
        self.rdc_vars.ncol3 = self.rdc_vars.ncol
        self.rdc_vars.tipo_dado = 2
        self.rdc_vars.tipoMM = 2
        self.rdc_vars.VarMM2 = self.global_vars.decliv_pixel
        self.rdc_vars.i3 = 0 
        self.rdc_vars.Xmin3 = self.rdc_vars.xmin
        self.rdc_vars.Xmax3 = self.rdc_vars.xmax
        self.rdc_vars.Ymin3 = self.rdc_vars.ymin
        self.rdc_vars.Ymax3 = self.rdc_vars.ymax
        nomeRST = fn_decli_pix
        self.global_vars.metrordc = self.global_vars.metro
        self.min_max()
        self.escreve_RDC(nomeRST)

    def escreve_decliv_pixel_jus(self):
        '''Esta função gera o mapa de numeração dos pixels jusantes da rede de drenagem'''

        # Abrindo o arquivo(fn : file name) para escrita dos resultados
        file_path = r'C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\resultados_test_modelo'
        fn_decli_pix_jus = file_path + r'\decliv_pixel_jus.RST'
        
        # Define os dados a serem escritos
        dados_decli_pix_jus = np.array([[float(self.global_vars.DECLIVpixjus[lin][col]) for col in range(self.rdc_vars.ncol)] for lin in range(self.rdc_vars.nlin)])
        tipo_dados = gdalconst.GDT_Float32

        # Obtendo o driver para escrita do arquivo em GeoTiff
        driver = gdal.GetDriverByName('RST')

        # Cria arquivo final
        dataset = driver.Create(fn_decli_pix_jus, self.rdc_vars.ncol, self.rdc_vars.nlin, 1, tipo_dados)

        # Escreve os dados na banda do arquivo
        banda = dataset.GetRasterBand(1)
        banda.WriteArray(dados_decli_pix_jus)

        # Fechando o arquivo
        dataset = None
        banda = None
        driver = None
        tipo_dados = None

        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem
        self.rdc_vars.nlin3 = self.rdc_vars.nlin
        self.rdc_vars.ncol3 = self.rdc_vars.ncol
        self.rdc_vars.tipo_dado = 2
        self.rdc_vars.tipoMM = 2
        self.rdc_vars.VarMM2 = self.global_vars.DECLIVpixjus
        self.rdc_vars.i3 = 0 
        self.rdc_vars.Xmin3 = self.rdc_vars.xmin
        self.rdc_vars.Xmax3 = self.rdc_vars.xmax
        self.rdc_vars.Ymin3 = self.rdc_vars.ymin
        self.rdc_vars.Ymax3 = self.rdc_vars.ymax
        nomeRST = fn_decli_pix_jus
        self.global_vars.metrordc = self.global_vars.metro
        self.min_max()
        self.escreve_RDC(nomeRST)
    
    def escreve_dist_rel_trechos(self):
        '''Esta função gera o arquivo com as distânicas relativas dentro do trecho'''

        # Abrindo o arquivo(fn : file name) para escrita dos resultados
        file_path = r'C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\resultados_test_modelo'
        fn_dist_rel_tre = file_path + r'\DISTtre.RST'
        
        # Define os dados a serem escritos
        dados_dist_rel_tre = np.array([[float(self.global_vars.DISTtre[lin][col]) for col in range(self.rdc_vars.ncol)] for lin in range(self.rdc_vars.nlin)])
        tipo_dados = gdalconst.GDT_Float32

        # Obtendo o driver para escrita do arquivo em GeoTiff
        driver = gdal.GetDriverByName('RST')

        # Cria arquivo final
        dataset = driver.Create(fn_dist_rel_tre, self.rdc_vars.ncol, self.rdc_vars.nlin, 1, tipo_dados)

        # Escreve os dados na banda do arquivo
        banda = dataset.GetRasterBand(1)
        banda.WriteArray(dados_dist_rel_tre)

        # Fechando o arquivo
        dataset = None
        banda = None
        driver = None
        tipo_dados = None

        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem
        self.rdc_vars.nlin3 = self.rdc_vars.nlin
        self.rdc_vars.ncol3 = self.rdc_vars.ncol
        self.rdc_vars.tipo_dado = 2
        self.rdc_vars.tipoMM = 2
        self.rdc_vars.VarMM2 = self.contadren
        self.rdc_vars.i3 = 0 
        self.rdc_vars.Xmin3 = self.rdc_vars.xmin
        self.rdc_vars.Xmax3 = self.rdc_vars.xmax
        self.rdc_vars.Ymin3 = self.rdc_vars.ymin
        self.rdc_vars.Ymax3 = self.rdc_vars.ymax
        self.rdc_vars.Varmax = np.amax()
        self.rdc_vars.Varmin = 0
        nomeRST = fn_dist_rel_tre
        self.global_vars.metrordc = self.global_vars.metro
        self.escreve_RDC(nomeRST)

    def escreve_num_pix_drenagem(self):
        '''Esta função gera o mapa de numeração dos píxels da rede de drenagem'''

        # Abrindo o arquivo(fn : file name) para escrita dos resultados
        file_path = r'C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\resultados_test_modelo'
        fn_num_pix_dren = file_path + 'num_pixels_drenagem.RST'
        
        # Define os dados a serem escritos
        dados_num_pix_dren = np.array([[float(self.global_vars.pixeldren[lin][col]) for col in range(self.rdc_vars.ncol)] for lin in range(self.rdc_vars.nlin)])
        tipo_dados = gdalconst.GDT_Float32

        # Obtendo o driver para escrita do arquivo em GeoTiff
        driver = gdal.GetDriverByName('RST')

        # Cria arquivo final
        dataset = driver.Create(fn_num_pix_dren, self.rdc_vars.ncol, self.rdc_vars.nlin, 1, tipo_dados)

        # Escreve os dados na banda do arquivo
        banda = dataset.GetRasterBand(1)
        banda.WriteArray(dados_num_pix_dren)

        # Fechando o arquivo
        dataset = None
        banda = None
        driver = None
       
        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem
        self.rdc_vars.nlin3 = self.rdc_vars.nlin
        self.rdc_vars.ncol3 = self.rdc_vars.ncol
        self.rdc_vars.tipo_dado = 1
        self.rdc_vars.tipoMM = 2
        self.rdc_vars.VarMM2 = self.contadren
        self.rdc_vars.i3 = 0 
        self.rdc_vars.Xmin3 = self.rdc_vars.xmin
        self.rdc_vars.Xmax3 = self.rdc_vars.xmax
        self.rdc_vars.Ymin3 = self.rdc_vars.ymin
        self.rdc_vars.Ymax3 = self.rdc_vars.ymax
        nomeRST = fn_num_pix_dren 
        self.global_vars.metrordc = self.global_vars.metro
        self.min_max()
        self.escreve_RDC(nomeRST)

    def escreve_num_trechos(self):
        '''Esta função escreve a numeração dos trechos'''
        # Abrindo o arquivo(fn : file name) para escrita dos resultados
        file_path = r'C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\resultados_test_modelo'
        fn_num_tre = file_path + r'\num_pixels_drenagem.RST'

        # Define os dados a serem escritos
        dados_num_tre = np.array([[float(self.global_vars.refcabtre[lin][col]) for col in range(self.rdc_vars.ncol)] for lin in range(self.rdc_vars.nlin)])
        tipo_dados = gdalconst.GDT_Float32

        # Obtendo o driver para escrita do arquivo em GeoTiff
        driver = gdal.GetDriverByName('RST')

        # Cria arquivo final
        dataset = driver.Create(fn_num_tre, self.rdc_vars.ncol, self.rdc_vars.nlin, 1, tipo_dados)

        # Escreve os dados na banda do arquivo
        banda = dataset.GetRasterBand(1)
        banda.WriteArray(dados_num_tre)

        # Fechando o arquivo
        dataset = None
        banda = None
        driver = None

        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem
        self.rdc_vars.nlin3 = self.rdc_vars.nlin
        self.rdc_vars.ncol3 = self.rdc_vars.ncol
        self.rdc_vars.tipo_dado = 1
        self.rdc_vars.tipoMM = 2
        self.rdc_vars.VarMM2 = self.global_vars.refcabtre
        self.rdc_vars.i3 = 0 
        self.rdc_vars.Xmin3 = self.rdc_vars.xmin
        self.rdc_vars.Xmax3 = self.rdc_vars.xmax
        self.rdc_vars.Ymin3 = self.rdc_vars.ymin
        self.rdc_vars.Ymax3 = self.rdc_vars.ymax
        nomeRST = fn_num_tre 
        self.global_vars.metrordc = self.global_vars.metro
        self.min_max()
        self.escreve_RDC(nomeRST)
    
    def escreve_tempo_canal(self):
        '''Esta função escreve os dados referentes aos cálculos do tempo de concentração para os canais da rede de drenagem da 
            bacia hidrográfica'''

        # Abrindo o arquivo(fn : file name) para escrita dos resultados
        file_path = r'C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\resultados_test_modelo'
        fn_temp_canal = file_path + r'\TempoCanal.RST'

        # Define os dados a serem escritos
        dados_temp_canal = np.array([[float(self.global_vars.TempoRioR[lin][col]) for col in range(self.rdc_vars.ncol)] for lin in range(self.rdc_vars.nlin)])
        tipo_dados = gdalconst.GDT_Float32

        # Obtendo o driver para escrita do arquivo em GeoTiff
        driver = gdal.GetDriverByName('RST')

        # Cria arquivo final
        dataset = driver.Create(fn_temp_canal, self.rdc_vars.ncol, self.rdc_vars.nlin, 1, tipo_dados)

        # Escreve os dados na banda do arquivo
        banda = dataset.GetRasterBand(1)
        banda.WriteArray(dados_temp_canal)

        # Fechando o arquivo
        dataset = None
        banda = None
        driver = None

        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem
        self.rdc_vars.nlin3 = self.rdc_vars.nlin
        self.rdc_vars.ncol3 = self.rdc_vars.ncol
        self.rdc_vars.tipo_dado = 2
        self.rdc_vars.tipoMM = 2
        self.rdc_vars.VarMM2 = self.global_vars.TempoRioR
        self.rdc_vars.i3 = 0 
        self.rdc_vars.Xmin3 = self.rdc_vars.xmin
        self.rdc_vars.Xmax3 = self.rdc_vars.xmax
        self.rdc_vars.Ymin3 = self.rdc_vars.ymin
        self.rdc_vars.Ymax3 = self.rdc_vars.ymax
        nomeRST = fn_temp_canal
        self.global_vars.metrordc = self.global_vars.metro
        self.min_max()
        self.escreve_RDC(nomeRST)

    def escreve_tempo_sup(self):
        '''Esta função constrói o mapa dos tempos de deslocamento da água para os píxel de superfícies'''
        # Abrindo o arquivo(fn : file name) para escrita dos resultados
        file_path = r'C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\resultados_test_modelo'
        fn_temp_sup = file_path + r'\TempoSup_por_cabeceira.RST'
        
        # Define os dados a serem escritos
        dados_temp_sup = np.array([[float(self.global_vars.TScabe2d[lin][col]) for col in range(self.rdc_vars.ncol)] for lin in range(self.rdc_vars.nlin)])
        tipo_dados = gdalconst.GDT_Float32

        # Obtendo o driver para escrita do arquivo em GeoTiff
        driver = gdal.GetDriverByName('RST')

        # Cria arquivo final
        dataset = driver.Create(fn_temp_sup, self.rdc_vars.ncol, self.rdc_vars.nlin, 1, tipo_dados)

        # Escreve os dados na banda do arquivo
        banda = dataset.GetRasterBand(1)
        banda.WriteArray(dados_temp_sup)

        # Fechando o arquivo
        dataset = None
        banda = None
        driver = None

        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem
        self.rdc_vars.nlin3 = self.rdc_vars.nlin
        self.rdc_vars.ncol3 = self.rdc_vars.ncol
        self.rdc_vars.tipo_dado = 2
        self.rdc_vars.tipoMM = 2
        self.rdc_vars.VarMM2 = self.global_vars.TScabe2d
        self.rdc_vars.i3 = 0 
        self.rdc_vars.Xmin3 = self.rdc_vars.xmin
        self.rdc_vars.Xmax3 = self.rdc_vars.xmax
        self.rdc_vars.Ymin3 = self.rdc_vars.ymin
        self.rdc_vars.Ymax3 = self.rdc_vars.ymax
        nomeRST = fn_temp_sup
        self.global_vars.metrordc = self.global_vars.metro
        self.min_max()
        self.escreve_RDC(nomeRST)

        # TempoS de deslocamento no mapa - píxels não fazem parte da cabeceira

        fn_temp_sup_Ncabe = file_path + r'\TempoSup_nao_de_cabeceira.RST'

        # Define os dados a serem escritos
        dados_temp_sup_Ncabe = np.array([[float(self.global_vars.TSnaocabe2d[lin][col]) for col in range(self.rdc_vars.ncol)] for lin in range(self.rdc_vars.nlin)])
        tipo_dados = gdalconst.GDT_Float32

        # Obtendo o driver para escrita do arquivo em GeoTiff
        driver = gdal.GetDriverByName('RST')

        # Cria arquivo final
        dataset = driver.Create(fn_temp_sup_Ncabe, self.rdc_vars.ncol, self.rdc_vars.nlin, 1, tipo_dados)

        # Escreve os dados na banda do arquivo
        banda = dataset.GetRasterBand(1)
        banda.WriteArray(dados_temp_sup_Ncabe)

        # Fechando o arquivo
        dataset = None
        banda = None
        driver = None 

        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem    
        self.rdc_vars.tipo_dado = 2
        self.rdc_vars.tipoMM = 2
        self.rdc_vars.VarMM2 = self.global_vars.TSnaocabe2d 
        nomeRST = fn_temp_sup_Ncabe
        self.min_max()
        self.escreve_RDC(nomeRST)

        # Tempo de deslocamento no mapa - todos os píxels
        fn_temp_sup_td = file_path + r'\TempoSup_todos.RST'

        # Define os dados a serem escritos
        dados_temp_sup_td = np.array([[float(self.global_vars.TStodos2d[lin][col]) for col in range(self.rdc_vars.ncol)] for lin in range(self.rdc_vars.nlin)])
        tipo_dados = gdalconst.GDT_Float32

        # Obtendo o driver para escrita do arquivo em GeoTiff
        driver = gdal.GetDriverByName('RST')

        # Cria arquivo final
        dataset = driver.Create(fn_temp_sup_td, self.rdc_vars.ncol, self.rdc_vars.nlin, 1, tipo_dados)

        # Escreve os dados na banda do arquivo
        banda = dataset.GetRasterBand(1)
        banda.WriteArray(dados_temp_sup_td)

        # Fechando o arquivo
        dataset = None
        banda = None
        driver = None         

        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem    
        self.rdc_vars.tipo_dado = 2
        self.rdc_vars.tipoMM = 2
        self.rdc_vars.VarMM2 = self.global_vars.TStodos2d
        nomeRST = fn_temp_sup_td
        self.min_max()
        self.escreve_RDC(nomeRST)

    def escreve_tempo_total(self):
        '''Esta função gera o mapa de conectividade dos píxels de superfície da rede de drenagem'''

        # Abrindo o arquivo(fn : file name) para escrita dos resultados
        file_path = r'C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\resultados_test_modelo'
        fn_temp_total = file_path + r'\TempoTotal.RST'

        # Determinaçãop do tempo de viagem máximo 
        tc_maximo = np.amax(self.global_vars.TempoTot)
        
        # Define os dados a serem escritos
        dados_temp_total = np.array([[float(self.global_vars.TempoTot[lin][col]) for col in range(self.rdc_vars.ncol)] for lin in range(self.rdc_vars.nlin)]) #tempo total não exist
        tipo_dados = gdalconst.GDT_Float32

        # Obtendo o driver para escrita do arquivo em GeoTiff
        driver = gdal.GetDriverByName('RST')

        # Cria arquivo final
        dataset = driver.Create(fn_temp_total, self.rdc_vars.ncol, self.rdc_vars.nlin, 1, tipo_dados)

        # Escreve os dados na banda do arquivo
        banda = dataset.GetRasterBand(1)
        banda.WriteArray(dados_temp_total)

        # Fechando o arquivo
        dataset = None
        banda = None
        driver = None   

        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem
        self.rdc_vars.nlin3 = self.rdc_vars.nlin
        self.rdc_vars.ncol3 = self.rdc_vars.ncol
        self.rdc_vars.tipo_dado = 2
        self.rdc_vars.tipoMM = 2
        self.global_vars.VarMM2 = self.global_vars.TempoTot
        self.rdc_vars.i3 = 0 
        self.rdc_vars.Xmin3 = self.rdc_vars.xmin
        self.rdc_vars.Xmax3 = self.rdc_vars.xmax
        self.rdc_vars.Ymin3 = self.rdc_vars.ymin
        self.rdc_vars.Ymax3 = self.rdc_vars.ymax
        self.rdc_vars.Varmax = tc_maximo
        self.rdc_vars.Varmin = 0
        nomeRST = self.fn_temp_total
        self.global_vars.metrordc = self.global_vars.metro
        self.escreve_RDC(nomeRST)

    def escreve_tre_cabec(self):
        '''Esta função gera o arquivo que possui as informações acerca dos trechos das cabeceiras'''

        # Abrindo o arquivo(fn : file name) para escrita dos resultados
        file_path = r'C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\resultados_test_modelo'
        fn_tre_cabec = file_path + r'\relacao_trechos_cabec.txt'
        with open(fn_tre_cabec, 'w', encoding = 'utf-8') as arquivo_txt:
            arquivo_txt.write('{:<12}{:<12}'.format('Cabeceira', 'Num.trechos'))
            for self.global_vars.numcabeaux in range(self.global_vars.Ncabec):
                arquivo_txt.write(f'{self.global_vars.numcabeaux:12d}{self.global_vars.numtre[self.global_vars.numcabeaux]:12d}')
        return arquivo_txt
    
    def escreve_trecho_pixel(self):
        '''Esta função gera o mapa de conectividade das cabeceiras'''

        # Abrindo o arquivo(fn : file name) para escrita dos resultados
        file_path = r'C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\resultados_test_modelo'
        fn_tre_pix = file_path + r'\TREpix.RST'

        # Define os dados a serem escritos
        dados_tre_pix = np.array([[float(self.global_vars.TREpix[lin][col]) for col in range(self.rdc_vars.ncol)] for lin in range(self.rdc_vars.nlin)])
        tipo_dados = gdalconst.GDT_Float32

        # Obtendo o driver para escrita do arquivo em GeoTiff
        driver = gdal.GetDriverByName('RST')
        
        # Cria arquivo final
        dataset = driver.Create(fn_tre_pix, self.rdc_vars.ncol, self.rdc_vars.nlin, 1, tipo_dados)

        # Escreve os dados na banda do arquivo
        banda = dataset.GetRasterBand(1)
        banda.WriteArray(dados_tre_pix)

        # Fechando o arquivo
        dataset = None
        banda = None
        driver = None   

        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem
        self.rdc_vars.nlin3 = self.rdc_vars.nlin
        self.rdc_vars.ncol3 = self.rdc_vars.ncol
        self.rdc_vars.tipo_dado = 1
        self.rdc_vars.tipoMM = 2
        self.rdc_vars.VarMM2 = self.global_vars.TREpix
        self.rdc_vars.i3 = 0 
        self.rdc_vars.Xmin3 = self.rdc_vars.xmin
        self.rdc_vars.Xmax3 = self.rdc_vars.xmax
        self.rdc_vars.Ymin3 = self.rdc_vars.ymin
        self.rdc_vars.Ymax3 = self.rdc_vars.ymax
        nomeRST = fn_tre_pix
        self.global_vars.metrordc = self.global_vars.metro
        self.min_max()
        self.escreve_RDC(nomeRST)
    
    def escreve_TS_pix_acum(self):
        '''Esta função gera os arquivos com os resultados para o tempo de concentração/escoamento'''

        # Abrindo o arquivo(fn : file name) para escrita dos resultados
        file_path = r'C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\resultados_test_modelo'
        fn_temp_pix_jus = file_path + r'\tempo_pixel_jus.RST'

        # Define os dados a serem escritos
        dados_temp_pix_jus = np.array([[float(self.global_vars.TSpix[lin][col]) for col in range(self.rdc_vars.ncol)] for lin in range(self.rdc_vars.nlin)])
        tipo_dados = gdalconst.GDT_Float32

        # Obtendo o driver para escrita do arquivo em GeoTiff
        driver = gdal.GetDriverByName('RST')
        
        # Cria arquivo final
        dataset = driver.Create(fn_temp_pix_jus, self.rdc_vars.ncol, self.rdc_vars.nlin, 1, tipo_dados)

        # Escreve os dados na banda do arquivo
        banda = dataset.GetRasterBand(1)
        banda.WriteArray(dados_temp_pix_jus)

        # Fechando o arquivo
        dataset = None
        banda = None
        driver = None   

        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem
        self.rdc_vars.nlin3 = self.rdc_vars.nlin
        self.rdc_vars.ncol3 = self.rdc_vars.ncol
        self.rdc_vars.tipo_dado = 2
        self.rdc_vars.tipoMM = 2
        self.rdc_vars.VarMM2 = self.global_vars.TSpix
        self.rdc_vars.i3 = 0 
        self.rdc_vars.Xmin3 = self.rdc_vars.xmin
        self.rdc_vars.Xmax3 = self.rdc_vars.xmax
        self.rdc_vars.Ymin3 = self.rdc_vars.ymin
        self.rdc_vars.Ymax3 = self.rdc_vars.ymax
        nomeRST = fn_temp_pix_jus
        self.global_vars.metrordc = self.global_vars.metro
        self.min_max()
        self.escreve_RDC(nomeRST)

        fn_temp_pix_jus_acum = file_path + r'\tempo_pixel_jus_acum.RST'
        # Define os dados a serem escritos
        dados_temp_pix_jus_acum = np.array([[float(self.global_vars.TSpixacum[lin][col]) for col in range(self.rdc_vars.ncol)] for lin in range(self.rdc_vars.nlin)])
        tipo_dado = gdalconst.GDT_Float32

        # Obtendo o driver para escrita do arquivo em GeoTiff
        driver = gdal.GetDriverByName('RST')

        # Cria o arquivo final
        dataset = driver.Create(fn_temp_pix_jus_acum,self.rdc_vars.ncol, self.rdc_vars.ncol, 1, tipo_dado)

        # Escreve os dados na banda do arquivo
        banda = dataset.GetRasterBand(1)
        banda.WriteArray(dados_temp_pix_jus_acum)

        self.rdc_vars.VarMM2 = self.global_vars.TSpixacum
        nomeRST = fn_temp_pix_jus
        self.min_max()
        self.escreve_RDC(nomeRST)       
    
    def escreve_hidrograma_dlr(self):
        '''Esta função gera contento o hidrograma total da bacia hidrográfica estudada'''
        file_name = r'C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\Bacia_mulugun\hidropixel_files\entrada_hidropixel\entrada_hidropixel\Input_bin\Output_bin\hidrograma_P24_max.txt'
        with open(file_name, 'w', encoding = 'utf-8') as arquivo_txt:
            arquivo_txt.write('tempo(min), vazão calculada(m³/s)\n')
            for k in range(self.blocos_vazao):
                arquivo_txt.write(f'{self.tempo_vazao_pixel[k]}, {self.vazao[k]}\n')

    def escreve_hietograma_pe(self):
        '''Esta função gera o arquivo contento o valor da precipitação efetiva por pixel durante os blocos de chuva'''

        # Recebe diretório e nome do arquivo do usurário      
        arquivo = r'C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\Bacia_mulugun\hidropixel_files\entrada_hidropixel\entrada_hidropixel\Input_bin\Output_bin\hietograma_pe_minus_ETP.txt'
        with open(arquivo, 'w', encoding = 'utf-8') as arquivo_txt:
            # JVD:optimize: Escreve cabeçalho
            arquivo_txt.write('Pixel,')
            for k in range(1,self.quantidade_blocos_chuva+1):
                if k < self.quantidade_blocos_chuva:
                    arquivo_txt.write(f'{self.time[k]},')
                else:
                    arquivo_txt.write(f'{self.time[k]}\n')

            # Escreve linhas com dados de precipitação efetiva por pixel
            for k in range(1,self.numero_total_pix+1):
                arquivo_txt.write(f'{k},')
                for w in range(self.quantidade_blocos_chuva):
                    if w < self.quantidade_blocos_chuva-1:
                        arquivo_txt.write(f'{self.hexc_pix[k-1][w]},')
                    else:
                        arquivo_txt.write(f'{self.hexc_pix[k-1][w]}'+'\n')

    def escreve_numb_pix_bacia(self):
        '''Esta função gera o mapa contendo a numeração dos pixels presentes na bacia hidrografíca'''
        # JVDopmize: determinação da perda inicial máxima
        numb_pix_max = np.amax(self.numb_pix_bacia)

        # Abrindo o arquivo(fn : file name) para escrita dos resultados
        # fn_numb_pix = self.dlg_exc_rain.le_1_pg4.text()
        file_path = r'C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\Bacia_mulugun\hidropixel_files\entrada_hidropixel\entrada_hidropixel\Input_bin\Output_bin'
        fn_numb_pix = file_path + r'\numb_pixel_bacia.RST'

        
        # Define os dados a serem escritos
        dados_numb_pix = np.array([[float(self.numb_pix_bacia[lin][col]) for col in range(self.rdc_vars.ncol)] for lin in range(self.rdc_vars.nlin)])
        tipo_dados = gdalconst.GDT_Float32

        # Obtendo o driver para escrita do arquivo em GeoTiff
        driver = gdal.GetDriverByName('RST')

        # Cria arquivo final
        dataset = driver.Create(fn_numb_pix, self.rdc_vars.ncol, self.rdc_vars.nlin, 1, tipo_dados)
        dataset.SetGeoTransform(self.rdc_vars.geotransform)
        dataset.SetProjection(self.rdc_vars.projection)

        # Escreve os dados na banda do arquivo
        banda = dataset.GetRasterBand(1)
        banda.WriteArray(dados_numb_pix)

        # Fechando o arquivo
        dataset = None
        banda = None
        driver = None
        tipo_dados = None

        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem
        self.rdc_vars.nlin3 = self.rdc_vars.nlin
        self.rdc_vars.ncol3 = self.rdc_vars.ncol
        self.rdc_vars.tipo_dado = 2
        self.rdc_vars.tipoMM = 2
        self.rdc_vars.VarMM2 = self.numb_pix_bacia
        self.rdc_vars.i3 = 0 
        self.rdc_vars.Xmin3 = self.X_minimo
        self.rdc_vars.Xmax3 = self.X_maximo
        self.rdc_vars.Ymin3 = self.Y_minimo
        self.rdc_vars.Ymax3 = self.Y_maximo
        self.rdc_vars.Varmax = numb_pix_max
        self.rdc_vars.Varmin = 0
        nomeRST = fn_numb_pix
        self.global_vars.metrordc = self.global_vars.metro
        self.escreve_RDC(nomeRST)    

    def escreve_perdas_ini(self):
        '''Esta função gera o mapa contendo os valores das perdas iniciais dos pixels presentes na bacia hidrografíca'''
        # JVDopmize: determinação da perda inicial máxima
        perda_ini_max = np.amax(self.perdas_iniciais)

        # Abrindo o arquivo(fn : file name) para escrita dos resultados
        file_path = r'C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\Bacia_mulugun\hidropixel_files\entrada_hidropixel\entrada_hidropixel\Input_bin\Output_bin'
        fn_perda_ini = file_path + r'\perdas_iniciais.RST'
        
        # Define os dados a serem escritos
        dados_perda_ini = np.array([[float(self.perdas_iniciais[lin][col]) for col in range(self.rdc_vars.ncol)] for lin in range(self.rdc_vars.nlin)])
        tipo_dados = gdalconst.GDT_Float32

        # Obtendo o driver para escrita do arquivo em GeoTiff
        driver = gdal.GetDriverByName('RST')

        # Cria arquivo final
        dataset = driver.Create(fn_perda_ini, self.rdc_vars.ncol, self.rdc_vars.nlin, 1, tipo_dados)
        dataset.SetGeoTransform(self.rdc_vars.geotransform)
        dataset.SetProjection(self.rdc_vars.projection)

        # Escreve os dados na banda do arquivo
        banda = dataset.GetRasterBand(1)
        banda.WriteArray(dados_perda_ini)

        # Fechando o arquivo
        dataset = None
        banda = None
        driver = None
        tipo_dados = None

        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem
        self.rdc_vars.nlin3 = self.rdc_vars.nlin
        self.rdc_vars.ncol3 = self.rdc_vars.ncol
        self.rdc_vars.tipo_dado = 2
        self.rdc_vars.tipoMM = 2
        self.rdc_vars.VarMM2 = self.perdas_iniciais
        self.rdc_vars.i3 = 0 
        self.rdc_vars.Xmin3 = self.X_minimo
        self.rdc_vars.Xmax3 = self.X_maximo
        self.rdc_vars.Ymin3 = self.Y_minimo
        self.rdc_vars.Ymax3 = self.Y_maximo
        self.rdc_vars.Varmax = perda_ini_max
        self.rdc_vars.Varmin = 0
        nomeRST = fn_perda_ini
        self.global_vars.metrordc = self.global_vars.metro
        self.escreve_RDC(nomeRST)      

    def escreve_S_potencial(self):
        '''Esta função gera o arquivo raster contendo os valores da retenção máxima (S) por pixel presente na bacia hidrográfica'''
        # JVDoptmize: calcula a retenção máxima
        max_retencao = np.amax(self.Spotencial)

        # Abrindo o arquivo(fn : file name) para escrita dos resultados
        file_path = r'C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\Bacia_mulugun\hidropixel_files\entrada_hidropixel\entrada_hidropixel\Input_bin\Output_bin'
        fn_Spotencial = file_path + r'\Spotencial.RST'
        
        # Define os dados a serem escritos
        dados_Spotencial = np.array([[float(self.Spotencial[lin][col]) for col in range(self.rdc_vars.ncol)] for lin in range(self.rdc_vars.nlin)])
        tipo_dados = gdalconst.GDT_Float32

        # Obtendo o driver para escrita do arquivo em GeoTiff
        driver = gdal.GetDriverByName('RST')

        # Cria arquivo final
        dataset = driver.Create(fn_Spotencial, self.rdc_vars.ncol, self.rdc_vars.nlin, 1, tipo_dados)
        dataset.SetGeoTransform(self.rdc_vars.geotransform)
        dataset.SetProjection(self.rdc_vars.projection)

        # Escreve os dados na banda do arquivo
        banda = dataset.GetRasterBand(1)
        banda.WriteArray(dados_Spotencial)

        # Fechando o arquivo
        dataset = None
        banda = None
        driver = None
        tipo_dados = None

        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem
        self.rdc_vars.nlin3 = self.rdc_vars.nlin
        self.rdc_vars.ncol3 = self.rdc_vars.ncol
        self.rdc_vars.tipo_dado = 2
        self.rdc_vars.tipoMM = 2
        self.rdc_vars.VarMM2 = self.Spotencial
        self.rdc_vars.i3 = 0 
        self.rdc_vars.Xmin3 = self.X_minimo
        self.rdc_vars.Xmax3 = self.X_maximo
        self.rdc_vars.Ymin3 = self.Y_minimo
        self.rdc_vars.Ymax3 = self.Y_maximo
        self.rdc_vars.Varmax = max_retencao
        self.rdc_vars.Varmin = 0
        nomeRST = fn_Spotencial
        self.global_vars.metrordc = self.global_vars.metro
        self.escreve_RDC(nomeRST)       

    def escreve_precipitacao_excedente(self):
        '''Esta função é responsável por gerar o arquivo raster contendo os valores da precipitação excedente por pixel presente na baica hidrográfica'''
        # JVDoptmize: determina precipitação excedente máxima
        pe_maxima = np.amax(self.pe_acumulada_pixel)

        # Abrindo o arquivo(fn : file name) para escrita dos resultados
        file_path = r'C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\Bacia_mulugun\hidropixel_files\entrada_hidropixel\entrada_hidropixel\Input_bin\Output_bin'
        fn_pe_acum = file_path + r'\pe_acumulada_pixel.RST'
        
        # Define os dados a serem escritos
        dados_pe_acum = np.array([[float(self.pe_acumulada_pixel[lin][col]) for col in range(self.rdc_vars.ncol)] for lin in range(self.rdc_vars.nlin)])
        tipo_dados = gdalconst.GDT_Float32

        # Obtendo o driver para escrita do arquivo em GeoTiff
        driver = gdal.GetDriverByName('RST')

        # Cria arquivo final
        dataset = driver.Create(fn_pe_acum, self.rdc_vars.ncol, self.rdc_vars.nlin, 1, tipo_dados)
        dataset.SetGeoTransform(self.rdc_vars.geotransform)
        dataset.SetProjection(self.rdc_vars.projection)

        # Escreve os dados na banda do arquivo
        banda = dataset.GetRasterBand(1)
        banda.WriteArray(dados_pe_acum)

        # Fechando o arquivo
        dataset = None
        banda = None
        driver = None
        tipo_dados = None

        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem
        self.rdc_vars.nlin3 = self.rdc_vars.nlin
        self.rdc_vars.ncol3 = self.rdc_vars.ncol
        self.rdc_vars.tipo_dado = 2
        self.rdc_vars.tipoMM = 2
        self.rdc_vars.VarMM2 = self.pe_acumulada_pixel
        self.rdc_vars.i3 = 0 
        self.rdc_vars.Xmin3 = self.X_minimo
        self.rdc_vars.Xmax3 = self.X_maximo
        self.rdc_vars.Ymin3 = self.Y_minimo
        self.rdc_vars.Ymax3 = self.Y_maximo
        self.rdc_vars.Varmax = pe_maxima
        self.rdc_vars.Varmin = 0
        nomeRST = fn_pe_acum
        self.global_vars.metrordc = self.global_vars.metro
        self.escreve_RDC(nomeRST)  

    def escreve_precipitacao_total_acum(self):
        '''Esta função gera o arquivo raster contendo a precipitação total acumulada por pixel presente na bacia hidrográfica'''
        # JVDoptmize: determina precipitação máxima acumulada
        p_acum_max = np.amax(self.chuva_total_pixel)

        # Abrindo o arquivo(fn : file name) para escrita dos resultados
        file_path = r'C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\Bacia_mulugun\hidropixel_files\entrada_hidropixel\entrada_hidropixel\Input_bin\Output_bin'
        fn_p_acum = file_path + r'\chuva_total_pixel.RST'
        
        # Define os dados a serem escritos
        dados_p_acum = np.array([[float(self.chuva_total_pixel[lin][col]) for col in range(self.rdc_vars.ncol)] for lin in range(self.rdc_vars.nlin)])
        tipo_dados = gdalconst.GDT_Float32

        # Obtendo o driver para escrita do arquivo em GeoTiff
        driver = gdal.GetDriverByName('RST')

        # Cria arquivo final
        dataset = driver.Create(fn_p_acum, self.rdc_vars.ncol, self.rdc_vars.nlin, 1, tipo_dados)
        dataset.SetGeoTransform(self.rdc_vars.geotransform)
        dataset.SetProjection(self.rdc_vars.projection)

        # Escreve os dados na banda do arquivo
        banda = dataset.GetRasterBand(1)
        banda.WriteArray(dados_p_acum)

        # Fechando o arquivo
        dataset = None
        banda = None
        driver = None
        tipo_dados = None

        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem
        self.rdc_vars.nlin3 = self.rdc_vars.nlin
        self.rdc_vars.ncol3 = self.rdc_vars.ncol
        self.rdc_vars.tipo_dado = 2
        self.rdc_vars.tipoMM = 2
        self.rdc_vars.VarMM2 = self.chuva_total_pixel
        self.rdc_vars.i3 = 0 
        self.rdc_vars.Xmin3 = self.X_minimo
        self.rdc_vars.Xmax3 = self.X_maximo
        self.rdc_vars.Ymin3 = self.Y_minimo
        self.rdc_vars.Ymax3 = self.Y_maximo
        self.rdc_vars.Varmax = p_acum_max
        self.rdc_vars.Varmin = 0
        nomeRST = fn_p_acum
        self.global_vars.metrordc = self.global_vars.metro
        self.escreve_RDC(nomeRST)  

    def escreve_volume_gerado_pixel(self):
        '''Esta função gera o arquivo raster contendo o volume gerado por pixel presente na bacia hidrográfica'''
        # JVDoptmize: determina precipitação máxima acumulada
        vol_max = np.amax(self.volume_total_pix)

        # Abrindo o arquivo(fn : file name) para escrita dos resultados
        file_path = r'C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\Bacia_mulugun\hidropixel_files\entrada_hidropixel\entrada_hidropixel\Input_bin\Output_bin'
        fn_vol = file_path + r'\volume_total_pix.RST'
        
        # Define os dados a serem escritos
        dados_vol = np.array([[float(self.volume_total_pix[lin][col]) for col in range(self.rdc_vars.ncol)] for lin in range(self.rdc_vars.nlin)])
        tipo_dados = gdalconst.GDT_Float32

        # Obtendo o driver para escrita do arquivo em GeoTiff
        driver = gdal.GetDriverByName('RST')

        # Cria arquivo final
        dataset = driver.Create(fn_vol, self.rdc_vars.ncol, self.rdc_vars.nlin, 1, tipo_dados)
        dataset.SetGeoTransform(self.rdc_vars.geotransform)
        dataset.SetProjection(self.rdc_vars.projection)

        # Escreve os dados na banda do arquivo
        banda = dataset.GetRasterBand(1)
        banda.WriteArray(dados_vol)

        # Fechando o arquivo
        dataset = None
        banda = None
        driver = None
        tipo_dados = None

        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem
        self.rdc_vars.nlin3 = self.rdc_vars.nlin
        self.rdc_vars.ncol3 = self.rdc_vars.ncol
        self.rdc_vars.tipo_dado = 2
        self.rdc_vars.tipoMM = 2
        self.rdc_vars.VarMM2 = self.volume_total_pix
        self.rdc_vars.i3 = 0 
        self.rdc_vars.Xmin3 = self.X_minimo
        self.rdc_vars.Xmax3 = self.X_maximo
        self.rdc_vars.Ymin3 = self.Y_minimo
        self.rdc_vars.Ymax3 = self.Y_maximo
        self.rdc_vars.Varmax = vol_max
        self.rdc_vars.Varmin = 0
        nomeRST = fn_vol
        self.global_vars.metrordc = self.global_vars.metro
        self.escreve_RDC(nomeRST) 

    def escreve_vazao_pico_pixel(self, unit):
        '''Esta função gera o arquivo raster contendo o volume gerado por pixel presente na bacia hidrográfica
           unit: identifica a unidade da vazão escolhida pelo usuário;
                - unit == 1: m³/s
                - unit != 1: L/s'''
        # JVDoptmize: determina precipitação máxima acumulada
        vazao_pixo_max = np.amax(self.vazao_pico)

        # Abrindo o arquivo(fn : file name) para escrita dos resultados
        file_path = r'C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\Bacia_mulugun\hidropixel_files\entrada_hidropixel\entrada_hidropixel\Input_bin\Output_bin'
        fn_vazao_pico = file_path + r'\vazao_pico_pixel.RST'

        # Define os dados a serem escritos
        if unit == 1:
            dados_vazao_pico = np.array([[float(self.vazao_pico[lin][col]) for col in range(self.rdc_vars.ncol)] for lin in range(self.rdc_vars.nlin)])
            tipo_dados = gdalconst.GDT_Float32
        else:
            dados_vazao_pico = np.array([[float(self.vazao_pico[lin][col]/1000) for col in range(self.rdc_vars.ncol)] for lin in range(self.rdc_vars.nlin)])
            tipo_dados = gdalconst.GDT_Float32            
        # Obtendo o driver para escrita do arquivo em GeoTiff
        driver = gdal.GetDriverByName('RST')

        # Cria arquivo final
        dataset = driver.Create(fn_vazao_pico, self.rdc_vars.ncol, self.rdc_vars.nlin, 1, tipo_dados)
        dataset.SetGeoTransform(self.rdc_vars.geotransform)
        dataset.SetProjection(self.rdc_vars.projection)

        # Escreve os dados na banda do arquivo
        banda = dataset.GetRasterBand(1)
        banda.WriteArray(dados_vazao_pico)

        # Fechando o arquivo
        dataset = None
        banda = None
        driver = None
        tipo_dados = None

        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem
        self.rdc_vars.nlin3 = self.rdc_vars.nlin
        self.rdc_vars.ncol3 = self.rdc_vars.ncol
        self.rdc_vars.tipo_dado = 2
        self.rdc_vars.tipoMM = 2
        self.rdc_vars.VarMM2 = self.vazao_pico
        self.rdc_vars.i3 = 0 
        self.rdc_vars.Xmin3 = self.X_minimo
        self.rdc_vars.Xmax3 = self.X_maximo
        self.rdc_vars.Ymin3 = self.Y_minimo
        self.rdc_vars.Ymax3 = self.Y_maximo
        self.rdc_vars.Varmax = vazao_pixo_max
        self.rdc_vars.Varmin = 0
        nomeRST = fn_vazao_pico
        self.global_vars.metrordc = self.global_vars.metro
        self.escreve_RDC(nomeRST) 

    def escreve_pe_calculada(self):
        '''Esta função é responsável por gerar o arquivo contento a precipitação efetiva para a bacia hidrográfica em questão'''
        # Abrindo o arquivo(fn : file name) para escrita dos resultados
        file_path = r'C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\Bacia_mulugun\hidropixel_files\entrada_hidropixel\entrada_hidropixel\Input_bin\Output_bin'
        fn_p_calc = file_path + r'\pe_calculada.txt'
        with open(fn_p_calc, 'w', encoding='utf-8') as arquivo_txt:
            arquivo_txt.write(f'Calculated excess rainfall (mm) = {self.chuva_excedente_calc}')

    def run_flow_tt(self):
        '''Esta função ordena a execução das outras funções da classe test'''

        # Definicões iniciais!

        # Define tipo:
        self.global_vars.tipo_decliv = 4
        # 1: declividade cte para subtrecho dada em funcao das cotas ini e fim do subtrecho, e sua extensao
        # 2: declividade cte para subtrecho dada pela media ponderada da decliv de cada pixel em relacao ao final do subtrecho
        # 3: declividade cte para subtrecho dada pela media artimetica da decliv de cada pixel em relacao ao final do subtrecho
        # 4: declividade variavel calculada invidualmente pixel a pixel ao longo do caminho, com imposicao de limites minimo e maximo, sendo
        #calculado tempo de um pixel para seu jusante e depois somados esses tempos
        
        # Define subtipo (valido para tipos 1, 2 e 3; tipodecliv=4 nao tem subtipo):
        self.global_vars.subtipodecliv = 'b'
        # a: aproximacao linear por regra de tres para tempos de escoamento dos pixels intermediarios
        # b: calculo via equacao do metodo SCS para cada tempo de escoamento dos pixels intermediarios, mantido S constante (tipo 1,2 ou 3)
        

        # Atribuição das variáveis
        self.global_vars.lado = 1
        self.global_vars.diagonal = 1.4142
        self.global_vars.coef_c = 1.3883
        self.global_vars.coef_d = 0.6017
        self.global_vars.coef_g = 2.5111
        self.global_vars.coef_h = 0.3276
        self.global_vars.n_canal = 0.05
        self.global_vars.max_comp_trecho = 1000
        self.global_vars.sheet_flow = 30.48
        self.global_vars.profundidade_resers = 5
        self.global_vars.P24 = 42.75

        # Funções de leitura dos arquivos
        print('Lendo arquivos de entrada...')
        arquivo_bacia = r'c:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\SmallExample\input_binary\1_WATERSHED_EXbin.RST'
        self.leh_bacia(arquivo_bacia, 1)
        self.leh_caracteristica_dRios()
        self.leh_classes_rios()
        A = 45
        B = 90
        C = 135
        D = 180
        E = 225
        F = 270
        G = 315
        H = 360
        self.leh_direcoes_de_fluxo(A,B,C,D,E,F,G,H)
        self.leh_drenagem()
        self.leh_modelo_numerico_dTerreno()
        self.leh_uso_do_solo()
        self.leh_uso_manning()
        self.leh_drainage_area()

        # Funções de processamento
        print('\nIniciando processamento...\n')

        if self.rdc_vars.unidaderef =='deg':
            # Sistema está em graus, assumindo lat e long: será feita a projeção para metros
            self.global_vars.metro = 0
        else:
            # Sistema está em metros, não é preciso fazer a projeção para metros
            self.global_vars.metro = 1
        
        print('Processando numera pixel...\n')
        self.numera_pixel()
        self.escreve_num_pix_dren()

        print('Processando distância de drenagem...\n')
        self.dist_drenagem()
        self.escreve_decliv_pixel()
        self.escreve_decliv_pixel_jus()

        print('Processando comprimento acumulado...\n')
        self.comprimento_acumulado()
        self.escreve_comprimento_acumulado()
        self.escreve_comprimento_acumulado_foz()

        print('Processando comprimento acumulado...\n')
        self.tempo_concentracao()

    def run_rainfall_interpolation(self, map_file):
        '''Esta função organiza a execução da função que realiza a interpolação da precipitação para todos os pixels presentes na bacia hidrográfica
           '''
        start = perf_counter()
        # Initial configuration
        if self.rdc_vars.unidaderef =='deg':
            # Sistema está em graus, assumindo lat e long: será feita a projeção para metros
            self.global_vars.metro = 0
        else:
            # Sistema está em metros, não é preciso fazer a projeção para metros
            self.global_vars.metro = 1

        # Reading input files
        print('Reading input files')
        arquivo_bacia = r"C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\Bacia_mulugun\hidropixel_files\entrada_hidropixel\entrada_hidropixel\Input_bin\bacia_recl.rst"
        self.leh_bacia(arquivo_bacia, 2)
        arquivo_posto = r"C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\Bacia_mulugun\hidropixel_files\entrada_hidropixel\entrada_hidropixel\Input_ascii\dados_postos_pluv.txt"
        self.leh_posto_pluv(arquivo_posto)
        arquivo_precipitacao = r"C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\Bacia_mulugun\hidropixel_files\entrada_hidropixel\entrada_hidropixel\rainfall_data.txt"
        self.leh_arquivo_precipitacao(arquivo_precipitacao )

        # Processing and wrinting output files
        print('\nWriting outputs...')
        if map_file == 1:
            self.rainfall_interpolation_map()
        else:    
            self.rainfall_interpolation()
        end = perf_counter()
        print(f'The processing time was{end-start}')

    def run_exc_rain(self):
        '''Esta função configura a ordem de execução da rotina excess rainfall'''
        start = perf_counter()
        # Initial configuration
        if self.rdc_vars.unidaderef =='deg':
            # Sistema está em graus, assumindo lat e long: será feita a projeção para metros
            self.global_vars.metro = 0
        else:
            # Sistema está em metros, não é preciso fazer a projeção para metros
            self.global_vars.metro = 1

        # Reading input files
        print('Reading input files')
        arquivo_bacia = r"C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\Bacia_mulugun\hidropixel_files\entrada_hidropixel\entrada_hidropixel\Input_bin\bacia_recl.rst"
        self.leh_bacia(arquivo_bacia, 2)
        curve_number = r"C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\Bacia_mulugun\hidropixel_files\entrada_hidropixel\entrada_hidropixel\Input_bin\curve_number_corrigido.rst"
        self.leh_CN(curve_number)
        self.numera_pix_bacia()
        parametros = r"C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\Bacia_mulugun\hidropixel_files\entrada_hidropixel\entrada_hidropixel\Input_ascii\parametros_e_caract_bacia\hydograph_parameters.txt"
        self.leh_parametros(parametros)
        # precipitacao_distribuida = r"C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\Bacia_mulugun\hidropixel_files\entrada_hidropixel\entrada_hidropixel\Input_ascii\Output_ascii\rainfall_file_rod1.txt"
        precipitacao_distribuida = r"C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\Bacia_mulugun\hidropixel_files\entrada_hidropixel\entrada_hidropixel\Input_ascii\Output_ascii\rainfall_file_minus377mmET.txt"
        self.leh_precip_distribuida(precipitacao_distribuida)
        
        # Processing and wrinting output files
        self.excess_rainfall()    
        print('Writing outputs...')
        # self.escreve_numb_pix_bacia()
        # self.escreve_S_potencial()
        # self.escreve_perdas_ini()
        # self.escreve_precipitacao_total_acum()
        # self.escreve_precipitacao_excedente()
        self.escreve_hietograma_pe()
        end = perf_counter()
        print(f'The processing time was: {(end-start)/60} min')     

    def run_flow_routing(self):
        '''Esta função ordena a execução das funções pertencentes a rotina flow routing'''
        start = perf_counter()
        # Initial configuration
        if self.rdc_vars.unidaderef =='deg':
            # Sistema está em graus, assumindo lat e long: será feita a projeção para metros
            self.global_vars.metro = 0
        else:
            # Sistema está em metros, não é preciso fazer a projeção para metros
            self.global_vars.metro = 1
            
        # Reading input files
        print('Reading input files')
        arquivo_bacia = r"C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\Bacia_mulugun\hidropixel_files\entrada_hidropixel\entrada_hidropixel\Input_bin\bacia_recl.rst"
        self.leh_bacia(arquivo_bacia, 3)
        self.numera_pix_bacia()
        # precipitacao_distribuida = r"C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\Bacia_mulugun\hidropixel_files\entrada_hidropixel\entrada_hidropixel\Input_ascii\Output_ascii\rainfall_file_rod1.txt"
        precipitacao_distribuida = r"C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\Bacia_mulugun\hidropixel_files\entrada_hidropixel\entrada_hidropixel\Input_ascii\Output_ascii\rainfall_file_minus377mmET.txt"
        self.leh_precip_distribuida(precipitacao_distribuida)
        parametros = r"C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\Bacia_mulugun\hidropixel_files\entrada_hidropixel\entrada_hidropixel\Input_ascii\parametros_e_caract_bacia\hydograph_parameters.txt"
        self.leh_parametros(parametros)
        # Processing and wrinting output files
        print('Processing and Writing outputs...')
        self.hidrograma_dlr()
        # self.escreve_vazao_pico_pixel(1)
        # self.escreve_volume_gerado_pixel()
        self.escreve_hidrograma_dlr()
        self.escreve_pe_calculada()
        end = perf_counter()
        print(f'The processing time was: {(end-start)/60} min')
        
    def leh_geotiff_escreve_ascii(self, arquivo, arquivo2, int_float):
        '''Esta função realiza a leitura do arquivo .tif enviado pelo user e o converte em .rst tipo ascii para leitura no visual basic''' 
        dados_lidos = gdal.Open(arquivo)

        # Lendo os dados raster como um array 
        dados_lidos_bacia = dados_lidos.GetRasterBand(1).ReadAsArray()

        # Tratamento de erro: verifica se o arquivo foi aberto corretamente
        if dados_lidos is not None:

            # Obtenção da dimensão da imagem raster
            self.rdc_vars.nlin = dados_lidos.RasterYSize           
            self.rdc_vars.ncol = dados_lidos.RasterXSize
            self.rdc_vars.geotransform = dados_lidos.GetGeoTransform()
            self.rdc_vars.projection = dados_lidos.GetProjection()
        bacia_ascii = np.zeros((self.rdc_vars.nlin,self.rdc_vars.ncol))

        # Leitura do arquivo ascii
        if int_float == 'int':
            with open(arquivo2, 'r') as arquivo_ascii:
                for lin in range(self.rdc_vars.nlin):
                    for col in range(self.rdc_vars.ncol):
                        bacia_ascii[lin,col] = int(arquivo_ascii.readline())

        elif int_float == 'float':
            with open(arquivo2, 'r') as arquivo_ascii:
                for lin in range(self.rdc_vars.nlin):
                    for col in range(self.rdc_vars.ncol):
                        bacia_ascii[lin,col] = float(arquivo_ascii.readline())  

        with open(r"C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\SmallExample\1_TravelTime\Input\drenagem",'w',encoding ='utf-8') as arquivo:
            for lin in range(self.rdc_vars.nlin):
                for col in range(self.rdc_vars.ncol):
                    arquivo_ascii.write(f'{str(int(bacia_ascii[lin,col]))}\n')
        return bacia_ascii, dados_lidos_bacia

    def leh_rst_escreve_geotiff(self, arquivo1, arquivo2, file_type):
        """Esta função lê os arquivos processados nas rotinas em visual basic, no formato .rst(ascii) e os escreve em geotiff (no diretório informado)
            arquivo1 = diretório do arquivo raster tipo rst ascii
            arquivo2 = arquivo raster tiff (será criado)"""

        # Convertendo arquivo ascii para geotiff
        self.rdc_vars.ncol = 1924
        self.rdc_vars.nlin = 962
        rst_to_raster = np.zeros((self.rdc_vars.nlin,self.rdc_vars.ncol))
        cont = 0

        # Leitura do arquivo ascii
        if file_type == 'int':
            with open(arquivo1, 'r') as arquivo_ascii:
                for lin in range(self.rdc_vars.nlin):
                    for col in range(self.rdc_vars.ncol):
                        rst_to_raster[lin,col] = int(arquivo_ascii.readline())
                        cont+=1
        elif file_type == 'float':
            with open(arquivo1, 'r') as arquivo_ascii:
                for lin in range(self.rdc_vars.nlin):
                    for col in range(self.rdc_vars.ncol):
                        rst_to_raster[lin,col] = float(arquivo_ascii.readline())
        if file_type == 'int':
            rst_to_raster = np.loadtxt(arquivo1, dtype=int)
        elif file_type == 'float':
            rst_to_raster = np.loadtxt(arquivo1, dtype=float)
        # Define os dados a serem escritos
        if file_type == 'int':
            tipo_dados = gdalconst.GDT_Int16
        else:
            tipo_dados = gdalconst.GDT_Float32

        # Obtendo o driver para escrita do arquivo em GeoTiff
        fn_geotiff = arquivo2
        driver = gdal.GetDriverByName('GTiff')

        # Cria arquivo final
        dataset = driver.Create(fn_geotiff, self.rdc_vars.ncol, self.rdc_vars.nlin, 1, tipo_dados)
        # dataset.SetGeoTransform(self.rdc_vars.geotransform)
        # dataset.SetProjection(self.rdc_vars.projection)

        # Escreve os dados na banda do arquivo
        banda = dataset.GetRasterBand(1)
        banda.WriteArray(rst_to_raster)

        # Fechando o arquivo
        dataset = None
        banda = None
        driver = None
        tipo_dados = None

        return cont

    def apaga_arquivos_temp(self):
        '''Esta função exclui os arquivos temporários criados durante a execução do plugin'''
        # Muda para o diretório especificado
        os.chdir(self.diretorio_atual + r'\temp')
        # Obtém todos os arquivos com a extensão .txt, .rst, .rdc
        arquivos_txt = glob.glob('*.txt')
        arquivos_rst = glob.glob('*.rst')
        arquivos_rdc = glob.glob('*.rdc')

        # Apaga todos os arquivos .txt
        for txt in arquivos_txt:
            os.remove(txt)

        for rst in arquivos_rst:
            os.remove(rst)

        for rdc in arquivos_rdc:            
            os.remove(rdc)

    def plot_hidrogramas_e_metricas(self):
        """Esta função gera o hidrograma calculado vs observado e adiciona as métricas de comparação"""
        # leh hidrograma observado
        hidrograma_obs = r"C:\Users\joao1\OneDrive\Documentos\arquivos_para_test\input_tif\output\hidrograma.txt"
        cont = 0
        with open(hidrograma_obs,'r',encoding = 'ISO-8859-1') as arquivo_txt:
            cabecalho = arquivo_txt.readline()
            linhas = arquivo_txt.readlines()
            vazoes_obs = np.zeros(len(linhas))
            tempos_obs = np.zeros(len(linhas))

            for linha in linhas:
                tempos_obs[cont] = linha.replace('\n','').split(',')[0]
                vazoes_obs[cont] = linha.replace('\n','').split(',')[1]
                cont+=1
                
        # Determinação do delta_t: deve ser o mesmo para o hidrograma calculado e observado
        delta_t = tempos_obs[2]-tempos_obs[1]
        # delta_t = self.dlg_flow_rout.le_2_pg1.text()

        # leh hidrograma calculado
        cont = 0
        hidrograma_calc = r"C:\Users\joao1\OneDrive\Documentos\arquivos_para_test\input_tif\output\hidrograma3.txt"
        with open(hidrograma_calc,'r',encoding = 'ISO-8859-1') as arquivo_txt:
            cabecalho = arquivo_txt.readline()
            linhas = arquivo_txt.readlines()
            vazoes_calc = np.zeros(len(linhas))
            tempos_calc = np.zeros(len(linhas))

            for linha in linhas:
                tempos_calc[cont] = linha.replace('\n','').split(',')[0]
                vazoes_calc[cont] = float(linha.replace('\n','').split(',')[1])
                cont+=1                

        # Calcula metricas para avaliação do modelo
        er_vazao_pico = ((np.amax(vazoes_calc) - np.amax(vazoes_obs))/np.amax(vazoes_obs))*100 # erro relativo da vazão de pico
        er_tempo_pico = ((tempos_calc[np.argmax(vazoes_calc)] - tempos_obs[np.argmax(vazoes_obs)])/tempos_obs[np.argmax(vazoes_obs)])*100 # erro relativo do tempo de pico
        nse = 1 - (np.sum((vazoes_calc - vazoes_obs) ** 2) / np.sum((vazoes_obs - np.mean(vazoes_obs)) ** 2)) # calculo do coeficiente de Nash-Sutcliffe
        rmse = np.sqrt(np.mean((vazoes_calc - vazoes_obs) ** 2)) # calcula erro medio quadratico
        
        # Calcula volume
        vol_obs = np.sum(vazoes_obs)*delta_t
        vol_calc = np.sum(vazoes_calc)*delta_t
        er_vol = ((vol_calc-vol_obs)/vol_obs)

        # Plotagem dos pontos e do polinomio geral
        plt.figure(figsize=(8, 6))
        plt.gcf().canvas.manager.window.setWindowTitle('Resulting Watershed Hydrograph')
        plt.title('HYDROGRAPH')
        plt.plot(tempos_obs, vazoes_obs,c='black', label="Observed Runoff")
        plt.plot(tempos_obs, vazoes_calc,c='red', label="Calculated Runoff")
        plt.xlabel('time (min)')
        plt.ylabel('Q(m³/s)')
        plt.legend()
        plt.grid()
        # Adicionando as métricas fora do gráfico com ajuste
        plt.figtext(0.1, 0.25, f'RMSE: {rmse:.2f}', fontsize=10)
        plt.figtext(0.1, 0.20, f'NS coefficient: {nse:.2f}', fontsize=10)
        plt.figtext(0.1,0.15, f'relative peak error: {er_vazao_pico:.2f}%', fontsize=10)
        plt.figtext(0.1, 0.10, f'relative time to peak error: {er_tempo_pico:.2f}%', fontsize=10)
        plt.figtext(0.1, 0.05, f'relative volume error: {er_vol:.2f}%', fontsize=10)

        plt.subplots_adjust(bottom=0.40)  # Ajusta a margem inferior para caber o texto
        plt.show()

    def run_22(self):
        '''Verifica possíveis inconsistências'''
        # Leitura do mesmo arquivo (bacia) por dois métodos: leitura do .rst bin; leitura do geotiff (.tif)
        arquivo_bacia_rst = r"C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\Bacia_mulugun\hidropixel_files\entrada_hidropixel\entrada_hidropixel\Input_ascii\arquivo_rodada_1\BACIA_RECL_ASCII.RST"
        arquivo_bacia_tif = r"C:\Users\joao1\OneDrive\Área de Trabalho\Pesquisa\Bacia_mulugun\hidropixel_files\entrada_hidropixel\entrada_hidropixel\bacia.tif"

        bacia_tif = self.leh_rst_escreve_geotiff(arquivo_bacia_rst,arquivo_bacia_tif,'int')

        # comparação do arquivo lido
        print(bacia_tif)

        # # Convertendo arquivo ascii para geotiff
        # fn_bacia_geotiff = r"C:\Users\joao1\OneDrive\Documentos\arquivos_para_test\TravelTime_rst_to_tif.tif"
        # # Define os dados a serem escritos
        # dados_p_acum = bacia_rst
        # tipo_dados = gdalconst.GDT_Float32

        # # Obtendo o driver para escrita do arquivo em GeoTiff
        # driver = gdal.GetDriverByName('GTiff')

        # # Cria arquivo final
        # dataset = driver.Create(fn_bacia_geotiff, self.rdc_vars.ncol, self.rdc_vars.nlin, 1, tipo_dados)
        # dataset.SetGeoTransform(self.rdc_vars.geotransform)
        # dataset.SetProjection(self.rdc_vars.projection)

        # # Escreve os dados na banda do arquivo
        # banda = dataset.GetRasterBand(1)
        # banda.WriteArray(dados_p_acum)

        # # Fechando o arquivo
        # dataset = None
        # banda = None
        # driver = None
        # tipo_dados = None

classe = DesenvolvePlugin()
classe.plot_hidrogramas_e_metricas()
 
