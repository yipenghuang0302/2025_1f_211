#include <stdlib.h>
#include <stdio.h>

int main () {

  int **x = malloc(sizeof(int*));

  printf("x = %p\n", x);
  fflush(stdout);

  *x = malloc(sizeof(int));

  printf("*x = %p\n", *x);
  fflush(stdout);

  printf("**x = %d\n", **x);
  fflush(stdout);

  **x = 8;

  free(*x);
  free(x);

}
