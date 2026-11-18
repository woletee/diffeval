"""Call compute and record an error if it raises."""


def _record(name, value, status, error, higher, protocol, details=None) -> dict:
    return {"name": name, "value": value, "status": status, "error": error, "higher_is_better": higher, "details": details or {}, "protocol": protocol}


def safe_metric(metric, samples, context) -> dict:
    try:
        result = metric.compute(samples, context)
    except Exception as exc:
        higher = getattr(metric, "higher_is_better", None)
        return _record(metric.name, None, "error", str(exc), higher, getattr(metric, "protocol", {}))
    return _record(result.name, result.value, result.status, result.error, result.higher_is_better, result.protocol, result.details)
