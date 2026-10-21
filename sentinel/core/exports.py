import csv
import io
import json

def csv_bytes(rows):
    out=io.StringIO(newline='')
    if rows:
        writer=csv.DictWriter(out,fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    return out.getvalue().encode('utf-8-sig')

def report_bytes(snapshot):
    return json.dumps(snapshot,indent=2,allow_nan=False).encode()
