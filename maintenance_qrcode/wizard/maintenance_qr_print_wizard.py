# -*- coding: utf-8 -*-

from odoo import _, fields, models, api
from odoo.exceptions import UserError


class MaintenanceQrPrintWizard(models.TransientModel):
    _name = "maintenance.qr.print.wizard"
    _description = "Equipment QR Code Label Layout Wizard"

    size = fields.Selection(
        selection=[
            ("dymo", "Dymo"),
            ("2x7xprice", "2 x 7"),
            ("4x7xprice", "4 x 7"),
            ("custom", "Custom Columns"),
        ],
        required=True,
        default="2x7xprice",
        string="Format",
    )
    copies = fields.Integer(default=1, required=True, string="Quantity")
    equipment_ids = fields.Many2many("maintenance.equipment", string="Equipment")
    custom_columns = fields.Integer(
        "Number of Columns",
        default=2,
        required=True,
        help="Number of columns per page (e.g., 2 for 2 columns)",
    )
    custom_rows = fields.Integer(
        "Number of Rows",
        default=7,
        required=True,
        help="Number of rows per page (e.g., 7 for 7 rows)",
    )
    header_color = fields.Char(
        "Label Header Color",
        default="#6b4096",
        help="Color for the QR label header. Enter a hex color code (e.g., #6b4096 for purple)",
    )
    rows = fields.Integer(compute="_compute_dimensions")
    columns = fields.Integer(compute="_compute_dimensions")

    @api.depends("size", "custom_columns", "custom_rows")
    def _compute_dimensions(self):
        for wizard in self:
            if wizard.size == "custom":
                wizard.columns = wizard.custom_columns
                wizard.rows = wizard.custom_rows
            elif wizard.size in ("2x7xprice",):
                wizard.columns = 2
                wizard.rows = 7
            elif wizard.size in ("4x7xprice",):
                wizard.columns = 4
                wizard.rows = 7
            elif "x" in wizard.size:
                parts = wizard.size.split("x")[:2]
                wizard.columns = int(parts[0]) if parts[0].isdigit() else 1
                wizard.rows = int(parts[1]) if parts[1].isdigit() else 1
            else:
                wizard.columns, wizard.rows = 1, 1

    def _prepare_report_data(self):
        if self.copies <= 0:
            raise UserError(_("Quantity must be greater than zero."))

        if self.size == "custom":
            if self.custom_columns <= 0 or self.custom_rows <= 0:
                raise UserError(_("Columns and rows must be greater than zero."))

        if not self.equipment_ids:
            raise UserError(_("Please select at least one equipment."))

        data = {
            "size": self.size,
            "copies": self.copies,
            "header_color": self.header_color,
            "equipment_ids": self.equipment_ids.ids,
            "quantity_by_equipment": {str(eq.id): self.copies for eq in self.equipment_ids},
            "columns": self.columns,
            "rows": self.rows,
            "custom_columns": self.columns if self.size == "custom" else None,
            "custom_rows": self.rows if self.size == "custom" else None,
        }
        return data

    def action_print(self):
        self.ensure_one()
        data = self._prepare_report_data()
        report_action = self.env.ref(
            "maintenance_qrcode.action_report_maintenance_equipment_qr"
        )
        # Pass None for docids, all data via data dict (like asset_management does)
        return report_action.report_action(
            None,
            data=data,
            config=False
        )

    @api.model
    def default_get(self, fields_list):
        """Set default equipment from context (active_ids)"""
        res = super(MaintenanceQrPrintWizard, self).default_get(fields_list)
        if self.env.context.get("active_ids"):
            res["equipment_ids"] = [(6, 0, self.env.context.get("active_ids"))]
        return res

