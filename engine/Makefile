CC = gcc
CFLAGS = -O2 -fPIC -Wall -Wextra -std=c11
LDLIBS = -lm

.PHONY: all clean

all: libmendel.so

libmendel.so: csrc/tensor_ops.c csrc/tensor_ops.h
	$(CC) $(CFLAGS) -shared -o $@ csrc/tensor_ops.c $(LDLIBS)

clean:
	rm -f libmendel.so
