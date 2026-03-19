# -*- coding: utf-8 -*-
{
    "name": "Maintenance QR Code",
    "summary": "Generate and print QR labels for maintenance equipment",
    "description": """
Maintenance QR Code
===================

Features:
- Auto/manual equipment code for maintenance equipment.
- QR payload and QR preview on equipment form.
- Batch print QR labels from list/form actions.
- Label size presets: A4 3x8, 50x30 mm, 70x50 mm.
""",
    "version": "19.0.1.0.0",
    "category": "Supply Chain/Maintenance",
    "author": "thanhcao",
    "maintainer": "thanhcao",
    "website": "https://github.com",
    "license": "LGPL-3",
    "depends": ["maintenance"],
    "data": [
        "security/ir.model.access.csv",
        "data/sequence.xml",
        "views/maintenance_equipment_views.xml",
        "views/maintenance_qr_wizard_views.xml",
        "report/maintenance_qr_templates.xml",
        "report/maintenance_qr_report.xml",
    ],
    "installable": True,
    "application": False,
}
