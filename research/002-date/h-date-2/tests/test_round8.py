"""Independent exact-fraction regression checks for H-DATE-2 round 8."""
from fractions import Fraction as F
import unittest
from exact_window_certificates import risks

class Round8Tests(unittest.TestCase):
    def test_two_distinct_strict_local_minima(self):
        a,r=F(3,5),F(9,10)
        loss={w:risks(a,r,1,w)[1] for w in (3,5,7,9,11)}
        self.assertLess(loss[5],loss[3]);self.assertLess(loss[5],loss[7])
        self.assertLess(loss[9],loss[7]);self.assertLess(loss[9],loss[11])
        self.assertNotEqual(loss[5],loss[9])

    def test_more_incremental_value_can_have_higher_total_risk(self):
        a,r=F(4,5),F(9,10)
        risk3=risks(a,r,1,3)
        risk5=risks(a,r,1,5)
        self.assertEqual(risk3[2],0)
        self.assertEqual(risk5[2],F(84231,7812500))
        self.assertLess(risk3[1],risk5[1])

    def test_full_information_optimality_when_r_at_most_alpha(self):
        for a,r in [(F(4,5),F(7,10)),(F(4,5),F(4,5)),(F(3,5),F(11,20))]:
            optimum=(1-(2*a-1)**2*(2*r-1))/2
            for w in (3,5,9):
                coarse,fine,v=risks(a,r,1,w)
                self.assertEqual(fine,optimum)
                self.assertEqual(coarse,optimum)
                self.assertEqual(v,0)

    def test_short_one_long_three_has_zero_value(self):
        for a,r in [(F(3,5),F(9,10)),(F(4,5),F(9,10)),(F(4,5),F(99,100))]:
            self.assertEqual(risks(a,r,1,3)[2],0)

    def test_finite_budget_short_above_one(self):
        a,r=F(4,5),F(99,100)
        v=risks(a,r,5,11)[1]
        self.assertLess(v,min(risks(a,r,1,w)[1] for w in (3,5,7,9,11)))

    def test_exact_risks_quoted(self):
        a,r=F(3,5),F(9,10)
        self.assertEqual(risks(a,r,1,3)[1],F(15023,31250))
        self.assertEqual(risks(a,r,1,5)[1],F(3752687,7812500))
        self.assertEqual(risks(a,r,1,7)[1],F(375381287,781250000))
        self.assertEqual(risks(a,r,1,9)[1],F(938402710301,1953125000000))
        self.assertEqual(risks(a,r,1,11)[1],F(29350868166949,61035156250000))

if __name__=='__main__':unittest.main()