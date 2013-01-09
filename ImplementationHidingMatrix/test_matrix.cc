// William Hartmann (hartmannw@gmail.com)
// This is free and unencumbered software released into the public domain.
// See the UNLICENSE file for more information.

#include "Matrix.h"
#include <iostream>

void PrintMatrix(const Matrix<int> &matrix)
{
  for(unsigned int r = 0; r < matrix.NumRows(); ++r)
  {
    for(unsigned int c = 0; c < matrix.NumCols(); ++c)
      std::cout<<matrix(r,c)<<" ";
    std::cout<<"\n";
  }
}

int main()
{
  Matrix<int> m;
  m.Initialize(3, 8);
  PrintMatrix(m);
  std::cout<<"\n";
  m.Initialize(4, 4, 9);
  PrintMatrix(m);
  std::cout<<"\n";
  m(1,1) = 1;
  m(1,2) = 2;
  m(2,1) = 3;
  m(2,2) = 4;
  PrintMatrix(m);
  std::cout<<"\n";
  return 0;
}
