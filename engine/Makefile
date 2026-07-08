CC = gcc
CFLAGS = -O2 -fPIC -Wall -Wextra -std=c11
LDLIBS = -lm

# Portable remove command: use native `rm` on Unix, and `cmd /C del /Q` on Windows
RM = rm -f
ifeq ($(OS),Windows_NT)
	RM = cmd /C del /Q
endif

.PHONY: all clean

all: libmendel.so

libmendel.so: csrc/tensor_ops.c csrc/tensor_ops.h
	$(CC) $(CFLAGS) -shared -o $@ csrc/tensor_ops.c $(LDLIBS)

clean:
	$(RM) libmendel.so
