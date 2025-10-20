# core/validators.py
import numpy as np
import struct
from qgis.core import QgsProject, QgsRasterLayer
from qgis.PyQt.QtWidgets import QMessageBox, QApplication, QProgressDialog
from qgis.PyQt.QtCore import QByteArray, Qt
from collections import deque
import os


class RasterValidator:
    def __init__(self, hidropixel, dlg_flow_tt, dlg_exc_rain, dlg_flow_rout):
        self.hidropixel = hidropixel
        self.dlg_flow_tt = dlg_flow_tt
        self.dlg_exc_rain = dlg_exc_rain
        self.dlg_flow_rout = dlg_flow_rout
        self.classes_uso_validas = set()

    def atualizar_validação(self, nome_validacao, status):
        self.hidropixel.validations[nome_validacao] = status
        self.atualizar_all_validated()

    def atualizar_all_validated(self):
        tot_esperado = 15  # total de funcoes de verificacao
        atuais = len(self.hidropixel.validations)

        if atuais < tot_esperado:
            faltam = tot_esperado - atuais
            print(f"Validation not complete: {faltam} checks remaining.")
        else:
            self.all_validated = all(self.hidropixel.validations.values())

    def atualizar_label_validacao(self, label, status):
        if status == 1:
            label.setText("✅ Validated")
        elif status == 0:
            label.setText("❌ Invalid")
        elif status == -1:
            label.setText("⚠️ Not selected")
        else:
            label.setText(status)

    def mostrar_mensagem_processando(self, titulo="Processing", mensagem="Please wait, validation is running..."):
        msg_box = QMessageBox(self.dlg_flow_tt)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle(titulo)
        msg_box.setText(mensagem)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setModal(False)
        msg_box.show()
        return msg_box

    def get_raster_info(self, path):
        layer = self.get_raster_layer_by_name(path)
        # provider = layer.dataProvider()
        extent = layer.extent()
        ncol = layer.width()
        nlin = layer.height()
        resx = extent.width() / ncol
        resy = extent.height() / nlin
        return nlin, ncol, resx, resy

    def raster_to_array(self, raster_layer):

        provider = raster_layer.dataProvider()
        band = 1  # assuming first band
        extent = raster_layer.extent()
        width = raster_layer.width()
        height = raster_layer.height()

        # Get the raster block
        block = provider.block(band, extent, width, height)
        if not block or block.isEmpty():
            raise RuntimeError("Failed to read raster block.")

        data = block.data()
        if data is None or data.isEmpty():
            raise RuntimeError("Raster block data is empty or unavailable.")

        pixel_count = width * height
        actual_bytes = data.size()

        # Determine bytes per pixel
        if actual_bytes % pixel_count != 0:
            raise RuntimeError(
                "Raster buffer size is not divisible by number of pixels.")

        bytes_per_pixel = actual_bytes // pixel_count

        # Map byte size to numpy dtype
        bytes_to_dtype = {
            1: np.uint8,
            2: np.int16,
            4: np.float32,  # Covers both Int32 and Float32
            8: np.float64
        }

        dtype = bytes_to_dtype.get(bytes_per_pixel)
        if not dtype:
            raise RuntimeError(
                f"Unsupported pixel size: {bytes_per_pixel} bytes")

        # Convert buffer to numpy array and reshape
        arr = np.frombuffer(data, dtype=dtype).reshape((height, width))
        return arr

    def get_raster_layer_by_name(self, name):
        for layer in QgsProject.instance().mapLayers().values():
            if layer.name() == name:
                return layer
        raise ValueError(f"Raster '{name}' not found in the project.")

    def validar_raster_bacia(self, path, modulo=1):
        try:
            if modulo == 1:
                label = self.dlg_flow_tt.label_90
                button = self.dlg_flow_tt
            elif modulo == 2:
                label = self.dlg_exc_rain.label_45
                button = self.dlg_exc_rain
            elif modulo == 3:
                label = self.dlg_flow_rout.label_14
                button = self.dlg_flow_rout
            else:
                QMessageBox.warning(button, "Warning",
                                    f"Invalid module: {modulo}")
                self.atualizar_validação("validar_raster_bacia", False)
                return

            if not path:
                self.atualizar_label_validacao(label, -1)
                QMessageBox.warning(button, "Warning",
                                    f"No watershed raster selected.")
                self.atualizar_validação("validar_raster_bacia", False)
                return

            layer = self.get_raster_layer_by_name(path)
            array = self.raster_to_array(layer)

            unique_values = np.unique(array)
            if not np.all(np.isin(unique_values, [0, 1])):
                QMessageBox.critical(
                    button,
                    "Error",
                    f"Basin raster contains values other than 0 and 1.\nValues found: {unique_values}"
                )
                self.atualizar_label_validacao(label, 0)
                self.atualizar_validação("validar_raster_bacia", False)
                return

            QMessageBox.information(
                self.dlg_flow_tt, "OK", "Valid basin raster.")
            self.atualizar_label_validacao(label, 1)
            # marcar validação como bem sucedida
            self.atualizar_validação("validar_raster_bacia", True)

        except Exception as e:
            QMessageBox.critical(self.dlg_flow_tt, "Unexpected error", str(e))
            self.atualizar_label_validacao(label, 0)
            # em caso de exceção, marca como falha
            self.atualizar_validação("validar_raster_bacia", False)

    def validar_raster_mde(self):
        try:
            name = self.dlg_flow_tt.cb_2_pg2.currentText()
            if not name:
                QMessageBox.warning(
                    self.dlg_flow_tt, "Warning", f"No DEM selected.")
                self.atualizar_label_validacao(self.dlg_flow_tt.label_96, -1)
                self.atualizar_validação("validar_raster_mde", False)
                return

            layer = self.get_raster_layer_by_name(name)
            array = self.raster_to_array(layer)

            if np.any(array < 0):
                QMessageBox.critical(
                    self.dlg_flow_tt, "Error", "Invalid DEM: contains negative values.")
                self.atualizar_label_validacao(self.dlg_flow_tt.label_96, 0)
                self.atualizar_validação("validar_raster_mde", False)
                return

            QMessageBox.information(
                self.dlg_flow_tt, "OK", "Valid DEM: no negative values found.")
            self.atualizar_label_validacao(self.dlg_flow_tt.label_96, 1)
            self.atualizar_validação("validar_raster_mde", True)

        except Exception as e:
            QMessageBox.critical(self.dlg_flow_tt, "Unexpected error", str(e))
            self.atualizar_label_validacao(self.dlg_flow_tt.label_96, 0)
            self.atualizar_validação("validar_raster_mde", False)

    def validar_direcoes_fluxo(self):
        try:
            fluxo = self.dlg_flow_tt.cb_3_pg2.currentText()
            if not fluxo:
                self.atualizar_label_validacao(self.dlg_flow_tt.label_98, -1)
                QMessageBox.warning(self.dlg_flow_tt, "Warning",
                                    f"Flow directions raster not selected.")
                self.atualizar_validação("validar_direcoes_fluxo", False)
                return

            if self.validar_direcoes(fluxo):
                QMessageBox.information(
                    self.dlg_flow_tt, "OK", "Valid flow directions raster.")
                self.atualizar_label_validacao(self.dlg_flow_tt.label_98, 1)
                self.atualizar_validação("validar_direcoes_fluxo", True)
            else:
                QMessageBox.critical(
                    self.dlg_flow_tt, "Error", "Invalid flow directions raster.")
                self.atualizar_label_validacao(self.dlg_flow_tt.label_98, 0)
                self.atualizar_validação("validar_direcoes_fluxo", False)

        except Exception as e:
            QMessageBox.critical(self.dlg_flow_tt, "Unexpected error", str(e))
            self.atualizar_label_validacao(self.dlg_flow_tt.label_98, 0)
            self.atualizar_validação("validar_direcoes_fluxo", False)

    def check_all_equal(self, paths):
        if not paths:
            return True

        info0 = self.get_raster_info(paths[0])
        for p in paths[1:]:
            info = self.get_raster_info(p)
            if info != info0:
                return False
        return True

    def verificar_dimensoes_rasters(self, paths, modulo=1):
        paths = [p for p in paths if p]

        if modulo == 1:
            label = self.dlg_flow_tt.label_95
            dlg = self.dlg_flow_tt
        elif modulo == 2:
            label = self.dlg_exc_rain.label_46
            dlg = self.dlg_exc_rain
        elif modulo == 3:
            label = self.dlg_flow_rout.label_10
            dlg = self.dlg_flow_rout
        else:
            QMessageBox.warning(self.dlg_flow_tt, "Warning",
                                f"Invalid module: {modulo}")
            self.atualizar_validação("verificar_dimensoes_rasters", False)
            return

        if not paths:
            QMessageBox.warning(
                dlg, "Warning", "No raster selected for validation.")
            self.atualizar_label_validacao(label, -1)
            self.atualizar_validação("verificar_dimensoes_rasters", False)
            return

        if self.check_all_equal(paths):
            QMessageBox.information(
                dlg, "Validation", "All rasters have the same dimension and resolution.")
            self.atualizar_label_validacao(label, 1)
            self.atualizar_validação("verificar_dimensoes_rasters", True)
        else:
            QMessageBox.critical(
                dlg, "Error", "Rasters have different dimensions or resolutions.")
            self.atualizar_label_validacao(label, 0)
            self.atualizar_validação("verificar_dimensoes_rasters", False)

    def validar_direcoes(self, fluxo_path):
        aviso = self.mostrar_mensagem_processando(
            mensagem="Flow direction validation is running..."
        )

        try:
            layer_fluxo = self.get_raster_layer_by_name(
                os.path.basename(fluxo_path))
            fluxo_arr = self.raster_to_array(layer_fluxo)

            # Basin mask
            nome_bacia = getattr(self.dlg_flow_tt, "cb_1_pg2", None)
            if nome_bacia:
                try:
                    nome_bacia = self.dlg_flow_tt.cb_1_pg2.currentText()
                    if nome_bacia:
                        bacia_arr = self.raster_to_array(
                            self.get_raster_layer_by_name(nome_bacia))
                        dentro_bacia = (bacia_arr == 1)
                    else:
                        dentro_bacia = np.ones_like(fluxo_arr, dtype=bool)
                except Exception:
                    dentro_bacia = np.ones_like(fluxo_arr, dtype=bool)
            else:
                dentro_bacia = np.ones_like(fluxo_arr, dtype=bool)

            vals = fluxo_arr[dentro_bacia]
            vals = vals[np.isfinite(vals)]
            raster_codes = sorted({int(v) for v in vals if v > 0})

            # gui codes
            campos = {
                (0, 1):  self.dlg_flow_tt.le_6_pg1.text(),
                (-1, 1): self.dlg_flow_tt.le_5_pg1.text(),
                (-1, 0): self.dlg_flow_tt.le_12_pg1.text(),
                (-1, -1): self.dlg_flow_tt.le_11_pg1.text(),
                (0, -1): self.dlg_flow_tt.le_10_pg1.text(),
                (1, -1): self.dlg_flow_tt.le_9_pg1.text(),
                (1, 0):  self.dlg_flow_tt.le_8_pg1.text(),
                (1, 1):  self.dlg_flow_tt.le_7_pg1.text(),
            }

            # Ensure filled and convert to int
            for vec, txt in campos.items():
                if txt.strip() == "":
                    aviso.close()
                    QMessageBox.critical(self.dlg_flow_tt, "Error",
                                         f"Empty field found for direction vector {vec}.")
                    return False
            interface_codes = [int(txt) for txt in campos.values()]

            # Duplicates check
            if len(interface_codes) != len(set(interface_codes)):
                aviso.close()
                QMessageBox.critical(self.dlg_flow_tt, "Error",
                                     "Duplicate directions found in the interface. Each must be unique.")
                return False

            # Raster codes must exist in interface
            missing = [c for c in raster_codes if c not in interface_codes]
            if missing:
                aviso.close()
                QMessageBox.critical(
                    self.dlg_flow_tt,
                    "Error",
                    f"The following direction code(s) are present in the raster (inside the basin) "
                    f"but missing in the interface: {missing}"
                )
                self.atualizar_validação("validar_direcoes", False)
                return False

            aviso.close()
            self.atualizar_validação("validar_direcoes", True)
            return True

        except Exception as e:
            aviso.close()
            QMessageBox.critical(self.dlg_flow_tt, "Unexpected Error", str(e))
            self.atualizar_validação("validar_direcoes", False)
            return False

    def encontrar_exutorio(self, raster_fluxo_data, raster_bacia_data, raster_acumulado_data):
        nlin, ncol = raster_bacia_data.shape

        max_valor = -np.inf
        exutorio = None

        for i in range(nlin):
            for j in range(ncol):
                if raster_bacia_data[i, j] != 1:
                    continue

                valor_acumulado = raster_acumulado_data[i, j]
                if np.isnan(valor_acumulado):
                    continue

                if valor_acumulado > max_valor:
                    max_valor = valor_acumulado
                    exutorio = (i, j)

        if exutorio is None:
            QMessageBox.critical(
                self.dlg_flow_tt, "Error", "No outlet found: watershed has no valid accumulated values.")
            return None

        return exutorio

    def processar_fluxo(self):
        nome_raster_acumulado = self.dlg_flow_tt.cb_6_pg2.currentText()
        if not nome_raster_acumulado:
            QMessageBox.critical(self.dlg_flow_tt, "Error",
                                 "Select the accumulated raster in the combobox.")
            return

        raster_fluxo = self.dlg_flow_tt.cb_3_pg2.currentText()
        raster_bacia = self.dlg_flow_tt.cb_1_pg2.currentText()
        raster_acumulado = nome_raster_acumulado

        layer_fluxo = self.get_raster_layer_by_name(
            os.path.basename(raster_fluxo))
        layer_bacia = self.get_raster_layer_by_name(
            os.path.basename(raster_bacia))
        layer_acumulado = self.get_raster_layer_by_name(
            os.path.basename(raster_acumulado))

        raster_fluxo_data = self.raster_to_array(layer_fluxo)
        raster_fluxo_data = np.where(np.ma.getmaskarray(
            raster_fluxo_data), 0, raster_fluxo_data)

        raster_bacia_data = self.raster_to_array(layer_bacia)
        raster_bacia_data = np.where(np.ma.getmaskarray(
            raster_bacia_data), 0, raster_bacia_data)

        raster_acumulado_data = self.raster_to_array(layer_acumulado)
        raster_acumulado_data = np.where(np.ma.getmaskarray(
            raster_acumulado_data), np.nan, raster_acumulado_data)

        exutorio = self.encontrar_exutorio(
            raster_fluxo_data, raster_bacia_data, raster_acumulado_data)
        area_exutorio = None
        if exutorio is None:
            return

        nlin, ncol = raster_fluxo_data.shape

        direcoes_dict = {
            (0, 1):  int(self.dlg_flow_tt.le_6_pg1.text()),
            (-1, 1): int(self.dlg_flow_tt.le_5_pg1.text()),
            (-1, 0): int(self.dlg_flow_tt.le_12_pg1.text()),
            (-1, -1): int(self.dlg_flow_tt.le_11_pg1.text()),
            (0, -1): int(self.dlg_flow_tt.le_10_pg1.text()),
            (1, -1): int(self.dlg_flow_tt.le_9_pg1.text()),
            (1, 0):  int(self.dlg_flow_tt.le_8_pg1.text()),
            (1, 1):  int(self.dlg_flow_tt.le_7_pg1.text()),
        }
        angulo_para_vetor = {ang: vec for vec, ang in direcoes_dict.items()}

        def dentro(i, j):
            return 0 <= i < nlin and 0 <= j < ncol

        if not (dentro(*exutorio) and raster_bacia_data[exutorio] == 1):
            QMessageBox.critical(
                self.dlg_flow_tt, "Error", "Invalid outlet or outlet outside the watershed.")
            # self.atualizar_validação("processar_fluxo", False)
            return

        status = np.full_like(raster_bacia_data, -1, dtype=np.int8)

        for i in range(nlin):
            for j in range(ncol):
                if raster_bacia_data[i, j] != 1 or status[i, j] != -1:
                    continue

                pilha = [(i, j)]
                visitando = set()
                caminho = []
                ultimo = (i, j)

                while pilha:
                    ci, cj = pilha[-1]
                    ultimo = (ci, cj)

                    if (ci, cj) in visitando:
                        for pi, pj in pilha:
                            status[pi, pj] = 0
                        break

                    visitando.add((ci, cj))
                    caminho.append((ci, cj))

                    if (ci, cj) == exutorio:
                        area_exutorio = raster_acumulado_data[exutorio]
                        for pi, pj in caminho:
                            status[pi, pj] = 1
                        break

                    flux = raster_fluxo_data[ci, cj]
                    vec = angulo_para_vetor.get(flux)
                    if vec is None:
                        for pi, pj in caminho:
                            status[pi, pj] = 0
                        break

                    ni, nj = ci + vec[0], cj + vec[1]
                    if not (dentro(ni, nj) and raster_bacia_data[ni, nj] == 1):
                        for pi, pj in caminho:
                            status[pi, pj] = 0
                        break

                    s = status[ni, nj]
                    if s == 1:
                        for pi, pj in caminho:
                            status[pi, pj] = 1
                        break
                    if s == 0 or (ni, nj) in visitando:
                        for pi, pj in caminho:
                            status[pi, pj] = 0
                        break

                    pilha.append((ni, nj))

                if status[i, j] == 0:
                    msgs = [
                        "ERROR: At least one pixel did not converge.",
                        f"Starting pixel: ({i}, {j})",
                        f"Last valid pixel: {ultimo}",
                        f"Outlet is: {exutorio}"
                    ]
                    QMessageBox.critical(
                        self.dlg_flow_tt, "Convergence Failure", "\n".join(msgs))
                    # self.atualizar_validação("processar_fluxo", False)
                    return

        QMessageBox.information(
            self.dlg_flow_tt,
            "Success",
            f"All pixels in the watershed converged to the outlet {exutorio}."
            f"\nAccumulated area at the outlet: {area_exutorio:.2f} km²."
        )
        # self.atualizar_validação("processar_fluxo", True)
        return

    def executar_validacao_fluxo(self):
        # Mostrar mensagem de processamento
        aviso = self.mostrar_mensagem_processando(
            mensagem="Flow validation is running..."
        )

        nome_fluxo = self.dlg_flow_tt.cb_3_pg2.currentText()
        nome_bacia = self.dlg_flow_tt.cb_1_pg2.currentText()
        nome_acumulado = self.dlg_flow_tt.cb_6_pg2.currentText()

        if not (nome_fluxo and nome_bacia and nome_acumulado):
            aviso.close()
            QMessageBox.critical(
                self.dlg_flow_tt, "Error", "Please select the flow, basin, and accumulation rasters.")
            self.atualizar_label_validacao(self.dlg_flow_tt.label_100, -1)
            self.atualizar_validação("executar_validacao_fluxo", False)
            return

        try:
            self.processar_fluxo()
            aviso.close()
            self.atualizar_label_validacao(self.dlg_flow_tt.label_100, 1)
            self.atualizar_validação("executar_validacao_fluxo", True)

        except Exception as e:
            aviso.close()
            QMessageBox.critical(self.dlg_flow_tt, "Unexpected Error", str(e))
            self.atualizar_label_validacao(self.dlg_flow_tt.label_100, 0)
            self.atualizar_validação("executar_validacao_fluxo", False)

    def validar_uso_cobertura(self):
        try:
            raster_bacia_nome = self.dlg_flow_tt.cb_1_pg2.currentText()
            raster_uso_nome = self.dlg_flow_tt.cb_7_pg2.currentText()

            if not raster_bacia_nome or not raster_uso_nome:
                self.atualizar_label_validacao(self.dlg_flow_tt.label_102, -1)
                QMessageBox.warning(
                    self.dlg_flow_tt,
                    "Warning",
                    "Please select both basin and land use/cover rasters."
                )
                self.atualizar_validação("validar_uso_cobertura", False)
                return

            layer_bacia = self.get_raster_layer_by_name(raster_bacia_nome)
            layer_uso = self.get_raster_layer_by_name(raster_uso_nome)

            array_bacia = self.raster_to_array(layer_bacia)
            array_uso = self.raster_to_array(layer_uso)

            # Ensure masked values become zeros for basin
            array_bacia = np.where(
                np.ma.getmaskarray(array_bacia), 0, array_bacia)
            mask_bacia = array_bacia == 1

            # Mask nodata in land use raster
            # check nodata later
            array_uso = np.where(np.ma.getmaskarray(
                array_uso), -9999, array_uso)

            valores_uso = array_uso[mask_bacia]
            valores_unicos = np.unique(valores_uso)

            valores_invalidos = [
                v for v in valores_unicos
                if not isinstance(v, (int, np.integer)) or v in (0, -9999)
            ]

            if valores_invalidos:
                self.atualizar_label_validacao(self.dlg_flow_tt.label_102, 0)
                QMessageBox.critical(
                    self.dlg_flow_tt,
                    "Invalid Land Use/Cover",
                    f"Land use/cover raster contains invalid values within the basin: {valores_invalidos}"
                )
                self.atualizar_validação("validar_uso_cobertura", False)
                return

            # Store valid classes for future use
            self.classes_uso_validas = set(valores_unicos)
            self.atualizar_label_validacao(self.dlg_flow_tt.label_102, 1)
            QMessageBox.information(
                self.dlg_flow_tt,
                "Validation Successful",
                "Land use/cover raster successfully validated."
            )
            self.atualizar_validação("validar_uso_cobertura", True)

        except Exception as e:
            self.atualizar_label_validacao(self.dlg_flow_tt.label_102, 0)
            QMessageBox.critical(self.dlg_flow_tt, "Unexpected Error", str(e))
            self.atualizar_validação("validar_uso_cobertura", False)

    def validar_tabela_manning_lulc(self):
        try:
            # Ensure land use classes were validated first
            if not hasattr(self, "classes_uso_validas") or not self.classes_uso_validas:
                QMessageBox.warning(
                    self.dlg_flow_tt,
                    "Warning",
                    "Please validate the land use/cover raster first."
                )
                self.dlg_flow_tt.label_104.setText(
                    "⚠️ Waiting for previous validation")
                self.atualizar_validação("validar_tabela_manning_lulc", False)
                return

            tabela = self.dlg_flow_tt.tbw_2_pg2
            linhas = tabela.rowCount()

            classes_tabela = set()
            manning_validos = {}

            for i in range(linhas):
                try:
                    classe_item = tabela.item(i, 0)
                    manning_item = tabela.item(i, 2)
                    if not classe_item or not manning_item:
                        continue

                    classe_id = int(classe_item.text())
                    manning = float(manning_item.text())

                    classes_tabela.add(classe_id)
                    manning_validos[classe_id] = manning
                except ValueError:
                    continue  # skip rows with invalid or empty values

            # Identify missing or invalid Manning classes
            faltando = sorted(self.classes_uso_validas - classes_tabela)
            manning_invalidos = sorted(
                cid for cid in self.classes_uso_validas
                if manning_validos.get(cid, 0) <= 0
            )

            if faltando or manning_invalidos:
                msg = []
                if faltando:
                    msg.append(f"Missing classes: {faltando}")
                if manning_invalidos:
                    msg.append(
                        f"Classes with invalid Manning's n (≤ 0): {manning_invalidos}")

                # self.dlg_flow_tt.label_104.setText("❌ Invalid")
                self.atualizar_label_validacao(self.dlg_flow_tt.label_104, 0)
                self.atualizar_validação("validar_tabela_manning_lulc", False)
                QMessageBox.critical(
                    self.dlg_flow_tt,
                    "Invalid Manning Table",
                    "The table has issues:\n" + "\n".join(msg)
                )
            else:
                # self.dlg_flow_tt.label_104.setText("✅ Validated")
                self.atualizar_label_validacao(self.dlg_flow_tt.label_104, 1)
                QMessageBox.information(
                    self.dlg_flow_tt,
                    "Validation Successful",
                    "All Manning's n values for land use classes are valid."
                )
                self.atualizar_validação("validar_tabela_manning_lulc", True)

        except Exception as e:
            # self.dlg_flow_tt.label_104.setText("❌ Error")
            self.atualizar_label_validacao(self.dlg_flow_tt.label_104, 0)
            self.atualizar_validação("validar_tabela_manning_lulc", False)
            QMessageBox.critical(self.dlg_flow_tt, "Unexpected Error", str(e))

    def validar_raster_rdn_classes(self):
        try:
            nome_raster = self.dlg_flow_tt.cb_5_pg2.currentText()
            label = self.dlg_flow_tt.label_112

            if not nome_raster:
                self.atualizar_label_validacao(label, -1)
                self.atualizar_validação("validar_raster_rdn_classes", False)
                return

            layer = self.get_raster_layer_by_name(nome_raster)
            array = self.raster_to_array(layer)

            array = array[np.isfinite(array)]

            if not np.all(np.equal(np.floor(array), array)):
                raise ValueError("Raster contains non-integer values.")

            unicos = np.unique(array.astype(int))
            if 0 not in unicos:
                raise ValueError(
                    "Raster does not contain the value 0 (non-network).")

            # Extract expected segments from the first column of the table
            expected_segments = []
            for row in range(self.dlg_flow_tt.tbw_1_pg2.rowCount()):
                item = self.dlg_flow_tt.tbw_1_pg2.item(row, 0)
                if item is None or not item.text().strip().isdigit():
                    raise ValueError(f"Invalid value in table at row {row+1}.")
                expected_segments.append(int(item.text().strip()))

            expected_segments = np.array(expected_segments, dtype=int)

            # Segments found in raster (excluding 0)
            raster_segments = unicos[unicos > 0]

            # Find missing segments
            missing_segments = np.setdiff1d(expected_segments, raster_segments)

            if len(missing_segments) > 0:
                raise ValueError(
                    f"Missing segment(s) in raster: {missing_segments.tolist()}")

            QMessageBox.information(
                self.dlg_flow_tt, "Validation", "RDN segments raster is valid.")
            self.atualizar_label_validacao(label, 1)
            self.atualizar_validação("validar_raster_rdn_classes", True)

        except Exception as e:
            QMessageBox.critical(self.dlg_flow_tt, "Validation Error", str(e))
            self.atualizar_label_validacao(label, 0)
            self.atualizar_validação("validar_raster_rdn_classes", False)

    def verificar_conectividade_rede(self):
        aviso = self.mostrar_mensagem_processando(
            mensagem="Validating drainage network connectivity..."
        )

        try:
            nome_rede = self.dlg_flow_tt.cb_4_pg2.currentText()
            nome_bacia = self.dlg_flow_tt.cb_1_pg2.currentText()
            nome_fluxo = self.dlg_flow_tt.cb_3_pg2.currentText()
            nome_acumulado = self.dlg_flow_tt.cb_6_pg2.currentText()

            if not nome_rede or not nome_bacia or not nome_fluxo or not nome_acumulado:
                aviso.close()
                self.atualizar_label_validacao(self.dlg_flow_tt.label_110, -1)
                self.atualizar_validação("verificar_conectividade_rede", False)
                return

            camada_rede = self.get_raster_layer_by_name(nome_rede)
            camada_bacia = self.get_raster_layer_by_name(nome_bacia)
            camada_fluxo = self.get_raster_layer_by_name(nome_fluxo)
            camada_acumulado = self.get_raster_layer_by_name(nome_acumulado)

            if not (camada_rede and camada_bacia and camada_fluxo and camada_acumulado):
                aviso.close()
                QMessageBox.critical(
                    self.dlg_flow_tt, "Error", "One or more required layers not found.")
                self.atualizar_label_validacao(self.dlg_flow_tt.label_110, -1)
                self.atualizar_validação("verificar_conectividade_rede", False)
                return

            rede_data = self.raster_to_array(camada_rede)
            bacia_data = self.raster_to_array(camada_bacia)
            acumulado_data = self.raster_to_array(camada_acumulado)

            exutorio = self.encontrar_exutorio(
                camada_fluxo, bacia_data, acumulado_data)
            if exutorio is None:
                aviso.close()
                self.atualizar_label_validacao(self.dlg_flow_tt.label_110, 0)
                self.atualizar_validação("verificar_conectividade_rede", False)
                return

            visitado = np.zeros_like(rede_data, dtype=bool)

            fila = deque([exutorio])
            visitado[exutorio] = True

            vizinhos = [(-1, -1), (-1, 0), (-1, 1),
                        (0, -1),          (0, 1),
                        (1, -1), (1, 0),  (1, 1)]

            while fila:
                i, j = fila.popleft()
                for di, dj in vizinhos:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rede_data.shape[0] and 0 <= nj < rede_data.shape[1]:
                        if not visitado[ni, nj] and rede_data[ni, nj] == 1:
                            visitado[ni, nj] = True
                            fila.append((ni, nj))

            for i in range(rede_data.shape[0]):
                for j in range(rede_data.shape[1]):
                    if rede_data[i, j] == 1 and not visitado[i, j]:
                        aviso.close()
                        QMessageBox.critical(
                            self.dlg_flow_tt,
                            "Error",
                            f"Network pixel ({i}, {j}) is not connected to the outlet."
                        )
                        self.atualizar_label_validacao(
                            self.dlg_flow_tt.label_110, 0)
                        self.atualizar_validação(
                            "verificar_conectividade_rede", False)
                        return

            aviso.close()
            QMessageBox.information(
                self.dlg_flow_tt,
                "Success",
                "All network pixels are connected to the outlet."
            )
            self.atualizar_label_validacao(self.dlg_flow_tt.label_110, 1)
            self.atualizar_validação("verificar_conectividade_rede", True)

        except Exception as e:
            aviso.close()
            QMessageBox.critical(self.dlg_flow_tt, "Unexpected Error", str(e))
            self.atualizar_label_validacao(self.dlg_flow_tt.label_110, 0)
            self.atualizar_validação("verificar_conectividade_rede", False)

    def verificar_acumulado_drenagem(self):
        from collections import deque

        aviso = self.mostrar_mensagem_processando(
            mensagem="Validating accumulated drainage values..."
        )

        try:
            path_acumulado = self.dlg_flow_tt.cb_6_pg2.currentText()
            path_bacia = self.dlg_flow_tt.cb_1_pg2.currentText()
            path_rede = self.dlg_flow_tt.cb_4_pg2.currentText()

            if not path_acumulado or not path_bacia or not path_rede:
                aviso.close()
                QMessageBox.warning(self.dlg_flow_tt, "Warning",
                                    "One or more rasters were not selected.")
                self.atualizar_label_validacao(self.dlg_flow_tt.label_114, -1)
                self.atualizar_validação("verificar_acumulado_drenagem", False)
                return

            acumulado_layer = self.get_raster_layer_by_name(path_acumulado)
            acumulado_data = self.raster_to_array(acumulado_layer)

            bacia_layer = self.get_raster_layer_by_name(path_bacia)
            bacia_data = self.raster_to_array(bacia_layer)

            rede_layer = self.get_raster_layer_by_name(path_rede)
            rede_data = self.raster_to_array(rede_layer)

            exutorio = self.encontrar_exutorio(
                None, bacia_data, acumulado_data)
            if exutorio is None:
                aviso.close()
                self.atualizar_label_validacao(self.dlg_flow_tt.label_114, 0)
                self.atualizar_validação("verificar_acumulado_drenagem", False)
                return

            nlin, ncol = bacia_data.shape
            visitado = np.zeros((nlin, ncol), dtype=bool)
            fila = deque()
            fila.append(exutorio)
            visitado[exutorio] = True

            direcoes = [(-1, -1), (-1, 0), (-1, 1),
                        (0, -1),          (0, 1),
                        (1, -1),  (1, 0), (1, 1)]

            while fila:
                i, j = fila.popleft()
                val_atual = acumulado_data[i, j]

                for di, dj in direcoes:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < nlin and 0 <= nj < ncol:
                        if visitado[ni, nj]:
                            continue
                        if bacia_data[ni, nj] != 1:
                            continue
                        if rede_data[ni, nj] != 1:
                            continue

                        val_vizinho = acumulado_data[ni, nj]

                        if np.isnan(val_vizinho) or val_vizinho <= 0:
                            aviso.close()
                            QMessageBox.critical(
                                self.dlg_flow_tt, "Error",
                                f"Invalid pixel ({ni}, {nj}) with accumulated value {val_vizinho}"
                            )
                            self.atualizar_label_validacao(
                                self.dlg_flow_tt.label_114, 0)
                            self.atualizar_validação(
                                "verificar_acumulado_drenagem", False)
                            return

                        if val_vizinho < val_atual:
                            visitado[ni, nj] = True
                            fila.append((ni, nj))

            for i in range(nlin):
                for j in range(ncol):
                    if bacia_data[i, j] == 1 and rede_data[i, j] == 1:
                        if not visitado[i, j]:
                            aviso.close()
                            QMessageBox.critical(
                                self.dlg_flow_tt, "Error",
                                f"Stream pixel ({i}, {j}) is not correctly connected to the outlet or has non-increasing values."
                            )
                            self.atualizar_label_validacao(
                                self.dlg_flow_tt.label_114, 0)
                            self.atualizar_validação(
                                "verificar_acumulado_drenagem", False)
                            return

            aviso.close()
            QMessageBox.information(
                self.dlg_flow_tt, "Validation",
                "All accumulated values are valid and increase upstream towards the outlet."
            )
            self.atualizar_label_validacao(self.dlg_flow_tt.label_114, 1)
            self.atualizar_validação("verificar_acumulado_drenagem", True)

        except Exception as e:
            aviso.close()
            QMessageBox.critical(self.dlg_flow_tt, "Unexpected Error", str(e))
            self.atualizar_label_validacao(self.dlg_flow_tt.label_114, 0)
            self.atualizar_validação("verificar_acumulado_drenagem", False)

    def validar_raster_cn(self):
        try:
            nome_bacia = self.dlg_exc_rain.cb_1_pg2.currentText()
            nome_cn = self.dlg_exc_rain.cb_2_pg2.currentText()

            if not nome_cn or not nome_bacia:
                self.atualizar_label_validacao(self.dlg_exc_rain.label_45, -1)
                self.atualizar_validação("validar_raster_cn", False)
                return

            cn_layer = self.get_raster_layer_by_name(nome_cn)
            bacia_layer = self.get_raster_layer_by_name(nome_bacia)

            cn_array = self.raster_to_array(cn_layer)
            bacia_array = self.raster_to_array(bacia_layer)

            # Mascara da bacia
            dentro_bacia = (bacia_array == 1)
            valores_cn = cn_array[dentro_bacia]

            # Validar valores CN
            if not np.all(np.isfinite(valores_cn)):
                QMessageBox.critical(self.dlg_exc_rain, "Error",
                                     "CN raster contains null or non-numeric values inside the basin.")
                self.atualizar_label_validacao(self.dlg_exc_rain.label_41, 0)
                self.atualizar_validação("validar_raster_cn", False)
                return

            if np.any(valores_cn <= 0) or np.any(valores_cn > 100):
                QMessageBox.critical(self.dlg_exc_rain, "Error",
                                     f"CN raster contains values out of range (>0 and ≤100). "
                                     f"Values found: min={np.min(valores_cn)}, max={np.max(valores_cn)}")
                self.atualizar_label_validacao(self.dlg_exc_rain.label_41, 0)
                self.atualizar_validação("validar_raster_cn", False)
                return

            QMessageBox.information(
                self.dlg_exc_rain, "Validation", "CN raster is valid.")
            self.atualizar_label_validacao(self.dlg_exc_rain.label_41, 1)
            self.atualizar_validação("validar_raster_cn", True)

        except Exception as e:
            QMessageBox.critical(self.dlg_exc_rain, "Unexpected error", str(e))
            self.atualizar_label_validacao(self.dlg_exc_rain.label_41, 0)
            self.atualizar_validação("validar_raster_cn", False)

    def verificar_tempos_de_viagem(self):
        aviso = self.mostrar_mensagem_processando(
            mensagem="Validating travel time raster..."
        )

        try:
            nome_tempo = self.dlg_flow_rout.cb_3_pg2.currentText()
            nome_bacia = self.dlg_flow_rout.cb_1_pg2.currentText()
            nome_rede = self.dlg_flow_rout.cb_3_pg2.currentText()
            nome_fluxo = self.dlg_flow_tt.cb_3_pg2.currentText()

            if not nome_tempo or not nome_bacia or not nome_fluxo:
                aviso.close()
                self.atualizar_label_validacao(self.dlg_flow_rout.label_20, -1)
                self.atualizar_validação("verificar_tempos_de_viagem", False)
                return

            tempo_array = self.raster_to_array(
                self.get_raster_layer_by_name(nome_tempo))
            bacia_array = self.raster_to_array(
                self.get_raster_layer_by_name(nome_bacia))
            fluxo_array = self.raster_to_array(
                self.get_raster_layer_by_name(nome_fluxo))

            rede_array = None
            if nome_rede:
                try:
                    rede_array = self.raster_to_array(
                        self.get_raster_layer_by_name(nome_rede))
                except:
                    pass

            nlin, ncol = bacia_array.shape

            direcoes_d8 = {
                1:  (0, 1),
                2:  (1, 1),
                4:  (1, 0),
                8:  (1, -1),
                16: (0, -1),
                32: (-1, -1),
                64: (-1, 0),
                128: (-1, 1)
            }

            visitado = np.zeros_like(bacia_array, dtype=bool)

            def seguir_fluxo(i, j):
                caminho = [(i, j)]
                while True:
                    if not (0 <= i < nlin and 0 <= j < ncol):
                        return True
                    if bacia_array[i, j] != 1:
                        return True
                    if visitado[i, j]:
                        return True
                    if not np.isfinite(tempo_array[i, j]) or tempo_array[i, j] <= 0:
                        return False
                    if rede_array is not None and rede_array[i, j] != 1:
                        return True

                    direcao = fluxo_array[i, j]
                    if direcao not in direcoes_d8:
                        return True

                    di, dj = direcoes_d8[direcao]
                    ni, nj = i + di, j + dj

                    if not (0 <= ni < nlin and 0 <= nj < ncol):
                        return True

                    tempo_atual = tempo_array[i, j]
                    tempo_prox = tempo_array[ni, nj]

                    if np.isfinite(tempo_prox) and tempo_prox < tempo_atual:
                        return False

                    visitado[i, j] = True
                    i, j = ni, nj
                    caminho.append((i, j))

            for i in range(nlin):
                for j in range(ncol):
                    if bacia_array[i, j] == 1 and not visitado[i, j]:
                        if rede_array is None or rede_array[i, j] == 1:
                            if not seguir_fluxo(i, j):
                                aviso.close()
                                QMessageBox.critical(
                                    self.dlg_flow_rout,
                                    "Error",
                                    f"Invalid travel time: non-positive or non-increasing values from pixel ({i}, {j})."
                                )
                                self.atualizar_label_validacao(
                                    self.dlg_flow_rout.label_20, 0)
                                self.atualizar_validação(
                                    "verificar_tempos_de_viagem", False)
                                return

            aviso.close()
            QMessageBox.information(
                self.dlg_flow_rout, "Validation", "Travel time raster is valid.")
            self.atualizar_label_validacao(self.dlg_flow_rout.label_20, 1)
            self.atualizar_validação("verificar_tempos_de_viagem", True)

        except Exception as e:
            aviso.close()
            QMessageBox.critical(self.dlg_flow_rout,
                                 "Unexpected error", str(e))
            self.atualizar_label_validacao(self.dlg_flow_rout.label_20, 0)
            self.atualizar_validação("verificar_tempos_de_viagem", False)

    def verificar_chuva_excedente_total(self):
        try:
            rain_name = self.dlg_flow_rout.cb_5_pg2.currentText()
            basin_name = self.dlg_flow_rout.cb_1_pg2.currentText()

            if not rain_name or not basin_name:
                self.atualizar_label_validacao(
                    self.dlg_flow_rout.label_22, '⚠️ Not selected')
                self.atualizar_validação(
                    "verificar_chuva_excedente_total", False)
                return

            rain_array = self.raster_to_array(
                self.get_raster_layer_by_name(rain_name))
            basin_array = self.raster_to_array(
                self.get_raster_layer_by_name(basin_name))

            inside_basin = (basin_array == 1)
            rain_values = rain_array[inside_basin]

            if not np.all(np.isfinite(rain_values)):
                QMessageBox.critical(
                    self.dlg_flow_rout, "Error",
                    "The excess rainfall raster contains null or non-numeric values inside the basin."
                )
                self.atualizar_label_validacao(self.dlg_flow_rout.label_22, 0)
                self.atualizar_validação(
                    "verificar_chuva_excedente_total", False)
                return

            if np.any(rain_values < 0):
                QMessageBox.critical(
                    self.dlg_flow_rout, "Error",
                    "Negative values found in the excess rainfall raster within the basin."
                )
                self.atualizar_label_validacao(self.dlg_flow_rout.label_22, 0)
                self.atualizar_validação(
                    "verificar_chuva_excedente_total", False)
                return

            QMessageBox.information(
                self.dlg_flow_rout, "Validation", "Total excess rainfall raster is valid.")
            self.atualizar_label_validacao(self.dlg_flow_rout.label_22, 1)
            self.atualizar_validação("verificar_chuva_excedente_total", True)

        except Exception as e:
            QMessageBox.critical(self.dlg_flow_rout,
                                 "Unexpected Error", str(e))
            self.atualizar_label_validacao(self.dlg_flow_rout.label_22, 0)
            self.atualizar_validação("verificar_chuva_excedente_total", False)

    def validar_hietograma_bin(self):
        aviso = self.mostrar_mensagem_processando(
            mensagem="Hyetograph file validation is running..."
        )

        try:
            path = self.dlg_flow_rout.le_4_pg2.text()
            if not path or not os.path.exists(path):
                aviso.close()
                QMessageBox.warning(self.dlg_flow_rout,
                                    "Warning", "File not found.")
                self.atualizar_label_validacao(
                    self.dlg_flow_rout.label_24, '⚠️ Not selected')
                self.atualizar_validação("validar_hietograma_bin", False)
                return

            # Lê o raster selecionado no combobox (para comparar o número de pixels)
            camada_nome = self.dlg_exc_rain.cb_1_pg2.currentText()
            raster = None
            for camada in QgsProject.instance().mapLayers().values():
                if camada.name() == camada_nome:
                    raster = camada
                    break

            if raster is None:
                aviso.close()
                QMessageBox.warning(self.dlg_flow_rout,
                                    "Warning", "No raster layer selected.")
                return

            provider = raster.dataProvider()
            extent = raster.extent()
            rows = raster.height()
            cols = raster.width()
            total_pixels_raster = rows * cols

            # Leitura do arquivo binario
            with open(path, 'rb') as f:
                # Lê cabeçalho
                n_pixels = struct.unpack('i', f.read(4))[0]
                n_blocos = struct.unpack('i', f.read(4))[0]
                discretizacao = struct.unpack('f', f.read(4))[0]
                duracao = struct.unpack('f', f.read(4))[0]

                # Verifica se ha correspondência com o número de pixels da bacia
                if n_pixels > total_pixels_raster:
                    aviso.close()
                    QMessageBox.critical(
                        self.dlg_flow_rout,
                        "Error",
                        f"The file specifies {n_pixels} pixels, "
                        f"but the raster contains only {total_pixels_raster}."
                    )
                    self.atualizar_label_validacao(
                        self.dlg_flow_rout.label_24, 0)
                    self.atualizar_validação("validar_hietograma_bin", False)
                    return

                # Lê dados de precipitação
                total_valores = n_pixels * n_blocos
                dados = np.fromfile(f, dtype=np.float32, count=total_valores)

                if dados.size != total_valores:
                    aviso.close()
                    QMessageBox.critical(
                        self.dlg_flow_rout,
                        "Error",
                        "Unexpected end of file: number of precipitation values is inconsistent."
                    )
                    self.atualizar_label_validacao(
                        self.dlg_flow_rout.label_24, 0)
                    self.atualizar_validação("validar_hietograma_bin", False)
                    return

                # Valida se todos os valores são positivos
                if np.any(dados < 0):
                    aviso.close()
                    QMessageBox.critical(
                        self.dlg_flow_rout,
                        "Error",
                        "The file contains negative precipitation values."
                    )
                    self.atualizar_label_validacao(
                        self.dlg_flow_rout.label_24, 0)
                    self.atualizar_validação("validar_hietograma_bin", False)
                    return

            # Se chegou ate aqui, esta tudo certo
            aviso.close()
            QMessageBox.information(
                self.dlg_flow_rout, "OK", "Hyetograph binary file is valid."
            )
            self.atualizar_label_validacao(self.dlg_flow_rout.label_24, 1)
            self.atualizar_validação("validar_hietograma_bin", True)

        except Exception as e:
            aviso.close()
            QMessageBox.critical(self.dlg_flow_rout,
                                 "Unexpected Error", str(e))
            self.atualizar_label_validacao(self.dlg_flow_rout.label_24, 0)
            self.atualizar_validação("validar_hietograma_bin", False)

    def validar_regioes_interesse_raster(self):
        if not self.dlg_flow_rout.groupBox_2.isChecked():
            QMessageBox.warning(self.dlg_flow_rout, "Warning",
                                "Select the checkbox \"hydrograph estimation for different watershed classes\" first.")
            return

        try:
            raster_name = self.dlg_flow_rout.cb_4_pg2.currentText()
            if not raster_name:
                QMessageBox.warning(self.dlg_flow_rout,
                                    "Warning", "No raster selected.")
                self.atualizar_label_validacao(
                    self.dlg_flow_rout.label_37, '⚠️ Not selected')
                self.atualizar_validação(
                    "validar_regioes_interesse_raster", False)
                return

            layer = self.get_raster_layer_by_name(raster_name)
            if layer is None:
                QMessageBox.critical(
                    self.dlg_flow_rout, "Error", "Raster not found in the project.")
                self.atualizar_label_validacao(self.dlg_flow_rout.label_37, 0)
                self.atualizar_validação(
                    "validar_regioes_interesse_raster", False)
                return

            array = self.raster_to_array(layer)

            if array is None:
                QMessageBox.critical(self.dlg_flow_rout,
                                     "Error", "Failed to read raster data.")
                self.atualizar_label_validacao(self.dlg_flow_rout.label_37, 0)
                self.atualizar_validação(
                    "validar_regioes_interesse_raster", False)
                return

            valid_values = (array >= 0) & (np.floor(array) == array)
            basin_mask = ~np.isnan(array)

            if not np.all(valid_values[basin_mask]):
                QMessageBox.critical(
                    self.dlg_flow_rout, "Error", "Raster contains negative or non-integer values inside the basin.")
                self.atualizar_label_validacao(self.dlg_flow_rout.label_37, 0)
                self.atualizar_validação(
                    "validar_regioes_interesse_raster", False)
                return

            QMessageBox.information(
                self.dlg_flow_rout, "OK", "Regions of interest raster is valid.")
            self.atualizar_label_validacao(self.dlg_flow_rout.label_37, 1)
            self.atualizar_validação("validar_regioes_interesse_raster", True)

        except Exception as e:
            QMessageBox.critical(self.dlg_flow_rout,
                                 "Unexpected Error", str(e))
            self.atualizar_label_validacao(self.dlg_flow_rout.label_37, 0)
            self.atualizar_validação("validar_regioes_interesse_raster", False)
