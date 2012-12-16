// William Hartmann (hartmannw@gmail.com)
// This is free and unencumbered software released into the public domain.
// See the UNLICENSE file for more information.

#include "OrbitalBody.h"
#include "GravitationalSystem.h"
#include "StringFunctions.h"
#define _USE_MATH_DEFINES
#include <cmath>
#include <iostream>
#include <vector>
#include <string>
#include <fstream>

// This file contains the necessary functions to load solar system data and
// simulate the orbits of the objects for a set number of days.

// Converts the Right Ascension data from NASA's Horizon database to degrees
// measured in radians.
double ConvertAscensionToRadians(double hours, double minutes, double seconds);

// Converts the declination data from NASA's Horizon database to degrees
// measured in radians.  Note that the degrees can be negative and the
// conversion handles this.
double ConvertDeclinationToRadians(double degrees, double minutes,
    double seconds);

// Loads the solar system data from the given textfile.  See the README file for
// further details on the format of the file.
GravitationalSystem LoadSolarSystem(std::string filename);

GravitationalSystem LoadSolarSystem(std::string filename)
{
  GravitationalSystem ret;
  std::ifstream fin;
  fin.open(filename.c_str(), std::ios::in);
  std::string line;
  while( getline(fin, line) )
  {
    std::vector<std::string> token;
    OrbitalBody o;
    std::string name;
    double weight;
    double ascension_one, ascension_two;
    double declination_one, declination_two;
    double delta_one, delta_two;

    // First line is name and weight.
    line = TrimString(line);
    TokenizeString(line, ' ', token);
    name = token[0];
    weight = ToNumber<double>(token[1]);
    getline(fin, line);
    token.clear();

    // Second line is current position.
    line = TrimString(line);
    TokenizeString(line, ' ', token);
    ascension_one = ConvertAscensionToRadians(
        ToNumber<double>(token[0]), 
        ToNumber<double>(token[1]), 
        ToNumber<double>(token[2]));
    declination_one = ConvertDeclinationToRadians(
        ToNumber<double>(token[3]), 
        ToNumber<double>(token[4]), 
        ToNumber<double>(token[5]));
    delta_one = ToNumber<double>(token[6]);
    getline(fin, line);
    token.clear();

    // Third line is position one hour in the future.
    line = TrimString(line);
    TokenizeString(line, ' ', token);
    ascension_two = ConvertAscensionToRadians(
        ToNumber<double>(token[0]), 
        ToNumber<double>(token[1]), 
        ToNumber<double>(token[2]));
    declination_two = ConvertDeclinationToRadians(
        ToNumber<double>(token[3]), 
        ToNumber<double>(token[4]), 
        ToNumber<double>(token[5]));
    delta_two = ToNumber<double>(token[6]);
    o.Initialize(name, weight, ascension_one, declination_one, delta_one, 
        ascension_two, declination_two, delta_two);
    ret.AddBody(o);
  }
  fin.close();
  return ret;
}

double ConvertAscensionToRadians(double hours, double minutes, double seconds)
{
    double ret;
    ret = (hours / 24) + (minutes / 1440) + (seconds / 86400);
    ret = ret * (M_PI * 2);
    return ret;
}

double ConvertDeclinationToRadians(double degrees, double minutes,
        double seconds)
{
    double ret;
    if(degrees < 0)
      ret = (degrees / 360) - (minutes / 21600) - (seconds / 1296000);
    else
      ret = (degrees / 360) + (minutes / 21600) + (seconds / 1296000);
    ret = ret * (M_PI * 2);
    return ret;
}

int main(int argc,char *argv[])
{
    GravitationalSystem solar_system;
    solar_system = LoadSolarSystem(std::string(argv[1]));
    double days = ToNumber<double>(std::string(argv[2]));
    std::cout<<solar_system.GetInformation()<<std::endl;

    // We assume 1440 minutes in a day.
    for(int i = 0; i < (1440 * days); ++i)
      solar_system.AdvanceStep();
    
    std::cout<<solar_system.GetInformation()<<std::endl;
    return 0;
}
