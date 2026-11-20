import sys
from pathlib import Path
import numpy as np
import pytest

sys.path.insert(0,str(Path(__file__).parents[1]/'src'))
from stats import minimum_benefit_test,partial_conjunction_2_of_3
from apply_logger import transform

UPSTREAM_MIN = '''#include "../../dataStructure/minimalIncrementCBF.h"
typedef struct WTinyLFU_params { request_t *req_local; } T;
  request_t *req_local;
  params->request_counter = 0;  // initialize request counter
  free_request(params->req_local);
if (minimalIncrementCBF_estimate(params->CBF,
                                         (void *)&window_victim->obj_id,
                                         sizeof(window_victim->obj_id)) >
            minimalIncrementCBF_estimate(params->CBF,
                                         (void *)&main_cache_victim->obj_id,
                                         sizeof(main_cache_victim->obj_id))) {
'''

def test_patcher_fails_closed():
    with pytest.raises(ValueError):transform('bad unrelated upstream')

def test_patcher_replaces_once():
    out=transform(UPSTREAM_MIN)
    assert out.count('date_logger_record(')==1
    assert 'if (date_admit) {' in out
    with pytest.raises(ValueError):transform(out)

def test_partial_conjunction():
    assert partial_conjunction_2_of_3([.001,.02,.8])==.04
    assert partial_conjunction_2_of_3([.001,.06,.06])==.12
    with pytest.raises(ValueError): partial_conjunction_2_of_3([.1,.2])

def test_negative_effect_bootstrap_does_not_false_claim():
    n=8192
    t=np.arange(n)
    baseline=np.full(n,1.0)
    treatment=np.full(n,1.02)
    result=minimum_benefit_test(t,baseline,treatment,n_requests=n,block_length=128,reps=299)
    assert result.p_one_sided>.1

def test_large_improvement_detected():
    n=8192
    rng=np.random.default_rng(12)
    x=np.maximum(0.01,1+rng.normal(0,.15,size=n))
    t=np.arange(n)
    result=minimum_benefit_test(t,x,.9*x,n_requests=n,block_length=128,reps=299)
    assert result.p_one_sided<.025
    assert result.estimated_relative_benefit==pytest.approx(.1)

def test_same_request_multiple_events_and_density():
    t=np.array([1,1,1,15,15,100,100,100,100])
    l2=np.array([3.,3.,3.,1.,1.,2.,2.,2.,2.])
    l3=l2.copy()
    result=minimum_benefit_test(t,l2,l3,n_requests=128,block_length=16,reps=299)
    assert result.mean_loss_baseline==pytest.approx(l2.mean())
    assert result.estimated_relative_benefit==pytest.approx(0)

def test_denominator_zero_and_bad_time():
    with pytest.raises(ValueError):minimum_benefit_test(np.arange(100),np.zeros(100),np.ones(100),n_requests=100,block_length=10)
    with pytest.raises(ValueError):minimum_benefit_test(np.array([10,9]),np.ones(2),np.ones(2),n_requests=20,block_length=4)

def test_determinism():
    n=2048; t=np.arange(n); x=np.ones(n); y=.9*np.ones(n)
    a=minimum_benefit_test(t,x,y,n_requests=n,block_length=32,reps=299,seed=12)
    b=minimum_benefit_test(t,x,y,n_requests=n,block_length=32,reps=299,seed=12)
    assert a==b
