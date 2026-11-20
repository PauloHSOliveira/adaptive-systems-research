"""Benchmark correctness first; CPU numbers are Python-specific and preliminary."""
import argparse
import json
import time
import sys

def metadata_bytes_snapshot(obj):
    """Approximate recursive CPython allocation size of policy state (not process RSS)."""
    seen = set()
    def size(x):
        if id(x) in seen: return 0
        seen.add(id(x))
        total = sys.getsizeof(x)
        if isinstance(x, dict):
            for k, v in x.items(): total += size(k) + size(v)
        elif isinstance(x, (list, tuple, set, frozenset)):
            for v in x: total += size(v)
        elif hasattr(x, "__slots__"):
            for field in x.__slots__:
                if hasattr(x, field): total += size(getattr(x, field))
        elif hasattr(x, "__dict__"):
            total += size(vars(x))
        return total
    return size(obj)

from .core import SketchAdmissionCache, LRUCache, ExactLFUCache
from .workloads import events

def run_one(scenario, n, seed, cache_size, sketch_size, epoch, policy):
    if policy == 'lru':
        instance = LRUCache(cache_size)
    elif policy == 'lfu_exact':
        instance = ExactLFUCache(cache_size)
    else:
        mode = 'cert' if policy.startswith('cabs') else 'point'
        holdoff = 200 if policy == 'cabs_holdoff' else 0
        instance = SketchAdmissionCache(cache_size, sketch_size, epoch, mode, holdoff)
    start = time.perf_counter_ns()
    for key, weight in events(scenario, n, seed):
        instance.request(key, weight)
    elapsed = time.perf_counter_ns() - start
    return dict(scenario=scenario, seed=seed, policy=policy, n=n,
                weighted_miss_cost=round(instance.weighted_misses, 2),
                miss_ratio=round(instance.misses/n, 6),
                switches=instance.switches, bypasses=instance.bypasses,
                cpu_ns_per_req=round(elapsed/n, 1),
                metadata_bytes_snapshot=metadata_bytes_snapshot(instance),
                cert_admissions=getattr(instance,'certified',0),
                sketch_entries=sketch_size if policy in ('cabs', 'cabs_holdoff', 'point') else None)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--n',type=int,default=50_000)
    p.add_argument('--seeds',type=int,default=3)
    p.add_argument('--k',type=int,default=100)
    p.add_argument('--m',type=int,default=500)
    p.add_argument('--epoch',type=int,default=10_000)
    p.add_argument('--output',default='results.json')
    args=p.parse_args()
    scenarios=('stationary','uniform','drift','reset_churn')
    policies=('lru','lfu_exact','point','cabs','cabs_holdoff')
    results=[]
    for scenario in scenarios:
        for seed in range(args.seeds):
            for policy in policies:
                results.append(run_one(scenario,args.n,seed,args.k,args.m,args.epoch,policy))
    with open(args.output,'w') as f:
        json.dump(dict(config=vars(args),results=results),f,indent=2)
    print('Wrote',args.output, 'with',len(results),'runs')
    for scenario in scenarios:
        print('\n',scenario)
        for policy in policies:
            subset=[r['weighted_miss_cost'] for r in results if r['scenario']==scenario and r['policy']==policy]
            print('%14s mean weighted miss cost: %.1f'%(policy,sum(subset)/len(subset)))

if __name__ == '__main__':
    main()
