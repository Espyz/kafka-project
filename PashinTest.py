a=[]
for i in range(11):
    a.append([])
    for j in range(11):
        a[i].append(' ')
        if (i == 5) or (j == 5) or (i == j) or (i == 10 - j):
            a[i][j] = '*'

for i in a:
    for j in i:
        print(j, end=' ')
    print()
