def merge(left,right):
    mArr = []
    while len(left) > 0 or len(right) > 0:
        if len(left)> 0 and len(right) > 0:
            if left[0] <= right[0]:
                mArr.append(left[0])
                left = left[1:]
            else:
                mArr.append(right[0])
                right = right[1:]
        elif len(left) > 0:
            mArr.append(left[0])
            left = left[1:]
        elif len(right) > 0:
            mArr.append(right[0])
            right = right[1:]
    return mArr

def mergeSort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr)//2
    left = arr[:mid]
    right = arr[mid:]
    left = mergeSort(left)
    right = mergeSort(right)
    return merge(left,right)