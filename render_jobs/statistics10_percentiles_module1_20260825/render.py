import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from main import Statistics10QuartilesDecilesPercentiles, SCORES, percentile


class Statistics10QuartilesDecilesPercentilesFinal(Statistics10QuartilesDecilesPercentiles):
    """Validated final scene wrapper using tolerance-based floating-point QA."""

    def validate_data(self):
        checks = [
            (percentile(SCORES, 25), (64.25, 3.25)),
            (percentile(SCORES, 50), (73.5, 5.5)),
            (percentile(SCORES, 75), (83.0, 7.75)),
            (percentile(SCORES, 80), (85.2, 8.2)),
            (percentile(SCORES, 30), (66.5, 3.7)),
            (percentile(SCORES, 70), (81.2, 7.3)),
        ]
        for got, expected in checks:
            assert abs(got[0] - expected[0]) < 1e-9
            assert abs(got[1] - expected[1]) < 1e-9
        assert abs(percentile([40,45,50,55,60,65,70,75,80], 75)[0] - 70) < 1e-9
        assert abs(percentile([60,65,70,75,80,85,90], 75)[0] - 82.5) < 1e-9
        assert abs(percentile([50,60,70,80,90,100,110], 75)[0] - 95) < 1e-9
        assert abs(percentile([10,12,14,16,18], 75)[0] - 16) < 1e-9
