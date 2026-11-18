#!/usr/bin/env python3
import json
import re
from pathlib import Path

# Patch upstream _config.yml without touching any other byte.
config = Path('_config.yml').read_text(encoding='utf-8')
out = []
seen_title = False
seen_description = False
for line in config.splitlines(keepends=True):
    if re.match(r'^title\s*:', line):
        out.append('title: Riverwatch RW-390 Field Bulletin\n')
        seen_title = True
    elif re.match(r'^description\s*:', line):
        out.append('description: Public October watershed observations\n')
        out.append('email: watershed@riverwatch.example\n')
        seen_description = True
    elif re.match(r'^email\s*:', line):
        out.append('email: watershed@riverwatch.example\n')
    else:
        out.append(line)
if not seen_title or not seen_description:
    raise SystemExit('Expected unique title and description lines in _config.yml')
Path('_config.yml').write_text(''.join(out), encoding='utf-8')

about = (
    '---\n'
    'title: "Riverwatch RW-390 Field Bulletin"\n'
    'permalink: /\n'
    'layout: single\n'
    '---\n'
    '\n'
    '## October snapshot\n'
    'Seven public observations from three stations are included in this bulletin.\n'
    '\n'
    '## Field desk\n'
    'Field desk: watershed@riverwatch.example\n'
    '\n'
    '## Alerts\n'
    'Aster Creek and Cedar Reach meet the published alert threshold.\n'
)
Path('_pages/about.md').write_text(about, encoding='utf-8')

summary = {
    'survey_id': 'RW-390',
    'report_title': 'Riverwatch RW-390 Field Bulletin',
    'contact_email': 'watershed@riverwatch.example',
    'reading_count': 7,
    'station_count': 3,
    'stations': [
        {'station_code': 'S-A', 'station_name': 'Aster Creek', 'nitrate_average': 3.8, 'phosphate_average': 1.2},
        {'station_code': 'S-B', 'station_name': 'Birch Run', 'nitrate_average': 2.7, 'phosphate_average': 0.6},
        {'station_code': 'S-C', 'station_name': 'Cedar Reach', 'nitrate_average': 5.0, 'phosphate_average': 1.5},
    ],
    'alerts': [
        {'station_code': 'S-A', 'station_name': 'Aster Creek', 'nitrate_average': 3.8, 'phosphate_average': 1.2},
        {'station_code': 'S-C', 'station_name': 'Cedar Reach', 'nitrate_average': 5.0, 'phosphate_average': 1.5},
    ],
}
Path('_data').mkdir(parents=True, exist_ok=True)
Path('_data/rw-390-summary.json').write_text(
    json.dumps(summary, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')

readings = [
    ('S-A', 'Aster Creek', 'nitrate', '3.7', '2055-10-02T09:15:00Z', 'Q-10'),
    ('S-A', 'Aster Creek', 'nitrate', '3.9', '2055-10-09T10:20:00Z', 'Q-14'),
    ('S-A', 'Aster Creek', 'phosphate', '1.2', '2055-10-04T08:40:00Z', 'Q-12'),
    ('S-B', 'Birch Run', 'nitrate', '2.7', '2055-10-03T07:55:00Z', 'Q-11'),
    ('S-B', 'Birch Run', 'phosphate', '0.6', '2055-10-11T09:05:00Z', 'Q-15'),
    ('S-C', 'Cedar Reach', 'nitrate', '5.0', '2055-10-06T11:30:00Z', 'Q-16'),
    ('S-C', 'Cedar Reach', 'phosphate', '1.5', '2055-10-13T12:10:00Z', 'Q-17'),
]
csv_lines = ['station_code,station_name,metric,value,observed_at,reading_id']
for row in readings:
    csv_lines.append(','.join(row))
Path('downloads').mkdir(parents=True, exist_ok=True)
Path('downloads/rw-390-readings.csv').write_text('\n'.join(csv_lines) + '\n', encoding='utf-8')

alerts = (
    '# RW-390 field alerts\n'
    '\n'
    '- S-A \u2014 Aster Creek: nitrate 3.8, phosphate 1.2\n'
    '- S-C \u2014 Cedar Reach: nitrate 5.0, phosphate 1.5\n'
)
Path('downloads/rw-390-alerts.md').write_text(alerts, encoding='utf-8')

print('RW-390 files written')
