"""
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ MODULE FOR CREATION OF GENERAL VARIABLES \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

Objective: This file is responsible for creating the general variables necessary for the Hidropixel Plugin operation.
Author: João Vitor Dias
Supervisor: Adriano Rolim
Date of last update: 30/11/2023
"""
# IMPORTING 
import numpy as np

class GlobalVariables:
    """
    This class is responsible for creating the general variables necessary for the Hidropixel Plugin operation.
    """
    def __init__(self,nlin,ncol):
        """
        This method is responsible for creating the general variables necessary for the Hidropixel Plugin operation.
        """
        # Matrix's declaration
        self.direcoes = np.empty((nlin,ncol), dtype = np.int16)
        self.dren = np.empty((nlin,ncol), dtype = np.int16)   
        self.MDEint = np.empty((nlin,ncol), dtype = np.int16)
        self.cabeceira = np.empty((nlin,ncol), dtype = np.int16)
        self.bacia = np.empty((nlin,ncol), dtype = np.int16)
        self.classerio = np.empty((nlin,ncol), dtype = np.int16)
        self.decliv_pixel = np.empty((nlin,ncol), dtype = np.int16)
        self.decliv_pixel_jus = np.empty((nlin,ncol), dtype = np.int16)
        self.usosolo = np.empty((nlin,ncol), dtype = np.int16)
        self.refcabtre = np.empty((nlin,ncol), dtype = np.int16)
        self.pixeldren = np.empty((nlin,ncol), dtype = np.int16)
        self.contaaux = np.empty((nlin,ncol))
        self.TREpix = np.empty((nlin,ncol), dtype = np.int16)
        self.CABEpix = np.empty((nlin,ncol), dtype = np.float16)
        self.numcabe = np.empty((nlin,ncol), dtype = np.float16)
        self.MEDreal = np.empty((nlin,ncol))
        self.MDE = np.empty((nlin,ncol), dtype = np.float64)
        self.DIST = np.empty((nlin,ncol), dtype = np.float64) # !
        self.DISTtre = np.empty((nlin,ncol), dtype = np.float64)# !
        self.DISTult = np.empty((nlin,ncol), dtype = np.float64)# !
        self.TS = np.empty((nlin,ncol), dtype = np.float64)
        self.TScabe = np.empty((nlin,ncol), dtype = np.float64)
        self.TScabe2d = np.empty((nlin,ncol), dtype = np.float64)
        self.TSnaocabe2d = np.empty((nlin,ncol), dtype = np.float64)
        self.TStodos2d = np.empty((nlin,ncol), dtype = np.float64)
        self.contadren = np.empty((nlin,ncol), dtype = np.float16)
        self.TempoRio = np.empty((nlin,ncol), dtype = np.float64)
        self.TempoRioR = np.empty((nlin,ncol), dtype = np.float64)
        self.Lac = np.empty((nlin,ncol), dtype = np.float64)
        self.Lfoz = np.empty((nlin,ncol), dtype = np.float64)
        self.TempoTot = np.empty((nlin,ncol), dtype = np.float64)
        self.DECLIVpix = np.empty((nlin,ncol), dtype = np.float64)
        self.Somaaux = np.empty((nlin,ncol), dtype = np.float64)
        self.Somaauxpond = np.empty((nlin,ncol), dtype = np.float64)
        self.SomaauxDist = np.empty((nlin,ncol), dtype = np.float64)
        self.DECLIVpixjus = np.empty((nlin,ncol),dtype = np.float64)
        self.TSpix = np.empty((nlin,ncol), dtype = np.float64)
        self.TSpixacum = np.empty((nlin,ncol), dtype = np.float64)
        self.Ltre = np.empty((nlin,ncol), dtype = np.float64)
        self.cotaini = np.empty((nlin,ncol), dtype = np.float64)
        self.cotafim = np.empty((nlin,ncol), dtype = np.float64)
        self.Stre = np.empty((nlin,ncol), dtype = np.float64)
        self.usotre = np.empty((nlin,ncol), dtype = np.float64)
        self.contaaux = np.empty((nlin,ncol), dtype = np.float64)
        self.delimitaBacia = np.zeros((nlin,ncol))
        self.TempoTotal_reclass = np.zeros((nlin,ncol))
        self.Spotencial = np.zeros((nlin,ncol))
        self.perdas_iniciais = np.zeros((nlin,ncol))
        self.chuva_acumulada_pixel = np.zeros((nlin,ncol))
        self.chuva_total_pixel = np.zeros((nlin,ncol))
        self.CN = np.zeros((nlin,ncol))
        self.reservoir = np.zeros((nlin,ncol))
        self.dren_area = np.zeros((nlin,ncol))
        self.coef_k_pixel = np.zeros((nlin,ncol))
        self.tempo_viagem_tot = np.zeros((nlin,ncol)) # da versão nova
        self.tempo_viagem = np.zeros((nlin,ncol)) # da versão nova
        self.nSolo = np.zeros((nlin,ncol))
        self.comp_pixel = np.zeros((nlin,ncol))
        self.divisao_trecho = np.zeros((nlin,ncol))
        self.comp_total = np.zeros((nlin,ncol))
        self.Seq = np.zeros((nlin,ncol))
        self.area_molhada = np.zeros((nlin,ncol))
        self.bankfull_width = np.zeros((nlin,ncol))
        self.rh_medio = np.zeros((nlin,ncol))
        self.tipo_escoamento = np.zeros((nlin,ncol))
        self.ttotal = np.zeros((nlin,ncol))
        self.tempo_total = np.zeros((nlin,ncol))
        self.classerio_aux = np.zeros((nlin,ncol))

        # vector's declaration
        self.lincontadren =  np.empty([], dtype = np.int16)
        self.colcontadren =  np.empty([], dtype = np.int16)
        self.lincabe = np.empty([], dtype = np.int16)
        self.colcabe = np.empty([], dtype = np.int16)
        self.Sclasse = np.empty([], dtype = np.int16)
        self.usaux = np.empty([], dtype = np.int16)
        self.uso_mann = np.empty([], dtype = np.int16)
        self.usaux2 = np.empty([], dtype = np.int16)
        self.Mann = np.empty([], dtype = np.int16)
        self.Mannclasse = np.empty([], dtype = np.int16)
        self.Rhclasse = np.empty([], dtype = np.int16)
        self.numtre = np.empty([], dtype = np.int16)
        self.dlin = np.empty((128), dtype = int)
        self.dcol = np.empty((128), dtype = int)
        self.tempo_intervalo = np.zeros((nlin*ncol))
        self.time = np.zeros((nlin*ncol))
        self.hacum = np.zeros((nlin*ncol))
        self.vazao_pixel = np.zeros((nlin*ncol))
        self.tempo_vazao_pixel = np.zeros((nlin*ncol))
        self.tempo_vazao = np.zeros((nlin*ncol))
        self.vazao_amortecida_pixel = np.zeros((nlin*ncol))
        self.vazao = np.zeros((nlin*ncol))
        self.coef_K = np.zeros((nlin*ncol))
        self.id_trechos = np.zeros((nlin*ncol))
        self.tempo_viagem_pixel = np.zeros((nlin*ncol))

        # string's declaration
        self.subtipodecliv = ""
        self.unidaderef3 = ""

        # Int's variables declaration
        self.linaux = 0
        self.colaux = 0
        self.linaux0 = 0
        self.colaux0 = 0
        self.linaux1 = 0
        self.colaux1 = 0
        self.linaux2 = 0
        self.colaux2 = 0
        self.linaux3 = 0
        self.colaux3 = 0
        self.n_tipo_uso = 0
        self.caminho = 0
        self.numcabeaux = 0
        self.numcabeaux2 = 0
        self.A = 0
        self.B = 0
        self.C = 0
        self.D = 0
        self.E = 0
        self.F = 0
        self.G = 0
        self.H = 0
        self.resplist = 0
        self.cont = 0
        self.t = 0
        self.tt = 0
        self.Nusomax = 0
        self.maxdir = 0
        self.Ntre = 0   
        self.metro = 0
        self.Ttreaux = 0
        self.casserioaux = 0
        self.nclasses = 0
        self.ll = 0
        self.cc = 0
        self.pixel_ref_dren = 0
        self.diraux = 0
        self.numtreauxmax = 0
        self.numtreaux = 0
        self.numtreaux2 = 0
        self.tipo_decliv = 4
        self.hexc = 0
        self.numero_total_pix = 0
        self.num_intervalos = 0
        self.volume_total = 0
        self.quantidade_blocos_chuva = 0
        self.chuva_excedente_calc = 0
        self.blocos_vazao = 0
        self.alfa, self.delta_t, self.criterio_parada, self.beta = 0,0,0,0
       
        # Real varibles declaration
        self.xmin = 0.0
        self.xmax = 0.0
        self.ymin = 0.0
        self.ymax = 0.0
        self.tc_max = 0.0
        self.dx = 0.0
        self.Xesq = 0.0
        self.Xdir = 0.0
        self.Yinf = 0.0
        self.Ysup = 0.0
        self.Xres = 0.0
        self.Yres = 0.0
        self.Xres2 = 0.0
        self.diagonal = 0.0
        self.dist_2 = 0.0
        self.lado = 0.0
        self.auxdist = 0.0
        self.tamcam = np.float64(0.0)
        self.Ncabe = np.float64(0.0)
        self.Ltreaux = np.float64(0.0)
        self.Streaux = np.float64(0.0)
        self.Lfozaux1 = np.float64(0.0)
        self.Lfozaux2 = np.float64(0.0)
        self.Velaux = np.float64(0.0)
        self.Rhaux = np.float64(0.0)
        self.naux = np.float64(0.0)
        self.Saux = np.float64(0.0)
        self.Laux = np.float64(0.0)
        self.P24 = np.float64(0.0)
        self.Taux = np.float64(0.0)
        self.DISTtreaux = np.float64(0.0)
        self.tamfoz = np.float64(0.0)
        self.Tempoauxac = np.float64(0.0)
        self.Tempoaux = np.float64(0.0)
        self.auxTempoCanal = np.float64(0.0)
        self.Streaux2 = np.float64(0.0)
        self.Difcota = np.float64(0.0)
        self.Lincr = np.float64(0.0)
        self.Smin = np.float64(0.0)
        self.tempocam = np.float64(0.0)
        self.Smax = np.float64(0.0)
        self.coef_c = 0.0
        self.coef_d = 0.0
        self.coef_g = 0.0
        self.coef_h = 0.0
        self.n_canal = 0.0
        self.max_comp_trecho = 0.0
        self.sheet_flow = 0.0
        self.profundidade_resers = 0.0
        self.n_total_trechos = 0.0

        # Int 4bytes
        self.numncabeaux = np.int32(0)
        self.Ncabec = np.int32(0)



