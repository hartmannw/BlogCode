// William Hartmann (hartmannw@gmail.com)
// This is free and unencumbered software released into the public domain.
// See the UNLICENSE file for more information.

#include "StringFunctions.h"


std::string TrimStringLeft(const std::string& s, 
    const std::string& delimiters /*= " \f\n\r\t\v"*/ )
{
  return s.substr( 0, s.find_last_not_of( delimiters ) + 1 );
}

std::string TrimStringRight(const std::string& s, 
    const std::string& delimiters /*= " \f\n\r\t\v"*/ )
{
  return s.substr( s.find_first_not_of( delimiters ) );
}

std::string TrimString(const std::string& s, 
    const std::string& delimiters /*= " \f\n\r\t\v"*/ )
{
  return TrimStringLeft( TrimStringRight( s, delimiters ), delimiters );
}

bool TokenizeString(std::string line, char delimiter,
    std::vector<std::string> &tokens)
{
  std::istringstream iss(line);
  std::string token;
  while(getline(iss, token, delimiter))
    if( token.length() > 0)
      tokens.push_back(token);

  return true;
}

