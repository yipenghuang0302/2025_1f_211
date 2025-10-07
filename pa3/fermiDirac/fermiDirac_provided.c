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
	FILE* multiplier_f = fopen(argv[1], "r");
	if (!multiplier_f) {
		perror("fopen failed");
		return EXIT_FAILURE;
	}

	FILE* multiplicand_f = fopen(argv[2], "r");
	if (!multiplicand_f) {
		perror("fopen failed");
		return EXIT_FAILURE;
	}

	char buff[8];

	int multiplier = 1;
	while ( fscanf(multiplier_f, "%s", buff) != -1 ) {
		multiplier *= atoi(buff);
	}
	int multiplicand = 1;
	while ( fscanf(multiplicand_f, "%s", buff) != -1 ) {
		multiplicand *= atoi(buff);
	}
	
	int product = multiplier * multiplicand;
	int prime_candidate = 2;
	
	while ( product!=1 ) {
		
		if ( is_prime(prime_candidate) ) {
			
			int fermi_dirac_prime = prime_candidate;
			
			while ( product%fermi_dirac_prime==0 && fermi_dirac_prime<product ) {
				fermi_dirac_prime *= fermi_dirac_prime;
			}
			
			while ( prime_candidate<=fermi_dirac_prime ) {
				if ( product%fermi_dirac_prime==0 ) {
					printf( "%d\n", fermi_dirac_prime );
					product = product/fermi_dirac_prime;
				}
				fermi_dirac_prime = sqrt(fermi_dirac_prime);
			} 
		}
		
		prime_candidate++;
		
	}

}