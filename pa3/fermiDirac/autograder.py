#!/usr/bin/python3

import os
import math
import datetime
import random
import subprocess
import oeis
from functools import reduce

primes = oeis.Sequence(a_number="A000040").data
fermi_dirac_primes = oeis.Sequence(a_number="A050376").data

def generate_test ( filenum, max_factors, path="./" ):

    bitstring0 = [bool(random.getrandbits(1)) for i in range(max_factors)]
    bitstring1 = [bool(random.getrandbits(1)) for i in range(max_factors)]

    product0 = 1
    product1 = 1

    factors0 = []
    factors1 = []

    for index, bit in enumerate(bitstring0):
        if bit:
            fermi_dirac_prime = fermi_dirac_primes[index]
            product0 *= fermi_dirac_prime
            factors0.append(fermi_dirac_prime)

    for index, bit in enumerate(bitstring1):
        if bit:
            fermi_dirac_prime = fermi_dirac_primes[index]
            product1 *= fermi_dirac_prime
            factors1.append(fermi_dirac_prime)

    factors = []
    product = product0 * product1

    for prime in primes:

        fermi_dirac_prime = prime
        while fermi_dirac_prime <= math.sqrt(product):
            fermi_dirac_prime *= fermi_dirac_prime

        while prime<=fermi_dirac_prime:
            if product % fermi_dirac_prime == 0:
                factors.append(fermi_dirac_prime)
                product //= fermi_dirac_prime
            fermi_dirac_prime = int(math.sqrt(fermi_dirac_prime))

        if product == 1:
            break

    sanity_check = 1
    for factor in factors:
        sanity_check *= factor 
    assert sanity_check == product0 * product1

    with open("{}tests/multiplicand{}.txt".format(path,filenum), "w") as test_file:
        test_file.write("\n".join( str(factor) for factor in factors0 ))
    with open("{}tests/multiplier{}.txt".format(path,filenum), "w") as test_file:
        test_file.write("\n".join( str(factor) for factor in factors1 ))
    with open("{}answers/answer{}.txt".format(path,filenum), "w") as answer_file:
        for factor in factors:
            print(str(factor), file=answer_file)

def generate_test_suite():

    os.makedirs("tests", exist_ok=True)
    os.makedirs("answers", exist_ok=True)

    generate_test ( 0, max_factors=1, path="./" )
    generate_test ( 1, max_factors=2, path="./" )
    generate_test ( 2, max_factors=4, path="./" )
    generate_test ( 3, max_factors=8, path="./" )
    generate_test ( 4, max_factors=16, path="./" )
    generate_test ( 5, max_factors=32, path="./" )
    generate_test ( 6, max_factors=61, path="./" )
    generate_test ( 7, max_factors=61, path="./" )

def test_fermiDirac ( filenum, path="./", verbose=False ):

    try:
        with open("{}answers/answer{}.txt".format(path,filenum), "r") as answer_file:
            answer_factors = set([ int(string) for string in answer_file.read().split() ])
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/answer{}.txt missing".format(filenum))

    try:
        result = subprocess.run(
            ["./fermiDirac", "tests/multiplier{}.txt".format(filenum), "tests/multiplicand{}.txt".format(filenum)],
            cwd=path,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="ASCII",
            timeout=datetime.timedelta(seconds=4).total_seconds(),
        )
        
        result_factors = set([ int(string) for string in result.stdout.splitlines() ])

        if verbose:
            print (' '.join(result.args))
            print ("answer_factors")
            print (answer_factors)
            print ("result_factors")
            print (result_factors)
        assert result_factors == answer_factors, "The program output does not print the correct list of Fermi-Dirac prime factors of the product.".format(filenum)
        return True
    except subprocess.TimeoutExpired as e:
        print (e.output)
        print ("Calling ./fermiDirac with the previous test case timed out. A more efficient algorithm implementation is needed.")
    except subprocess.CalledProcessError as e:
        print (e.output)
        print ("Calling ./fermiDirac returned an error.")
    except ValueError as e:
        print (' '.join(result.args))
        print (result.stdout)
        print ("Please check your output formatting.")
    except AssertionError as e:
        print (result.stdout)
        print (e.args[0])

    return False

def grade_fermiDirac( path="./", verbose=False ):

    score = 0

    try:
        subprocess.run( ["make", "clean"], cwd=path, check=True, )
        subprocess.run( ["make", "-B"], cwd=path, check=True, )
    except subprocess.CalledProcessError as e:
        print ("Couldn't compile fermiDirac.c.")
        return score

    if test_fermiDirac(0,path,verbose):
        score += 1
        if test_fermiDirac(1,path,verbose):
            score += 1
            if test_fermiDirac(2,path,verbose):
                score += 1
                if test_fermiDirac(3,path,verbose):
                    score += 1
                    if test_fermiDirac(4,path,verbose):
                        score += 1
                        if test_fermiDirac(5,path,verbose):
                            score += 1
                            if test_fermiDirac(6,path,verbose):
                                score += 1
                                if test_fermiDirac(7,path,verbose):
                                    score += 1
                                    allPass = True
                                    for filenum in range(8,25):
                                        generate_test (
                                            filenum,
                                            max_factors=61,
                                            path=path
                                        )
                                        allPass &= test_fermiDirac(filenum,path,verbose)
                                        if allPass:
                                            score += 1
                                        else:
                                            break

    print ("Score on fermiDirac: {} out of 25.".format(score))
    return score

if __name__ == '__main__':
#     generate_test_suite()
    grade_fermiDirac(verbose=True)
    exit()
