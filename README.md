# Maintenance QR Code

Generate and print QR labels for equipment in Odoo Maintenance.

## Key Features
- Internal equipment code (`x_equipment_code`) with auto-sequence.
- Manual edit of equipment code by Equipment Manager.
- QR payload that opens equipment form directly in Odoo.
- QR preview tab on equipment form.
- Batch print labels from list/form actions.
- Label size presets:
  - A4 (3x8 labels)
  - 50x30 mm
  - 70x50 mm

## Business Flow
1. Open **Maintenance > Equipment**.
2. Create equipment or open an existing one.
3. Generate or manually edit `Equipment Code`.
4. Use **Action > Print QR Code**.
5. Select size/copies and print PDF labels.

## Security
- Code generation is restricted to `maintenance.group_equipment_manager`.
- Access to equipment data still follows standard Maintenance ACLs/rules.

## Technical Notes
- Module: `maintenance_qrcode`
- Depends on: `maintenance`
- No external Python package required (uses Odoo barcode/report stack).

## Installation
1. Copy module folder `maintenance_qrcode` into your custom addons path.
2. Restart Odoo.
3. Update Apps list.
4. Install module **Maintenance QR Code**.

## Upgrade
- Apps > search module > **Upgrade**
- or CLI: `-u maintenance_qrcode`

## Configuration
- Verify `web.base.url` points to your real server URL so scanned QR opens the correct host.

## Screenshots
Add screenshots under `static/description/` and reference them in `static/description/index.html`.

## License
LGPL-3

## Support
For support, include your contact details in manifest (`author`, `website`) and on Odoo Apps listing.
