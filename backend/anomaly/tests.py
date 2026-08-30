from io import BytesIO

import numpy as np
import pandas as pd
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase

from anomaly.ml.anomaly import run_anomaly_pipeline
from anomaly.ml.anomaly_model_factory import AnomalyModelFactory
from anomaly.services.evaluation_service import EvaluationService
from core.ml.dataset_analyzer import DatasetAnalyzer
from core.services.file_service import FileService


class FileServiceTests(SimpleTestCase):

    def test_rejects_non_csv_case_insensitively(self):
        file = SimpleUploadedFile("dataset.txt", b"a,b\n1,2\n")

        with self.assertRaisesMessage(ValueError, "Only CSV files are allowed."):
            FileService.validate_csv_file(file)

    def test_accepts_csv_extension_case_insensitively(self):
        file = SimpleUploadedFile("dataset.CSV", b"a,b\n1,2\n")
        FileService.validate_csv_file(file)

    def test_rejects_empty_csv(self):
        file = BytesIO(b"")
        file.name = "empty.csv"

        with self.assertRaisesMessage(ValueError, "CSV file is empty."):
            FileService.read_csv_file(file)

    def test_rejects_csv_with_empty_column_name(self):
        file = BytesIO(b",value\n1,2\n")
        file.name = "dataset.csv"

        with self.assertRaisesMessage(ValueError, "CSV file contains an empty column name."):
            FileService.read_csv_file(file)

    def test_reads_valid_csv(self):
        file = BytesIO(b"amount,score\n10,0.1\n20,0.2\n")
        file.name = "dataset.csv"

        df = FileService.read_csv_file(file)

        self.assertEqual(df.shape, (2, 2))
        self.assertListEqual(df.columns.tolist(), ["amount", "score"])


class ModelFactoryTests(SimpleTestCase):

    def test_supported_models_are_constructed(self):
        for model_name in ("isolation_forest", "lof", "svm", "one_class_svm", "dbscan"):
            with self.subTest(model_name=model_name):
                model = AnomalyModelFactory.get_model(model_name)
                self.assertIsNotNone(model)

    def test_rejects_invalid_contamination(self):
        for contamination in (0, -0.1, 0.5, 0.9):
            with self.subTest(contamination=contamination):
                with self.assertRaises(ValueError):
                    AnomalyModelFactory.get_model("isolation_forest", contamination)

    def test_rejects_unknown_model(self):
        with self.assertRaisesMessage(ValueError, "Unsupported anomaly model"):
            AnomalyModelFactory.get_model("does_not_exist")


class DatasetAnalyzerTests(SimpleTestCase):

    def test_detects_labelled_dataset(self):
        df = pd.DataFrame({"amount": [1, 2], "label": [0, 1]})
        result = DatasetAnalyzer.analyze(df)

        self.assertEqual(result["dataset_type"], "labelled")
        self.assertEqual(result["target_column"], "label")

    def test_detects_unlabelled_dataset(self):
        df = pd.DataFrame({"amount": [1, 2], "score": [0.1, 0.2]})
        result = DatasetAnalyzer.analyze(df)

        self.assertEqual(result["dataset_type"], "unlabelled")
        self.assertIsNone(result["target_column"])


class EvaluationServiceTests(SimpleTestCase):

    def test_evaluates_anomaly_counts_and_scores(self):
        predictions = np.array([1, 0, 1, 0])
        scores = np.array([0.1, 0.2, 0.8, 0.4])

        result = EvaluationService.evaluate(predictions, scores)

        self.assertEqual(result["total_records"], 4)
        self.assertEqual(result["anomaly_count"], 2)
        self.assertEqual(result["anomaly_percentage"], 50.0)
        self.assertEqual(result["average_score"], 0.375)
        self.assertEqual(result["lowest_score"], 0.1)

    def test_handles_no_score_array(self):
        result = EvaluationService.evaluate(np.array([0, 0]))
        self.assertNotIn("average_score", result)


class AnomalyPipelineTests(SimpleTestCase):

    def test_pipeline_handles_missing_and_infinite_values(self):
        df = pd.DataFrame({
            "amount": [10.0, np.nan, 12.0, np.inf, 11.0, 9.0],
            "frequency": [1.0, 2.0, np.nan, 4.0, 3.0, 2.0],
        })

        result = run_anomaly_pipeline(
            df=df,
            dataset_info=DatasetAnalyzer.analyze(df),
            model_name="isolation_forest",
            contamination=0.2,
            scaler_type="standard",
            dataset_name="test.csv",
        )

        result_df = result["df"]

        self.assertEqual(len(result_df), len(df))
        self.assertFalse(result_df["anomaly_score"].isna().any())
        self.assertTrue(result_df["result"].isin(["Normal", "Anomaly"]).all())
        self.assertIn("pca_x", result_df.columns)
        self.assertIn("pca_y", result_df.columns)

    def test_pipeline_handles_single_feature(self):
        df = pd.DataFrame({"amount": [1.0, 2.0, 3.0, 100.0]})

        result = run_anomaly_pipeline(
            df=df,
            dataset_info=DatasetAnalyzer.analyze(df),
            model_name="isolation_forest",
            contamination=0.25,
            scaler_type="standard",
            dataset_name="single-feature.csv",
        )

        self.assertEqual(result["df"]["pca_x"].shape[0], 4)
        self.assertEqual(result["df"]["pca_y"].shape[0], 4)


class SupervisedEvaluationTests(SimpleTestCase):

    def test_calculates_accuracy_precision_recall_f1_and_confusion_matrix(self):
        y_true = np.array([0, 0, 1, 1])
        predictions = np.array([0, 1, 1, 0])

        result = EvaluationService.evaluate(
            predictions=predictions,
            y_true=y_true,
        )

        self.assertEqual(result["accuracy"], 0.5)
        self.assertEqual(result["precision"], 0.5)
        self.assertEqual(result["recall"], 0.5)
        self.assertEqual(result["f1_score"], 0.5)
        self.assertEqual(
            result["confusion_matrix"],
            {
                "true_negative": 1,
                "false_positive": 1,
                "false_negative": 1,
                "true_positive": 1,
            },
        )

    def test_calculates_false_positive_and_negative_rates(self):
        result = EvaluationService.evaluate_supervised(
            y_true=np.array([0, 0, 0, 1]),
            predictions=np.array([0, 1, 0, 1]),
        )

        self.assertEqual(result["false_positive_rate"], round(1 / 3, 4))
        self.assertEqual(result["false_negative_rate"], 0.0)
        self.assertEqual(result["specificity"], round(2 / 3, 4))

    def test_accepts_common_text_labels(self):
        result = EvaluationService.evaluate_supervised(
            y_true=np.array(["normal", "anomaly", "normal", "fraud"]),
            predictions=np.array([0, 1, 0, 1]),
        )

        self.assertEqual(result["accuracy"], 1.0)
        self.assertEqual(result["precision"], 1.0)
        self.assertEqual(result["recall"], 1.0)
        self.assertEqual(result["f1_score"], 1.0)

    def test_rejects_unknown_labels(self):
        with self.assertRaisesMessage(ValueError, "Unsupported ground-truth label value"):
            EvaluationService.normalize_labels(
                np.array(["normal", "unknown"])
            )

    def test_rejects_missing_labels(self):
        with self.assertRaisesMessage(ValueError, "Ground-truth labels contain missing values."):
            EvaluationService.normalize_labels(
                np.array([0, np.nan])
            )

    def test_rejects_length_mismatch(self):
        with self.assertRaisesMessage(
            ValueError,
            "Ground-truth labels and predictions must have the same length.",
        ):
            EvaluationService.evaluate_supervised(
                y_true=np.array([0, 1]),
                predictions=np.array([0]),
            )


class BenchmarkServiceTests(SimpleTestCase):

    def test_benchmark_requires_target_column(self):
        from anomaly.services.benchmark_service import BenchmarkService

        df = pd.DataFrame({"amount": [1.0, 2.0, 3.0]})

        with self.assertRaisesMessage(ValueError, "Target column 'label' was not found."):
            BenchmarkService.compare_models(df, target_column="label")


class Phase2BenchmarkTests(SimpleTestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            "feature_a": [0.0, 0.2, 0.1, 0.3, 9.0, 8.5, 9.5, 0.1, 0.2, 8.8, 0.0, 0.1],
            "feature_b": [0.0, 0.1, 0.2, 0.1, 9.0, 8.2, 9.1, 0.2, 0.1, 8.7, 0.2, 0.1],
            "label": [0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0],
        })

    def test_model_comparison_contains_all_models(self):
        from anomaly.services.benchmark_service import BenchmarkService

        result = BenchmarkService.compare_models(
            self.df, target_column="label", contamination=0.25, seed=42
        )
        self.assertEqual(
            set(result["model"]),
            {"isolation_forest", "lof", "one_class_svm", "dbscan"},
        )
        self.assertTrue((result["f1_score"] >= 0).all())

    def test_contamination_experiment_records_each_setting(self):
        from anomaly.services.benchmark_service import BenchmarkService

        result = BenchmarkService.contamination_experiment(
            self.df,
            target_column="label",
            contaminations=(0.10, 0.20),
            models=("isolation_forest",),
        )
        self.assertEqual(len(result), 2)
        self.assertListEqual(
            sorted(result["contamination"].tolist()), [0.10, 0.20]
        )

    def test_threshold_experiment_records_thresholds(self):
        from anomaly.services.benchmark_service import BenchmarkService

        result = BenchmarkService.threshold_experiment(
            self.df,
            target_column="label",
            model_name="isolation_forest",
            quantiles=(0.90, 0.95),
        )
        self.assertEqual(len(result), 2)
        self.assertTrue(result["threshold"].notna().all())

    def test_weighted_ensemble_evaluation(self):
        from anomaly.services.benchmark_service import BenchmarkService

        result = BenchmarkService.ensemble_evaluation(
            self.df,
            target_column="label",
            models=("isolation_forest", "lof", "one_class_svm"),
            contamination=0.25,
        )
        self.assertEqual(result["model"], "weighted_ensemble")
        self.assertEqual(len(result["weights"]), 3)
        self.assertAlmostEqual(sum(result["weights"]), 1.0)

    def test_repeated_runs_have_seed_records(self):
        from anomaly.services.benchmark_service import BenchmarkService

        result = BenchmarkService.repeated_runs(
            self.df,
            target_column="label",
            seeds=(7, 42),
            models=("isolation_forest",),
        )
        self.assertEqual(result["seed"].tolist(), [7, 42])
        self.assertTrue(result["runtime_seconds"].ge(0).all())

    def test_statistical_summary_and_tests(self):
        from anomaly.services.benchmark_service import BenchmarkService
        from anomaly.services.benchmark_statistics import BenchmarkStatistics

        repeated = BenchmarkService.repeated_runs(
            self.df,
            target_column="label",
            seeds=(7, 21, 42),
            models=("isolation_forest", "lof", "one_class_svm"),
        )
        summary = BenchmarkStatistics.summarize(repeated)
        self.assertEqual(len(summary), 3)

        friedman = BenchmarkStatistics.friedman_test(repeated, metric="f1_score")
        self.assertIn("p_value", friedman)

        pairwise = BenchmarkStatistics.pairwise_wilcoxon(
            repeated, metric="f1_score"
        )
        self.assertEqual(len(pairwise), 3)

    def test_report_writer_creates_artifacts(self):
        from tempfile import TemporaryDirectory
        from anomaly.services.benchmark_report_service import BenchmarkReportService

        with TemporaryDirectory() as tmp:
            path = BenchmarkReportService.write_markdown(
                f"{tmp}/report.md",
                {"name": "test", "source": "test", "citation": "test",
                 "rows": 1, "features": 1, "label_mapping": "0/1"},
                pd.DataFrame({"model": ["test"], "f1_score": [1.0]}),
                pd.DataFrame(),
                pd.DataFrame(),
                {"model": "weighted_ensemble"},
                pd.DataFrame({"model": ["test"], "f1_score_mean": [1.0]}),
                {"p_value": 1.0},
                pd.DataFrame(),
            )
            self.assertTrue(path.endswith("report.md"))
            self.assertTrue(open(path, encoding="utf-8").read().startswith("# Anomaly Detection Benchmark Report"))
