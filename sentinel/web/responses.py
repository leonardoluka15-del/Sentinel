import json

def send(handler,body,status=200,content_type='application/json',filename=None):
    if not isinstance(body,bytes): body=json.dumps(body,allow_nan=False).encode()
    handler.send_response(status)
    handler.send_header('Content-Type',content_type)
    handler.send_header('Content-Length',str(len(body)))
    handler.send_header('Cache-Control','no-store')
    handler.send_header('X-Content-Type-Options','nosniff')
    handler.send_header('X-Frame-Options','DENY')
    handler.send_header('Referrer-Policy','no-referrer')
    handler.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; connect-src 'self'; img-src 'self' data:; frame-ancestors 'none'")
    if filename: handler.send_header('Content-Disposition',f'attachment; filename="{filename}"')
    handler.end_headers(); handler.wfile.write(body)
