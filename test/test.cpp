#include <gtest/gtest.h>

#include "library.h"

TEST(TestFoo, OutOfBounds) {
    foo(10, 2);
}
