# CBMC automatic bounds checking of C and C++ programms

## How to run?

If you don't have [`cmbc`](http://www.cprover.org/cbmc/) installed this [`Dockerfile`](./Dockerfile) has got you covered:
```
$ docker build -t cbmc .
$ docker run -it --rm -v $(pwd):/mnt cbmc
(docker) $ cd /mnt
```

Now that you are in the docker or you have `cbmc` on your path you can run our tool on your sources e.g. our [`main.cpp`](./src/main.cpp) file:
```
$ ./tool.py src/main.cpp
```

Our tools all bound check asserts to the code.
For example from your make we call library function `foo` that assignes to static array.
`cbmc` can detect these accesses and provides checks that we insert as asserts.

For access:
```
int x[10];
x[i] = val;
```

We generate asserts:
```
assert(!((signed long int)i >= 10l));
assert(4l * (signed long int)i >= 0l);
```

To verify that this actually works we can build the project:
```
$ mkdir build
$ cd build
$ cmake ..
$ make
$ ./src/main
main: /mnt/src/library.h:7: void foo(int, int): Assertion `!((signed long int)i >= 10l)' failed.
Aborted
```

Or even run tests (once built):
```
$ ./test/runtests
Running main() from /mnt/ubuntu-build/_deps/googletest-src/googletest/src/gtest_main.cc
[==========] Running 1 test from 1 test suite.
[----------] Global test environment set-up.
[----------] 1 test from TestFoo
[ RUN      ] TestFoo.OutOfBounds
runtests: /mnt/test/../src/library.h:9: void foo(int, int): Assertion `!((signed long int)i >= 10l)' failed.
Aborted
```

## Notes

We insert all the asserts not just those which the program violates.
This is because `--show-properties --bounds-check` displays all properties (bounds conditions) and without `--show-properties` it evaluates each property - whether it was violated or not.
This could be trivially added since the properties are labeled but we were short on time.
