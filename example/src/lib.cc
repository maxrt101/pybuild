#include <greet.h>
#include <cstdio>

void greet(const std::string& name) {
  printf("Hello, %s!\n", name.c_str());
}
