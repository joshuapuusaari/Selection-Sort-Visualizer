class Step:
    # Constructor
    # actionType: Action being performed. e.g.: select, swap, complete
    # currentList: Current array
    # i: Current unsorted index
    def __init__(self, actionType, currentList, min, i):
        self.actionType = actionType
        self.currentList = currentList.copy()
        self.min = min
        self.i = i
    