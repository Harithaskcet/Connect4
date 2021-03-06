from django.shortcuts import render, get_object_or_404
from .models import Connect
# Create your views here.
player = 1
def home(request):
    return render(request,'GetUser.html')

def createUser(request, player1, player2):
    if request.method == 'GET' or request.method == 'POST':
        global player, playerA, playerB
        player = 1
        playerA = player1
        playerB = player2
        userList = Connect.objects
        users = [player1, player2]
        for user in users:
            if userList.filter(user=user).exists():
                userDetail = get_object_or_404(Connect, user=user)
                print(userDetail)
                userDetail.moves = []
                grid = []
                for i in range(0,6):
                    arr = []
                    for j in range(0,7):
                        arr.append(0)
                    grid.append(arr)
                userDetail.grid = grid
                userDetail.save()
            else:
                player = Connect()
                player.user = user
                player.moves = []
                grid = []
                for i in range(0,6):
                    arr = []
                    for j in range(0,7):
                        arr.append(0)
                    grid.append(arr)
                player.grid = grid
                player.save()
        userA = get_object_or_404(Connect, user=player1)
        print(userA.grid)
        return render(request,'GamePlay.html', { 
            'checks': userA.grid,
            'row': [0,1,2,3,4,5],
            'col':[0,1,2,3,4,5,6],
            'turn': 'Yellow Turn',
            'Amoves':[],
            'Bmoves': [],
            'PlayerA': userA.user,
            'PlayerB': player2 })

def update(request, row, col, playerA, playerB):
    if request.method == 'GET' or request.method == 'POST':
        global player
        print(player, playerA, playerB)
        userA = get_object_or_404(Connect, user=playerA)
        userB = get_object_or_404(Connect, user=playerB)
        mat = userA.grid 
        if player == 1:
            for x in range(5,-1,-1):
                print(mat[x][col])
                if mat[x][col] == 0:
                    mat[x][col] = 1
                    move = userA.moves
                    move.append(col+1)
                    userA.moves = move
                    userA.grid = mat
                    userB.grid = mat
                    player = 2
                    print("player role")
                    print(player)
                    userA.save()
                    userB.save()
                    print(userA.grid)
                    if patternSearch(userA.grid, [1,1,1,1]):
                        return render(request, 'GamePlay.html', {
                            'checks': userA.grid,
                            'row': [0,1,2,3,4,5],
                            'col':[0,1,2,3,4,5,6],
                            'turn': 'Yellow Won!',
                            'Amoves':move,
                            'Bmoves':userB.moves,
                            'PlayerA':userA.user,
                            'PlayerB':playerB })
                    else:
                        return render(request, 'GamePlay.html', {
                            'checks': userA.grid,
                            'row': [0,1,2,3,4,5],
                            'col':[0,1,2,3,4,5,6],
                            'turn': 'Red Turn',
                            'Amoves':move,
                            'Bmoves':userB.moves,
                            'PlayerA':userA.user,
                            'PlayerB': playerB  })
            return render(request, 'GamePlay.html', {
                'checks': userA.grid,
                'row': [0,1,2,3,4,5],
                'col':[0,1,2,3,4,5,6],
                'turn': 'Yellow Turn',
                'error': 'Invalid Move',
                'Amoves':userA.moves,
                'Bmoves':userB.moves,
                'PlayerA':userA.user,
                'PlayerB':playerB })
        else:
            for x in range(5,-1,-1):
                if mat[x][col] == 0:
                    mat[x][col] = 2
                    move = userB.moves
                    move.append(col+1)
                    userB.moves = move
                    userA.grid = mat
                    userB.grid = mat
                    player = 1
                    print("player role")
                    print(player)
                    userA.save()
                    userB.save()
                    print(userB.moves)
                    if patternSearch(userA.grid, [2,2,2,2]):
                        return render(request, 'GamePlay.html', {
                            'checks': userA.grid,
                            'row': [0,1,2,3,4,5],
                            'col':[0,1,2,3,4,5,6],
                            'turn': 'Red Won!',
                            'Amoves':userA.moves,
                            'Bmoves':move,
                            'PlayerA':userA.user,
                            'PlayerB':playerB })
                    else:
                        return render(request, 'GamePlay.html', {
                            'checks': userA.grid,
                            'row': [0,1,2,3,4,5],
                            'col':[0,1,2,3,4,5,6],
                            'turn': 'Yellow Turn',
                            'Amoves':userA.moves,
                            'Bmoves':move,
                            'PlayerA':userA.user,
                            'PlayerB':playerB  })
            return render(request, 'GamePlay.html', {
                'checks': userA.grid,
                'row': [0,1,2,3,4,5],
                'col':[0,1,2,3,4,5,6],
                'turn': 'Red Turn',
                'error': 'Invalid Move',
                'Amoves':userA.moves,
                'Bmoves':userB.moves,
                'PlayerA':userA.user,
                'PlayerB':playerB  })

def search2D(grid, row, col, word): 
    dirs = [[-1, 0], [1, 0], [1, 1],[1, -1], [-1, -1], [-1, 1],[0, 1], [0, -1]] 
    if grid[row][col] != word[0]: 
        return False
    for x, y in dirs: 
        rd, cd = row + x, col + y 
        flag = True
        for k in range(1, len(word)): 
            if (0 <= rd <6 and
                0 <= cd < 7 and
                word[k] == grid[rd][cd]): 
                rd += x 
                cd += y 
            else: 
                flag = False
                break 
        if flag: 
            return True
    return False

def patternSearch(grid, word):
    for row in range(0,6): 
        for col in range(0,7): 
            if search2D(grid, row, col, word):
                return True
            



