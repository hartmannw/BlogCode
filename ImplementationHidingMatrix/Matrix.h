// William Hartmann (hartmannw@gmail.com)
// This is free and unencumbered software released into the public domain.
// See the UNLICENSE file for more information.

#ifndef MATRIX_H_
#define MATRIX_H_

#include<vector>

template <class T>
class Matrix
{
 private:
  std::vector<std::vector<double> > matrix_;
  unsigned int rows_;
  unsigned int cols_;

 public:
  Matrix() : rows_(0), cols_(0) {}
  ~Matrix() {}

  Matrix(unsigned int rows, unsigned int cols){ Initialize(rows, cols);}
  Matrix(unsigned int rows, unsigned int cols, T value){ 
      Initialize(rows, cols, value); }
  
  void Initialize(unsigned int rows, unsigned int cols);
  void Initialize(unsigned int rows, unsigned int cols);

  T operator() (unsigned int row, unsigned int col) const;
  T& operator() (unsigned int row, unsigned int col);
  unsigned int NumRows() const { return rows_;}
  unsigned int NumCols() const { return cols_;}

};

void Initialize(unsigned int rows, unsigned int cols)
{
  rows_ = rows;
  cols_ = cols;
  matrix.resize(rows_);
  for(unsigned int r = 0; r < rows_; ++r)
    matrix[r].resize(cols_);
}

void Initialize(unsigned int rows, unsigned int cols, T value)
{
  rows_ = rows;
  cols_ = cols;
  matrix.resize(rows_);
  for(unsigned int r = 0; r < rows_; ++r)
    matrix[r].resize(cols_, value);
}

template <class T>
T operator() (unsigned int row, unsigned int col) const
{
  return matrix[row][col];
}

template <class T>
T& operator() (unsigned int row, unsigned int col)
{
  return matrix[row][col];
}

#endif
