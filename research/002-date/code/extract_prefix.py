#!/usr/bin/env python3
"""Extract a bounded, sanitized prefix of libCacheSim oracleGeneral (packed 24B) from zstd.

Requires curl and zstd on PATH. Reads only the first requested records; source SHA-256
is NOT computed because the whole source is intentionally not downloaded.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import struct
import subprocess

RECORD = struct.Struct('<IQIq')  # timestamp (u32), obj_id (u64), size (u32), next (i64)
assert RECORD.size == 24


def read_exact(pipe, size: int) -> bytes:
    data = bytearray()
    while len(data) < size:
        chunk = pipe.read(size - len(data))
        if not chunk:
            raise EOFError(f'Unexpected end of compressed stream after {len(data)} of {size} bytes')
        data.extend(chunk)
    return bytes(data)


def extract(source: str, output: Path, n: int) -> dict:
    if n <= 0:
        raise ValueError('records must be positive')
    output.parent.mkdir(parents=True, exist_ok=True)
    curl = subprocess.Popen(['curl', '-fLsS', '--', source], stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL)
    zstd = subprocess.Popen(['zstd', '-dc'], stdin=curl.stdout, stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL)
    assert curl.stdout and zstd.stdout
    curl.stdout.close()
    digest = hashlib.sha256()
    try:
        with output.open('wb') as handle:
            for _ in range(n):
                rec = read_exact(zstd.stdout, RECORD.size)
                timestamp, obj_id, _size, _next = RECORD.unpack(rec)
                # Object-unit experiment and guard against future-access information.
                safe = RECORD.pack(timestamp, obj_id, 1, -2)
                handle.write(safe)
                digest.update(safe)
    except Exception:
        output.unlink(missing_ok=True)
        raise
    finally:
        zstd.stdout.close()
        # Intentional early exit: terminate producers once prefix is complete.
        zstd.terminate()
        curl.terminate()
        try:
            zstd.wait(timeout=3)
        except subprocess.TimeoutExpired:
            zstd.kill(); zstd.wait()
        try:
            curl.wait(timeout=3)
        except subprocess.TimeoutExpired:
            curl.kill(); curl.wait()

    result = {
        'source_url': source,
        'source_full_sha256': None,
        'subset_sha256': digest.hexdigest(),
        'record_format': '<IQIq',
        'record_size_bytes': RECORD.size,
        'records': n,
        'subset_bytes': n * RECORD.size,
        'normalization': {'obj_size': 1, 'next_access_vtime': -2},
        'note': 'Prefix digest only; full-source integrity not verified',
    }
    output.with_suffix(output.suffix + '.manifest.json').write_text(
        json.dumps(result, indent=2, sort_keys=True) + '\n')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-url', required=True)
    parser.add_argument('--records', type=int, default=910000)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(extract(args.source_url, args.output, args.records), indent=2))
