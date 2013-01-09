CC=g++
CFLAGS=-Wall -O2
INCLUDE=

all: test_matrix

test_matrix: Matrix.o test_matrix.cc
	$(CC) $(CFLAGS) $(INCLUDE) -o test_matrix Matrix.o test_matrix.cc

Matrix.o: Matrix.h Matrix.cc
	$(CC) $(CFLAGS) $(INCLUDE) -c Matrix.cc

clean:
	rm *.o test_matrix
