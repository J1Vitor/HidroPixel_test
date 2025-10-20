"""
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ MODULE FOR CREATION OF RDC's VARIABLES \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

Objective: This file is responsible for creating the RDC's variables necessary for the Hidropixel Plugin operation.
Author: João Vitor Dias
Supervisor: Adriano Rolim
Date of last update: 30/11/2023

"""
# IMPORTING libs
import numpy as np


class RDCVariables:
    """
    This class is responsible for creating the RDC's variables necessary for the Hidropixel Plugin operation.
    """

    def __init__(self, nlin, ncol):
        """
        This method is responsible for creating the RDC's variables necessary for the Hidropixel Plugin operation.
        """
        # Matrix's declaration
        self.Var2D = np.empty((nlin, ncol), dtype=float)
        self.xx = np.empty((nlin, ncol), dtype=float)
        self.yy = np.empty((nlin, ncol), dtype=float)
        self.P2lc = np.empty((nlin, ncol), dtype=float)
        self.VarMM2 = np.empty((nlin, ncol), dtype=float)
        self.VarMM3 = np.empty((nlin, ncol, 0), dtype=float)
        self.cell = np.empty((nlin, ncol), dtype=np.int16)

        # string's declaration
        self.iauxchar1 = ""
        self.iauxchar2 = ""
        self.ichar = ""
        self.cabecalho = ""
        self.textoaux = ""
        self.nomeRST = ""
        self.nomeRDC = ""
        self.sistemaref = ""
        self.unidaderef = ""
        self.geotransform = []
        self.projection = None
        self.projection = ""

        # Int's variables declaration
        self.i = 0
        self.narq = 0
        self.lin = 0
        self.col = 0
        self.nlin = 0
        self.ncol = 0
        self.arg = 0
        self.KC2 = 0
        self.pixnul = 0
        self.lin3 = 0
        self.lin2 = 0
        self.col2 = 0
        self.col3 = 0
        self.nlin3 = 0
        self.resolucao = 0
        self.ncol3 = 0
        self.tipodado = 0
        self.tamnum = 0
        self.num = 0
        self.cont = 0
        self.tipoMM = 0
        self.TipoAnaliseFaixa = 0
        self.i3 = 0
        self.cellaux = 0
        self.invalueraster = 0
        self.linstac = 0
        self.linst = 0
        self.gerasrack = 0
        self.metrordc = 0
        self.tipo = 0
        self.tipo_dado = 0
        self.tipo1 = 0
        self.tipo2 = 0

        # Real varibles declaration
        self.coordxie = 0.0
        self.coordyie = 0.0
        self.parax = 0.0
        self.paray = 0.0
        self.delta = 0.0
        self.xmin = 0.0
        self.Xmin3 = 0.0
        self.Xmax3 = 0.0
        self.Ymin3 = 0.0
        self.Ymax3 = 0.0
        self.dx3 = 0.0
        self.Varmin = 0.0
        self.Varmax = 0.0
        self.varaux = 0.0
