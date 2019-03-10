def Average(inputList):
    cdef result
    result = 0

    for i in inputList:
        result += i

    return result / len( inputList)

def Max(inputList):
    cdef result
    result = inputList[0]

    for i in inputList[1:]:
        if i > result:
            result = i

    return result

def Min(inputList):
    cdef result
    result = inputList[0]

    for i in inputList[1:]:
        if i < result:
            result = i

    return result


def AverageOfRange(inputList, startIdx, endIdx):
    cdef result
    result = 0

    for i in inputList[startIdx : endIdx]:
        result += i

    return result / len(inputList[startIdx : endIdx])


def MaxOfRange(inputList, startIdx, endIdx):
    cdef result
    result = inputList[startIdx]

    for i in inputList[startIdx+1 : endIdx]:
        if i > result:
            result = i

    return result


def MinOfRange(inputList, startIdx, endIdx):
    cdef result
    result = inputList[startIdx]

    for i in inputList[startIdx+1 : endIdx]:
        if i < result:
            result = i

    return result


def RSI(inputList, startIdx, endIdx):
    cdef totalGain, totalLoss, avgGain, avgLoss, rs, rsi, count
    totalGain = totalLoss = avgGain = avgLoss = rs = rsi = count = 0

    for i in inputList[startIdx : endIdx]:
        idx = startIdx + count
        lastIdx = startIdx - 1 + count
        val = inputList[idx]
        lastVal = inputList[lastIdx]

        if val > lastVal:
            totalGain += val - lastVal
        elif val < lastVal:
            totalLoss += lastVal - val
        count+=1

    avgGain = totalGain / count
    avgLoss = totalLoss / count

    if avgLoss == 0: return 0
    rs = avgGain / avgLoss
    rsi = 100 - (100 / (1 + rs))
    return rsi

'''
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
'''