# To add
# - show inbound and outbound
# - Auto covert every 15 mins to numbers
import pickle
import os
import string
from ReadPKL import ReadPKL


def getTimetable(FileName):
    # global Interval
    Name = FileName.split('-')
    Current = os.getcwd()
    # print(Current)
    BusNum = Name[0]
    Bound = Name[1]

    if '.txt' not in FileName:
        FileName = FileName + '.txt'
    with open(FileName, 'r') as file:
        RawDataList = file.read()
    # RawData = open(FileName, 'r')
    # RawDataList = RawData.read()
    RawDataList = RawDataList.split('\n')
    LineDic = {}
    TimetableDic = {}
    IsRecurrent = False

    LineNum = 0
    while True:
        if LineNum > len(RawDataList) - 1:
            break
        TimeLines = 1
        while True:
            try:
                Line = RawDataList[LineNum + TimeLines]
                # print(RawDataList[0], RawDataList[1])
            except IndexError:
                break
            FirstLetter = Line.split()[0]
            IsTime = False
            if FirstLetter[0].isnumeric() == 1:
                TimeLines += 1
            else:
                break
            # if FirstLetter.isalpha() == 0 and IsTime == 0:
            #     TimeLines += 1
            # else:
            #     break

        for i in range(TimeLines):
            Line = RawDataList[LineNum]
            Line = Line.replace('â€™', '\'')
            Line = Line.replace(':', '')
            FirstLetter = Line.split()[0]
            WithPun = False
            for j in FirstLetter:
                if j in string.punctuation:
                    if j == ':':
                        pass
                    else:
                        WithPun = True
                        break
                else:
                    pass
            if FirstLetter.isalpha() == 0 and WithPun == 0:
                TimeList = Line.split('\t')
                if LineNum == 1:
                    IsRecurrent = CheckRecurrent(TimeList)
                    if IsRecurrent is True:
                        Interval, TimeList = FindRecurrentTime(TimeList)
                        RepeatTimeListDic = FindRepeatTime(Interval, TimeList)
                        List = list(Interval.keys())
                        for k in range(len(List)):
                            Del = List[k] + 1 - k
                            TimeList.pop(Del)
                        TimeList = InsertRepeatTimeList(RepeatTimeListDic, TimeList)
                else:
                    if IsRecurrent is True:
                        RepeatTimeListDic = FindRepeatTime(Interval, TimeList)
                        TimeList = InsertRepeatTimeList(RepeatTimeListDic, TimeList)
            else:
                StopName = Line

            if 0 < i < TimeLines - 1:
                # TimeList.append('\n')
                TimetableDic.setdefault(StopName, []).append(TimeList)
                # TimetableDic.setdefault(StopName, []).append('\n')
                # TimetableDic[StopName] = [TimeList, '\n']
            LineNum += 1
        if TimeLines > 2:
            TimetableDic[StopName].append(TimeList)
        else:
            TimetableDic[StopName] = TimeList
    # print(str(TimetableDic['Broadmead Union Street (B16)']))
    LineDic[int(BusNum)] = TimetableDic
    return LineDic


def CheckRecurrent(List):
    Matching = [R for R in List if 'then every' in R]
    # print(Matching)
    if Matching is []:
        return False
    elif Matching is not []:
        return True


def FindRecurrentTime(List):
    Pos = 0
    Interval = {}
    Count = 0
    while Count < len(List):
        i = List[Count]
        if i.isnumeric() == 0 and ':' not in i:
            Recurrent = i.split(' ')
            for j in Recurrent:
                if j.isnumeric() == 1:
                    Pos -= 1
                    Interval[Pos] = j
                    List.pop(Count)
                    break
        else:
            Count += 1
        Pos += 1
    return Interval, List


def FindRepeatTime(Interval, TimeList):
    RepeatTimeListDic = {}
    PrevLength = 0
    for recur in Interval:
        RepeatTimeList = []
        Repeat = Interval[recur]
        IntervalTimeList = [int(t) for t in Repeat]
        Start = TimeList[recur]
        StartTime = [int(t) for t in Start]
        End = TimeList[recur + 1]
        while True:
            StartTime[-1] += IntervalTimeList[-1]
            StartTime[-2] += IntervalTimeList[-2]
            # NewTime = Start + Repeat * RepeatTime
            # NewTimeList = [int(t) for t in str(NewTime)]
            if StartTime[-1] > 9:
                StartTime[-2] += 1
                StartTime[-1] -= 10

            if StartTime[-2] > 5:
                StartTime[-3] += 1
                StartTime[-2] = StartTime[-2] - 6

            if StartTime[-3] > 9:
                StartTime[-4] += 1
                StartTime[-3] -= 10
            Hour = int(str(StartTime[-4])+str(StartTime[-3]))
            if Hour > 23:
                StartTime[-3] = 24 - Hour
                StartTime[-4] = 0

            # Start = int(''.join(str(t) for t in NewTimeList))
            RepeatTimeList.append(''.join(str(t) for t in StartTime))
            if RepeatTimeList[-1] == End:
                RepeatTimeList.pop()
                if recur != list(Interval.keys())[0]:
                    Position = recur + PrevLength - 1
                else:
                    Position = recur

                RepeatTimeListDic[Position] = RepeatTimeList
                PrevLength += len(RepeatTimeList) - 1
                break
    return RepeatTimeListDic


def InsertRepeatTimeList(Dictionary, TimeList):
    for Key in Dictionary:
        Times = Dictionary[Key]
        for i in range(len(Times)):
            TimeList.insert(Key + 1 + i, Times[i])
    return TimeList


'''Save dictionary into .pkl file (Need to import module pickle)'''
def WriteDic(Dictionary):
    with open('TimetableDic.pkl', 'a+b') as file:
        pickle.dump(Dictionary, file)
        # pass
    with open('TimetableDic.txt', 'a') as file:
        for key in Dictionary:
            ListwithKey = Dictionary[key]
            for k in ListwithKey:
                List = ListwithKey[k]
                file.writelines(str(k) + '\n')
                file.writelines(str(List) + '\n')


# FileName = '1-NorthBound-BroomhillWhitmoreAvenue-CribbsCausewayBusStation.txt'
FileNameList = [
    '1-NorthBound-BroomhillWhitmoreAvenue-CribbsCausewayBusStation.txt',
    '1-SouthBound-CribbsCausewayBusStation-BroomhillWhitmoreAvenue.txt',
    '2-SouthBound-CribbsCauseway-Stockwood',
    '2-SouthBound-Stockwood-CribbsCauseway',
    '73-Northbound-BristolTempleMeadsStation-CribbsCausewayBusStation.txt'
    ]
# FileName = '73-Northbound-BristolTempleMeadsStation-CribbsCausewayBusStation.txt'
# Bound = 'Outbound'
os.chdir('RawTimetableData')
for fileName in FileNameList:
    Timetable = getTimetable(fileName)
    # print(Timetable)
    WriteDic(Timetable)

# ReadPKL('TimetableDic.pkl', 'rb')

'''Load dictionary from .pkl file without losing original variable type '''
File = open('TimetableDic.pkl', 'rb')
Dic = pickle.load(File)
dict(Dic)
print(Dic)
