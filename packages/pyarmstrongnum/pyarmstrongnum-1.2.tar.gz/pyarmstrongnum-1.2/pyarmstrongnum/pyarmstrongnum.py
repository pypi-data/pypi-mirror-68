class pyarmstrongnum():
    def armstrong(num):
        num = [int(i) for i in str(num)]
        answer = [num[x]**len(num) for x in range(len(num))]
        num = int(''.join(str(y) for y in num))
        if sum(answer) ==num:
            return str(num) + " is an Armstrong number."
        else:
            return str(num) + " is not an Armstrong number."