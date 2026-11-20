import unittest
from fractions import Fraction
from exact_window_certificates import value,risks
from certify_monotonic_width import certify,F3,F4
from hmm_window_value import value as fast_value

class Round6Tests(unittest.TestCase):
    def test_original_r09_global_value_exact(self):
        v,_,_=value(Fraction(4,5),Fraction(9,10),1,5)
        self.assertEqual(v,Fraction(84231,7812500))
    def test_a08_r09_w5_beats_all_w_in_conjectured_range(self):
        base=value(Fraction(4,5),Fraction(9,10),1,5)[0]
        for w in range(11,31,2):
            self.assertGreater(base,value(Fraction(4,5),Fraction(9,10),1,w)[0])
    def test_window_short_five_positive_at_r099(self):
        a,r=Fraction(4,5),Fraction(99,100)
        self.assertGreater(value(a,r,5,11)[0],0)
        for w in range(3,12,2):
            self.assertEqual(value(a,r,1,w)[0],0)
    def test_risk_decomposition(self):
        a,r=Fraction(4,5),Fraction(99,100)
        for s,w in ((1,11),(5,11),(1,5)):
            coarse,fine,delta=risks(a,r,s,w)
            self.assertEqual(coarse-fine,delta)
            self.assertEqual(delta,value(a,r,s,w)[0])
    def test_numeric_dp_and_exact(self):
        for a,r,s,w in [(Fraction(4,5),Fraction(9,10),1,5),
                        (Fraction(4,5),Fraction(99,100),5,11),
                        (Fraction(3,5),Fraction(19,20),5,11)]:
            self.assertAlmostEqual(fast_value(float(a),float(r),s,w).value,
                                   float(value(a,r,s,w)[0]),places=13)
    def test_root_certified_monotonicity(self):
        assert certify(128)[0]
        assert certify(256)[0]
    def test_polynomial_root_witness_at_u_zero(self):
        self.assertEqual(F3(Fraction(3,5),Fraction(0)),Fraction(-434,625))
        self.assertEqual(F4(Fraction(3,5),Fraction(0)),Fraction(191,625))

if __name__=='__main__':unittest.main()