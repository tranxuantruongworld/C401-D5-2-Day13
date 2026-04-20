# Added by Member F (Công)
import yaml
import os
from .logging_config import get_logger
from .metrics import snapshot

log = get_logger()

def load_alert_rules():
    rules_path = os.path.join("config", "alert_rules.yaml")
    if not os.path.exists(rules_path):
        return []
    with open(rules_path, "r") as f:
        data = yaml.safe_load(f)
        return data.get("alerts", [])

def check_alerts():
    """
    Checks the current metrics snapshot against the alert rules.
    Logs a warning for each triggered alert.
    """
    rules = load_alert_rules()
    current_metrics = snapshot()
    
    for rule in rules:
        condition = rule.get("condition")
        name = rule.get("name")
        
        # Simple parser for condition string like "latency_p95_ms > 5000 for 30m"
        parts = condition.split()
        if len(parts) < 3:
            continue
            
        metric_name = parts[0]
        operator = parts[1]
        
        # Added by Member F (Công) - Handle non-numeric thresholds
        try:
            threshold = float(parts[2])
        except (ValueError, TypeError):
            continue
            
        # Map yaml metric name to snapshot metric name
        metric_map = {
            "latency_p95_ms": "latency_p95",
            "error_rate_pct": "error_rate_pct",
            "hourly_cost_usd": "total_cost_usd"
        }
        
        actual_metric_name = metric_map.get(metric_name)
        if not actual_metric_name:
            continue
            
        if actual_metric_name not in current_metrics:
            if metric_name == "error_rate_pct":
                traffic = current_metrics.get("traffic", 0)
                errors = sum(current_metrics.get("error_breakdown", {}).values())
                actual_value = (errors / traffic * 100) if traffic > 0 else 0
            else:
                continue
        else:
            actual_value = current_metrics[actual_metric_name]
        
        triggered = False
        if operator == ">":
            triggered = actual_value > threshold
        elif operator == "<":
            triggered = actual_value < threshold
            
        if triggered:
            log.warning(
                "alert_triggered",
                alert_name=name,
                condition=condition,
                actual_value=actual_value,
                runbook=rule.get("runbook")
            )
