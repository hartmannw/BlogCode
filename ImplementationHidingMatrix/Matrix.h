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
  std::vector<std::vector<T> > matrix_;
  unsigned int rows_;
  unsigned int cols_;

 public:
  Matrix() : rows_(0), cols_(0) {}
  ~Matrix() {}

  Matrix(unsigned int rows, unsigned int cols){ Initialize(rows, cols);}
  Matrix(unsigned int rows, unsigned int cols, T value){ 
      Initialize(rows, cols, value); }
  
  void Initialize(unsigned int rows, unsigned int cols);
  void Initialize(unsigned int rows, unsigned int cols, T value);

  T operator() (unsigned int row, unsigned int col) const;
  T& operator() (unsigned int row, unsigned int col);
  unsigned int NumRows() const { return rows_;}
  unsigned int NumCols() const { return cols_;}

};

template <class T>
void Matrix<T>::Initialize(unsigned int rows, unsigned int cols)
{
  rows_ = rows;
  cols_ = cols;
  matrix_.resize(rows_);
  for(unsigned int r = 0; r < rows_; ++r)
    matrix_[r].resize(cols_);
}

template <class T>
void Matrix<T>::Initialize(unsigned int rows, unsigned int cols, T value)
{
  rows_ = rows;
  cols_ = cols;
  matrix_.clear(); // There may be old values and we want to flush those first.
                   // Otherwise the new value may not be set at every position.
  matrix_.resize(rows_);
  for(unsigned int r = 0; r < rows_; ++r)
    matrix_[r].resize(cols_, value);
}

template <class T>
T Matrix<T>::operator() (unsigned int row, unsigned int col) const
{
  return matrix_[row][col];
}

template <class T>
T& Matrix<T>::operator() (unsigned int row, unsigned int col)
{
  return matrix_[row][col];
}

#endif
