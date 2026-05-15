#!/bin/bash
# run_tests.sh
# ------------
# Runs the test suite and generates a summary report.
# Used in CI/CD pipelines and local development.
#
# Usage:
#   ./scripts/run_tests.sh              # run all tests
#   ./scripts/run_tests.sh smoke        # run by marker
#   ./scripts/run_tests.sh critical

MARKER=${1:-""}
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
REPORT_DIR="reports"
LOG_FILE="${REPORT_DIR}/test_run_${TIMESTAMP}.log"

mkdir -p "$REPORT_DIR"

echo "========================================"
echo "  Running Test Suite"
echo "  Timestamp: $TIMESTAMP"
echo "  Marker: ${MARKER:-all}"
echo "========================================"

# Run tests
if [ -n "$MARKER" ]; then
    pytest tests/ -v -m "$MARKER" | tee "$LOG_FILE"
else
    pytest tests/ -v | tee "$LOG_FILE"
fi

EXIT_CODE=${?}

# Summary
echo "========================================"
if [ $EXIT_CODE -eq 0 ]; then
    echo "  RESULT: PASSED ✓"
else
    echo "  RESULT: FAILED ✗"
fi
echo "  Log saved to: $LOG_FILE"
echo "========================================"

exit $EXIT_CODE