from mfq import MFQScheduler

file_names = ['input1.txt', 'input2.txt', 'input3.txt', 'input4.txt','input5.txt']


for i in range(len(file_names)):
    print("-"*100)
    print(file_names[i],"의 MFQ 스케줄링")
    MFQScheduler(file_names[i])
