# from concurrent.futures import ProcessPoolExecutor
# import numpy as np
# import cv2
# import os
# import glob
# import time
# from osgeo import gdal
# # gdal.UseExceptions()
import glob

# def leh_asc_to_np_array(arquivo1):
#     '''Lê arquivo .asc e converte para array NumPy'''
#     lins = 650
#     cols = 885
#     rst_to_raster = np.zeros((lins, cols))

#     with open(arquivo1, 'r') as arquivo_ascii:
#         for _ in range(6):
#             next(arquivo_ascii)
#         for lin in range(lins):
#             for col in range(cols):
#                 rst_to_raster[lin, col] = float(arquivo_ascii.readline())
#     return rst_to_raster


# def desenhar_escala_colormap(imagem, min_val=0, max_val=255, colormap=cv2.COLORMAP_OCEAN):
#     """Adiciona uma barra de escala colorida vertical ao canto inferior direito da imagem"""
#     altura, largura = imagem.shape[:2]
#     escala_altura = 200
#     escala_largura = 30

#     # Cria barra vertical de valores (0 a 255)
#     gradiente = np.linspace(
#         max_val, min_val, escala_altura).reshape(-1, 1).astype(np.uint8)
#     barra = cv2.applyColorMap(gradiente, colormap)

#     # Coloca valores numéricos (mín e máx)
#     imagem[-escala_altura-10:-10, largura -
#            escala_largura - 10:largura - 10] = barra

#     # Escreve valores
#     fonte = cv2.FONT_HERSHEY_SIMPLEX
#     cv2.putText(imagem, f'{max_val}', (largura - escala_largura - 40, altura - escala_altura - 15),
#                 fonte, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
#     cv2.putText(imagem, f'{min_val}', (largura - escala_largura - 40, altura - 15),
#                 fonte, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

#     return imagem


# def processar_imagem(caminho_asc):
#     '''Processa um arquivo ASC e retorna imagem pronta para o vídeo'''
#     nome_arquivo = f'{os.path.basename(caminho_asc).split(".")[0]} min'
#     img = leh_asc_to_np_array(caminho_asc)

#     if img.dtype != np.uint8:
#         img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

#     img_color = cv2.applyColorMap(img, cv2.COLORMAP_OCEAN)

#     bacia = gdal.Open(
#         r"D:\lixo_de_ouro\codigos\Hidropixel_Tapacura_Karol\MDT_30m_pitrem_watershed.tif")
#     bacia_raster = bacia.GetRasterBand(1).ReadAsArray()

#     pixels_zero = bacia_raster == 0
#     img_color[pixels_zero] = [255, 255, 255]

#     # Texto com o nome do arquivo (canto superior esquerdo)
#     cv2.putText(img_color, nome_arquivo, (10, 25),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

#     # Escala de cores (canto inferior direito)
#     img_color = desenhar_escala_colormap(img_color)

#     return img_color


# if __name__ == '__main__':
#     inicio_time = time.time()
#     os.chdir(r"C:\PyQGIS\hidropixel\temp\maps")
#     lista_mapas = sorted(glob.glob('*.asc'), key=len)

#     with ProcessPoolExecutor() as executor:
#         frames = list(executor.map(processar_imagem, lista_mapas))

#     altura, largura = frames[0].shape[:2]
#     video_saida = 'animacao_chuva.mp4'
#     fps = 1
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     video = cv2.VideoWriter(video_saida, fourcc, fps, (largura, altura))

#     for frame in frames:
#         video.write(frame)
#         print("Frame adicionado")

#     video.release()
#     fim_time = time.time()
#     print(
#         f"Vídeo finalizado com sucesso.\nTempo de processamento: {fim_time - inicio_time:.2f} segundos")

import numpy as np
from osgeo import ogr, gdal, gdalconst
import os, glob
# leh matriz da bacia para capturar limites
bacia_dataset = gdal.Open(
    r"D:\lixo_de_ouro\simulacoes\artigo_\EventoJun2022_subbacias\bac1_FlowTravelTime.tif")
nlin = bacia_dataset.RasterYSize
ncol = bacia_dataset.RasterXSize
geotransform = bacia_dataset.GetGeoTransform()
projection = bacia_dataset.GetProjection()

os.chdir(r"C:\PyQGIS\hidropixel\temp")
bacias = glob.glob('*.rst')
rst_to_raster = np.zeros((nlin, ncol))

for bacia in bacias:
    with open(bacia, 'r') as arquivo_ascii:
        for lin in range(nlin):
            for col in range(ncol):
                rst_to_raster[lin, col] = float(
                    arquivo_ascii.readline())


    # Define os dados a serem escritos
    tipo_dados = gdalconst.GDT_Float32

    # Obtendo o driver para escrita do arquivo em GeoTiff
    fn_geotiff = os.path.basename(bacia).replace(".rst",".tif")
    driver = gdal.GetDriverByName('GTiff')

    # Cria arquivo final
    dataset = driver.Create(
        fn_geotiff, ncol, nlin, 1, tipo_dados)
    dataset.SetGeoTransform(geotransform)
    dataset.SetProjection(projection)
    # Escreve os dados na banda do arquivo
    banda = dataset.GetRasterBand(1)
    banda.WriteArray(rst_to_raster)
