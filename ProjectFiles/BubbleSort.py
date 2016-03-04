list1 = [4,3,2,24,32,4 , 23, 235, 23442]
length = len(list1)
for count1 in range(0, length):
    for count2 in range(count1+1, length):
        if list1[count1] > list1[count2]:
            temp = list1[count1]
            list1[count1] = list1[count2]
            list1[count2] = temp
            print (list1)
                
