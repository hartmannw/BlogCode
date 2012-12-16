// William Hartmann (hartmannw@gmail.com)
// This is free and unencumbered software released into the public domain.
// See the UNLICENSE file for more information.

#ifndef STRINGFUNCTIONS_
#define STRINGFUNCTIONS_

#include<string>
#include<sstream>
#include<vector>

// Contains assorted std::string functions.

// Converts any number type to a std::string.
template <typename T> std::string ToString( T number)
{
  std::ostringstream ss;
  ss << number;
  return ss.str();
}

// Converts a string to any number type.
template <typename T> T ToNumber(std::string s)
{
  T number;
  std::stringstream ss(s);
  ss >> number;
  return number;
}

// Functions to trim surrounding white space from a string. The default is white
// space, but other characters can be set through the delimiter variable.
std::string TrimStringRight(const std::string& s,
    const std::string& delimiters = " \f\n\r\t\v" );
std::string TrimStringLeft(const std::string& s, 
    const std::string& delimiters = " \f\n\r\t\v" );
std::string TrimString(const std::string& s, 
    const std::string& delimiters = " \f\n\r\t\v" );

// Converts a string to a vector of strings by splitting the string based on the
// given delimiter.
bool TokenizeString(std::string line, char delimiter, 
    std::vector<std::string> &tokens);

#endif
