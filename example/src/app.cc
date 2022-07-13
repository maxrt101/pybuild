
#include <cstdio>
#include <greet.h>

int main(int argc, char ** argv) {
#ifdef _DEBUG
  printf("Debug is on!\n");
#endif

  if (argc != 2) {
    fprintf(stderr, "Usage: %s NAME\n", argv[0]);
    return 1;
  }

  greet(argv[1]);

  return 0;
}
