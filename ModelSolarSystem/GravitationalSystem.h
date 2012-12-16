// William Hartmann (hartmannw@gmail.com)
// This is free and unencumbered software released into the public domain.
// See the UNLICENSE file for more information.

#ifndef GRAVITATIONALSYSTEM_H_
#define GRAVITATIONALSYSTEM_H_

#include<vector>
#include<sstream>
#include "OrbitalBody.h"

// Stores a set of OrbitalBodies and models their interaction.  Each time
// AdvanceStep is called, the entire system is moved one minute in to the 
// future.
class GravitationalSystem
{
 public:
  GravitationalSystem(){};
  ~GravitationalSystem(){};

  // Appends an initialized OribtalBody to the system.
  void AddBody(OrbitalBody body){bodies_.push_back(body);}

  // Moves the entire system one minute into the future by updating the 
  // positions and velocities of each object.
  void AdvanceStep();

  // Returns a string containing information for each body in the system. Each
  // body is given its own line.
  std::string GetInformation();

  // Accessor functions for member data.
  OrbitalBody body(unsigned int i){return bodies_[i];}
  std::vector<OrbitalBody> bodies(){ return bodies_;}

 private:
  std::vector<OrbitalBody> bodies_; // Objects in the system.
};

#endif
