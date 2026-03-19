# Maintenance QR Code (Odoo 19)

Generate and print QR labels for Maintenance Equipment in Odoo.

## Overview

This module extends `maintenance.equipment` with:

- Internal equipment code (`x_equipment_code`) generated from sequence.
- QR payload URL that opens the equipment form directly.
- QR preview block on equipment form.
- Label print wizard with multiple layouts.

The module is designed for fast equipment lookup in operations, warehouse, and maintenance teams.

## Main Features

- Auto-generate equipment code per company sequence.
- Manual code generation button for Equipment Managers.
- Unique code validation (no duplicate equipment code).
- QR label wizard from equipment form/list header button.
- Label layout options:
  - `Dymo` (single label style)
  - `2 x 7`
  - `4 x 7`
  - `Custom Columns` (user-defined rows/columns)
- Configurable label header color.

## Usage

1. Go to **Maintenance > Equipment**.
2. Create/open equipment.
3. Generate equipment code (manager role) if empty.
4. Click **Equipment QR Label**.
5. Select format, quantity, and print PDF.

## Security

- Code generation is restricted to `maintenance.group_equipment_manager`.
- Record access follows standard Odoo Maintenance ACL/rules.

## Technical Information

- Technical name: `maintenance_qrcode`
- Version: `19.0.1.0.0`
- License: `LGPL-3`
- Dependency: `maintenance`
- External Python libraries: none

## Installation

1. Put module folder `maintenance_qrcode` in custom addons path.
2. Restart Odoo service.
3. Update Apps list.
4. Install **Maintenance QR Code**.

## Upgrade

- UI: Apps → search `Maintenance QR Code` → **Upgrade**
- CLI: `odoo -d <db_name> -u maintenance_qrcode`

## Notes for Production

- Set `web.base.url` correctly so scanned QR opens the correct host.
- Validate PDF output with your real printer settings (paper scaling disabled).

## License

LGPL-3
