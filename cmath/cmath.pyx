def Average(inputList, numOfLastItem=False):
    cdef result
    result = 0

    if numOfLastItem is False:
        for i in inputList:
            result += i
        return result / len( inputList )

    else:
        toIdx = -1
        fromIdx = (numOfLastItem * -1) - 1
        for i in inputList[fromIdx : toIdx]:
            result += i

        return result / len( inputList[fromIdx : toIdx] )


def Max(inputList, numOfLastItem=False):
    cdef result
    result = -999999999

    if numOfLastItem is False:
        for i in inputList:
            if i > result:
                result = i
    else:
        toIdx = -1
        fromIdx = (numOfLastItem * -1) - 1
        for i in inputList[fromIdx : toIdx]:
            if i > result:
                result = i

    return result


def Min(inputList, numOfLastItem=False):
    cdef result
    result = 999999999

    if numOfLastItem is False:
        for i in inputList:
            if i < result:
                result = i
    else:
        toIdx = -1
        fromIdx = (numOfLastItem * -1) - 1
        for i in inputList[fromIdx : toIdx]:
            if i < result:
                result = i

    return result