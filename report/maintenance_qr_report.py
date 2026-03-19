# -*- coding: utf-8 -*-
from collections import defaultdict
from odoo import models


def _prepare_data(env, docids, data):
    """Prepare data for QR label report (asset label style)."""
    Equipment = env['maintenance.equipment']

    if not data:
        return {}

    qty_by_equipment_in = data.get('quantity_by_equipment') or {}
    if not qty_by_equipment_in:
        return {}

    total = 0
    equipment_ids = [int(eid) for eid in qty_by_equipment_in.keys()]
    equipments = Equipment.search([('id', 'in', equipment_ids)], order='name desc')
    quantity_by_equipment = defaultdict(list)

    for equipment in equipments:
        q = qty_by_equipment_in.get(str(equipment.id), 0)
        if not q:
            continue
        qr_value = equipment.x_qr_payload or ''
        quantity_by_equipment[equipment].append((qr_value, q))
        total += q

    size = data.get('size')
    if size == '2x7xprice':
        columns, rows = 2, 7
    elif size == '4x7xprice':
        columns, rows = 4, 7
    elif size == 'dymo':
        columns, rows = 1, 1
    elif size == 'custom':
        columns = data.get('custom_columns') or data.get('columns') or 2
        rows = data.get('custom_rows') or data.get('rows') or 7
    else:
        columns = data.get('columns') or 1
        rows = data.get('rows') or 1
    header_color = data.get('header_color', '#6b4096')

    return {
        'quantity': quantity_by_equipment,
        'page_numbers': (total - 1) // (rows * columns) + 1 if (rows * columns) > 0 else 1,
        'columns': columns,
        'rows': rows,
        'header_color': header_color,
    }


class ReportMaintenanceEquipmentQr(models.AbstractModel):
    _name = 'report.maintenance_qrcode.report_maintenance_equipment_qr'
    _description = 'Maintenance Equipment QR Label Report'

    def _get_report_values(self, docids, data):
        return _prepare_data(self.env, docids, data)
