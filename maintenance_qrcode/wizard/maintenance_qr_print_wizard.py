# -*- coding: utf-8 -*-

from odoo import _, fields, models
from odoo.exceptions import UserError


class MaintenanceQrPrintWizard(models.TransientModel):
    _name = "maintenance.qr.print.wizard"
    _description = "Maintenance QR Print Wizard"

    equipment_ids = fields.Many2many("maintenance.equipment", string="Equipment")
    size = fields.Selection(
        selection=[
            ("a4_3x8", "A4 - 3 x 8 labels"),
            ("50x30", "Label 50 x 30 mm"),
            ("70x50", "Label 70 x 50 mm"),
        ],
        required=True,
        default="a4_3x8",
        string="Label Size",
    )
    copies = fields.Integer(default=1, required=True)

    def action_print(self):
        self.ensure_one()
        if self.copies < 1:
            raise UserError(_("Copies must be greater than zero."))

        equipments = self.equipment_ids
        if not equipments:
            active_ids = self.env.context.get("active_ids", [])
            equipments = self.env["maintenance.equipment"].browse(active_ids)
        if not equipments:
            raise UserError(_("Please select at least one equipment."))

        report_action = self.env.ref("maintenance_qrcode.action_report_maintenance_equipment_qr")
        return report_action.report_action(
            equipments,
            data={
                "size": self.size,
                "copies": self.copies,
            },
        )
