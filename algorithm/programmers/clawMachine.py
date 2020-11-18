def solution(board, moves):
    answer = 0
    basket = []
    arr = [[] for _ in range(len(board))]
    for i in range(len(board)):
        for j in range(len(board[i])):
            arr[j].append(board[i][j])

    for m in moves:
        for i in range(len(arr[m-1])):
            if arr[m-1][i] != 0:
                if basket and basket[-1] == arr[m-1][i]:
                    basket.pop()
                    arr[m-1][i] = 0
                    answer +=2
                else:
                    basket.append(arr[m-1][i])
                    arr[m-1][i] = 0
                break        
    return answer
