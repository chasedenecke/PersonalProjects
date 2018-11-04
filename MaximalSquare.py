# https://www.coderbyte.com/editor/guest:Maximal%20Square:Python

# Read the link above for a description of the problem this program is trying to solve
def MaximalSquare(strArr): 
    numRows = len(strArr)
    numColumns = len(strArr[0])
    biggestSquare = 0
    # These outer two loops iterate through entire 2d array of chars. Their indices represent the top left corner of a square.
    for i in range(0, numRows):
        for j in range(0, numColumns):
            maxDimension = 0
            zeroFound = False
            # This inner loop tries to find the biggest square that starts at the top left corner indicated by the outer two loops.
            while 1:
                # This for loop expands the square on the right side. If we have found a 3x3 square of 1's and are checking
                # to see if there's a 4x4 square, this loop would check all the indices represented by X's in the following picture
                # 111X
                # 111X
                # 111X
                for x in range(0, maxDimension):
                    if strArr[x+i][maxDimension+j] == "0":
                        zeroFound = True
                        break
                # This for loop expands the square on the bottom side. If we have found a 3x4 rectangle of 1's (the above loop
                # would have found the rightmost column of 1's) and are checking to see if there's a 4x4 square, 
                # this loop would check all the indices represented by X's in the following picture
                # 1111
                # 1111
                # 1111
                # XXXX
                if zeroFound == False: # If the above loop found a 0, don't waste time checking the bottom side
                    for x in range(0, maxDimension + 1):
                        if strArr[maxDimension+i][x+j] == "0":
                            zeroFound = True
                            break
                if zeroFound == True:
                    break
                maxDimension += 1
                if maxDimension > biggestSquare:
                    biggestSquare = maxDimension
                # These loop breaking if statements are hard to explain.
                # At this point, we have already found some square of side length N within the array.
                # If looking for a square of side length N+1 would trigger an index out of bounds exception
                # (reading a spot in the array that doesn't exist), then we break the inner loop.
                # We do the samae thing for the outer loops.
                if j + biggestSquare >= numColumns or i + biggestSquare >= numRows:
                    break
            if j + biggestSquare >= numColumns:
                break
        if i + biggestSquare >= numRows:
            break
                    
    # code goes here 
    return biggestSquare * biggestSquare
      
print(MaximalSquare(["10100", "10111", "11111", "10010"]))












  