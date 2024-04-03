# Import the code for the dialog
import os.path
import sys, os
import matplotlib.pyplot as plt
import time
# Importing libs
import numpy as np
import matplotlib as plt
from osgeo import ogr, gdal
import matplotlib.pyplot as plt
from pathlib import Path
from modulos_files.RDC_variables import RDCVariables
from modulos_files.global_variables import GlobalVariables


class Test():
    '''
    Criada para testar e desenvolver as funções do módulo hidroPixel
    '''
    def __init__(self):
        # Criando instâncias das classes
        self.global_vars = GlobalVariables()
        self.rdc_vars = RDCVariables()

    def leh_bacia(self):
        self.inicio = time.time()
        """Esta função é utilizada para ler as informações da bacia hidrográfica (arquivo .rst)"""
        arquivo = r"C:\Users\joao1\OneDrive\Área de Trabalho\Calcula_Tc_SCS_decliv_indiv_grandesmatrizes_utm_LL\bacia.rst"
        # Tratamento de erros: verifica se o arquivo foi corretamente enviado
        if arquivo:
            # Realizando a abertura do arquivo raster e coletando as informações referentes as dimensões do mesmo
            rst_file_bacia = gdal.Open(arquivo)

            # Lendo os dados raster como um array 
            dados_lidos_bacia = rst_file_bacia.GetRasterBand(1).ReadAsArray()
            
            # Tratamento de erro: verifica se o arquivo foi aberto corretamente
            if rst_file_bacia is not None:

                # atualizando os valores das variáveis para coletar o número de linhas e colunas do arquivo raster lido
                self.rdc_vars.nlin = rst_file_bacia.RasterYSize               
                self.rdc_vars.ncol = rst_file_bacia.RasterXSize

                # Determinando o numéro de elementos contidos no arquivo raster
                num_elements_bacia = dados_lidos_bacia.size

                # Tratamento de erros: verifica se o número de elementos (pixel) do arquivo está de acordo com as dimensões da matriz da bacia hidrográfica
                if num_elements_bacia != self.rdc_vars.nlin * self.rdc_vars.ncol:
                    result = f"ERROR! As dimensões do arquivo raster ({self.rdc_vars.nlin},{self.rdc_vars.ncol}) são diferentes do número total de \
                        elementos {num_elements_bacia}. Assim, não é possível ler o arquivo raster '{arquivo}' e armazená-lo na matriz destinada."
                    # QMessageBox.warning(None, "ERROR!", result)
                else:
                    # Reorganizando os dados lidos da bacia em uma nova matriz chamada bacia.

                    # global_vars.bacia = dados_lidos_bacia
                    self.global_vars.bacia = dados_lidos_bacia
                    # Fechando o dataset GDAL

                    rst_file_bacia = None
            else:
                """Caso o arquivo raster apresente erros durante a abertura, ocorrerá um erro"""
                resulte = f"Failde to open the raster file: {arquivo}"
                # QMessageBox.warning(None, "ERROR!", resulte)

        else:
            result ="Nenhum arquivo foi selecionado!"
            # QMessageBox.warning(None, "ERROR!", result)
        
        print(f'Qtd pix bacia: {np.count_nonzero(self.global_vars.bacia)}\nPassou bacia')

        
    def leh_caracteristica_dRios(self):
        """Esta função é utilizada para ler as informações acerca da característica dos rios de uma bacia hidrográfica (texto .rst)"""

        # Abrindo o arquivo de texto (.txt) com as informações acerca das classes dos rios
        file = r"C:\Users\joao1\OneDrive\Área de Trabalho\Calcula_Tc_SCS_decliv_indiv_grandesmatrizes_utm_LL\caracteristicas_classes_rios.txt"
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
                indice, Scla, Mann, Rh = map(float, line.split())

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
        """Esta função é utilizada para ler as informações acerca da classe dos rios da bacia hidrográfica (arquivo raster -  .rst)"""
        arquivo = r"C:\Users\joao1\OneDrive\Área de Trabalho\Calcula_Tc_SCS_decliv_indiv_grandesmatrizes_utm_LL\classes_rios.rst"
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

    def leh_direcoes_de_fluxo(self):
        """Esta função é utilizada para ler as informações acerca da direção de escoamento dos rios (arquivo raster - .rst)"""

        # Definindo a numeração das direções &
        # Definindo a posição relativa dos pixels vizinhos
        # lin viz = lin centro + dlin(i)
        # col viz = col centro + dcol(i)

        self.global_vars.dlin = {
                            1: -1,
                            2: 0,
                            4: 1,
                            8: 1,
                            16: 1,
                            32: 0,
                            64: -1,
                            128: -1
                            }
        self.global_vars.dcol = {
                            1: 1,
                            2: 1,
                            4: 1,
                            8: 0,
                            16: -1,
                            32: -1,
                            64: -1,
                            128: 0
                            }

       
        # ATENÇÃO PARA O VALOR NUMÉRICO DAS DIRECÕES
        # ---------------------------------------------------------
        # - G  H  A      ArcView:  32 64 128    MGB-IPH:  64  128  1 -
        # - F  *  B                16  *  1               32   *   2 -
        # - E  D  C                 8  4  2               16   8   4 -

        # Recebendo os arquivos necessários
        self.rdc_vars.nomeRST = r"C:\Users\joao1\OneDrive\Área de Trabalho\Calcula_Tc_SCS_decliv_indiv_grandesmatrizes_utm_LL\dir.rst"
        self.rdc_vars.nomeRDC = r"C:\Users\joao1\OneDrive\Área de Trabalho\Calcula_Tc_SCS_decliv_indiv_grandesmatrizes_utm_LL\dir.RDC"

        # Abrindo o arquivo RDC
        arquivo = self.rdc_vars.nomeRDC
        with open(arquivo, 'r') as rdc_file:
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
                    self.rdc_vars.unidaderef3 = value
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

        # Iniciando a iterações com base nas linhas e colunas
        if self.global_vars.maxdir > 128:
            # Mapeamento das direções de fluxo do tipo idrisi
            idrisi_map = {
                45: 1,
                90: 2,
                135: 4,
                180: 8,
                225: 16,
                270: 32,
                315: 64,
                360: 128
            }
            
            for lin in range(self.rdc_vars.nlin):
                for col in range(self.rdc_vars.ncol):
                    # Verifica se o valor atual da variável maxdir está presente no mapeamento
                    if self.global_vars.direcoes[lin, col] in idrisi_map:
                        # Atualiza o valor do elemento atual da matriz dir de acordo com os novos valores
                        self.global_vars.direcoes[lin, col] = idrisi_map[self.global_vars.direcoes[lin, col]]


        # Tratamento das direções na borda
        self.global_vars.direcoes[0, :] = 128
        self.global_vars.direcoes[-1, :] = 8
        self.global_vars.direcoes[:, 0] = 32
        self.global_vars.direcoes[:, -1] = 2


    def leh_drenagem(self):
        """Esta função é utilizada para ler as informações acerca da drenagem dos rios (arquivo raster - .rst)"""
        # Obtendo o arquivo referente as calasses dos rios da bacia hidrográfica
        arquivo = r'C:\Users\joao1\OneDrive\Área de Trabalho\Calcula_Tc_SCS_decliv_indiv_grandesmatrizes_utm_LL\DRENAGEM.RST'
        # Abrindo o arquivo raster com as informações acerda do sistema de drenagem da bacia hidrográfica
        rst_file_drenagem = gdal.Open(arquivo)
        
        # Lendo os dados raster como um array
        dados_lidos_drenagem = rst_file_drenagem.GetRasterBand(1).ReadAsArray()

        # Tratamento de erros: verifica se o arquivo raster foi aberto corretamente
        if rst_file_drenagem is not None:
            # Reorganizando os dados lidos na matriz destinadas às informações da drenagem da bacia hidrográfica
            self.global_vars.dren = dados_lidos_drenagem
            
            # Fechando o dataset GDAl referente ao arquivo raster
            rst_file_drenagem = None
        else:
            """Caso o arquivo raster apresente erros durante a abertura, ocorrerá um erro"""
            resulte = f"Failde to open the raster file: {arquivo}"
            # QMessageBox.warning(None, "ERROR!", resulte)


    def leh_modelo_numerico_dTerreno(self):
        """Esta função é utilizada para ler as informações acerca do modelo numérico do terreno (arquivo raster - .rst)"""

        # Obtendo o arquivo referente ao MDE da bacia hidrográfica
        arquivo = r'C:\Users\joao1\OneDrive\Área de Trabalho\Calcula_Tc_SCS_decliv_indiv_grandesmatrizes_utm_LL\mntfill.rst'

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
        arquivo = r'C:\Users\joao1\OneDrive\Área de Trabalho\Calcula_Tc_SCS_decliv_indiv_grandesmatrizes_utm_LL\info_P24.txt'

        # lendo os arquivos acerda da precipitação das últimas 24 horas
        with open(arquivo, 'r', encoding = 'utf-8') as arquivo_txt:
            arquivo_txt.readline()
            dados_lidos_P24 = float(arquivo_txt.read()) # considerando que no arquivo só possui um valor de precipitação

        # Armazenando o valor da precipitação de 24 horas em uma variável específica
        self.global_vars.P24 = dados_lidos_P24

    def leh_uso_do_solo(self):
        """Esta função é utilizada para ler as informações acerca do uso do solo (arquivo raster - .rst)"""

        # Obtendo o arquivo raster referente ao uso do solo
        arquivo = r'C:\Users\joao1\OneDrive\Área de Trabalho\Calcula_Tc_SCS_decliv_indiv_grandesmatrizes_utm_LL\uso_solo.RST'

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
        arquivo = r'C:\Users\joao1\OneDrive\Área de Trabalho\Calcula_Tc_SCS_decliv_indiv_grandesmatrizes_utm_LL\relacao_uso_Manning.txt'

        # Criando variável extra, para armazenar os tipos de uso e coeficente de Manning
        uso_manning = []
        coef_maning = []
        uso_manning_val = []
        coef_maning_val = []
        # Abrindo o arquivo que contém o coeficiente de Manning para os diferentes usos do solo
        with open(arquivo, 'r', encoding='utf-8') as arquivo_txt:
        #  Ignora a primeira linha, pois ela contém apenas o cabeçalho
            firt_line = arquivo_txt.readline()
            # Lê as informações de uso do solo e coeficiente de Manning 
            for line in arquivo_txt:
                # Coletando as informações de cada linha
                info = line.strip().split()
                # Armazenando os valores das linhas nas suas respectivas variáveis
                uso_manning = int(info[0])
                coef_maning = float(info[1])

                # Adicionando os valores nas variáveis destinadas
                uso_manning_val = np.append(uso_manning_val, uso_manning)
                coef_maning_val = np.append(coef_maning_val, coef_maning)

        # Adicionando cada valor às suas respectivas variáveis
        self.global_vars.usaux = uso_manning_val
        self.global_vars.Mann = coef_maning_val


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

    def comprimento_acumulado(self,lado):
        """Definir objetivo da função"""
        self.Lfoz = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol), dtype=np.float64)
        self.Lac = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol), dtype=np.float64)
        self.global_vars.lado = lado
        self.global_vars.diagonal = lado*np.sqrt(2.0)
        
        # Iniciando a iteração para varrer todos os elementos da bacia hidrográfica
        for col in range(self.rdc_vars.ncol):
            for lin in range(self.rdc_vars.nlin):
                # Delimitando apenas os elementos que estão presentes na bacia hidrográfica
                if self.global_vars.bacia[lin,col] == 1:
                    # Coletando as informações referentes ao sistema de drenagem da bacia hidrográfica
                    if self.global_vars.dren[lin,col] == 1:
                        self.global_vars.linaux = lin
                        self.global_vars.colaux = col
                        self.global_vars.caminho = 0
                        
                        while self.global_vars.caminho == 0:

                            # Criando condição de parada
                            condicao = self.global_vars.linaux <= 1 or self.global_vars.linaux >= self.rdc_vars.nlin \
                            or self.global_vars.colaux<=1 or self.global_vars.colaux>= self.rdc_vars.ncol \
                            or self.global_vars.bacia[self.global_vars.linaux][self.global_vars.colaux] == 0

                            if condicao:
                                self.global_vars.caminho = 1

                            else:
                                # Continuar caminho: determina a contagem das distâncias projetadas (WGS84) e \
                                # determina as coordenadas verticais do pixel+

                                self.global_vars.Xesq = self.rdc_vars.xmin + (self.global_vars.colaux - 1)*self.global_vars.Xres
                                self.global_vars.Xdir = self.global_vars.Xesq + self.global_vars.Xres
                                self.global_vars.Yinf = self.global_vars.ymax - self.global_vars.linaux*self.global_vars.Yres
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
                                        self.global_vars.auxdist = self.global_vars.dx*self.global_vars.lado

                                    else:
                                        self.global_vars.auxdist = self.global_vars.dx*self.global_vars.diagonal
                                        
                                # Atualizando o comprimento do rio desde o pixel inicial
                                self.global_vars.tamcam += self.global_vars.auxdist
                                self.global_vars.tamfoz = self.global_vars.tamcam

                                # Condição para verificar se o tamanho do rio é maior que o armazenameto do pixel
                                condicao3 = self.global_vars.tamcam > self.Lac[self.global_vars.linaux, self.global_vars.colaux]
                                if condicao3:
                                    # O valor do pixel é armazenado em um novo rio
                                    self.Lac[self.global_vars.linaux, self.global_vars.colaux] = self.global_vars.tamcam
                                
                                # Armazena o pixel contabilizado
                                self.global_vars.linaux2 = self.global_vars.linaux
                                self.global_vars.colaux2 = self.global_vars.colaux

                                # determina o próximo píxel do caminho
                                self.global_vars.diraux = self.global_vars.direcoes[self.global_vars.linaux, self.global_vars.colaux]
                                self.global_vars.linaux += self.global_vars.dlin[self.global_vars.diraux]
                                self.global_vars.colaux += self.global_vars.dcol[self.global_vars.diraux]
                                # JVD: alocação redundante(caminho = 0)
                                self.global_vars.sda = 0

                        # Atulizando a variável lfoz
                        self.Lfoz[lin, col] = self.global_vars.tamfoz
                        
        print('Passou compri_acumulado')

    def numera_pixel(self):
        '''
        Esta função enumera os píxels presentes na rede de drenagem
        '''
        # self.cabeceira = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol), dtype=np.int32)
        self.contadren = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol), dtype=np.float64)
        self.numcabe = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol), dtype=np.float64)
        self.cabeceira = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol))
        self.numcabeaux = 0
        
        # Enumerando os píxels pertencentes à bacia e à rede de drenagem
        pix_bacia_e_dren = (self.global_vars.bacia == 1) & (self.global_vars.dren == 1)

        self.rdc_vars.cont += np.sum(pix_bacia_e_dren)

        self.contadren[pix_bacia_e_dren] = self.rdc_vars.cont

        pixel_dren = np.where(self.global_vars.dren == 1)
        self.lincontadren = np.array(pixel_dren[0])
        self.colcontadren = np.array(pixel_dren[1])


        # Numeração dos píxels internos a bacia: São chamados de cabeceira, pois o caminho do fluxo é iniciado a partir de cada um deles
        for col in range(1, self.rdc_vars.ncol - 1):
            for lin in range(1, self.rdc_vars.nlin - 1):
            
                # Atualizará apenas os píxel que estão na bacia hidrográfica(cabeceira == 1)
                if self.global_vars.bacia[lin][col] == 1:
                    # A priori, todos os píxels serão considerados de cabeceira
                    self.cabeceira[lin][col] = 1
                    # Cria vizinhança 3x3 para estudar a direção de fluxo do píxel central.
                    for linaux in range(lin - 1, lin + 2):
                        for colaux in range(col - 1, col + 2):
                            # Para cada vizinho, verifica a direção de fluxo dela e para qual pixel ele drena
                            self.global_vars.diraux = self.global_vars.direcoes[linaux][colaux]
                            self.global_vars.linaux2 = linaux + self.global_vars.dlin[self.global_vars.diraux]
                            self.global_vars.colaux2 = colaux + self.global_vars.dcol[self.global_vars.diraux]

                            # Se algum vizinho drenar para o central em análise, este não é de cabeceira
                            if self.global_vars.linaux2 == lin and self.global_vars.colaux2 == col:
                                self.cabeceira[lin][col] = 0

                    # Contagem de píxels que são cabeceira
                    if self.cabeceira[lin][col] == 1:
                        self.numcabeaux += 1
                        self.numcabe[lin][col] = self.numcabeaux

        # Atualiza variáveis globais
        self.global_vars.numcabe = self.numcabe
        self.global_vars.Ncabec = self.numcabeaux
        self.fim = time.time()
        print(self.fim - self.inicio)
        print('Passou numera_pix')

    def dist_drenagem(self):
        """Esta funçao determina a distância incremental percorrida pela água na rede de drenagem,
            assim como a declividade pixel a pixel"""

        self.DIST = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol))
        self.pixeldren = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol))
        self.Difcota = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol)) 
        self.DECLIVpixjus = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol))
        self.global_vars.lado = 1
        self.global_vars.diagonal = np.sqrt(2)
        a = 0
        # iterando sobre os elementos do arquivo raster
        for col in range(self.rdc_vars.ncol):
            for lin in range(self.rdc_vars.nlin):
                # Relaizando operações no apenas na região da bacia hidográfica
                if self.global_vars.bacia[lin][col] == 1:
                    self.global_vars.linaux = lin
                    self.global_vars.colaux = col
                    self.global_vars.caminho = 0
                    self.global_vars.tamcam = 0.0

                    if self.global_vars.dren[lin][col] == 1:
                        self.global_vars.caminho = 1

                    else:
                        while self.global_vars.caminho == 0:
                            
                            condicao = (self.global_vars.linaux<= 1
                            or self.global_vars.linaux>=self.rdc_vars.nlin
                            or self.global_vars.colaux<=1 or self.global_vars.colaux>= self.rdc_vars.ncol
                            or self.global_vars.bacia[self.global_vars.linaux][self.global_vars.colaux]==0)

                            # Verificando a resposta da variável condicao
                            if condicao:
                                self.global_vars.caminho = 1
                            
                            else:
                                # Criando a segunda condição: 
                                # valores pertencentes ao sistema de drenagem da bacia
                                condicao2 = self.global_vars.dren[self.global_vars.linaux][self.global_vars.colaux]== 1

                                if condicao2:
                                    # Após alocação do pixel da rede de drenagem: encerra o processo de busca
                                    self.global_vars.caminho = 1
                                    self.DIST[lin][col] = self.global_vars.tamcam
                                    self.pixeldren[lin][col] = self.contadren[self.global_vars.linaux][self.global_vars.colaux]
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
                                    'METRO VARIA COM O ARQUIVO DE ENTRADA, PARA O EXEMPLO ATUAL É IGUAL A 1'
                                    self.global_vars.metro = 1
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
                                        self.Difcota = self.global_vars.MDE[self.global_vars.linaux2][self.global_vars.colaux2] - self.global_vars.MDE[self.global_vars.linaux][self.global_vars.colaux]
                                        self.DECLIVpixjus[self.global_vars.linaux2][self.global_vars.colaux2] = self.Difcota/self.global_vars.Lincr*1000.0
                                        self.global_vars.Streaux = self.DECLIVpixjus[self.global_vars.linaux2][self.global_vars.colaux2]
                                        self.global_vars.Ltreaux = self.global_vars.Lincr
                                        self.global_vars.usaux = self.global_vars.usosolo[self.global_vars.linaux2][self.global_vars.colaux2]
                                        self.global_vars.Smin = 10 #em m/km

                                        if self.global_vars.Streaux < self.global_vars.Smin:
                                            self.global_vars.Streaux = self.global_vars.Smin
                                        
                                        self.global_vars.Smax = 600 #em m/km
                                        if self.global_vars.Streaux > self.global_vars.Smax:
                                            self.global_vars.Streaux = self.global_vars.Smax

                                        # JVD: correção da indexação para o python (inicia no zero)
                                        self.global_vars.TSpix = 5.474 * ((self.global_vars.Mann[self.global_vars.usaux - 1] *self.global_vars.Ltreaux)**0.8) \
                                            / ((self.global_vars.P24**0.5)*((self.global_vars.Streaux/1000.0)**0.4))

        self.fim = time.time()
        print(self.fim - self.inicio)
        print('Passou dist_drenagem')

    def dist_trecho(self):
        ''' Esta função determina o número dos diferentes trechos que existem na bacia hidrográfica estudada'''
        self.global_vars.numtre = 0
        self.global_vars.numtreauxmax = 0
        self.global_vars.Ntre
        self.global_vars.TREpix = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol))
        condicao1 = None
        
        #ARPlidar: loop para contar o número máximo de trechos 
        for col in range(1, self.rdc_vars.ncol):
            for lin in range(1, self.rdc_vars.nlin):

                # Ações realizadas apenas na região da bacia
                if self.global_vars.bacia[lin][col] == 1:

                    # ARPlidar
                    if self.global_vars.numcabe[lin][col] > 0:
                        self.global_vars.numcabeaux = self.global_vars.numcabe[lin][col]
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
        self.fim = time.time()
        print(self.fim - self.inicio)
        self.global_vars.Ntre = self.global_vars.numtreauxmax + 1

        # Percorrendo o caminho desde as cabeceiras e granvando as distâncias relativas de cada trecho de uso do solo contínuo
        self.global_vars.numtre = 0
        self.global_vars.refcabtre = 0
        
        for col in range(self.rdc_vars.ncol):
            for lin in range(self.rdc_vars.nlin):
                # Verificando os elementos da região da bacia
                if self.global_vars.numcabe[lin][col] > 0:
                    self.global_vars.numcabeaux = self.global_vars.numcabe[lin][col]
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
                    self.global_vars.TREpix[self.global_vars.linaux2][self.global_vars.colaux2]

                    while self.global_vars.caminho == 0:
                        self.global_vars.diraux = self.global_vars.direcoes[self.global_vars.linaux][self.global_vars.colaux]
                        self.global_vars.linaux += self.global_vars.dlin[self.global_vars.diraux]
                        self.global_vars.colaux += self.global_vars.dcol[self.global_vars.diraux]

                        if condicao1 or condicao2:
                            '''Verificar as variáveis usadas, há incoerências'''
                            # Mudou o tipo de uso do solo ou alcançou a rede de drenagem,
                            # então terminou o trecho no píxel anterior
                            self.global_vars.numtreaux +=1
                            self.global_vars.numtre[self.global_vars.numtreaux] = self.global_vars.numtreaux
                            self.global_vars.Ltre[self.global_vars.numtreaux][self.global_vars.numtreaux] = self.global_vars.DIST[self.global_vars.linaux3][self.global_vars.colaux3] \
                                                                                                            - self.global_vars.DIST[self.global_vars.linaux][self.global_vars.colaux] 
                            # Grava a distância (DIST) do último píxel do trecho
                            self.global_vars.DISTult[self.global_vars.numtreaux][self.global_vars.numtreaux] = self.global_vars.DIST[self.global_vars.linaux][self.global_vars.colaux]
                            self.global_vars.cotaini[self.global_vars.numtreaux][self.global_vars.numtreaux] = self.global_vars.MDE[self.global_vars.linaux][self.global_vars.colaux]
                            self.global_vars.cotafim = [self.global_vars.numtreaux][self.global_vars.numtreaux] = self.global_vars.MDE[self.global_vars.linaux][self.global_vars.colaux]
                            
                            a1 = (self.global_vars.cotaini[self.global_vars.numtreaux][self.global_vars.numtreaux] - self.global_vars.cotafim[self.global_vars.numtreaux][self.global_vars.numtreaux])
                            b1 = self.global_vars.Ltre[self.global_vars.numtreaux][self.global_vars.numtreaux]*1000.0
                            self.global_vars.Stre[self.global_vars.numtreaux][self.global_vars.numtreaux] = a1 / b1
                            self.global_vars.usotre[self.global_vars.numtreaux][self.global_vars.numtreaux] = self.global_vars.usaux

                            # ARPlidar: adiciona a bacia como condição
                            condicao4 = self.global_vars.dren[self.global_vars.linaux][self.global_vars.colaux] == 1 or self.global_vars.bacia[self.global_vars.linaux][self.global_vars.colaux]
                            if condicao4:
                                self.global_vars.caminho = 1
                                self.global_vars.refcabtre[self.global_vars.linaux3][self.global_vars.colaux3] = self.global_vars.numtreaux
                                self.global_vars.refcabtre[self.global_vars.linaux2][self.global_vars.colaux2] = self.global_vars.numtreaux
                            else:
                                # Vai continuar o cominho, mas em um novo trecho
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

        # Percorre novamente o caminho desde às cabeceiras, gravando distancias relativas de cada pixel dentro de cada trecho de uso do solo continuo 
        self.global_vars.DISTtre = 0
        self.global_vars.CABEpix = 0
        self.global_vars.DECLIVpix = 0

        # Percorrendo os elementos da bacia hidrográfica
        for col in range(self.rdc_vars.ncol):
            for lin in range(self.rdc_vars.nlin):
                # Os cálculos são executados apenas na região da bacia hidrográfica
                if self.global_vars.bacia[lin][col] == 1:
                    # ARPlidar
                    if self.global_vars.numcabe[lin][col] > 0:
                        self.global_vars.numcabeaux = self.global_vars.numcabe[lin][col]
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
                        self.global_vars.DISTtre[self.global_vars.linaux2][self.global_vars.colaux2] = self.global_vars.DIST[lin][col] - self.global_vars.DISTult[self.global_vars.numcabeaux][1]

                        # ARPdecliv: calcula a declividade do píxel relativo ao último píxel do trecho
                        c1 = (self.global_vars.MDE[self.global_vars.linaux2][self.global_vars.colaux2] - self.rdc_vars.cotafim[self.global_vars.numcabeaux][1])
                        d1 = self.global_vars.DISTtre[self.global_vars.linaux2][self.global_vars.colaux2]*1000.0 
                        self.global_vars.DECLIVpix[[self.global_vars.linaux2][self.global_vars.colaux2]] = c1 / d1

                        # Grava qual cabeceira o píxel em questão faz parte
                        self.global_vars.CABEpix[self.global_vars.linaux2][self.global_vars.colaux2] = self.global_vars.numcabeaux

                        while self.global_vars.caminho == 0:
                            self.global_vars.diraux = self.global_vars.direcoes[self.global_vars.linaux][self.global_vars.colaux]
                            self.global_vars.linaux += self.global_vars.dlin[self.global_vars.diraux]
                            self.global_vars.colaux += self.global_vars.dcol[self.global_vars.diraux]
                            
                            if condicao1 or condicao2:
                                # Mudou o tipo de uso do solo ou alcançou a rede de drenagem, 
                                # então terminou um trecho no píxel anterior
                                self.global_vars.numtreaux += 1
                                self.global_vars.numtre[self.global_vars.numtreaux] = self.global_vars.numtreaux
                                
                                # Grava a distância do píxel relativo ao trecho
                                self.global_vars.DISTtre[self.global_vars.linaux][self.global_vars.colaux] = self.global_vars.DIST[self.global_vars.linaux][self.global_vars.colaux] - self.global_vars.DISTult[self.global_vars.numcabeaux][self.global_vars.numcabeaux + 1]

                                self.global_vars.usotre[self.global_vars.numcabeaux][self.global_vars.numcabeaux] = self.global_vars.usaux

                                # ARPlidar: adiciona a bacia hidrográfica como uma condição
                                if self.global_vars.dren[self.global_vars.linaux][self.global_vars.colaux] ==1 or self.global_vars.bacia[self.global_vars.linaux][self.global_vars.colaux] == 0:
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

                                    # Calcula a declividade do píxel relativo ao último píxel do trecho
                                    e1 = self.global_vars.MDE[self.global_vars.linaux2][self.global_vars.colaux2] - self.global_vars.cotafim[self.global_vars.numcabeaux][self.global_vars.numcabeaux + 1] 
                                    f1 = self.global_vars.DISTtre[self.global_vars.linaux2][self.global_vars.colaux2]*1000.0
                                    self.global_vars.DECLIVpix[self.global_vars.linaux2][self.global_vars.colaux2] = e1 / f1

                            else:
                                # Vai continuar caminhando, e grava os valores dos pares (nlin,ncol) do último píxel que passou           
                                self.global_vars.linaux2 = self.global_vars.linaux
                                self.global_vars.colaux2 = self.global_vars.colaux
                                self.global_vars.usaux = self.global_vars.usosolo[self.global_vars.linaux][self.global_vars.colaux]

                                # Grava qual cabeceira o píxel em questão pertence
                                self.global_vars.CABEpix[self.global_vars.linaux2][self.global_vars.colaux2] = self.global_vars.numcabeaux

                                # Grava a DIST do píxel relativo ao trecho
                                self.global_vars.DISTtre[self.global_vars.linaux2][self.global_vars.colaux2] = self.global_vars.DIST[self.global_vars.linaux2][self.global_vars.colaux2] \
                                                                                                               - self.global_vars.DISTult[self.global_vars.numcabeaux][self.global_vars.numcabeaux + 1]

                                # ARPdecliv: Calcula a declividade o píxel relativo ao último píxel do trecho  
                                g1 = self.global_vars.MDE[self.global_vars.linaux2][self.global_vars.colaux2] - self.global_vars.cotafim[self.global_vars.numcabeaux][self.global_vars.numcabeaux + 1]
                                h1 = self.global_vars.DISTtre[self.global_vars.linaux2][self.global_vars.colaux2]*1000.0
                                self.global_vars.DECLIVpix[self.global_vars.linaux2][self.global_vars.colaux2] =  g1/h2
        
        for col in range(self.rdc_vars.ncol):
            for lin in range(self.rdc_vars.nlin):
                # Os cálculo são realizados apenas na região da baica hidrográficia 
                if self.global_vars.bacia[lin][col] == 1:
                    # ARPlidar
                    if self.global_vars.numcabe[lin][col] > 0:
                        self.global_vars.numcabeaux = self.global_vars.numcabe[lin][col]
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
                        self.global_vars.numtreaux2 = 1

                        # Para o cálculo da média aritmética
                        self.global_vars.Somaaux[self.global_vars.numcabeaux][self.global_vars.numcabeaux2] += self.global_vars.DECLIVpix[lin][col]
                        self.global_vars.contaaux[self.global_vars.numcabeaux][self.global_vars.numcabeaux2] = self.global_vars.Somaaux[self.global_vars.numcabeaux][self.global_vars.numcabeaux2] + 1

                        # Para o cálculo da média ponderada
                        self.global_vars.Somaauxpond[self.global_vars.numcabeaux][self.global_vars.numcabeaux2] += self.global_vars.DECLIVpix[lin][col] * self.global_vars.DISTtre[lin][col]
                        self.global_vars.SomaauxDist[self.global_vars.numcabeaux][self.global_vars.numcabeaux2] += self.global_vars.DISTtre[lin][col]

                        while self.global_vars.caminho == 0:
                            self.global_vars.diraux = self.global_vars.direcoes[self.global_vars.linaux][self.global_vars.colaux]
                            self.global_vars.linaux += self.global_vars.dlin[self.global_vars.diraux]
                            self.global_vars.colaux += self.global_vars.dcol[self.global_vars.diraux]
                            

                            if condicao1 or condicao2:
                                # Mudou o tipo de uso do solo ou alcançou a rede de drenagem, 
                                # então terminou um trecho no píxel anterior
                                self.global_vars.numtreaux += 1
                                 # ARPlidar: adiciona a bacia hidrográfica como uma condição
                                if self.global_vars.dren[self.global_vars.linaux][self.global_vars.colaux] == 1 or self.global_vars.bacia[self.global_vars.linaux][self.global_vars.colaux] == 0:
                                    self.global_vars.caminho = 1
                                else:
                                    # Vai continuar o caminho, porém em um novo trecho
                                    self.global_vars.linaux3 = self.global_vars.linaux
                                    self.global_vars.colaux3 = self.global_vars.colaux
                                    self.global_vars.linaux2 = self.global_vars.linaux
                                    self.global_vars.colaux2 = self.global_vars.colaux
                                    self.global_vars.usaux = self.global_vars.usosolo[self.global_vars.linaux][self.global_vars.colaux]

                                    # ARPdecliv: grava qual trecho o píxel em questão pertence
                                    self.global_vars.numtreaux2 += 1

                                    # ARPdecliv: para a média aritmética
                                    self.global_vars.Somaaux[self.global_vars.numcabeaux][self.global_vars.numcabeaux2] += self.global_vars.DECLIVpix[self.global_vars.linaux][self.global_vars.colaux]
                                    self.global_vars.contaaux[self.global_vars.numcabeaux][self.global_vars.numcabeaux2] += 1

                                    # ARPdecliv: para a média ponderada
                                    self.global_vars.Somaauxpond[self.global_vars.numcabeaux][self.global_vars.numcabeaux2] += self.global_vars.DECLIVpix[self.global_vars.linaux][self.global_vars.colaux] * self.global_vars.DISTtre[self.global_vars.linaux][self.global_vars.colaux]
                                    self.global_vars.SomaauxDist[self.global_vars.numcabeaux][self.global_vars.numcabeaux2] += self.global_vars.DISTtre[self.global_vars.linaux][self.global_vars.colaux]
                            
                            else:
                                # Vai continuar caminhando, e grava os valores dos pares (nlin,ncol) do último píxel que passou           
                                self.global_vars.linaux2 = self.global_vars.linaux
                                self.global_vars.colaux2 = self.global_vars.colaux
                                self.global_vars.usaux = self.global_vars.usosolo[self.global_vars.linaux][self.global_vars.colaux]


                                # ARPdecliv: para a média aritmética
                                self.global_vars.Somaaux[self.global_vars.numcabeaux][self.global_vars.numcabeaux2] += self.global_vars.DECLIVpix[self.global_vars.linaux][self.global_vars.colaux]
                                self.global_vars.contaaux[self.global_vars.numcabeaux][self.global_vars.numcabeaux2] += 1

                                # ARPdecliv: para a média ponderada
                                self.global_vars.Somaauxpond[self.global_vars.numcabeaux][self.global_vars.numcabeaux2] += self.global_vars.DECLIVpix[self.global_vars.linaux][self.global_vars.colaux] * self.global_vars.DISTtre[self.global_vars.linaux][self.global_vars.colaux]
                                self.global_vars.SomaauxDist[self.global_vars.numcabeaux][self.global_vars.numcabeaux2] += self.global_vars.DISTtre[self.global_vars.linaux][self.global_vars.colaux]
                            
        # Escrevendo o arquivo de análise dos trechos
        with open('analise_declividades_trechos.txt', 'w') as arquivo_txt:
            # Escrevendo o cabeçalho do arquivo: formatação deve ser precisa!
            arquivo_txt.write('{:<14}{:<14}{:<14}{:<14}{:<14}\n'.format('Num_pixel', 'Num_trecho', 'Decliv_1', 'Decliv_2', 'Decliv_3'))
            
            for self.global_vars.numcabeaux in range(self.global_vars.Ncabec):
                self.global_vars.numcabeaux = self.global_vars.numtre[self.global_vars.numcabeaux]

                for t in range(self.global_vars.numtreaux):
                    self.global_vars.Streaux = self.global_vars.Somaaux[self.global_vars.numcabeaux][t] / self.global_vars.contaaux[self.global_vars.numcabeaux][t]
                    self.global_vars.Streaux2 = self.global_vars.Somaauxpond[self.global_vars.numcabeaux][t] / self.global_vars.SomaauxDist[self.global_vars.numcabeaux][t]
                    # Escrevendo as linhas do arquivo conforme os valores das variáveis
                    arquivo_txt.write('{:<14}{:<14}{:<14.4f}{:<14.4f}{:<14.4f}\n'.format(self.global_vars.numcabeaux, t, self.global_vars.Stre[self.global_vars.numcabeaux][t], self.global_vars.Streaux, self.global_vars.Streaux2))

                    if self.global_vars.tipo_decliv == 3:
                        self.global_vars.Stre[self.global_vars.numcabeaux][t] = self.global_vars.Streaux
                    elif self.global_vars.tipo_decliv == 2:
                        self.global_vars.Stre[self.global_vars.numcabeaux][t] = self.global_vars.Streaux2
                        
        print('Passou dist_trecho')
    def tempo_canal(self):
        '''
        Esta função é responsável por determinar o tempo de derlocamento da foz até o exutório da bacia hidrográfica
        '''
        condicao = None
        condicao2 = None
        self.classerio_aux = np.zeros((self.rdc_vars.nlin,self.rdc_vars.ncol))
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
                                self.global_vars.Lfozaux1 = self.Lfoz[self.global_vars.linaux1][self.global_vars.colaux1]
                                self.global_vars.Lfozaux2 = self.Lfoz[self.global_vars.linaux2][self.global_vars.colaux2]
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
                                    
                                    # Calculando o tempo de deslocamento do percuso em min 
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
                                    self.global_vars.Lfozaux1 = self.Lfoz[self.global_vars.linaux1][self.global_vars.colaux1]
                                    self.global_vars.Lfozaux2 = self.Lfoz[self.global_vars.linaux2][self.global_vars.colaux2]
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
                                        
                                        # Calculando o tempo de deslocamento do percuso em min 
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
    def tempo_sup(self):
        """
        Esta função função determina o tempo de concentração/escoamento para os píxels da superfície da rede de drenagem (aqueles que não são canais)
        """
        for lin in range(self.rdc_vars.nlin):
            for col in range(self.global_vars):
                if self.global_vars.num_elements_bacia[lin][col] > 0:
                    self.global_vars.numcabeaux = self.global_vars.numcabe[lin][col]
                    self.global_vars.lincabe[self.global_vars.numcabeaux] = lin
                    self.global_vars.colcabe[self.global_vars.numcabeaux] = col


        for self.global_vars.numcabeaux in range(self.global_vars.Ncabec):
            self.global_vars.numtreaux = self.global_vars.numtre[self.global_vars.numcabeaux]

            for t in range(self.global_vars.numtreaux):
                self.global_vars.usaux = self.global_vars.numtre[self.global_vars.numcabeaux][t]
                self.global_vars.Ltreaux = self.global_vars.Ltre[self.global_vars.numcabeaux][t]
                self.global_vars.Streaux = self.global_vars.Stre[self.global_vars.numcabeaux][t] 

                if self.global_vars.Streaux > 0:
                    # Determinando o Ts
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
                if self.global_vars.bacia[lin][col]:
                    self.global_vars.numcabeaux = self.global_vars.CABEpix[lin][col]
                    self.global_vars.Taux = 0

                    # Verificando se o píxel é válido e executando cabeceiras
                    if self.global_vars.numcabeaux > 0 or self.global_vars.numcabe[lin][col] == 0:
                        
                        self.global_vars.t = self.global_vars.refcabtre[lin][col]
                        self.global_vars.Ltreaux = self.global_vars.Ltre[self.global_vars.numcabeaux][self.global_vars.t]
                        self.global_vars.Ttreaux = self.global_vars.Ts[self.global_vars.numcabeaux][self.global_vars.t]
                        self.global_vars.DISTtreaux = self.global_vars.DISTtre[lin][col]
                        self.global_vars.Taux = self.global_vars.DISTtreaux * self.global_vars.Ttreaux / self.global_vars.Ltreaux

                        # ARPdecliv
                        if self.global_vars.subtipodecliv == 'b':
                            self.global_vars.Streaux = self.global_vars.Stre(self.global_vars.numcabeaux)[t]
                            self.global_vars.usaux = self.global_vars.usotre
                            
                            if self.global_vars.Streaux > 0:
                                self.global_vars.Taux = 5.474 * ((self.global_vars.Mann[self.global_vars.usaux] * self.global_vars.DISTtreaux)**0.8) / ((self.global_vars.P24**0.5)*((self.global_vars.Streaux / 1000.0)**0.4))
                            else:
                                self.global_vars.Taux

                        self.global_vars.numtreaux = self.global_vars.numtre[self.global_vars.numcabeaux]

                        if self.global_vars.t < self.global_vars.numtreaux:
                            # É preciso calcular o tempo sup(?) dos trechos à jusante
                            tt = self.global_vars.t + 1
                            for tt in range(self.global_vars.numtreaux):
                                self.global_vars.Taux += self.global_vars.Ts[self.global_vars.numcabeaux][tt]
                        
                        self.global_vars.TSnaocabe2d[lin][col] = self.global_vars.Taux

        self.global_vars.TStodos2d = self.global_vars.TSnaocabe2d + self.global_vars.TScabe2d
        if self.global_vars.tipo_decliv == 4:
            # zerando as variáveis usadas
            self.global_vars.TSnaocabe2d = None
            self.global_vars.TStodos2d = None
            self.global_vars.TScabe2d = None
            self.global_vars.TScabe = None

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
                        while caminho == 0:
                            condicao = self.global_vars.linaux <= 1 or self.global_vars.linaux >=self.rdc_vars.nlin or self.global_vars.colaux <= 1 or self.global_vars.colaux >=self.rdc_vars.nlin
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

    def tempo_total(self):
        '''
        Esta função determina o tempo total de escoamento (tempo de concentração) da bacia hidrográfica
        '''
        for col in range(self.rdc_vars.ncol):
            for lin in range(self.rdc_vars.nlin):
                # Os procedimentos são realizados ao longo da bacia hidrográfica
                if self.global_vars.bacia[lin][col] == 1:
                    # Ainda, as verificaçãoes seão baseadas na rede de drenagem
                    if self.global_vars.dren[lin][col] == 1:
                        self.global_vars.TempoTot[lin][col] = self.global_vars.TempoRio[lin][col]
                    else:
                        # ARPlidar
                        self.global_vars.pixel_ref_dren = self.global_vars.pixeldren[lin][col]
                        self.global_vars.ll = self.global_vars.lincontadren[self.global_vars.pixel_ref_dren]
                        self.global_vars.cc = self.global_vars.colcontadren[self.global_vars.pixel_ref_dren]
                        self.global_vars.auxTempoCanal = self.global_vars.TempoRio[self.global_vars.ll][self.global_vars.cc]
                    
                    if global_vars.tipo_decliv == 4:
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

            for col in range(self.rdc_vars.ncol3):
                for lin in range(self.rdc_vars.nlin3):
                    if self.rdc_vars.VarMM3[lin][col][self.rdc_vars.i3] > self.rdc_vars.Varmax:
                        self.rdc_vars.Varmax = self.rdc_vars.VarMM3[lin][col][self.rdc_vars.i3]
                        
                    elif self.rdc_vars.VarMM3[lin][col][self.rdc_vars.i3] < self.rdc_vars.Varmin:
                        self.rdc_vars.Varmin = self.rdc_vars.VarMM3[lin][col][self.rdc_vars.i3]
    
    def tamanho_numero(self, varaux, num):
        '''
        Esta função
        '''
        negativo, nzeros, pp, varaux2, limsup = None
        
        if varaux < 0:
            negativo = 1
        else:
            negativo = 0
        
        varaux2 = np.abs(varaux)
        
        for pp in range(11):
            limsup = 10.0**pp
            if varaux2 < limsup:
                nzeros = pp
                break
        # Se o valor for inteiro
        if num == 1:
            if nzeros == 0:
                tamnum = 1 + negativo
            else:
                self.global_vars.tamnum = nzeros + negativo
        # Se o valor for real
        else:
            if nzeros == 0:
                self.global_vars.tamnum = 8 + 1 + negativo
            else:
                self.global_vars.tamnum = 8 + nzeros + negativo     

        return self.global_vars.tamnum

    def aux_RDC(self, file, textoaux, varaux, tamnum):
        """
        Esta função é responsável por formatar as informações dos arquivos de saida do programa
        """
        if tamnum == 1:
            file.write(f'{textoaux:14s}{varaux:1d}\n')
            return file
        elif tamnum == 2:
            file.write(f'{textoaux:14s}{varaux:2d}\n')
            return file
        elif tamnum == 3:
            file.write(f'{textoaux:14s}{varaux:3d}\n')
            return file
        elif tamnum == 4:
            file.write(f'{textoaux:14s}{varaux:4d}\n')
            return file
        elif tamnum == 5:
            file.write(f'{textoaux:14s}{varaux:5d}\n')
            return file
        elif tamnum == 6:
            file.write(f'{textoaux:14s}{varaux:7d}\n')
            return file
        elif tamnum == 8:
            file.write(f'{textoaux:14s}{varaux:8d}\n')
            return file
        elif tamnum == 9:
            file.write(f'{textoaux:14s}{varaux:9.7f}\n')
            return file
        elif tamnum == 10:
            file.write(f'{textoaux:14s}{varaux:10.7f}\n')
            return file
        elif tamnum == 11:
            file.write(f'{textoaux:14s}{varaux:11.7f}\n')
            return file
        elif tamnum == 12:
            file.write(f'{textoaux:14s}{varaux:12.7f}\n')
            return file
        elif tamnum == 13:
            file.write(f'{textoaux:14s}{varaux:13.7f}\n')
            return file
        elif tamnum == 14:
            file.write(f'{textoaux:14s}{varaux:14.7f}\n')
            return file
        elif tamnum == 15:
            file.write(f'{textoaux:14s}{varaux:15.7f}\n')
            return file
        elif tamnum == 16:
            file.write(f'{textoaux:14s}{varaux:16.7f}\n')
            return file
        elif tamnum == 17:
            file.write(f'{textoaux:14s}{varaux:17.7f}\n')
            return file
        elif tamnum == 18:
            file.write(f'{textoaux:14s}{varaux:18.7f}\n')
            return file
        elif tamnum == 19:
            file.write(f'{textoaux:14s}{varaux:19.7f}\n')
            return file

    def escreve_RDC(self, nome_RST):
        """
        Esta função constrói os arquivos de saída das diferentes funcionalidades do programa
        """
        # Identifica a posição da extensão no arquivo .rst
        pos_ext = nome_RST.find('.rst')

        # Atribui o nome do arquivo .rst ao novo arquivo .rdc
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
            self.aux_RDC(rdc_file, textoaux, self.global_vars.varaux, tamnum)

            # Escreve a linha com o número de linhas
            self.global_vars.varaux = self.rdc_vars.nlin3
            self.rdc_vars.num = 1 # num = 1 : integer
            textoaux = 'rows        : ' 
            tamnum = self.tamanho_numero(self.global_vars.varaux, self.rdc_vars.num)
            self.aux_RDC(rdc_file, textoaux, self.global_vars.varaux, tamnum)

            # Escreve a linha com o sistema de referência
            rdc_file.write(f'ref. system : {self.rdc_vars.sistemaref}\n')

            # Escreve a linha com a unidade de referência
            if self.global_vars.metro == 1:
                rdc_file.write(f'ref. units  : m\n')
            else:
                rdc_file.write(f'ref. units  : deg\n')
            
            # Escreve linha com distância unitária de referência
            rdc_file.write(f'unit dist.  : {1.0:<9.7f}\n')

            # Escreve a linha com o valor mínimo dos dados
            self.global_vars.varaux = self.rdc_vars.Varmin
            self.rdc_vars.num = 2 # num = 2 : real
            textoaux = 'min. value  : '
            tamnum = self.tamnum(self.global_vars.varaux, self.rdc_vars.num)
            self.aux_RDC(rdc_file, testoaux,self.global_vars.varaux, tamnum)

            # Escreve a linha com o valor máximo dos dados
            self.global_vars.varaux = self.rdc_vars.Varmax
            self.rdc_vars.num = 2 # num = 2 : real
            textoaux = 'max. value  : '
            tamnum = self.tamnum(self.global_vars.varaux, self.rdc_vars.num)
            self.aux_RDC(rdc_file, testoaux,self.global_vars.varaux, tamnum)

            # Escreve a linha com o valor mínimo de exebição
            self.global_vars.varaux = self.rdc_vars.Varmin
            self.rdc_vars.num = 2 # num = 2 : real
            textoaux = 'display min : '
            tamnum = self.tamnum(self.global_vars.varaux, self.rdc_vars.num)
            self.aux_RDC(rdc_file, testoaux,self.global_vars.varaux, tamnum) 

            #  Escreve a linha com o valor máximo para exibição 
            self.global_vars.varaux = self.rdc_vars.Varmax
            self.rdc_vars.num = 2 # num = 2 : real
            textoaux = 'display max : '
            tamnum = self.tamnum(self.global_vars.varaux, self.rdc_vars.num)
            self.aux_RDC(rdc_file, testoaux,self.global_vars.varaux, tamnum)

            # Escreve a linha com a unidade dos dados
            rdc_file.write(f'value units : unspecified\n')

            # Escreve a linha com o valor do erro dos dados
            rdc_file.write(f'value error : unknown\n')

            # Escreve a linha com a definição do sinalizador
            rdc_file.write(f'flag value  : {0:1d}\n')

            # Escreve a linha com o número de categorias da legenda
            rdc_file.write(f'legend cats : {0:1d}')

            # Escreve a linha sobre a criação da imagem
            rdc_file.write(f'lineage     : This file was created automatically by an ARP and JVD PYTHON program')
        
        return nome_rdc
    def escreve_comprimento_acumulado(self):
        """
        Esta função é responsável por formular os arquivos de saída (tanto o raster (.rst), quanto sua documentação (.rdc))
        para os dados referentes aos comprimentos da rede de drenagem da bacia hidrográfica
        """

        # Abrindo o arquivo(fn : file name) para escrita dos resultados
        fn_comp_acum = 'ComprimAcu.rst'
        # Possivelmente será alterado, a depender dos resultados das variáveis LAc e Lfoz
        with open(fn_cump_acum, 'wb') as arquivo1:
            # Escrevendo o resultado do comprimento da rede de drenagem
            for lin in range(self.rdc_vars.nlin):
                dados_comp_acum = [float(self.global_vars.LAc[lin][col]) for col in range(self.rdc_vars.ncol)]
                arquivo1.write(dados_comp_acum.tobytes())

        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem
        self.rdc_vars.nlin3 = self.rdc_vars.nlin
        self.rdc_vars.ncol3 = self.rdc_vars.ncol
        self.rdc_vars.tipo_dado = 2
        self.rdc_vars.tipoMM = 2
        self.global_vars.VarMM2 = float(self.global_vars.LAc)
        self.rdc_vars.i3 = 0 
        self.rdc_vars.Xmin3 = self.rdc_vars.xmin
        self.rdc_vars.Xmax3 = self.rdc_vars.xmax
        self.rdc_vars.Ymin3 = self.rdc_vars.ymin
        self.rdc_vars.Ymin3 = self.rdc_vars.ymax
        nomeRST = fn_comp_acum
        self.global_vars.metrordc = self.global_vars.metro
        self.escreve_RDC(nomeRST)

        # Escrevendo o resultado do comprimento da rede de drenagem
        fn_comp_foz = 'ComprimFoz.rst'
        with open(fn_comp_foz, 'wb') as arquivo2:
            for lin in range(self.rdc_vars.nlin):
                dados_comp_foz = [float(self.global_vars.Lfoz[lin][col]) for col in range(self.rdc_vars.ncol)]
                arquivo2.write(dados_comp_foz.tobytes())
        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da foz da bacia hidrográfica
        self.global_vars.VarMM2 = float(self.global_vars.Lfoz)
        nomeRST = fn_comp_foz
        self.escreve_RDC(nomeRST)

    def escreve_conectividade(self):
        """
        Esta função é responsável por formular os arquivos de saída (tanto o raster (.rst), quanto sua documentação (.rdc))
        para os dados referentes ao mapa de conectividade das cabeceiras da bacia hidrográfica
        """
        # Abrindo o arquivo(fn : file name) para escrita dos resultados
        fn_cab_pix = 'CABEpix.rst'
        # Possivelmente será alterado, a depender dos resultados das variáveis LAc e Lfoz
        with open(fn_cump_acum, 'wb') as arquivo1:
            # Escrevendo o resultado do comprimento da rede de drenagem
            for lin in range(self.rdc_vars.nlin):
                dados_cab_pix = [float(self.global_vars.CABEpix[lin][col]) for col in range(self.rdc_vars.ncol)]
                arquivo1.write(dados_cab_pix.tobytes())

        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem
        self.rdc_vars.nlin3 = self.rdc_vars.nlin
        self.rdc_vars.ncol3 = self.rdc_vars.ncol
        self.rdc_vars.tipo_dado = 2
        self.rdc_vars.tipoMM = 2
        self.global_vars.VarMM2 = float(self.global_vars.CABEpix)
        self.rdc_vars.i3 = 0 
        self.rdc_vars.Xmin3 = self.rdc_vars.xmin
        self.rdc_vars.Xmax3 = self.rdc_vars.xmax
        self.rdc_vars.Ymin3 = self.rdc_vars.ymin
        self.rdc_vars.Ymin3 = self.rdc_vars.ymax
        nomeRST = fn_cab_pix
        self.global_vars.metrordc = self.global_vars.metro
        self.escreve_RDC(nomeRST)

        # Escrevendo o resultado do mapa de conectividade dos pixels da superficie a rede de drenagem
        fn_n_conect_dren = 'num_conexao_drenagem.rst'
        with open(fn_comp_foz, 'wb') as arquivo2:
            for lin in range(self.rdc_vars.nlin):
                dados_n_conect_dren = [float(self.global_vars.pixeldren[lin][col]) for col in range(self.rdc_vars.ncol)]
                arquivo2.write(dados_n_conect_dren.tobytes())
        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da foz da bacia hidrográfica
        self.global_vars.VarMM2 = float(self.global_vars.pixeldren)
        nomeRST = fn_n_conect_dren
        self.escreve_RDC(nomeRST)

    def escreve_dados_trecho(self):
        # Esta função escreve os dados de saída referentes aos diferentes trechos dos canais da bacia hidrográfica
        with open('dados_trechos_superf.txt') as arquivo_txt:
            arquivo_txt.write('{:<10}{:<6}{:<6}{:<10}{:<10}{:<12}{:<6}\n'.format('Cabeceira', 'Trecho', 'L(m)', 'Z_ini(m)', 'Z_fim(m)','Decliv(m/km)', 'Uso'))
            
            for self.global_vars.numcabeaux in range(self.global_vars.Ncabec):
                self.global_vars.numcabeaux = self.global_vars.numtre[self.global_vars.numcabeaux]

            for t in range(self.global_vars.numtreaux):
                if self.global_vars.usotre[self.global_vars.numcabeaux][t] == 0:
                        print(f'{t}; {self.global_vars.numcabeaux}  Uso zero')
                        input('Press enter to continue...')
                # Escrevendo as linhas do arquivo conforme os valores das variáveis
                arquivo_txt.write('{:<10}{:<6}{:<10.2f}{:<10.2f}{:<10.2f}{:<12.6f}{:<6}\n'.format(self.global_vars.numcabeaux, t, self.global_vars.Ltre[self.global_vars.numcabeaux][t], self.global_vars.cotaini[self.global_vars.numcabeaux][t], self.global_vars.cotafim[self.global_vars.numcabeaux][t],\
                                                                                    self.global_vars.Stre[self.global_vars.numcabeaux][t],self.global_vars.usotre[self.global_vars.numcabeaux][t]))

    def escreve_declivi_pixel(self):
        '''Esta função gera o mapa de numeração dos pixels da rede de drenagem'''
        # Abrindo o arquivo(fn : file name) para escrita dos resultados
        fn_decli_pix = 'decliv_pixel.rst'
        # Possivelmente será alterado, a depender dos resultados das variáveis LAc e Lfoz
        with open(fn_decli_pix, 'wb') as arquivo1:
            # Escrevendo o resultado do comprimento da rede de drenagem
            for lin in range(self.rdc_vars.nlin):
                dados_decli_pix = [float(self.global_vars.decliv_pixel[lin][col]) for col in range(self.rdc_vars.ncol)]
                arquivo1.write(dados_decli_pix.tobytes())

        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem
        self.rdc_vars.nlin3 = self.rdc_vars.nlin
        self.rdc_vars.ncol3 = self.rdc_vars.ncol
        self.rdc_vars.tipo_dado = 2
        self.rdc_vars.tipoMM = 2
        self.global_vars.VarMM2 = float(self.global_vars.decliv_pixel)
        self.rdc_vars.i3 = 0 
        self.rdc_vars.Xmin3 = self.rdc_vars.xmin
        self.rdc_vars.Xmax3 = self.rdc_vars.xmax
        self.rdc_vars.Ymin3 = self.rdc_vars.ymin
        self.rdc_vars.Ymin3 = self.rdc_vars.ymax
        nomeRST = fn_decli_pix
        self.global_vars.metrordc = self.global_vars.metro
        self.escreve_RDC(nomeRST)

    def escreve_decliv_pixel_jus(self):
        '''Esta função gera o mapa de numeração dos pixels jusantes da rede de drenagem'''
        # Abrindo o arquivo(fn : file name) para escrita dos resultados
        fn_decli_pix_jus = 'decliv_pixel_jus.rst'
        # Possivelmente será alterado, a depender dos resultados das variáveis LAc e Lfoz
        with open(fn_decli_pix_jus, 'wb') as arquivo1:
            # Escrevendo o resultado do comprimento da rede de drenagem
            for lin in range(self.rdc_vars.nlin):
                dados_decli_pix_jus = [float(self.global_vars.decliv_pixel_jus[lin][col]) for col in range(self.rdc_vars.ncol)]
                arquivo1.write(dados_decli_pix_jus.tobytes())

        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem
        self.rdc_vars.nlin3 = self.rdc_vars.nlin
        self.rdc_vars.ncol3 = self.rdc_vars.ncol
        self.rdc_vars.tipo_dado = 2
        self.rdc_vars.tipoMM = 2
        self.global_vars.VarMM2 = float(self.global_vars.decliv_pixel_jus)
        self.rdc_vars.i3 = 0 
        self.rdc_vars.Xmin3 = self.rdc_vars.xmin
        self.rdc_vars.Xmax3 = self.rdc_vars.xmax
        self.rdc_vars.Ymin3 = self.rdc_vars.ymin
        self.rdc_vars.Ymin3 = self.rdc_vars.ymax
        nomeRST = fn_decli_pix_jus
        self.global_vars.metrordc = self.global_vars.metro
        self.escreve_RDC(nomeRST)
    
    def escreve_dist_rel_trechos(self):
        '''Esta função gera o arquivo com as distânicas relativas dentro do trecho'''
        # Abrindo o arquivo(fn : file name) para escrita dos resultados
        fn_dist_rel_tre = 'DISTtre.rst'
        # Possivelmente será alterado, a depender dos resultados das variáveis LAc e Lfoz
        with open(fn_dist_rel_tre, 'wb') as arquivo1:
            # Escrevendo o resultado do comprimento da rede de drenagem
            for lin in range(self.rdc_vars.nlin):
                dados_dist_rel_tre = [float(self.global_vars.DISTtre[lin][col]) for col in range(self.rdc_vars.ncol)]
                arquivo1.write(dados_dist_rel_tre.tobytes())

        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem
        self.rdc_vars.nlin3 = self.rdc_vars.nlin
        self.rdc_vars.ncol3 = self.rdc_vars.ncol
        self.rdc_vars.tipo_dado = 2
        self.rdc_vars.tipoMM = 2
        self.global_vars.VarMM2 = float(self.global_vars.DISTtre)
        self.rdc_vars.i3 = 0 
        self.rdc_vars.Xmin3 = self.rdc_vars.xmin
        self.rdc_vars.Xmax3 = self.rdc_vars.xmax
        self.rdc_vars.Ymin3 = self.rdc_vars.ymin
        self.rdc_vars.Ymin3 = self.rdc_vars.ymax
        nomeRST = fn_dist_rel_tre
        self.global_vars.metrordc = self.global_vars.metro
        self.escreve_RDC(nomeRST)

    def escreve_num_pix_cabec(self):
        '''Esta função escreve a numeração das cabeceiras'''
        # Abrindo o arquivo(fn : file name) para escrita dos resultados
        fn_num_cab = 'NUM_CABECEIRAS.rst'
        # Possivelmente será alterado, a depender dos resultados das variáveis LAc e Lfoz
        with open(fn_num_cab , 'wb') as arquivo1:
            # Escrevendo o resultado do comprimento da rede de drenagem
            for lin in range(self.rdc_vars.nlin):
                dados_num_cab = [float(self.global_vars.numcabe[lin][col]) for col in range(self.rdc_vars.ncol)]
                arquivo1.write(dados_num_cab.tobytes())

        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem
        self.rdc_vars.nlin3 = self.rdc_vars.nlin
        self.rdc_vars.ncol3 = self.rdc_vars.ncol
        self.rdc_vars.tipo_dado = 2
        self.rdc_vars.tipoMM = 2
        self.global_vars.VarMM2 = float(self.global_vars.numcabe)
        self.rdc_vars.i3 = 0 
        self.rdc_vars.Xmin3 = self.rdc_vars.xmin
        self.rdc_vars.Xmax3 = self.rdc_vars.xmax
        self.rdc_vars.Ymin3 = self.rdc_vars.ymin
        self.rdc_vars.Ymin3 = self.rdc_vars.ymax
        nomeRST = fn_num_cab 
        self.global_vars.metrordc = self.global_vars.metro
        self.escreve_RDC(nomeRST)

    def escreve_num_pix_drenagem(self):
        '''Esta função gera o mapa de numeração dos píxels da rede de drenagem'''
        # Abrindo o arquivo(fn : file name) para escrita dos resultados
        fn_num_pix_dren = 'num_pixels_drenagem.rst'
        # Possivelmente será alterado, a depender dos resultados das variáveis LAc e Lfoz
        with open(fn_num_pix_dren, 'wb') as arquivo1:
            # Escrevendo o resultado do comprimento da rede de drenagem
            for lin in range(self.rdc_vars.nlin):
                dados_num_pix_dren = [float(self.global_vars.contadren[lin][col]) for col in range(self.rdc_vars.ncol)]
                arquivo1.write(dados_num_pix_dren.tobytes())

        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem
        self.rdc_vars.nlin3 = self.rdc_vars.nlin
        self.rdc_vars.ncol3 = self.rdc_vars.ncol
        self.rdc_vars.tipo_dado = 1
        self.rdc_vars.tipoMM = 2
        self.global_vars.VarMM2 = float(self.global_vars.contadren)
        self.rdc_vars.i3 = 0 
        self.rdc_vars.Xmin3 = self.rdc_vars.xmin
        self.rdc_vars.Xmax3 = self.rdc_vars.xmax
        self.rdc_vars.Ymin3 = self.rdc_vars.ymin
        self.rdc_vars.Ymin3 = self.rdc_vars.ymax
        nomeRST = fn_num_pix_dren 
        self.global_vars.metrordc = self.global_vars.metro
        self.escreve_RDC(nomeRST)

    def escreve_num_trechos(self):
        '''Esta função escreve a numeração dos trechos'''
        # Abrindo o arquivo(fn : file name) para escrita dos resultados
        fn_num_tre = 'num_pixels_drenagem.rst'
        # Possivelmente será alterado, a depender dos resultados das variáveis LAc e Lfoz
        with open(fn_num_tre, 'wb') as arquivo1:
            # Escrevendo o resultado do comprimento da rede de drenagem
            for lin in range(self.rdc_vars.nlin):
                dados_num_tre = [float(self.global_vars.refcabtre[lin][col]) for col in range(self.rdc_vars.ncol)]
                arquivo1.write(dados_num_tere.tobytes())

        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem
        self.rdc_vars.nlin3 = self.rdc_vars.nlin
        self.rdc_vars.ncol3 = self.rdc_vars.ncol
        self.rdc_vars.tipo_dado = 1
        self.rdc_vars.tipoMM = 2
        self.global_vars.VarMM2 = float(self.global_vars.refcabtre)
        self.rdc_vars.i3 = 0 
        self.rdc_vars.Xmin3 = self.rdc_vars.xmin
        self.rdc_vars.Xmax3 = self.rdc_vars.xmax
        self.rdc_vars.Ymin3 = self.rdc_vars.ymin
        self.rdc_vars.Ymin3 = self.rdc_vars.ymax
        nomeRST = fn_num_tre 
        self.global_vars.metrordc = self.global_vars.metro
        self.escreve_RDC(nomeRST)
    
    def escreve_tempo_canal(self):
        '''Esta função escreve os dados referentes aos cálculos do tempo de concentração para os canais da rede de drenagem da 
            bacia hidrográfica'''
        self.global_vars.TempoRioR = float(self.global_vars.TempoRio)

        # Abrindo o arquivo(fn : file name) para escrita dos resultados
        fn_temp_canal = 'TempoCanal.rst'
        # Possivelmente será alterado, a depender dos resultados das variáveis LAc e Lfoz
        with open(fn_temp_canal, 'wb') as arquivo1:
            # Escrevendo o resultado do comprimento da rede de drenagem
            for lin in range(self.rdc_vars.nlin):
                dados_temp_canal = [float(self.global_vars.TempoRioR[lin][col]) for col in range(self.rdc_vars.ncol)]
                arquivo1.write(dados_temp_canal.tobytes())

        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem
        self.rdc_vars.nlin3 = self.rdc_vars.nlin
        self.rdc_vars.ncol3 = self.rdc_vars.ncol
        self.rdc_vars.tipo_dado = 2
        self.rdc_vars.tipoMM = 2
        self.global_vars.VarMM2 = float(self.global_vars.TempoRioR)
        self.rdc_vars.i3 = 0 
        self.rdc_vars.Xmin3 = self.rdc_vars.xmin
        self.rdc_vars.Xmax3 = self.rdc_vars.xmax
        self.rdc_vars.Ymin3 = self.rdc_vars.ymin
        self.rdc_vars.Ymin3 = self.rdc_vars.ymax
        nomeRST = fn_temp_canal
        self.global_vars.metrordc = self.global_vars.metro
        self.escreve_RDC(nomeRST)

    def escreve_tempo_sup(self):
        '''Esta função constrói o mapa dos tempos de deslocamento da água para os píxel de superfícies'''
        # Abrindo o arquivo(fn : file name) para escrita dos resultados
        fn_temp_sup = 'TempoSup_por_cabeceira.rst'
        with open(fn_temp_sup, 'wb') as arquivo1:
            # Escrevendo o resultado do comprimento da rede de drenagem
            for lin in range(self.rdc_vars.nlin):
                dados_temp_sup = [float(self.global_vars.TScabe2d[lin][col]) for col in range(self.rdc_vars.ncol)]
                arquivo1.write(dados_temp_sup.tobytes())

        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem
        self.rdc_vars.nlin3 = self.rdc_vars.nlin
        self.rdc_vars.ncol3 = self.rdc_vars.ncol
        self.rdc_vars.tipo_dado = 2
        self.rdc_vars.tipoMM = 2
        self.global_vars.VarMM2 = float(self.global_vars.TScabe2d)
        self.rdc_vars.i3 = 0 
        self.rdc_vars.Xmin3 = self.rdc_vars.xmin
        self.rdc_vars.Xmax3 = self.rdc_vars.xmax
        self.rdc_vars.Ymin3 = self.rdc_vars.ymin
        self.rdc_vars.Ymin3 = self.rdc_vars.ymax
        nomeRST = fn_temp_sup
        self.global_vars.metrordc = self.global_vars.metro
        self.escreve_RDC(nomeRST)

        # TempoS de deslocamento no mapa - píxels não fazem parte da cabeceira
        fn_temp_sup_Ncabe = 'TempoSup_nao_de_cabeceira.rst'
        with open(fn_temp_sup_Ncabe, 'wb') as arquivo2:
        # Escrevendo o resultado do comprimento da rede de drenagem
            for lin in range(self.rdc_vars.nlin):
                dados_temp_sup_Ncabe = [float(self.global_vars.TSnaocabe2d[lin][col]) for col in range(self.rdc_vars.ncol)]
                arquivo2.write(dados_temp_sup_Ncabe.tobytes())

        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem    
        self.rdc_vars.tipo_dado = 2
        self.rdc_vars.tipoMM = 2
        self.global_vars.VarMM2 = float(self.global_vars.TSnaocabe2d)   
        nomeRST = fn_temp_sup_Ncab
        self.escreve_RDC(nomeRST)

        # TempoS de deslocamento no mapa - todos os píxels
        fn_temp_sup_td = 'TempoSup_todos.rst'
        with open(fn_temp_sup_td, 'wb') as arquivo3:
        # Escrevendo o resultado do comprimento da rede de drenagem
            for lin in range(self.rdc_vars.nlin):
                dados_temp_sup_td = [float(self.global_vars.TStodos2d[lin][col]) for col in range(self.rdc_vars.ncol)]
                arquivo3.write(dados_temp_sup_td.tobytes())

        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem    
        self.rdc_vars.tipo_dado = 2
        self.rdc_vars.tipoMM = 2
        self.global_vars.VarMM2 = float(self.global_vars.TStodos2d)   
        nomeRST = fn_temp_sup_td
        self.escreve_RDC(nomeRST)

    def escreve_tempo_total(self):
        '''Esta função gera o mapa de conectividade dos píxels de superfície da rede de drenagem'''
        # Abrindo o arquivo(fn : file name) para escrita dos resultados
        fn_temp_total = 'TempoTotal.rst'
        with open(fn_temp_total, 'wb') as arquivo1:
            # Escrevendo o resultado do comprimento da rede de drenagem
            for lin in range(self.rdc_vars.nlin):
                dados_temp_total = [float(self.global_vars.TempoTotal[lin][col]) for col in range(self.rdc_vars.ncol)]
                arquivo1.write(dados_temp_total.tobytes())

        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem
        self.rdc_vars.nlin3 = self.rdc_vars.nlin
        self.rdc_vars.ncol3 = self.rdc_vars.ncol
        self.rdc_vars.tipo_dado = 2
        self.rdc_vars.tipoMM = 2
        self.global_vars.VarMM2 = float(self.global_vars.TempoTotal)
        self.rdc_vars.i3 = 0 
        self.rdc_vars.Xmin3 = self.rdc_vars.xmin
        self.rdc_vars.Xmax3 = self.rdc_vars.xmax
        self.rdc_vars.Ymin3 = self.rdc_vars.ymin
        self.rdc_vars.Ymin3 = self.rdc_vars.ymax
        nomeRST = fn_temp_total
        self.global_vars.metrordc = self.global_vars.metro
        self.escreve_RDC(nomeRST)

    def escreve_tre_cabec(self):
        '''Esta função gera o arquivo que possui as informações acerca dos trechos das cabeceiras'''
        # Abrindo o arquivo(fn : file name) para escrita dos resultados
        fn_tre_cabec = 'relacao_trechos_cabec.txt'
        with open(fn_tre_cabec, 'w') as arquivo_txt:
            arquivo_txt.write('{:<12}{:<12}'.format('Cabeceira', 'Num.trechos'))
            for self.global_vars.numcabeaux in range(self.global_vars.Ncabec):
                arquivo_txt.write(f'{self.global_vars.numcabeaux:12d}{self.global_vars.numtre[self.global_vars.numcabeaux]:12d}')
        return arquivo_txt
    
    def escreve_trecho_pixel(self):
        '''Esta função gera o mapa de conectividade das cabeceiras'''
        # Abrindo o arquivo(fn : file name) para escrita dos resultados
        fn_tre_pix = 'TREpix.rst'
        with open(fn_tre_pix, 'wb') as arquivo1:
            for lin in range(self.global_vars.rdc_vars.nlin):
                dados_tre_pix = [float(self.global_vars.TREpix[lin][col] for col in range(self.rdc_vars.ncol))]
                arquivo1.write(dados_tre_pix.tobytes())
        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem
        self.rdc_vars.nlin3 = self.rdc_vars.nlin
        self.rdc_vars.ncol3 = self.rdc_vars.ncol
        self.rdc_vars.tipo_dado = 1
        self.rdc_vars.tipoMM = 2
        self.global_vars.VarMM2 = float(self.global_vars.TREpix)
        self.rdc_vars.i3 = 0 
        self.rdc_vars.Xmin3 = self.rdc_vars.xmin
        self.rdc_vars.Xmax3 = self.rdc_vars.xmax
        self.rdc_vars.Ymin3 = self.rdc_vars.ymin
        self.rdc_vars.Ymin3 = self.rdc_vars.ymax
        nomeRST = fn_tre_pix
        self.global_vars.metrordc = self.global_vars.metro
        self.escreve_RDC(nomeRST)
    
    def escreve_TS_pix_acum(self):
        '''Esta função gera os arquivos com os resultados para o tempo de concentração/escoamento'''
        # Abrindo o arquivo(fn : file name) para escrita dos resultados
        fn_temp_pix_jus = 'tempo_pixel_jus.rst'
        with open(fn_temp_pix_jus, 'wb') as arquivo1:
            for lin in range(self.global_vars.rdc_vars.nlin):
                dados_temp_pix_jus = [float(self.global_vars.TSpix[lin][col] for col in range(self.rdc_vars.ncol))]
                arquivo1.write(dados_temp_pix_jus.tobytes())
        # Alocando as variáveis para escrita da documentação do arquivo rdc para o comprimento da rede de drenagem
        self.rdc_vars.nlin3 = self.rdc_vars.nlin
        self.rdc_vars.ncol3 = self.rdc_vars.ncol
        self.rdc_vars.tipo_dado = 2
        self.rdc_vars.tipoMM = 2
        self.global_vars.VarMM2 = float(self.global_vars.TSpix)
        self.rdc_vars.i3 = 0 
        self.rdc_vars.Xmin3 = self.rdc_vars.xmin
        self.rdc_vars.Xmax3 = self.rdc_vars.xmax
        self.rdc_vars.Ymin3 = self.rdc_vars.ymin
        self.rdc_vars.Ymin3 = self.rdc_vars.ymax
        nomeRST = fn_temp_pix_jus
        self.global_vars.metrordc = self.global_vars.metro
        self.escreve_RDC(nomeRST)

        fn_temp_pix_jus_acum = 'tempo_pixel_jus_acum.rst'
        with open(fn_temp_pix_jus_acum, 'wb') as arquivo2:
            for lin in range(self.global_vars.rdc_vars.nlin):
                dados_temp_pix_jus_acum = [float(self.global_vars.TSpixacum[lin][col] for col in range(self.rdc_vars.ncol))]
                arquivo2.write(dados_temp_pix_jus_acum.tobytes())

        self.global_vars.VarMM2 = float(self.global_vars.TSpixacum) 
        nomeRST = fn_temp_pix_jus
        self.escreve_RDC(nomeRST)       


cla_test = Test()
cla_test.leh_bacia()
cla_test.leh_caracteristica_dRios()
cla_test.leh_classes_rios()
cla_test.leh_direcoes_de_fluxo()
cla_test.leh_drenagem()
cla_test.leh_modelo_numerico_dTerreno()
cla_test.leh_precipitacao_24h()
cla_test.leh_uso_do_solo()
cla_test.leh_uso_manning()
cla_test.numera_pixel()
# cla_test.comprimento_acumulado(1)
# cla_test.dist_drenagem()
cla_test.dist_trecho()
cla_test.tempo_canal()
cla_test.tempo_sup()
cla_test.tempo_total()
cla_test.min_max()
cla_test.tamanho_numero()
cla_test.escreve_RDC()
cla_test.escreve_comprimento_acumulado()
cla_test.escreve_conectividade()
cla_test.escreve_dados_trecho()
cla_test.escreve_declivi_pixel()
cla_test.escreve_declivi_pixel_jus()
cla_test.escreve_dit_rel_trechos()
cla_test.escreve_num_pix_cabec()
cla_test.escreve_num_pix_drenagem()
cla_test.escreve_num_trechos()
cla_test.escreve_tempo_canal()
cla_test.escreve_tempo_total()
cla_test.escreve_tre_cabec()
cla_test.escreve_trecho_pixel()
cla_test.escreve_TS_pix_acum()



