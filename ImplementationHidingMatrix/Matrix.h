// William Hartmann (hartmannw@gmail.com)
// This is free and unencumbered software released into the public domain.
// See the UNLICENSE file for more information.

#ifndef MATRIX_H_
#define MATRIX_H_

#include<vector>

// Matrix is a simple implementation of a two-dimensional data structure. It
// defines the desired functionality of the class, but the actual implementation
// may not be efficient. The implementation can be improved in the future if 
// necessary. Data is stored and accessed in a row x column format.
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

  // Constructors.
  Matrix(unsigned int rows, unsigned int cols){ Initialize(rows, cols);}
  Matrix(unsigned int rows, unsigned int cols, T value){ 
      Initialize(rows, cols, value); }
 
  // Initialization functions. 
  void Initialize(unsigned int rows, unsigned int cols);
  void Initialize(unsigned int rows, unsigned int cols, T value);

  // Accessors for the data in the matrix.
  T operator() (unsigned int row, unsigned int col) const;
  T& operator() (unsigned int row, unsigned int col);

  // Accessors for the size of the matrix.
  unsigned int NumRows() const { return rows_;}
  unsigned int NumCols() const { return cols_;}

};

// Initializes the size of the matrix and allocates space, but does not set a
// specific value for the data.
template <class T>
void Matrix<T>::Initialize(unsigned int rows, unsigned int cols)
{
  rows_ = rows;
  cols_ = cols;
  matrix_.resize(rows_);
  for(unsigned int r = 0; r < rows_; ++r)
    matrix_[r].resize(cols_);
}

// Initializes the matrix and allocates space. Sets all data equal to value.
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

// Allows a member of the matrix to be accessed as m(2,4). Does not provide any
// bounds checking.
template <class T>
T Matrix<T>::operator() (unsigned int row, unsigned int col) const
{
  return matrix_[row][col];
}

// We return a reference so value can be set using notation like
// Matrix<int> m(10, 10); 
// m(2,4) = 8;
template <class T>
T& Matrix<T>::operator() (unsigned int row, unsigned int col)
{
  return matrix_[row][col];
}

#endif
