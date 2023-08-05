#Henry Jacobson grudat20 ovn7

from matrix import Matrix,Vector

def main():
    A = Matrix(3,3)
    A.setVals([1,0,5,2,5,2,9,4,3])
    b = Matrix(3,1)
    b.setVals([0,2,3])
    I = Matrix(3,3)
    I.ID()
    assert 9 == A.Trace()
    assert A**2 == A*A
    assert A*A**-1 == I
    assert A**-1 == I*A**-1
    assert A**4*A**-8 == A**-4
    assert -178 == A.det()
    assert 13 == (b.Transpose()*b).vals[0]
    assert -b == b-2*b
    assert A != 2
    assert A.size() == [3,3]
    assert b.size() == [3,1]

    A = Matrix(2,4)
    A.setVals([1,1,1,1,1,2,3,4])
    A = A.Transpose()
    b = Matrix(4,1)
    b.setVals([6,5,7,10])
    res = Matrix(2,1)
    res.setVals([3.5,1.4]) #values from wikipedia when doing least square
    assert res == A.solveLin(b)
    assert res == A%b #same as A\b in Matlab
    assert A*2 == A+A

    A = Matrix(2,1)
    B = Matrix(2,1)
    C = Matrix(2,2)
    A.setVals([5,6])
    B.setVals([4,3])
    C.setVals([5,4,6,3])
    assert C == A.combMat(B)
    assert A == (C.splitMat(1))[0]
    assert B == (C.splitMat(1))[1]
    assert -9 == C.det()

    A = Matrix(2,2)
    B = Matrix(2,2)
    A.setVals([1,5,2,3])
    B.setVals([3,5,2,1])
    assert B*A != A*B
    assert 4 == (A+B).vals[0]

    v = Vector(3)
    u = Vector(3)
    w = Vector(2)
    z = Vector(1)
    v.setVals([1,3,7])
    u.setVals([5,3,-2])
    w.setVals([3,4])
    z.setVals([2])
    assert 5 == w.norm()
    assert 0 == u*v
    assert 0 == u*u.cross(v)
    assert 0 == v*u.cross(v)
    assert 0 == v.scalarProj(u.cross(v))
    assert 1 == (w.Normalize()).norm()
    assert 2 == z.norm()
    assert 600 == 150*z.norm()*2

    A = Matrix(2,2)
    x = Vector(2)
    A.setVals([3,0,0,3])
    x.setVals([2,1])
    assert 3*x == A*x

    A = Matrix(3,3)
    b = Vector(3)
    A.setVals([1,1,1,1,-2,1,1,1,-2])
    b.setVals([-2,1,1])
    C = A.solveLin(b)
    assert C[1] == -1 and C[2] == -1

    A = Matrix(8,8) #base we found in theoretical physics
    A.setVals([1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 0,1,1,1,0,0,0,0,\
         0,0,0,0,1,1,1,0, 0,1,-2,1,0,0,0,0, 0,1,1,-2,0,0,0,0, 0,0,0,0,1,-2,1,0, 0,0,0,0,1,1,-2,0])
    assert 0 != A.det()

if __name__=="__main__":
    main()