import json, re

with open(r'c:\Users\misha\Downloads\NAMAZ\prayer_data.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

with open(r'c:\Users\misha\Downloads\NAMAZ\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

lines = ['const PRAYER_DB = {']
for date, times in db.items():
    lines.append(f'    "{date}":{{Fajr:"{times["Fajr"]}",Dhuhr:"{times["Dhuhr"]}",Asr:"{times["Asr"]}",Maghrib:"{times["Maghrib"]}",Isha:"{times["Isha"]}"}},')
lines.append('};')
new_db_block = '\n'.join(lines)

pattern = r'const PRAYER_DB = \{[\s\S]*?\};'
new_html = re.sub(pattern, new_db_block, html, count=1)

with open(r'c:\Users\misha\Downloads\NAMAZ\index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f'Done! {len(db)} entries embedded.')
print('First:', list(db.items())[0])
print('Last: ', list(db.items())[-1])
