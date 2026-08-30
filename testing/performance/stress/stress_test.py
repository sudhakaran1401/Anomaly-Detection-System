"""
HTTP concurrency stress test.

Escalates concurrency and reports throughput, latency, errors,
error rate, and the first observed degradation point.

Example:
    python testing/performance/stress/stress_test.py \
      --url http://127.0.0.1:8000/ --requests 500

This is a generic HTTP/server concurrency test. It does not perform
ADS authentication or execute anomaly/classification workflows.
Those application-level workflows are covered by the Locust load test.
"""

import argparse
import concurrent.futures
import statistics
import time
import urllib.request


DEFAULT_WORKERS = (5, 10, 25, 50, 100)


def request(url, timeout):
    start = time.perf_counter()
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            response.read(256)
            return response.status, time.perf_counter() - start, None
    except Exception as exc:
        return None, time.perf_counter() - start, str(exc)


def run(url, total, workers, timeout):
    started = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(
            pool.map(
                lambda _: request(url, timeout),
                range(total),
            )
        )

    elapsed = time.perf_counter() - started
    latencies = [duration for _, duration, _ in results]
    errors = [result for result in results if result[0] is None]

    successes = [
        result
        for result in results
        if result[0] is not None and 200 <= result[0] < 400
    ]

    throughput = total / elapsed if elapsed > 0 else 0.0
    error_rate = (len(errors) / total * 100) if total else 0.0

    sorted_latencies = sorted(latencies)
    p95_index = max(0, int(len(sorted_latencies) * 0.95) - 1)
    p95 = sorted_latencies[p95_index] if sorted_latencies else 0.0

    mean_latency = statistics.mean(latencies) if latencies else 0.0

    return {
        "workers": workers,
        "requests": total,
        "elapsed": elapsed,
        "throughput": throughput,
        "successes": len(successes),
        "errors": len(errors),
        "error_rate": error_rate,
        "mean_latency": mean_latency,
        "p95_latency": p95,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--requests", type=int, default=500)
    parser.add_argument("--timeout", type=float, default=10)
    args = parser.parse_args()

    if args.requests <= 0:
        parser.error("--requests must be greater than 0")

    results = []

    print(f"URL: {args.url}")
    print(f"Requests per level: {args.requests}")
    print(f"Timeout: {args.timeout:.1f}s")
    print()

    for workers in DEFAULT_WORKERS:
        result = run(
            args.url,
            args.requests,
            workers,
            args.timeout,
        )
        results.append(result)

        print(
            f"workers={result['workers']} "
            f"requests={result['requests']} "
            f"elapsed={result['elapsed']:.2f}s "
            f"throughput_rps={result['throughput']:.2f} "
            f"successes={result['successes']} "
            f"errors={result['errors']} "
            f"error_rate={result['error_rate']:.2f}% "
            f"mean_latency_ms={result['mean_latency'] * 1000:.2f} "
            f"p95_latency_ms={result['p95_latency'] * 1000:.2f}"
        )

    first_degradation = next(
        (
            result
            for result in results
            if result["errors"] > 0
        ),
        None,
    )

    print()
    if first_degradation:
        print(
            "first_degradation: "
            f"workers={first_degradation['workers']} "
            f"error_rate={first_degradation['error_rate']:.2f}%"
        )
    else:
        print("first_degradation: none observed")


if __name__ == "__main__":
    main()
