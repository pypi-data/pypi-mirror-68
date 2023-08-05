import numpy.testing as nt
import unittest

from spatialmath.base.vectors import *
import spatialmath.base as tr
from spatialmath.base.quaternions import *
        
class TestQuaternion(unittest.TestCase):
    def test_ops(self):
        nt.assert_array_almost_equal(eye(), np.r_[1,0,0,0])

        nt.assert_array_almost_equal(pure(np.r_[1,2,3]), np.r_[0,1,2,3])
        nt.assert_array_almost_equal(pure([1,2,3]), np.r_[0,1,2,3])
        nt.assert_array_almost_equal(pure((1,2,3)), np.r_[0,1,2,3])
        
        nt.assert_equal(qnorm(np.r_[1,2,3,4]), math.sqrt(30))
        nt.assert_equal(qnorm([1,2,3,4]), math.sqrt(30))
        nt.assert_equal(qnorm((1,2,3,4)), math.sqrt(30))
                        
        nt.assert_array_almost_equal(unit(np.r_[1,2,3,4]), np.r_[1,2,3,4]/math.sqrt(30))
        nt.assert_array_almost_equal(unit([1,2,3,4]), np.r_[1,2,3,4]/math.sqrt(30))
        
        nt.assert_array_almost_equal(qqmul(np.r_[1,2,3,4],np.r_[5,6,7,8]), np.r_[-60,12,30,24])
        nt.assert_array_almost_equal(qqmul([1,2,3,4],[5,6,7,8]), np.r_[-60,12,30,24])
        nt.assert_array_almost_equal(qqmul(np.r_[1,2,3,4],np.r_[1,2,3,4]), np.r_[-28,4,6,8])
        
        nt.assert_array_almost_equal(matrix(np.r_[1,2,3,4])@np.r_[5,6,7,8], np.r_[-60,12,30,24])
        nt.assert_array_almost_equal(matrix([1,2,3,4])@np.r_[5,6,7,8], np.r_[-60,12,30,24])
        nt.assert_array_almost_equal(matrix(np.r_[1,2,3,4])@np.r_[1,2,3,4], np.r_[-28,4,6,8])
        
        nt.assert_array_almost_equal(pow(np.r_[1,2,3,4],0), np.r_[1,0,0,0])
        nt.assert_array_almost_equal(pow(np.r_[1,2,3,4],1), np.r_[1,2,3,4])
        nt.assert_array_almost_equal(pow([1,2,3,4],1), np.r_[1,2,3,4])
        nt.assert_array_almost_equal(pow(np.r_[1,2,3,4],2), np.r_[-28,4,6,8])
        nt.assert_array_almost_equal(pow(np.r_[1,2,3,4],-1), np.r_[1,-2,-3,-4])
        nt.assert_array_almost_equal(pow(np.r_[1,2,3,4],-2), np.r_[-28,-4,-6,-8])
        
        nt.assert_equal(isequal(np.r_[1,2,3,4], np.r_[1,2,3,4]), True)
        nt.assert_equal(isequal(np.r_[1,2,3,4], np.r_[5,6,7,8]), False)
        nt.assert_equal(isequal(np.r_[1,1,0,0]/math.sqrt(2), np.r_[-1,-1,0,0]/math.sqrt(2)), True)
        
        s = qprint(np.r_[1,1,0,0], file=None)
        nt.assert_equal(isinstance(s,str), True)
        nt.assert_equal(len(s) > 2, True)
        s = qprint([1,1,0,0], file=None)
        nt.assert_equal(isinstance(s,str), True)
        nt.assert_equal(len(s) > 2, True)
        
        nt.assert_equal(qprint([1,2,3,4], file=None), "1.000000 < 2.000000, 3.000000, 4.000000 >")
        
        nt.assert_equal( isunitvec( rand()), True)
        
    def test_rotation(self):
        # rotation matrix to quaternion
        nt.assert_array_almost_equal(r2q(tr.rotx(180,'deg')), np.r_[0,1,0,0])
        nt.assert_array_almost_equal(r2q(tr.roty(180,'deg')), np.r_[0,0,1,0])
        nt.assert_array_almost_equal(r2q(tr.rotz(180,'deg')), np.r_[0,0,0,1])
        
        # quaternion to rotation matrix
        nt.assert_array_almost_equal(q2r(np.r_[0,1,0,0]), tr.rotx(180,'deg'))
        nt.assert_array_almost_equal(q2r(np.r_[0,0,1,0]), tr.roty(180,'deg'))
        nt.assert_array_almost_equal(q2r(np.r_[0,0,0,1]), tr.rotz(180,'deg'))
        
        nt.assert_array_almost_equal(q2r([0,1,0,0]), tr.rotx(180,'deg'))
        nt.assert_array_almost_equal(q2r([0,0,1,0]), tr.roty(180,'deg'))
        nt.assert_array_almost_equal(q2r([0,0,0,1]), tr.rotz(180,'deg'))
        
        # quaternion - vector product
        nt.assert_array_almost_equal(qvmul(np.r_[0,1,0,0], np.r_[0,0,1]), np.r_[0,0,-1])
        nt.assert_array_almost_equal(qvmul([0,1,0,0], [0,0,1]), np.r_[0,0,-1])

    def test_slerp(self):
        q1 = np.r_[0,1,0,0]
        q2 = np.r_[0,0,1,0]
        
        nt.assert_array_almost_equal(slerp(q1, q2, 0), q1)
        nt.assert_array_almost_equal(slerp(q1, q2, 1), q2)
        nt.assert_array_almost_equal(slerp(q1, q2, 0.5), np.r_[0,1,1,0]/math.sqrt(2))
        
        q1 = [0,1,0,0]
        q2 = [0,0,1,0]
        
        nt.assert_array_almost_equal(slerp(q1, q2, 0), q1)
        nt.assert_array_almost_equal(slerp(q1, q2, 1), q2)
        nt.assert_array_almost_equal(slerp(q1, q2, 0.5), np.r_[0,1,1,0]/math.sqrt(2))
    
    def test_rotx(self):
         pass

if __name__ == '__main__':
    unittest.main()
