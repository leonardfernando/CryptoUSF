#!/usr/bin/env python
""" prime.py
    A library of routines to find prime numbers.

    When run from the commandline it randomly generates and displays a prime
    number of the size provided by the 'size' argument.

    References:
      HAC - "Handbook of Applied Cryptography",Menezes, van Oorschot, Vanstone; 1996
      https://inventwithpython.com/rabinMiller.py
      http://rosettacode.org/wiki
"""
from os import urandom


def fermat_little_test(p, a):
    """ Fermat Little Test. Included as a curiosity only.
        p - possible Prime,
        a - any integer

        Fermat's Liitle test says that non-primes always have the property that:
        a**(p-1) == 0  mod(p)
        """
    if pow(a, p - 1, p) == 1:
        return True  # could be prime
    else:
        return False  # is NOT prime


def rabin_miller(possiblePrime, aTestInteger):
    """ The Rabin-Miller algorithm to test possible primes
        taken from HAC algorithm 4.24, without the 't'
        """
    assert (1 <= aTestInteger <= (possiblePrime - 1)), 'test integer %d out of range for %d' % (
    aTestInteger, possiblePrime)
    # assert( possiblePrime % 2 == 1 ), 'possiblePrime must be odd'
    # calculate s and r such that (possiblePrime-1) = (2**s)*r  with r odd
    r = possiblePrime - 1
    s = 0
    while (r % 2) == 0:
        s += 1
        r = r / 2
    y = pow(aTestInteger, r, possiblePrime)
    if (y != 1 and y != (possiblePrime - 1)):
        j = 1
        while (j <= s - 1 and y != possiblePrime - 1):
            y = pow(y, 2, possiblePrime)  # (y*y) % n
            if y == 1:
                return False  # failed - composite
            j = j + 1
        if y != (possiblePrime - 1):
            return False  # failed - composite
    return True  # success, still a possible prime


def is_prime(possible_prime):
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
    count = 0
    k = 3
    if possible_prime < 2: #checking if value is greater than 1 and 0
        return False

    if possible_prime % 2 == 0: #checking if value is even
        return False

    if possible_prime % 2 != 0: #if value is not even, rabin miller test initiated
        while count <= k:
            for i in primes:
                return rabin_miller(possible_prime, i)
            count += 1
    return True


def int_to_string(long_int, padto=None):
    """ Convert integer long_int into a string of bytes, as per X9.62.
        If 'padto' defined, result is zero padded to this length.
        """
    if long_int > 0:
        octet_string = ""
        while long_int > 0:
            long_int, r = divmod(long_int, 256)
            octet_string = chr(r) + octet_string
    elif long_int == 0:
        octet_string = chr(0)
    else:
        raise ValueError('int_to-string unable to convert negative numbers')

    if padto:
        padlen = padto - len(octet_string)
        assert padlen >= 0
        octet_string = padlen * chr(0) + octet_string
    return octet_string


def string_to_int(octet_string):
    """ Convert a string of bytes into an integer, as per X9.62. """
    long_int = 0L
    for c in octet_string:
        long_int = 256 * long_int + ord(c)
    return long_int


def new_random_prime(size_in_bytes):
    """ Finds a prime number of close to a specific integer size.
    """
    possible_prime = string_to_int(urandom(size_in_bytes))
    if not possible_prime % 2:  # even, +1 to make odd
        possible_prime += 1

    while True:
        if is_prime(possible_prime):
            break
        else:
            possible_prime += 2

    return possible_prime


# -- Command line code, only executed when file is run as 'main'
import click


@click.version_option(0.1)
@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--my_option', '-o', default=1, help='help text for option goes here')
@click.option('--my_option2', '-x', default=1, help='help text for other option')
@click.argument('size', type=int)
def prime(my_option, my_option2, size):
    """ Generate a prime number of a given size in bytes. """

    p = new_random_prime(size)

    click.echo(p)


if __name__ == '__main__':
    prime()

