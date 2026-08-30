from django.test import SimpleTestCase

from anomaly.services.performance_service import PerformanceService


class Phase4PerformanceTests(SimpleTestCase):

    def test_benchmark_is_reproducible_shape(self):
        first = PerformanceService.benchmark(sizes=(20,), random_state=42)
        second = PerformanceService.benchmark(sizes=(20,), random_state=42)

        self.assertEqual(
            [(r["dataset_size"], r["model"]) for r in first],
            [(r["dataset_size"], r["model"]) for r in second],
        )
        self.assertEqual(len(first), 4)

    def test_benchmark_records_runtime_and_memory(self):
        results = PerformanceService.benchmark(sizes=(20,), random_state=42)
        for result in results:
            self.assertGreaterEqual(result["runtime_seconds"], 0)
            self.assertGreater(result["peak_memory_mb"], 0)
