from sentinel.analytics.registry import analyze

def detect(row,history,capacity):
    findings=[]
    def add(kind,severity,detail): findings.append(dict(kind=kind,severity=severity,detail=detail))
    if not row['available']: add('availability','critical','Node unreachable in simulated telemetry.')
    else:
        if row['cpu']>90: add('cpu','critical',f"CPU utilization {row['cpu']}% exceeds 90%.")
        if row['latency']>80: add('latency','high',f"Latency {row['latency']} ms exceeds 80 ms.")
        if row['loss']>2: add('packet_loss','high',f"Packet loss {row['loss']}% exceeds 2%.")
        if row['traffic']/capacity>0.85: add('capacity','high','Traffic exceeds 85% of provisioned capacity.')
        if len(history)>10:
            scores=analyze([x['cpu'] for x in history[-40:]])
            if abs(scores['robust_z'])>4 and row['cpu']>75:
                add('statistical','medium',f"CPU robust z-score {scores['robust_z']:.2f}. Statistical signal, not a confirmed fault.")
    return findings
