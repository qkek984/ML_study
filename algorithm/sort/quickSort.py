def quickSort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr)//2]
    less , equal, more = [], [], []
    for item in arr:
        if item < pivot:
            less.append(item)
        elif item == pivot:
            equal.append(item)
        else:
            more.append(item)
    return quickSort(less) + equal + quickSort(more)