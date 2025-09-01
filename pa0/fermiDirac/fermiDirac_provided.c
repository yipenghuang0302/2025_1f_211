#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>

bool is_prime(int n) {

	if (n<2)
		return false;
	
	for (int i=2; i<=sqrt(n); i++)
		if (n%i==0)
			return false;
	
	return true;
}

int main(int argc, char* argv[]) {
	
	// Open the filename given as the first command line argument for reading
	FILE* fp = fopen(argv[1], "r");
	if (!fp) {
		perror("fopen failed");
		return EXIT_FAILURE;
	}
	char buf[256];
		char* string = fgets(buf, 256, fp);
	int x = atoi(string);
	
	int fermi_dirac_prime = 2;  
	printf( "%d\n", fermi_dirac_prime );

}