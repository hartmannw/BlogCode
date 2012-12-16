// William Hartmann (hartmannw@gmail.com)
// This is free and unencumbered software released into the public domain.
// See the UNLICENSE file for more information.

#include "GravitationalSystem.h"

// Moves the entire system one minute into the future.  Uses Newton's law of 
// gravitation to calculate the acceleration for each object.  Once the
// acceleration is determined, position and velocity information are updated.
void GravitationalSystem::AdvanceStep()
{
  std::vector<double> ax, ay, az;
  for(unsigned int i = 0; i < bodies_.size(); ++i)
  {
    ax.push_back(0);
    ay.push_back(0);
    az.push_back(0);
    // First calculate the accelerations.
    for(unsigned int j=0; j < bodies_.size(); ++j)
    {
      if(i != j) // An object does not interact gravitational with itself.
      {
        double distance = std::sqrt( std::pow(bodies_[i].x() - bodies_[j].x(),2)
            + std::pow(bodies_[i].y() - bodies_[j].y(), 2)
            + std::pow(bodies_[i].z() - bodies_[j].z(), 2));
        // GRAVITY is #defined in OrbitalBody.h
        ax[i] += - (GRAVITY * (bodies_[j].mass() * 
            (bodies_[i].x() - bodies_[j].x()))) / pow(distance, 3);
        ay[i] += - (GRAVITY * (bodies_[j].mass() * 
            (bodies_[i].y() - bodies_[j].y()))) / pow(distance, 3);
        az[i] += - (GRAVITY * (bodies_[j].mass() * 
            (bodies_[i].z() - bodies_[j].z()))) / pow(distance, 3);
      }
    }
  }
  // Update the positions and velocities for each body.
  for(unsigned int i = 0; i < bodies_.size(); i++)
  {
    bodies_[i].UpdatePosition();
    bodies_[i].UpdateVelocity(ax[i], ay[i], az[i]);
  }
  return;
}

std::string GravitationalSystem::GetInformation()
{
  std::ostringstream ss;
  for(unsigned int i = 0; i < bodies_.size(); i++)
  {
    ss << "Body " << (i+1) <<": "<<bodies_[i].GetInformation()<<"\n";
  }
  return ss.str();
}

