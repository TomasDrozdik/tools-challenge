include_directories(../src)

add_executable(runtests
    test.cpp
)

target_link_libraries(runtests gtest_main)

include(GoogleTest)
gtest_discover_tests(runtests)
