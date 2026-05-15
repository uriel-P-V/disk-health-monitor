#!/bin/bash
# check_disk.sh
# -------------
# Monitors disk usage and reports health status.
# Exits with code 1 if any disk is in warning or critical state.
#
# Usage:
#   ./scripts/check_disk.sh
#   ./scripts/check_disk.sh /home

# Configuration
WARNING_THRESHOLD=${WARNING_THRESHOLD:-80}
CRITICAL_THRESHOLD=${CRITICAL_THRESHOLD:-95}
PATH_TO_CHECK=${1:-"/"}

echo "========================================"
echo "  Disk Health Monitor"
echo "  Path: $PATH_TO_CHECK"
echo "  Warning threshold:  ${WARNING_THRESHOLD}%"
echo "  Critical threshold: ${CRITICAL_THRESHOLD}%"
echo "========================================"

# Get disk usage percentage
USAGE=$(df "$PATH_TO_CHECK" | awk 'NR==2 {print $(NF-1)}' | tr -d '%')

if [ -z "$USAGE" ]; then
    echo "ERROR: Could not read disk usage for $PATH_TO_CHECK"
    exit 1
fi

echo "  Current usage: ${USAGE}%"

# Classify status
if [ "$USAGE" -ge "$CRITICAL_THRESHOLD" ]; then
    STATUS="CRITICAL"
    EXIT_CODE=1
elif [ "$USAGE" -ge "$WARNING_THRESHOLD" ]; then
    STATUS="WARNING"
    EXIT_CODE=1
else
    STATUS="HEALTHY"
    EXIT_CODE=0
fi

echo "  Status: $STATUS"
echo "========================================"

exit $EXIT_CODE