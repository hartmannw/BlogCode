CC=g++
CFLAGS=-Wall -O2
INCLUDE=

all: ModelSolarSystem

ModelSolarSystem: OrbitalBody.o GravitationalSystem.o StringFunctions.o \
	ModelSolarSystem.cc
	$(CC) $(CFLAGS) $(INCLUDE) -o ModelSolarSystem OrbitalBody.o \
		GravitationalSystem.o StringFunctions.o ModelSolarSystem.cc

GravitationalSystem.o: GravitationalSystem.h GravitationalSystem.cc
	$(CC) $(CFLAGS) $(INCLUDE) -c GravitationalSystem.cc

OrbitalBody.o: OrbitalBody.cc OrbitalBody.h
	$(CC) $(CFLAGS) $(INCLUDE) -c OrbitalBody.cc

StringFunctions.o: StringFunctions.h StringFunctions.cc
	$(CC) $(CFLAGS) $(INCLUDE) -c StringFunctions.cc

clean:
	rm *.o ModelSolarSystem
