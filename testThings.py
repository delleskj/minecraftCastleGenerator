def test_function():
    thisDict = {0: ["a", "b", "c", "d"]}
    print(thisDict[0][0])
    thisDict[0][2] = "z"
    thisDict[1] = "z"
    print(thisDict)
    for thing in thisDict.values():
        print(thing)