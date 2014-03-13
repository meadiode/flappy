

cdef extern from "Matrix.h" namespace "lime":
    cdef cppclass Matrix:
        Matrix(double inSX=1,double inSY=1, double inTX=0, double inTY=0)
        
        bool IsIdentity()
        Matrix Mult(const Matrix &inLHS)
        Matrix Inverse()

        double m00, m01, mtx
        double m10, m11, mty