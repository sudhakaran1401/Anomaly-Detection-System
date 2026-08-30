"""
HTTP load test with no third-party dependency.

Example:
    python testing/performance/load/run_load_test.py \
      --url http://127.0.0.1:8000/ --requests 100 --workers 10
"""
import argparse
import concurrent.futures
import statistics
import time
import urllib.request


def one(url, timeout):
    start = time.perf_counter()
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            response.read(1024)
            return response.status, time.perf_counter() - start, None
    except Exception as exc:
        return None, time.perf_counter() - start, str(exc)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--requests", type=int, default=100)
    parser.add_argument("--workers", type=int, default=10)
    parser.add_argument("--timeout", type=float, default=10)
    args = parser.parse_args()

    started = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(lambda _: one(args.url, args.timeout), range(args.requests)))
    elapsed = time.perf_counter() - started

    latencies = [r[1] for r in results]
    errors = [r for r in results if r[0] is None]
    successes = [r for r in results if r[0] is not None and 200 <= r[0] < 500]

    print(f"requests={args.requests}")
    print(f"workers={args.workers}")
    print(f"elapsed_seconds={elapsed:.3f}")
    print(f"throughput_rps={args.requests / elapsed:.2f}")
    print(f"successes={len(successes)}")
    print(f"errors={len(errors)}")
    print(f"mean_latency_ms={statistics.mean(latencies)*1000:.2f}")
    print(f"p95_latency_ms={sorted(latencies)[max(0, int(len(latencies)*0.95)-1)]*1000:.2f}")


if __name__ == "__main__":
    main()
