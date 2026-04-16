import json, re

import openpyxl
wb = openpyxl.load_workbook(r'c:\Users\misha\Downloads\NAMAZ\kuttippuram_namaz_2026_full.xlsx')
ws = wb.active
rows = list(ws.iter_rows(values_only=True))
db = {}
for r in rows[1:]:
    date, fajr, dhuhr, asr, maghrib, isha = r
    if date:
        db[str(date)] = {'Fajr': str(fajr), 'Dhuhr': str(dhuhr), 'Asr': str(asr), 'Maghrib': str(maghrib), 'Isha': str(isha)}

with open(r'c:\Users\misha\Downloads\NAMAZ\prayer_data.json', 'w', encoding='utf-8') as f:
    json.dump(db, f)

print(f'prayer_data.json updated: {len(db)} entries')
print('Sample Jan 1:', db.get('2026-01-01'))
print('Sample Apr 16:', db.get('2026-04-16'))
