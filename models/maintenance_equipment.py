# -*- coding: utf-8 -*-

from urllib.parse import quote_plus

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError


class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"

    _MOJIBAKE_MARKERS = ("Ã", "Â", "Ä", "áº", "á»", "Ä‘", "â", "�")

    x_equipment_code = fields.Char(
        string="Equipment Code",
        copy=False,
        index=True,
        tracking=True,
        help="Internal unique code generated from sequence.",
    )
    x_qr_payload = fields.Char(
        string="QR Payload",
        compute="_compute_qr_fields",
        help="Raw value encoded in QR.",
    )
    x_qr_url = fields.Char(
        string="QR URL",
        compute="_compute_qr_fields",
        help="QR image endpoint URL.",
    )
    x_qr_image_html = fields.Html(
        string="QR Preview",
        compute="_compute_qr_fields",
        sanitize=False,
    )
    x_qr_name_display = fields.Char(
        string="QR Name Display",
        compute="_compute_qr_name_display",
        help="Equipment name normalized for QR label printing.",
    )
    x_qr_name_entities = fields.Char(
        string="QR Name Entities",
        compute="_compute_qr_name_display",
        help="Equipment name converted to HTML entities for safe PDF rendering.",
    )

    _x_equipment_code = models.Constraint(
        "unique(x_equipment_code)",
        "Another equipment already exists with this Equipment Code!",
    )

    @api.depends("x_equipment_code", "company_id")
    def _compute_qr_fields(self):
        base_url = (self.env["ir.config_parameter"].sudo().get_param("web.base.url") or "").rstrip("/")
        for record in self:
            if not record.id:
                record.x_qr_payload = False
                record.x_qr_url = False
                record.x_qr_image_html = False
                continue

            # Prefer internal code in URL for readability, but record id is sufficient for routing.
            record_url = f"{base_url}/web#id={record.id}&model=maintenance.equipment&view_type=form"
            record.x_qr_payload = record_url
            encoded = quote_plus(record_url)
            qr_url = f"/report/barcode/?barcode_type=QR&value={encoded}&width=220&height=220"
            record.x_qr_url = qr_url
            record.x_qr_image_html = (
                '<div class="o_maintenance_qr_preview">'
                f'<img src="{qr_url}" alt="QR Code" style="max-width:220px;max-height:220px;"/>'
                "</div>"
            )

    @api.depends("name")
    def _compute_qr_name_display(self):
        for record in self:
            normalized = record._repair_mojibake(record.name) or record.name or ""
            record.x_qr_name_display = normalized
            record.x_qr_name_entities = ''.join(f'&#{ord(ch)};' for ch in normalized)

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record, vals in zip(records, vals_list):
            if not vals.get("x_equipment_code"):
                record._assign_equipment_code_if_needed()
        return records

    def _assign_equipment_code_if_needed(self):
        sequence = self.env["ir.sequence"]
        for record in self.filtered(lambda r: not r.x_equipment_code):
            company = record.company_id or self.env.company
            record.x_equipment_code = sequence.with_company(company).next_by_code("maintenance.equipment.code")

    def action_generate_equipment_code(self):
        if not self.env.user.has_group("maintenance.group_equipment_manager"):
            raise AccessError(_("Only Equipment Managers can generate equipment codes."))

        generated = 0
        for record in self:
            if not record.x_equipment_code:
                record._assign_equipment_code_if_needed()
                generated += 1

        if not generated:
            raise UserError(_("Selected equipment already has code."))
        return True

    def action_open_qr_print_wizard(self):
        action = self.env.ref("maintenance_qrcode.action_maintenance_qr_print_wizard").read()[0]
        action["context"] = {
            "active_model": "maintenance.equipment",
            "active_ids": self.ids,
            "default_equipment_ids": [(6, 0, self.ids)],
        }
        return action

    def _repair_mojibake(self, text):
        """Best-effort fix for common UTF-8 decoded as latin1 strings in reports."""
        if not text or not isinstance(text, str):
            return text
        if not any(marker in text for marker in self._MOJIBAKE_MARKERS):
            return text
        for source_encoding in ("cp1252", "latin1"):
            try:
                repaired = text.encode(source_encoding, errors="ignore").decode("utf-8", errors="ignore")
                if repaired and not any(marker in repaired for marker in self._MOJIBAKE_MARKERS):
                    return repaired
            except UnicodeError:
                continue
        try:
            repaired = text.encode("latin1", errors="ignore").decode("utf-8", errors="ignore")
            if repaired:
                return repaired
        except UnicodeError:
            pass
        return text

    def _qr_display_text(self, text):
        self.ensure_one()
        return self._repair_mojibake(text)

    def _qr_display_html_entities(self, text):
        self.ensure_one()
        display_text = self._repair_mojibake(text) or ""
        return "".join(f"&#{ord(ch)};" for ch in display_text)

    def _qr_display_code(self):
        self.ensure_one()
        return self.x_equipment_code or self.serial_no or "-"
