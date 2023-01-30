"""
The ISBN is used to uniquely identify books.
I.e: 0-201-36186-8
    Can be parsed to
        0 - Country
        20 - Publisher
        1 - 36186 - Book Number
        8 - Check

The last two digits is check digits - used to validate if the code
    is corret. The cumulative sum of the digits is computed, then the
    cumulative som of the cumulative sum is computed. For valid ISBN
    , the sum-of-the-sum must be equal to zero mod N.
"""

# ISBN - 13 CHECK DIGIT CALCULATION

# 978-1?38551992


def calculateISBN(isbn):
    # assert len(isbn) == 13, "Should be 13 digits long!"
    out = 0
    for x in range(len(isbn)):
        if x % 2 == 1:
            out += isbn[x]*3
        else:
            out += isbn[x]
    missing_nbr = out % 10
    print("missing number %d \n" % missing_nbr)
    
    out = isbn[:4] + [missing_nbr] + isbn[4:]

    out = ''.join(list(map(str, out))) 
    print(out) 
    print(f"ISBN: {out[:3]}-{out[3:]}")
    return out

# number format (ISBN) 
# ISBN: XXX-XXXXXXXXXX
# should be one 
if __name__=="__main__":
    MISSING_ISBN_STRING =  978138551992
    isbn = list(map(int, str(MISSING_ISBN_STRING)))
    calculateISBN(isbn)