#!/usr/bin/env python3
"""Strict, fail-closed instrumentation for a checked-out libCacheSim source.

Not a substitute for compiling and running equivalence tests on libCacheSim.
Run --check first, then --apply; optional --diff PATH writes an exact unified diff
based on the checkout being patched.
"""
import argparse
import difflib
from pathlib import Path
import re
import sys

ORIGINAL_INCLUDE = '#include "../../dataStructure/minimalIncrementCBF.h"'
ORIGINAL_FIELD = '  request_t *req_local;'
ORIGINAL_INIT = '  params->request_counter = 0;  // initialize request counter'
ORIGINAL_CLOSE = '  free_request(params->req_local);'
PATTERN = re.compile(
    r'if\s*\(minimalIncrementCBF_estimate\(params->CBF,\s*'
    r'\(void\s*\*\)&window_victim->obj_id,\s*'
    r'sizeof\(window_victim->obj_id\)\)\s*>\s*'
    r'minimalIncrementCBF_estimate\(params->CBF,\s*'
    r'\(void\s*\*\)&main_cache_victim->obj_id,\s*'
    r'sizeof\(main_cache_victim->obj_id\)\)\)\s*\{'
)
REPLACEMENT = '''const int freq_candidate = minimalIncrementCBF_estimate(
            params->CBF, (void *)&window_victim->obj_id,
            sizeof(window_victim->obj_id));
        const int freq_victim = minimalIncrementCBF_estimate(
            params->CBF, (void *)&main_cache_victim->obj_id,
            sizeof(main_cache_victim->obj_id));
        DEBUG_ASSERT(freq_candidate >= 0 && freq_victim >= 0);
        const bool date_admit = freq_candidate > freq_victim;
        date_logger_record(params->logger, (uint64_t)cache->n_req,
                           (uint64_t)req->obj_id,
                           (uint64_t)window_victim->obj_id,
                           (uint64_t)main_cache_victim->obj_id,
                           freq_candidate, freq_victim, date_admit);
        if (date_admit) {'''


def transform(source: str) -> str:
    if 'date_logger_record(' in source or '#include "date_admission_log.h"' in source:
        raise ValueError('already instrumented: refusing to instrument twice')
    for anchor in (ORIGINAL_INCLUDE, ORIGINAL_FIELD, ORIGINAL_INIT, ORIGINAL_CLOSE):
        if source.count(anchor) != 1:
            raise ValueError(f'anchor occurrence count !=1: {anchor}')
    if len(PATTERN.findall(source)) != 1:
        raise ValueError('could not identify exactly one W-TinyLFU comparator; verify pinned upstream')
    source = source.replace(ORIGINAL_INCLUDE,
                            ORIGINAL_INCLUDE+'\n#include "date_admission_log.h"')
    source = source.replace(ORIGINAL_FIELD,
                            ORIGINAL_FIELD+'\n  date_admission_logger_t *logger;')
    source = source.replace(ORIGINAL_INIT,
                            ORIGINAL_INIT+'\n  params->logger = date_logger_open_from_env();')
    source = source.replace(ORIGINAL_CLOSE,
                            '  if (date_logger_close(params->logger)) {\n'
                            '    fprintf(stderr, "DATE log close failed\\n");\n'
                            '  }\n'+ORIGINAL_CLOSE)
    source = PATTERN.sub(lambda _: REPLACEMENT, source, count=1)
    return source


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--checkout', type=Path, required=True)
    ap.add_argument('--check', action='store_true', help='verify anchors, do not modify checkout')
    ap.add_argument('--apply', action='store_true', help='apply exactly once to source and copy header')
    ap.add_argument('--diff', type=Path, help='write unified diff for source (valid for this checkout)')
    args = ap.parse_args()
    if not (args.check or args.apply or args.diff):
        ap.error('provide --check or --apply or --diff')
    path = args.checkout/'libCacheSim/cache/eviction/WTinyLFU.c'
    old = path.read_text()
    new = transform(old)
    header = Path(__file__).with_name('date_admission_log.h')
    if args.diff:
        args.diff.write_text(''.join(difflib.unified_diff(
            old.splitlines(True), new.splitlines(True),
            fromfile='a/libCacheSim/cache/eviction/WTinyLFU.c',
            tofile='b/libCacheSim/cache/eviction/WTinyLFU.c')))
    if args.apply:
        path.write_text(new)
        (path.parent/'date_admission_log.h').write_bytes(header.read_bytes())
    print(f'PASS anchors in {path}; generated replacement (not compiled).')

if __name__ == '__main__':
    main()
