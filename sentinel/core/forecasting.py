from sentinel.analytics.registry import analyze

def forecast(history,capacity):
    values=[r['traffic']/capacity*100 for r in history[-36:]]
    stats=analyze(values)
    point=max(0,stats['forecast']); uncertainty=1.96*stats['forecast_error']*(6**0.5)
    return {'utilization_next_6_samples':round(point,2),'lower':round(max(0,point-uncertainty),2),
            'upper':round(point+uncertainty,2),'risk':'high' if point>85 else 'normal',
            'method':'Linear least squares; heuristic interval from persistence errors, not calibrated probability.'}
