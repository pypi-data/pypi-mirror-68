#Henry Jacobson grudat20 projekt

import math

class SizeError(Exception):
    """Exception for wrong size of matrices."""

class Matrix:
    """A class implementing linear algebra matrices and
        typical functions available for matrices."""

    def __init__(self,rows,columns):
        """Initialize matrix with a number of rows and columns."""
        if not isinstance(rows, int) or not isinstance(columns,int):
            raise TypeError("Only integer value for columns and rows for matrix.")
        if (rows < 0 or columns < 0):
            print("Size error: negative sizes")
            exit(0)
        self.r = rows
        self.c = columns
        self.vals = [None]*rows*columns

    def setVals(self,values):
        """Give values to matrix in list values row by row left to right."""
        if not isinstance(values,list):
            raise TypeError("Matrix values need to be in a list.")
        for i in values:
            if not isinstance(i,(float,int)):
                raise TypeError("Matrix values need to be real numbers.")
        if (self.r*self.c != len(values)):
            return
        self.vals = values

    def zero(self):
        """Makes the matrix a zero matrix."""
        for i in range(self.r*self.c):
            self.vals[i] = 0

    def ID(self):
        """Makes the matrix an identity matrix."""
        if (self.r != self.c):
            print("Size error: {}x{} is not square".format(self.r,self.c))
            exit(0)
        for i in range(self.r*self.c):
            if (i%(self.c+1) == 0):
                self.vals[i] = 1
            else:
                self.vals[i] = 0

    def __str__(self):
        """Defines string of matrix object."""
        if (self.r == 0 or self.c == 0):
            return ""
        n=10 #this n should equal the expression after the colon in line (***)
        out = " _"+" "*n*(self.c)+" "*2*(self.c-1)+" "*3+"_\n"
        for i in range(self.r):
            out += "\uFF5c"
            for j in range(self.c):
                out += " " + '{:10.4f}'.format(self.vals[j+i*self.c]) + " " # (***)
            out += " \uFF5c\n" 
        out += " \u203E"+" "*n*(self.c)+" "*2*(self.c-1)+" "*3+"\u203E"
        return out

    def __add__(self,other):
        """Returns addition of two matrices."""
        if (self.r != other.r or self.c != other.c):
            raise SizeError("Size error: {}x{} vs {}x{}".format(self.r,self.c,other.r,other.c))
        array_out = [0]*self.r*self.c
        for i in range(self.r):
            indx = i*self.c
            for j in range(self.c):
                array_out[indx] = self.vals[indx]+other.vals[indx]
                indx += 1
        out = Matrix(self.r,self.c)
        out.setVals(array_out)
        return out 

    def __mul__(self,other):
        """Returns multiplication of two matrices or a matrix with a factor."""
        if isinstance(other, Matrix):
            if (self.c != other.r):
                raise SizeError("Size error: Can not perform multiplication of {}x{} vs {}x{}".format(self.r,self.c,other.r,other.c))
            array_out = [0]*self.r*other.c
            for i in range(self.r*other.c):
                indx_val = 0
                for j in range(self.c):
                    indx_val += self.vals[j+self.c*(i//other.c)]*other.vals[other.c*j+i%other.c]
                array_out[i] = indx_val
            out = Matrix(self.r,other.c)
            out.setVals(array_out)
            return out
        elif isinstance(other,(int,float)):
            array_out = [0]*self.r*self.c
            for i in range(self.r):
                indx = i*self.c
                for j in range(self.c):
                    array_out[indx] = self.vals[indx]*other
                    indx += 1
            out = Matrix(self.r,self.c)
            out.setVals(array_out)
            return out
        raise TypeError("Multiplication only valid between matrices or with real numbers.")

    __rmul__ = __mul__

    def __truediv__(self,other):
        """Returns multiplication by other inverse to the right or 
            division by factor."""
        if isinstance(other, Matrix):
            if (self.c != other.c or other.c != other.r):
                raise SizeError("Size error: Can not perform multiplication by inverse of {}x{} vs {}x{}".format(self.r,self.c,other.r,other.c))
            return self*(other**-1)
        elif isinstance(other,(int,float)):
            return self*(1/other)
        raise TypeError("Division only valid with real numbers or inverse of matrix.")

    def __neg__(self):
        """Returns changed sign of all values in matrix."""
        array_out = [0]*self.r*self.c
        for i in range(self.r):
            indx = i*self.c
            for j in range(self.c):
                array_out[indx] = -self.vals[indx]
                indx += 1
        out = Matrix(self.r,self.c)
        out.setVals(array_out)
        return out

    def __sub__(self,other):
        """Returns difference of two matrices."""
        return self+(-other)

    def __pow__(self,factor):
        """Raises a matrix to an whole number or takes inverse 
            if factor is negative one."""
        if not isinstance(factor,int):
            raise SizeError("Can only raise matrix to real numbers.")
        if (self.c != self.r):
            raise SizeError("Size error: {}x{} is not square.".format(self.r,self.c))
        if (factor < 0):
            part1 = Matrix(self.r,self.c)
            part1.ID()
            part = self.solveLin(part1)
        else:
            part = self
        if abs(factor) == 1:
            return part
        out = part*part
        for i in range(abs(factor)-2):
            out = out*part
        return out

    def __mod__(self,other):
        """Returns multiplication of self inverse from the right to other if
            matrix, otherwise takes modulus of each element in self.""" 
        if isinstance(other, Matrix):
            out = self.solveLin(other)
            return out #same as Matlabs A\b
        elif isinstance(other,int):
            out = Matrix(self.r,self.c)
            for i in range(self.r*self.c):
                out.vals[i] = self.vals[i]%other
            return out
        raise TypeError("Modulus takes in an integer or matrix argument.")

    def __eq__(self,other):
        """Checks if matrices are equal at every position."""
        try:
            if (self.r != other.r or self.c != other.c):
                return False
            n=10 #catch rounding erros
            for i in range(self.r*self.c):
                self.vals[i] = round(self.vals[i],n)
                other.vals[i] = round(other.vals[i],n)
                if (self.vals[i] != other.vals[i]):
                    return False
            return True
        except AttributeError:
            return False

    def __getitem__(self,index):
        """The value at the index in the matrix, counting by rows first."""
        if self.c*self.r-1 < index or index<0:
            raise IndexError("Index not in matrix.")
        return self.vals[index]

    def size(self):
        """The size of the matrix in a list, columns and rows.""" 
        out = [self.r,self.c]
        return out

    def Transpose(self):
        """Returns transpose of the matrix, swapping rows with columns."""
        out = Matrix(self.c,self.r)
        for i in range(self.c*self.r):
            out.vals[i%self.c*self.r+i//self.c] = self.vals[i]
        return out

    def Trace(self):
        """Returns the trace of the matrix, sum of all diagonal elements."""
        if (self.c != self.r):
            raise SizeError("Size error: {}x{} is not square.".format(self.r,self.c))
        out = 0
        for i in range(self.c):
            out += self.vals[i+i*self.c]
        return out

    def combMat(self,other):
        """Returns the two matrices in a singular matrix, side by side."""
        if (self.r != other.r):
            raise SizeError("Size error: Can not combine {}x{} with {}x{} side by side.".format(self.r,self.c,other.r,other.c))
        tot_c = self.c+other.c
        out = Matrix(self.r,tot_c)
        for i in range(self.r):
            for j in range(self.c):
                out.vals[i*tot_c+j] = self.vals[i*self.c+j]
            for j in range(other.c):
                out.vals[i*tot_c+self.c+j] = other.vals[i*other.c+j]
        return out

    def splitMat(self,col):
        """Splits the matrix by column col and returns the objects in a list."""
        out1 = Matrix(self.r,col)
        out2 = Matrix(self.r,self.c-col)
        for i in range(self.r):
            for j in range(col):
                out1.vals[i*col+j] = self.vals[i*self.c+j]
            for j in range(self.c-col):
                out2.vals[i*(self.c-col)+j] = self.vals[i*self.c+(self.c-col)+j]
        out = [out1,out2]
        return out

    def __rowSwap(self,row1,row2):
        """Swaps places of row1 and row2."""
        try:
            for i in range(self.c):
                temp = self.vals[i+(row1-1)*self.c]
                self.vals[i+(row1-1)*self.c] = self.vals[i+(row2-1)*self.c]
                self.vals[i+(row2-1)*self.c] = temp
        except IndexError:
            print("Not valid rows in matrix.")
        except TypeError:
            print("Rows must be integer numbers.")

    def __rowAdd(self,row1,row2,factor):
        """Adds row2*factor to row1."""
        try:
            for i in range(self.c):
                self.vals[i+row2*self.c] += self.vals[i+row1*self.c]*factor
        except:
            print("Rows must be integer numbers and factor needs to be a number.")

    def __rowMult(self,row,factor):
        """Multiplies a row by factor."""
        try:
            for i in range(self.c):
                self.vals[i+row*self.c] *= factor
                if self.vals[i+row*self.c] == 0:
                    self.vals[i+row*self.c] = 0 #dont want negative 0
        except:
            print("Rows must be integer numbers and factor needs to be a number.")

    def solveLin(self,other):
        """Solves self*x=other and returns x for each solution for
            each column in other."""
        try:
            if (self.c != other.r):
                new_left_side = self.Transpose()*self
                new_right_side = self.Transpose()*other
                out = new_left_side.solveLin(new_right_side)
                return out
            partial = self.__gaussElimination(other)
            out = partial[0].__jordanElimination(partial[1])
            return out[1]
        except AttributeError:
            print("Other must be a matrix.")

    def __gaussElimination(self,other):
        """Returns the gaussian elimination of self and other in 
            self*x = other."""
        c = self.c
        r = self.r
        out = Matrix(other.r,other.c)
        copy = Matrix(r,c)
        for i in range(other.r*other.c):
            out.vals[i] = other.vals[i]
        for i in range(r*c):
            copy.vals[i] = self.vals[i]
        for i in range(r-1):
            if (copy.vals[i*c+i] == 0): #row starts with 0, so swap with another
                for j in range(1,r-i): #search remaining rows
                    if (copy.vals[i*c+i+j*c] != 0):
                        row2 = (i*c+i+j*c)//c+1
                        copy.__rowSwap(i+1,row2)
                        out.__rowSwap(i+1,row2)
                        break
            for j in range(r-i-1):
                if (copy.vals[i%c+c*(j+1)+i*c] == 0 or copy.vals[i%c+i*c] == 0): #already 0 at value to be reduced or 0 to start with
                    continue 
                factor = -copy.vals[i%c+c*(j+1)+i*c] / copy.vals[i%c+i*c] 
                copy.__rowAdd((i%c+i*c)//c, (i%c+c*(j+1)+i*c)//c , factor)
                out.__rowAdd((i%c+i*c)//c, (i%c+c*(j+1)+i*c)//c, factor)
        out = [copy,out]
        return out
    
    def __jordanElimination(self,other):
        """Returns the jordan elimination of self and other in 
            self*x = other."""
        r = self.r
        c = self.c
        out = Matrix(other.r,other.c)
        copy = Matrix(r,c)
        for i in range(other.r*other.c):
            out.vals[i] = other.vals[i]
        for i in range(r*c):
            copy.vals[i] = self.vals[i]
        for i in range(r):
            if (copy.vals[i+i*c] != 1 and copy.vals[i+i*c] != 0):
                factor = 1/copy.vals[i+i*c]
                copy.__rowMult(i,factor)
                out.__rowMult(i,factor)
        for i in range(r-1):
            if (copy.vals[r*c-1-i*c-i] == 0):
                print("Solve Error: No singular solution.")
                exit(0)
            for j in range(r-i-1):
                if (copy.vals[r*(c-1)-1-i-j*c] == 0):
                    continue
                factor = -copy.vals[r*(c-1)-1-i-i*c-j*c] / copy.vals[r*c-1-i-i*c]
                copy.__rowAdd((r*c-1-i-i*c)//c, (r*(c-1)-1-i-i*c-j*c)//c, factor)
                out.__rowAdd((r*c-1-i-i*c)//c, (r*(c-1)-1-i-i*c-j*c)//c, factor)
        out = [copy,out]
        return out    

    def det(self):
        """Calculates the determinant using gaussian elimination."""
        if (self.r != self.c):
            print("Size error: {}x{} is not square".format(self.r,self.c))
            exit(0)
        dummy = Matrix(self.r,1)
        dummy.zero()
        partial = self.__gaussElimination(dummy)
        out = 1
        for i in range(self.r):
            out *= partial[0].vals[i*self.c+i] #Diagonal multiplication to get determinant after gaussian elimination.
        return out

class Vector(Matrix):
    """A class implementing euclidean vectors and typical operations you
        can do with them."""

    def __init__(self,rows):
        super(Vector, self).__init__(rows,1)

    def __mul__(self,other):
        """Returns the dot product of two vectors or multiplication of each
            element by a number."""
        if isinstance(other, Vector):
            if (self.r != other.r):
                raise SizeError("Size error: Can not take dot product of {}-dimensional vector with {}-dimensional vector.".format(self.r,other.r))
            out = self.Transpose()*other
            return out.vals[0]
        elif isinstance(other,(float,int)):
            out = Vector(self.r)
            for i in range(self.r):
                out.vals[i] = self.vals[i]*other
            return out
        raise TypeError("Vector multiplication only valid between vectors or vector and numbers.")

    def cross(self,other):
        """Returns the cross product of the two vectors."""
        try:
            if (self.r != 3 or other.r != 3):
                raise SizeError("Size error: Cross product only valid in dimension 3.")
            out = Vector(3)
            for i in range(3):
                out.vals[i] = self.vals[(i+1)%3]*other.vals[(i+2)%3]-self.vals[(i+2)%3]*other.vals[(i+1)%3]
            return out
        except AttributeError:
            print("Cross product only valid between two vectors.")

    def norm(self):
        """Returns the euclidean vector length."""
        out = 0
        for i in range(self.r):
            out += self.vals[i]**2
        return math.sqrt(out)

    def scalarProj(self,other):
        """Returns the scalar projection of self onto other."""
        if isinstance(other, Vector):
            if (self.r != other.r):
                raise SizeError("Size error: Can not take scalar projection of {}-dimensional vector with {}-dimensional vector.".format(self.r,other.r))
            out = self*(other/other.norm())
            if (out < 1e-10):
                out = 0
            return out
        raise TypeError("Scalar projection only valid between vectors.")

    def Normalize(self):
        """Return a vector of length one in same direction."""
        out = Vector(self.r)
        norm = self.norm()
        for i in range(self.r):
            out.vals[i] = self.vals[i]/norm
        return out