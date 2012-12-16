// William Hartmann (hartmannw@gmail.com)
// This is free and unencumbered software released into the public domain.
// See the UNLICENSE file for more information.

#ifndef ORBITALBODY_
#define ORBITALBODY_
#include <iostream>
#include <cmath>
#include <string>
#include <sstream>

#define KM_PER_AU 149597870.691   // value used in NASA's HORIZONS system.
#define GRAVITY 7.17633288458e-17 // defined in terms of AU / 
                                  // (10^24kg * minutes^2)

// Defines an object to be used in a gravitational system.  An OrbitalBody has a
// position (x,y,z), velocity (dx,dy,dz), and mass.  Positions are in terms of
// AU, velocity is in terms of AU per minute, and mass is in terms of 10^24 kg.
class OrbitalBody
{
 public:
  OrbitalBody(){}
  ~OrbitalBody(){}
  // Determines the position and velocity data based on the declination, 
  // ascension, and delta information.  Ascension and declination are angles
  // given in terms of radians and delta is the distance of the object to some
  // predefined center in terms of AU.  The difference between _one and _two is
  // that _two gives values for the object one hour in the future.  A one hour
  // difference is used, even though the unit for velocity is minutes, because
  // the HORIZONS data does not give enough precision; the difference in postion
  // between to consecutive minutes does not provide an accurate velocity
  // estimate.
  void Initialize(std::string name, double mass, double ascension_one, 
      double declination_one, double delta_one, double ascension_two, 
      double declination_two, double delta_two);

  // Set of accessor functions.
  double mass() const { return mass_;}
  double x() const { return x_; }
  double y() const { return y_; }
  double z() const { return z_; }
  double dx() const { return dx_; }
  double dy() const { return dy_; }
  double dz() const { return dz_; }

  // Updates the postion of the OrbitalBody based on the current velocity
  // information.  The new position corresponds to one minute in the future.
  void UpdatePosition();

  // Given acceleration information in terms of AU per minute, the velocity is
  // updated.
  void UpdateVelocity(double ax, double ay, double az);

  // Returns a string containing the objects names, position, and velocity
  // information.
  std::string GetInformation();

  // Returns the distance between the OrbitalBody and any other body in terms of
  // AU.
  double DistanceFrom(const OrbitalBody &body);

 private:
  std::string name_;
  double mass_;
  double x_, y_, z_;    // position
  double dx_, dy_, dz_; // velocity
};

#endif
