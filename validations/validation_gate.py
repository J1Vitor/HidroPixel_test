"""Gatekeeper for Hidropixel data-validation steps.

Este modulo expõe funcões que verificam se todas as checagens do Data Validation
Tool foram realizadas e se todas retornaram sucesso antes de liberar a execucao
das simulacões dos diferentes modulos do Hidropixel.

Uso:
    from validations.validation_gate import ensure_validations_pass
    ok = ensure_validations_pass(self.hidropixel, module=1, parent=self.dlg_flow_tt)

Retorna True somente se todas as checagens obrigatorias existirem em
'hidropixel.validations' e tiverem valor True. Caso contrário mostra um
QMessageBox detalhando o que falta ou o que falhou.
"""
from qgis.PyQt.QtWidgets import QMessageBox

# Lista de checagens obrigatorias por modulo.
# Assumimos algumas chaves que o codigo do plugin usa via atualizar_validacao(...).
REQUIRED_CHECKS = {
    1: [  # Flow Travel Time
        'validar_raster_bacia',
        'validar_raster_mde',
        'validar_direcoes_fluxo',
        'verificar_dimensoes_rasters',
        'validar_uso_cobertura',
        'validar_tabela_manning_lulc',
        'verificar_conectividade_rede',
        'verificar_acumulado_drenagem',
        'executar_validacao_fluxo',
    ],
    2: [  # Excess Rainfall
        'validar_raster_bacia',
        'validar_raster_cn',
        'verificar_dimensoes_rasters',
    ],
    3: [  # Flow Routing
        'verificar_tempos_de_viagem',
        'verificar_chuva_excedente_total',
        'validar_hietograma_bin',
        'validar_regioes_interesse_raster',
        'verificar_dimensoes_rasters',
    ],
}

# Map internal validation keys to human-friendly labels used in the UI/messages
label_mensagem = {
    'validar_raster_bacia': 'Validate Basin Raster',
    'validar_raster_mde': 'Validate DEM',
    'validar_direcoes_fluxo': 'Validate Flow Directions',
    'verificar_dimensoes_rasters': 'Validate Dimensions',
    'validar_uso_cobertura': 'LULC Validation',
    'validar_tabela_manning_lulc': "LULC Classes Validation",
    'verificar_conectividade_rede': 'RDN Validation',
    'verificar_acumulado_drenagem': 'Validate Drainage Areas',
    'executar_validacao_fluxo': 'Validate Flow Directions',
    'validar_raster_cn': 'Validate CN',
    'verificar_tempos_de_viagem': 'Validate Travel Time',
    'verificar_chuva_excedente_total': 'Validate Excess Rainfall',
    'validar_hietograma_bin': 'Validate Hyetograph',
    'validar_regioes_interesse_raster': 'Validate ROI'
}


def ensure_validations_pass(hidropixel, module, parent=None):
    """Verifica se todas as validacões obrigatorias para 'module' foram
    executadas e tiveram sucesso.

    Args:
        hidropixel: instância principal do plugin (deve expor 'validations' dict).
        module: int {1,2,3} - identifica o modulo (1: FT, 2: Excess Rain, 3: Flow Rout).
        parent: QWidget opcional usado como pai para QMessageBox.

    Returns:
        bool: True se todas as validacões obrigatorias existirem e forem True.

    Efeitos colaterais:
        - Mostra QMessageBox informando quais validacões estao faltando ou falharam.
        - Nao altera o dicionário 'hidropixel.validations'.
    """
    if not hasattr(hidropixel, 'validations') or not isinstance(hidropixel.validations, dict):
        QMessageBox.critical(parent, 'Validation Gate',
                             'Internal error: plugin has no validations registry.')
        return False

    if module not in REQUIRED_CHECKS:
        QMessageBox.warning(parent, 'Validation Gate',
                            f'Unknown module: {module}')
        return False

    # Work on a copy so we can adjust required checks dynamically
    required = list(REQUIRED_CHECKS[module])

    # Special-case: for Flow Routing (module 3) the ROI check
    # ('validar_regioes_interesse_raster') is only required when
    # the Flow Routing dialog has groupBox_2 checked AND the
    # cb_4_pg2 control is not empty/None (i.e. user selected an ROI input).
    # We use the provided `hidropixel` instance (expected to expose
    # `dlg_flow_rout`) to inspect the current GUI state. If any of the
    # attributes are missing we assume the check is not required.
    if module == 3 and 'validar_regioes_interesse_raster' in required:
        try:
            dlg = getattr(hidropixel, 'dlg_flow_rout', None)
            group_box_checked = False
            cb_has_value = False
            if dlg is not None:
                gb = getattr(dlg, 'groupBox_2', None)
                cb = getattr(dlg, 'cb_4_pg2', None)
                if gb is not None and callable(getattr(gb, 'isChecked', None)):
                    group_box_checked = gb.isChecked()
                # cb may be a QgsMapLayerComboBox or similar; check currentText or currentLayer
                if cb is not None:
                    # Prefer currentText (string), fall back to currentLayer existence
                    try:
                        text = cb.currentText()
                        cb_has_value = (text is not None and text != '')
                    except Exception:
                        # Not all combo-like widgets implement currentText; try currentLayer
                        try:
                            layer = cb.currentLayer()
                            cb_has_value = (layer is not None)
                        except Exception:
                            cb_has_value = False

            # If either group box is unchecked or cb has no value, then ROI check is not required
            if not (group_box_checked and cb_has_value):
                required = [r for r in required if r !=
                            'validar_regioes_interesse_raster']
        except Exception:
            # On any unexpected error inspecting the dialog, be conservative and treat the ROI
            # check as not required to avoid blocking the user due to UI inspection issues.
            required = [r for r in required if r !=
                        'validar_regioes_interesse_raster']
    missing = [k for k in required if k not in hidropixel.validations]
    failed = [k for k in required if hidropixel.validations.get(k) is False]

    if missing or failed:
        lines = []
        if missing:
            lines.append('Pending checks (not executed):')
            for k in missing:
                lines.append(f'  - {label_mensagem.get(k, k)}')
        if failed:
            lines.append('Failed checks:')
            for k in failed:
                lines.append(f'  - {label_mensagem.get(k, k)}')

        msg = '\n'.join(lines)
        QMessageBox.critical(parent or None, 'Data Validation', msg)
        return False

    return True


def all_modules_ready(hidropixel, parent=None):
    """Checa todos os modulos (1,2,3). Retorna um dicionário com o status de
    cada modulo e um booleano agregado.

    Retorno:
        (ready_all, detail)
        ready_all: bool - True se todos os modulos estiverem prontos.
        detail: dict - mapeia modulo -> (ok: bool, missing:list, failed:list)
    """
    results = {}
    overall = True
    for module, reqs in REQUIRED_CHECKS.items():
        missing = [k for k in reqs if k not in getattr(
            hidropixel, 'validations', {})]
        failed = [k for k in reqs if getattr(
            hidropixel, 'validations', {}).get(k) is False]
        ok = (not missing) and (not failed)
        results[module] = {'ok': ok, 'missing': missing, 'failed': failed}
        if not ok:
            overall = False

    if not overall:
        # constroi mensagem resumida
        lines = ['Validation summary:']
        for module, info in results.items():
            if info['ok']:
                lines.append(f'  Module {module}: OK')
            else:
                parts = []
                if info['missing']:
                    parts.append(f'missing: {info["missing"]}')
                if info['failed']:
                    parts.append(f'failed: {info["failed"]}')
                lines.append(f'  Module {module}: ' + '; '.join(parts))

        QMessageBox.critical(
            parent or None, 'Data Validation', '\n'.join(lines))

    return overall, results


__all__ = ['ensure_validations_pass', 'all_modules_ready', 'REQUIRED_CHECKS']
