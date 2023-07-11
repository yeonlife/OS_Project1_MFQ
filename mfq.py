def MFQScheduler(f_name):

    #1. 데이터를 저장할 리스트 생성
    # Process ID 리스트 생성
    pid_list = []

    # AT, BT, TT, WT 리스트 생성
    at_list = []
    bt_list = []
    tt_list = []
    wt_list = []


    # input 데이터 불러오기
    f = open(f_name)   # input data 파일 열기
    input_data = f.readlines()   # input data에 있는 text 리스트에 저장

    p_num = int(input_data[0])   # 프로세스 개수 (첫번째 줄은 프로세스 수 의미)

    for process in input_data[1:]:   # input의 두번째 줄 ~ 마지막 줄
        # 프로세스 id, arrival time, burst time 순서대로 있는 숫자들을 각 리스트에 추가
        pid, at, bt = process.split(" ")
        pid_list.append(pid)
        at_list.append(int(at))
        bt_list.append(int(bt[0]))



    

    #필요한 변수 설정하기
    t=0                          # cpu time
    cpu_wt=0                     # cpu 안에 아무 process가 없는 time
    cpu = []                     # [[process_id, run_time],[process_id, run_time], ...] 과 같은 형태로 저장됨
    result = {}                  # process 실행 종료 시 process_id를 key값 으로, process 실행 종료 시간을 value 값으로 저장하는 딕셔너리
    not_ready = [a for a in pid_list]             # arrival time 오기 전 즉, 처음 ready queue에 들어가기 전 까지 process id를 저장하는 리스트
    original_bt_list = [a for a in bt_list]         # bt_list는 갱신되므로, 원래 bt를 저장하는 리스트 생성
    pid_at_dict = dict(zip(pid_list, at_list))      # pid를 key 값으로, at를 value 값으로 가지는 딕셔너리 생성
    sorted_pid_at = dict(sorted(pid_at_dict.items(), key=lambda x: x[1]))    #pid_at_dict를 at를 기준으로 오름차순 정렬

    # Ready Queue 생성
    rq0 = []
    rq1 = []
    rq2 = []

    # AT와 BT를 이용하여 MFQ 스케줄링 구현하기
    while len(result) < p_num:

        #0st stage: RQ0에 process 할당
        for i in range(p_num):
            temp_at = list(sorted_pid_at.values())[i]
            temp_pid = list(sorted_pid_at.keys())[i]

            if temp_at <= t and temp_pid in not_ready:
                rq0.append(temp_pid)   #rq0에 process id를 추가
                not_ready.remove(temp_pid)
                cpu_wt = 0   # 프로세스가 생성되었으므로, cpu_wt 값 초기화

        '''
        t에 따른 출력 확인
        print("t=",t)
        print("rq0",rq0,"rq1",rq1,"rq2",rq2)
        print("output",result)
        print("")
        '''

        if len(rq0)!= 0:   #1st stage: RQ0 RR 스케줄링 실행, time quantum = 2
            temp_index = pid_list.index(rq0[0])
            temp_bt = bt_list[temp_index]

            if temp_bt <= 2:
                cpu.append([rq0[0], temp_bt])   #cpu timeline에 기록
                t += temp_bt
                result[rq0.pop(0)] = t   #process 실행 종료 시간 딕셔너리에 추가
            
            else:   #preemption 발생한 경우
                cpu.append([rq0[0], 2])   #cpu timeline에 기록
                t += 2
                bt_list[temp_index] -= 2   #남은 bt 계산
                rq1.append(rq0.pop(0))   #다음 RQ로 process 이동

    
        else:   #len(rq0) == 0일 때
            if len(rq1) != 0:   #2nd stage: RQ1 RR 스케줄링 실행, time quantum = 4
                temp_index = pid_list.index(rq1[0])
                temp_bt = bt_list[temp_index]

                if temp_bt <= 4:
                    cpu.append([rq1[0], temp_bt])   #cpu timeline에 기록
                    t += temp_bt
                    result[rq1[0]] = t   #proces 실행 종료 시간 딕셔너리에 추가
                    rq1.pop(0)   #현재 RQ에서 process 삭제
                else:   #preemption 발생한 경우
                    cpu.append([rq1[0], 4])   #cpu timeline에 기록
                    t += 4
                    bt_list[temp_index] -= 4   #남은 bt 계산
                    rq2.append(rq1.pop(0))   #다음 RQ로 process 이동


            else:   #len(rq0) ==0 and len(rq1) == 0 일 때
                if len(rq2) != 0:   #3rd stage: RQ2 FCFS 스케줄링 실행
                    temp_index = pid_list.index(rq2[0])
                    temp_bt = bt_list[temp_index]

                    cpu.append([rq2[0], temp_bt])
                    result[rq2[0]] = t + temp_bt   #프로세스 실행 종료 시간 딕셔너리에 추가
                    rq2.pop(0)
                    t += temp_bt

                else:   #현재 ready queue에 아무 process도 없는 상태
                    t += 1
                    cpu_wt += 1
                    
                    for j in range(p_num):
                        if t == list(sorted_pid_at.values())[j]:   #바로 다음 t에 process가 created 된다면
                            cpu.append(["-", cpu_wt])



    # TT 계산
    for i in pid_list:
        tt = result[i] - at_list[pid_list.index(i)]
        tt_list.append(tt)   #실행종료까지 걸린 시간 - AT


    # WT = TT - BT이므로, wt_list는 tt_list와 bt_list를 통해 구함
    for p in range(p_num):
        wt_list.append(tt_list[p] - original_bt_list[p])

    #전체 프로세스의 TT, WT 평균
    tt_mean = sum(tt_list) / len(tt_list)
    wt_mean = sum(wt_list) / len(wt_list)


    #OUTPUT
    print("")

    #output 1) 스케줄링 결과
    print("[스케줄링 결과]")

    print("="*30)

    for temp_proc in cpu:   #cpu timeline 그리기
        p_id, t = temp_proc

        if p_id == "-":
            print(p_id*t, end='|')
        else:
            if t == 0:
                continue
            elif t == 1:
                print(p_id, end='|')
            elif t == 2:
                print(str(p_id)+ " ", end='|')
            else:
                if t % 2 != 0:   #t가 2 이상 홀수인 경우
                    print(" " * (t//2) + p_id + " " * (t//2), end="|")
                else:   #t가 짝수인 경우
                    print(" " * (t//2-1)+ p_id + " " * (t//2), end="|")

    print("")
    print("="*30)
    print("cpu timeine:",cpu)

    print("")

    #output 2) 프로세스별 TT, WT
    print("[각 프로세스 별 TT와 WT]")

    for i in range(p_num):
        print("%s번째 프로세스: TT %2d / WT %2d"%(pid_list[i], tt_list[i], wt_list[i]))

    print("")

    #output 3) 프로세스 TT, WT 평균
    print("[전체 프로세스의 TT 평균과 WT 평균]")
    print("전체 프로세스의 TT 평균:", tt_mean)
    print("전체 프로세스의 WT 평균:", wt_mean)
