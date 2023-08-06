import asyncio
import argparse
import sys

import aioredis

from aioredis_watchdog import watchdog


async def stdout_callback(key: str, value: bytes):
    print("[*] Modified key: ", key, "#", value.decode("UTF-8"))


async def pipeline_callback_stdout(key: str, value: bytes):
    print(key, value.decode("UTF-8"), flush=True)


async def pipeline_callback_stderr(key: str, value: bytes):
    print(key, value.decode("UTF-8"), file=sys.stderr, flush=True)


async def _main(args):
    cs = args.redis_connection_string
    count = args.count
    quiet = args.quiet
    pattern = args.redis_pattern
    pipeline = args.pipeline

    if pipeline:
        standard_output = sys.stderr
        callbacks = [pipeline_callback_stdout]

        if not quiet:
            callbacks.append(pipeline_callback_stderr)
    else:
        standard_output = sys.stdout
        callbacks = [stdout_callback]

    redis = await aioredis.create_redis_pool(cs)

    if not quiet:
        print(f"[*] Starting monitoring '{cs}'", file=standard_output)

    if not quiet and count > 0:
        print(f"[*] Monitoring '{count}' changes", file=standard_output)

    await watchdog(pattern, callbacks, redis, count)


def main():
    parser = argparse.ArgumentParser(
        description='Redis Watchdog cli'
    )
    parser.add_argument("-s", "--redis-connection-string",
                        default="redis://localhost",
                        help="redis connection string")
    parser.add_argument("-r", "--redis-pattern",
                        default="*",
                        help="redis pattern")
    parser.add_argument("-c", "--count",
                        default=-1,
                        type=int,
                        help="maximum number of changes to watch")
    parser.add_argument("-q", "--quiet",
                        action="store_true",
                        default=False,
                        help="quiet mode")
    parser.add_argument("-P", "--pipeline",
                        action="store_true",
                        default=False,
                        help="pipeline mode")

    parsed = parser.parse_args()

    asyncio.run(_main(parsed))


if __name__ == '__main__':
    main()
