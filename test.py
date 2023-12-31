# Import the code for the dialog
import os.path
import sys, os

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

        
    def leh_caracteristica_dRios(self):
        """Esta função é utilizada para ler as informações acerca da característica dos rios de uma bacia hidrográfica (texto .rst)"""

        # Abrindo o arquivo de texto (.txt) com as informações acerca das classes dos rios
        file = r"C:\Users\joao1\OneDrive\Área de Trabalho\Calcula_Tc_SCS_decliv_indiv_grandesmatrizes_utm_LL\caracteristicas_classes_rios.txt"
        with open(file, 'r', encoding='utf-8') as arquivo_txt:
            #  Atualizando as variáveis que dependem
            arquivo_txt.readline()
            self.global_vars.nclasses =int(arquivo_txt.readline().strip())
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

        # Definindo a numeração das direções
        self.global_vars.A = 1
        self.global_vars.B = 2
        self.global_vars.C = 4
        self.global_vars.D = 8
        self.global_vars.E = 16
        self.global_vars.F = 32
        self.global_vars.G = 64
        self.global_vars.H = 128

        # Definindo a posição relativa dos pixels vizinhos
        # lin viz = lin centro + dlin(i)
        # col viz = col centro + dcol(i)
        self.global_vars.dlin = [-1, 0, 1, 1, 1, 0, -1, 1]
        self.global_vars.dcol = [1, 1, 1, 0, -1, -1, -1, 0]

       
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
            self.global_vars.direcoes =dados_lidos_direcoes

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

        f = (A - B) / A # Definição do achatamento do elipsóide 
        e2 = (2*f) - (f**2) # Determinando o quadrado da excentricidade
        rn = A / ((1 - e2*(np.sin(ylat)))**0.2) # Determinando o raio da curvatura da Terra na latitude ylat

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

        return self.global_vars.dist_2

    def comprimento_acumulado(self):
        """Definir objetivo da função"""
        self.Lfoz = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol), dtype=np.float64)

        # Iniciando a iteração para varrer todos os elementos da bacia hidrográfica
        for col in range(self.rdc_vars.ncol):
            for lin in range(self.rdc_vars.nlin):
                # Delimitando apenas os elementos que estão presentes na bacia hidrográfica
                if self.global_vars.bacia[lin,col] == 1:
                    # Coletando as informações referentes ao sistema de drenagem da bacia hidrográfica
                    if self.global_vars.dren[lin,col] == 1:
                        self.global_vars.linaux = lin
                        self.global_vars.colaux = col

                        while self.global_vars.caminho == 0:
                            # Criando condição de parada
                            condicao = self.global_vars.linaux < 1 or self.global_vars.linaux > self.rdc_vars.nlin or self.global_vars.colaux < 1 \
                                or self.global_vars.colaux > self.rdc_vars.ncol or self.global_vars.bacia[self.global_vars.linaux, self.global_vars.colaux]==1
                            
                            if condicao:
                                # Se a condição "condicao" for verdadeira, o valor da variável caminho é alterada
                                self.global_vars.caminho = 1

                            else:
                                # Continuar caminho: determina a contagem das distâncias projetadas (WGS84) e \
                                # determina as coordenadas verticais do pixel+
                                self.global_vars.Xesq = self.global_vars.xmin + (self.global_vars.colaux - 1)*self.global_vars.Xres
                                self.global_vars.Xdir = self.global_vars.Xesq + self.global_vars.Xres
                                self.global_vars.Yinf = self.global_vars.ymax - self.global_vars.linaux*self.global_vars.Yres
                                self.global_vars.Ysup = self.global_vars.Yinf + self.global_vars.Yres

                                # Determinando a posição relativa ao pixel anterior
                                condicao2 = self.global_vars.linaux2 == self.global_vars.linaux or self.global_vars.colaux2 == self.global_vars.colaux
                                if condicao2:
                                    if self.global_vars.linaux2 == self.global_vars.linaux:
                                        self.global_vars.tipo = 1 
                                    else:
                                        self.global_vars.tipo = 2
                                else:
                                    self.global_vars.tipo = 3

                                # Deteminando a distância incremental projetada
                                if self.global_vars.metro == 0:
                                    project = self.project(self.global_vars.Xesq, 
                                                           self.global_vars.Xdir, 
                                                           self.global_vars.Ysup, 
                                                           self.global_vars.Yinf, 
                                                           self.global_vars.tipo,
                                                           self.global_vars.auxdist, 
                                                           self.global_vars.lado, 
                                                           self.global_vars.diagonal)
                                else:
                                    if self.global_vars.tipo == 1 or self.global_vars.tipo ==2:
                                        self.global_vars.auxdist = self.global_vars.dx*self.global_vars.lado
                                    else:
                                        self.global_vars.auxdist = self.global_vars.dx*self.global_vars.diagonal
                                
                                # Atualizando o comprimento do rio desde o pixel inicial
                                self.global_vars.tamcam += self.global_vars.auxdist
                                self.global_vars.tamfoz = self.global_vars.tamcam

                                # Condição para verificar se o tamanho do rio é mair que o armazenameto do pixel
                                condicao3 = self.global_vars.tamcam > self.global_vars.Lac[self.global_vars.linaux, self.global_vars.colaux]
                                if condicao3:
                                    # O valor do pixel é armazenado em um novo rio
                                    self.global_vars.Lac[self.global_vars.linaux, self.global_vars.colaux] = self.global_vars.tamcam
                                
                                # Armazena o pixel contabilizado
                                self.global_vars.linaux2 = self.global_vars.linaux
                                self.global_vars.colaux2 = self.global_vars.colaux

                                # determina o próximo píxel do caminho
                                self.global_vars.diraux = self.global_vars.dren[self.global_vars.linaux, self.global_vars.colaux]
                                self.global_vars.caminho = 0
                                self.global_vars.linaux += self.global_vars.dlin[self.global_vars.diraux]
                                self.global_vars.colaux += self.global_vars.dcol[self.global_vars.diraux] 
                                self.global_vars.sda = 0

                        # Atulizando a variável lfoz
                        self.Lfoz[lin, col] = self.global_vars.tamfoz

    def numera_pixel(self):
        '''
        Esta função enumera os píxels presentes na rede de drenagem
        '''
        self.lincontadren = np.zeros(self.global_vars.dren.shape[0], dtype=np.int16)
        self.colcontadren = np.zeros(self.global_vars.dren.shape[1], dtype=np.int16)
        self.cabeceira = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol), dtype=np.int32)
        guarda_numLinha = []
        cont = 0
        # loop para numerar os píxels pertencentes à rede de drenagem
        for lin in range(self.rdc_vars.nlin):
            for col in range(self.rdc_vars.ncol):
                # As operações serão executadas apenas na região da bacia hidrográfica
                if self.global_vars.bacia[lin][col] == 1:
                    # Iterando sob a rede de drenagem da bacia hidrográfica
                    if self.global_vars.dren[lin][col] == 1:
                        self.rdc_vars.cont += 1

        # ARPlidar: loop extra para guardar lincontadren e colcontradren
        for lin in range(self.rdc_vars.nlin):
            for col in range(self.rdc_vars.ncol):
                # As operações serão executadas apenas na região da bacia hidrográfica
                if self.global_vars.bacia[lin][col] == 1:
                    # Iterando sob a rede de drenagem da bacia hidrográfica
                    if self.global_vars.dren[lin][col] == 1:
                        self.rdc_vars.cont1 += 1
                        self.contadren[lin][col] = self.rdc_vars.cont1

                        # ARPlidar: guarda lin e col desse em funcao do numero do pixel da drenagem
                        # (para otimizar calculo TempoTotal)
                        self.lincontadren[lin] = lin
                        self.colcontadren[col] = col

        # Nomeração dos píxels internos a bacia: 
        # São chamados de cabeceira, pois o caminho do fluxo iniciado 
        # a partir de cada um deles é anaisado posteriormente
        for lin in range(1, self.rdc_vars.nlin - 1):
            for col in range(1, self.rdc_vars.ncol - 1):
                # Iterando apenas na região da bacia hidrográfica
                if self.global_vars.bacia[lin][col] == 1:
                    # A principio, é cabeceira
                    self.cabeceira[lin][col] == 1
                    
                    # Loop na vizinha 3x3
                    for linauxi in range(lin - 1, lin + 1):
                        for colauxi in range(col - 1, col + 1):
                            # Para cada vizinho, vê a direção de fluxo dele e
                            # para qual pixel ele drena
                            self.global_vars.diraux = self.global_vars.direcoes[linauxi][colauxi]
                            self.global_vars.linaux2 = linauxi + self.global_vars.dlin[self.global_vars.diraux]
                            self.global_vars.colaux2 = colauxi + self.global_vars.dcol[self.global_vars.diraux]
                            
                            # Caso algum vizinho drenar para o pixel central em análise, 
                            # ele não é de cabeceira
                            if self.global_vars.linaux2 == lin and self.global_vars.colaux2 == col:
                                self.global_vars.cabeceira[lin][col] = 0

                    if self.global_vars.cabeceira[lin][col] == 1:
                        self.global_vars.numcabeaux += 1
                        self.global_vars.numcabe[lin][col] = self.global_vars.numcabeaux
        print(self.cabeceira)                
        self.global_vars.Ncabec = self.global_vars.numcabeaux

    def dist_drenagem(self):
        """Definir objetivo da função"""
        self.contadren = np.zeros((self.rdc_vars.nlin, self.rdc_vars.ncol), dtype=np.float64)
        # iterando sobre os elementos do arquivo raster
        for col in range(self.rdc_vars.ncol):
            if col % 50 == 0:
                print(f'col = {col}')
    
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
                            condicao = self.global_vars.linaux<= 1 or self.global_vars.linaux>=self.rdc_vars.nlin \
                            or self.global_vars.colaux<=1 or self.global_vars.colaux>= self.rdc_vars.ncol \
                            or self.global_vars.bacia[self.global_vars.linaux][self.global_vars.colaux]

                            # Verificando a resposta da variável condicao
                            if condicao:
                                self.global_vars.caminho = 1
                            
                            else:
                                # Criando a segunda condição: 
                                # valores pertencentes ao sistema de drenagem da bacia
                                condicao2 = self.global_vars.dren[self.global_vars.linaux][self.global_vars.colaux]==1
                                if condicao2:
                                    # Após alocação do pixel da rede de drenagem: encerra o processo de busca
                                    self.global_vars.caminho = 1
                                    self.global_vars.DIST[lin][col] = self.global_vars.tamcam
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
                                    self.global_vars.Xesq = self.global_vars.xmin + (self.global_vars.colaux2 - 1)*self.global_vars.Xres
                                    self.global_vars.Xdir = self.global_vars.Xesq + self.global_vars.Xres
                                    self.global_vars.Yinf = self.global_vars.ymax - self.global_vars.linaux2 * self.global_vars.Yres
                                    self.global_vars.Ysup = self.global_vars.Yinf + self.global_vars.Yres

                                    # Determina a posição relativa ao píxel anterior
                                    condicao3 = self.global_vars.linaux2 == self.global_vars.linaux or self.global_vars.colaux2 == self.global_vars.colaux
                                    if condicao3:
                                        if self.global_vars.linaux2 == self.global_vars.linaux:
                                            self.global_vars.tipo = 1
                                        else:
                                            self.global_vars.tipo = 2
                                    else:
                                        self.global_vars.tipo = 3

                                    # Determinando a distância incremental projetada
                                    if self.global_vars.metro == 1:
                                        project = self.project(self.global_vars.Xesq,
                                                           self.global_vars.Xdir,
                                                           self.global_vars.Ysup,
                                                           self.global_vars.Yinf,
                                                           self.global_vars.tipo,
                                                           self.global_vars.auxdist,
                                                           self.global_vars.lado,
                                                           self.global_vars.diagonal)
                                    else:
                                        condicao4 = self.global_vars.tipo == 1 or self.global_vars.tipo == 2
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

                                        self.global_vars.TSpix = 5.474 * ((self.global_vars.Mann[self.global_vars.usaux] *self.global_vars.Ltreaux)**0.8) \
                                            / ((self.global_vars.P24**0.5)*((self.global_vars.Streaux/1000.0)**0.4))

    def dist_trecho(self):
        ''' Definir o objetivo da função'''
        self.global_vars.numtre = 0
        self.global_vars.numtreauxmax = 0
        condicao1 = None
        
        #ARPlidar: loop para contar o número máximo de trechos 
        for col in range(1, self.rdc_vars.ncol -1 ):
            for lin in range(1, self.rdc_vars.nlin - 1):
                # Ações realizadas apenas na região da bacia
                if self.global_vars.bacia == 1:
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
                        # Grava qual treco o píxel em questão pertence
                        self.global_vars.numtreaux2 = 1

                        while self.global_vars.caminho == 0:
                            self.global_vars.diraux = self.global_vars.direcoes[lin][col]
                            self.global_vars.linaux += self.global_vars.dlin[self.global_vars.diraux]
                            self.global_vars.colaux += self.global_vars.dcol[self.global_vars.diraux]

                            condicao1 = self.global_vars.usaux != self.global_vars.usosolo[self.global_vars.linaux][self.global_vars.colaux]
                            condicao2 = self.global_vars.dren[self.global_vars.linaux][self.global_vars.colaux] == 1
                           
                            if condicao1 or condicao2:
                                # Mudou o uso do solo ou alcançou a rede de drengem, 
                                # então terminou um trecho no píxel anterior
                                self.global_vars.numtreaux += 1
                                if self.global_vars.numtreaux > self.global_vars.numtreauxmax:
                                    self.global_vars.numtreauxmax = self.global_vars.numtreaux
                                # ARPlidar: incluindo o teste da bacia
                                condicao3 = self.global_vars.dren[self.global_vars.linaux][self.global_vars.colaux] == 1 or self.global_vars.bacia[self.global_vars.linaux][self.global_vars.colaux]
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
        
        self.global_vars.Ntre = self.global_vars.numtreaux + 1
        # Percorrendo o caminho desde as cabeceiras e granvando as distâncias relativas de cada trecho de uso do solo contínuo
        self.global_vars.numtre = 0
        self.global_vars.refcabtre = 0
        
        for col in range(1, self.rdc_vars.ncol - 1):
            if col % 50 == 0:
                print(col)
            for lin in range(1, self.rdc_vars.nlin -1):
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
                        self.global_vars.diraux = self.global_vars.direcoes[lin][col]
                        self.global_vars.linaux += self.global_vars.dlin[self.global_vars.diraux]
                        self.global_vars.colaux += self.global_vars.dcol[self.global_vars.diraux]

                        if condicao1 or condicao2:
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
        for col in range(1, self.rdc_vars.ncol - 1):
            if col % 50 == 0:
                print(Col)
            for lin in range(self.rdc_vars.nlin - 1):
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
                                if self.global_vars.dren[self.global_vars.linaux][self.global_vars.colaux] ==1 or self.global_vars.bacia[self.global_vars.linaux][self.global_vars.colaux] == 1:
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
        
        for col in range(1, self.rdc_vars.ncol - 1):
            if col % 50 == 0:
                print(f'col = {col}')
            for lin in range(1, self.global_vars.nlin - 1):
                # Os cálculo são realizados apenas na região da baica hidrográficia 
                if self.global_vars.bacia[lin][col] == 1:
                    # ARPlidar
                    if self.global_vars.numcabe[lin][col] > 0:
                        self.global_vars.numcabeaux = self.global_vars.numcabe[lin][col]
                        if self.global_vars.numcabeaux == 1882:
                            print(self.global_vars.numcabeaux)
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
                        self.global_vars.Somaaux[self.global_variables.numcabeaux][self.global_variables.numcabeaux2] += self.global_vars.DECLIVpix[lin][col]
                        self.global_vars.contaaux[self.global_variables.numcabeaux][self.global_variables.numcabeaux2] = self.global_vars.Somaaux[self.global_variables.numcabeaux][self.global_variables.numcabeaux2] + 1

                        # Para o cálculo da média ponderada
                        self.global_vars.Somaauxpond[self.global_variables.numcabeaux][self.global_variables.numcabeaux2] += self.global_vars.DECLIVpix[lin][col] * self.global_vars.DISTtre[lin][col]
                        self.global_vars.SomaauxDist[self.global_variables.numcabeaux][self.global_variables.numcabeaux2] += self.global_vars.DISTtre[lin][col]

                        while self.global_vars.caminho == 0:
                            self.global_vars.diraux = self.global_vars.direcoes[self.global_vars.linaux][self.global_vars.colaux]
                            self.global_vars.linaux += self.global_vars.dlin[self.global_vars.diraux]
                            self.global_vars.colaux += self.global_vars.dcol[self.global_vars.diraux]
                            

                            if condicao1 or condicao2:
                                # Mudou o tipo de uso do solo ou alcançou a rede de drenagem, 
                                # então terminou um trecho no píxel anterior
                                self.global_vars.numtreaux += 1
                                 # ARPlidar: adiciona a bacia hidrográfica como uma condição
                                if self.global_vars.dren[self.global_vars.linaux][self.global_vars.colaux] ==1 or self.global_vars.bacia[self.global_vars.linaux][self.global_vars.colaux] == 1:
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
            # Escrevendo o cabeçalho do arquivo
            arquivo_txt.white('{:<14}{:<14}{:<14}{:<14}{:<14}\n'.format('Num_pixel', 'Num_trecho', 'Decliv_1', 'Decliv_2', 'Decliv_3'))
            
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
    
    def tempo_canal(self):
        '''
        Esta função é responsável por determinar o tempo de derlocamento da foz até o exutório da bacia hidrográfica
        '''
        condicao = None
        condicao2 = None
        self.classerio_aux = np.zeros((self.rdc_vars.nlin,self.rdc_vars.ncol))
        for col in range(self.rdc_vars.ncol):
            if col  % 50 == 0:
                print(f'col = {col}')
            for lin in range(self.rdc_vars.nlin):
                # O cáclulos são executados apenas na região da bacia
                if self.global_vars.bacia[lin][col] == 1:
                    # ainda, os cálculos acontecerão na rede de drenagem da bacia hidrográfica
                    if  self.global_vars.dren[lin][col] == 1:
                        self.global_vars.linaux = lin
                        self.global_vars.colaux = col
                        self.global_vars.linaux2 = lin
                        self.global_vars.colaux2 = col
                        self.global_vars.linaux3 = lin
                        self.global_vars.colaux3 = col
                        self.global_vars.caminho = 0
                        self.global_vars.Tempoauxac = 0

                        # Guarda as características do tipo de trecho que o píxel em questão faz parte
                        self.classerio_aux = self.global_vars.classerio[lin][col]

                        while self.global_vars.caminho == 0:
                            condicao = self.global_vars.linaux < 1 or self.global_vars.linaux > self.global_vars.nlin or self.global_vars.colaux < 1 or self.global_vars.colaux > self.global_vars.ncol    
                            
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
                                if  condicao2:
                                    self.global_vars.Lfozaux1 = self.global_vars.Lfoz[self.global_vars.linaux1][self.global_vars.colaux1]
                                    self.global_vars.Lfozaux2 = self.global_vars.Lfoz[self.global_vars.linaux2][self.global_vars.colaux2]
                                    # Determina a diferença entre o píxel do Lfoz inicial e o do final
                                    self.global_vars.Laux = self.global_vars.Lfozaux1 - self.global_vars.Lfozaux2
                                    
                                    # A declividade(Saux), o coeficiente de Manning(naux) e o raio hidráulico(Rhaux) são aqueles do tipo de rio (rede de drenagem)
                                    self.global_vars.Saux = self.global_vars.Sclasse[self.classerio_aux]
                                    self.global_vars.naux = self.global_vars.Mannclasse[self.classerio_aux]
                                    self.global_vars.Rhaux = self.global_vars.Rhclasse[self.classerio_aux]

                                    # Determinando a velocidade do percurso
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
        Esta função função determina o tempo sup(?)
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
            if lin % 50 == 0:
                print(f'lin = {lin}')
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
                if col % 50 == 0:
                    print(f'col = {col}')
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
            if col % 50 == 0:
                print(f'col = {col}')
            
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
            for col in range(self.rdc_vars.ncol):
                for lin in range(self.rdc_vars.nlin):
                    if self.rdc_vars.VarMM2[lin][col] > self.rdc_vars.Varmax:
                        self.rdc_vars.Varmax = self.rdc_vars.VarMM2[lin][col]
                    
                    elif self.rdc_vars.VarMM2[lin][col] < self.rdc_vars.Varmin:
                        self.rdc_vars.Varmin = self.rdc_vars.VarMM2[lin][col]

            for col in range(self.rdc_vars.ncol):
                for lin in range(self.rdc_vars.nlin):
                    if self.rdc_vars.VarMM3[lin][col][self.rdc_vars.i3] > self.rdc_vars.Varmax:
                        self.rdc_vars.Varmax = self.rdc_vars.VarMM3[lin][col][self.rdc_vars.i3]
                        
                    elif self.rdc_vars.VarMM3[lin][col][self.rdc_vars.i3] < self.rdc_vars.Varmin:
                        self.rdc_vars.Varmin = self.rdc_vars.VarMM3[lin][col][self.rdc_vars.i3]
    
    def tamanho_numero(self):
        '''
        Esta função
        '''
        negativo, nzeros, pp, varaux2, limsup = None
        
        if self.global_vars.varaux < 0:
            negativo = 1
        else:
            negativo = 0
        
        varaux2 = np.abs(self.global_vars.varaux)
        
        for pp in range(11):
            limsup = 10.0**pp
            if varaux2 < limsup:
                nzeros = pp
                break
        # Se o valor for inteiro
        if self.rdc_vars == 1:
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
cla_test.comprimento_acumulado()
cla_test.dist_drenagem()
cla_test.numera_pixel()
