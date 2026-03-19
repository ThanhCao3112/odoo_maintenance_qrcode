# Odoo Apps Pre-Submit Checklist (Maintenance QR Code)

## 1) Package & Metadata
- [ ] Folder name = technical name: `maintenance_qrcode`
- [ ] `__manifest__.py` has correct `name`, `summary`, `version`, `license`, `depends`
- [ ] Version matches target series (example: `19.0.x.y.z`)
- [ ] No absolute/local paths in code
- [ ] No duplicate/legacy files left in package

## 2) Code Quality
- [ ] No traceback on install/upgrade
- [ ] No debug prints, temp code, commented legacy blocks
- [ ] Access rights and business rules are consistent
- [ ] XML IDs are unique and stable

## 3) Functional Validation
- [ ] Install module on clean DB
- [ ] Create equipment, auto-generate code works
- [ ] Manual edit code works (manager)
- [ ] Duplicate code is blocked by unique constraint
- [ ] `Equipment QR Label` button works from list and form header
- [ ] All label sizes render correctly in PDF
- [ ] QR scan opens correct equipment record
- [ ] Wizard supports `Dymo`, `2x7`, `4x7`, and `Custom`

## 4) Security & Permissions
- [ ] Non-manager cannot generate code
- [ ] Manager can generate/edit code
- [ ] Existing maintenance ACL/rules are not broken

## 5) Multi-company
- [ ] Sequence behavior verified for multiple companies
- [ ] Record access follows company rules

## 6) UX & Report
- [ ] Report has no unwanted invoice-like header/footer
- [ ] Label content includes code + name (+ category if required)
- [ ] Fonts and spacing remain readable in print
- [ ] No obsolete entries appear in Action/Print gear menu

## 7) Odoo Apps Listing Assets
- [ ] `README.md` completed
- [ ] `static/description/index.html` completed and clean
- [ ] `static/description/icon.(png|jpg|svg)` available
- [ ] Add real screenshots in `static/description/` (optional but recommended)
- [ ] App listing text is consistent with actual features

## 8) Upload Dry Run
- [ ] Zip contains only module folder at root
- [ ] Test zip install on staging server
- [ ] Upload to Odoo Apps and check parser warnings

## 9) Release Artifacts
- [ ] Tag release in VCS
- [ ] Keep changelog entry for this version
- [ ] Backup previous stable package
