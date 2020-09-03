def solution(s):
    stack=[]
    for item in s:
        if not stack:
            stack.append(item)
        elif stack[-1]== '(':
            if item == ')':
                stack.pop()
            else:
                stack.append(item)
        else:
            stack.append(item)
    if stack:
        return False
    else:
        return True
