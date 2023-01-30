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

# isbn = list(map(int, input("ISBN - 13 stream: ")))
# 978-1?38551992
isbn = list(map(int, str(978138551992)))
print(isbn)

def calculateMissingDigit(list_isbn: list):
    i = 0
    while True:
        list_isbn = list_isbn[:4] + [i] + list_isbn[4:]
        if calculateISBN(list_isbn):
            break
        i += 1
        if i == 13:
            break

def calculateISBN(isbn):
    # assert len(isbn) == 13, "Should be 13 digits long!"
    out = 0
    for x in range(len(isbn) ):
        if x % 2 == 1:
            out += isbn[x]*3
        else:
            out += isbn[x]
    print(out) 
    diff = out % 10
    return diff

# calculateMissingDigit(isbn)
# print(calculateISBN([9,7,8,0,3,0,6,4,0,6,1,5]))
missing_nbr = calculateISBN(isbn)
print("missing number %d \n" % missing_nbr)
out = isbn[:4] + [missing_nbr] + isbn[4:]
first = ''.join(list(map(str, out[:3])))
sec = ''.join(list(map(str, out[3:])))
print(f"isbn: {first}-{sec}")
print(out)

# should be one 
