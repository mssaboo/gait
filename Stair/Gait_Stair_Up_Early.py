#Note: In this code (x,y,z) == (z,y,x) for IMU readings;
#IMU[0] = IMU z component; IMU[1] = IMU y component; IMU[2] = IMU x component;
#Z Axis is perpendicular to the plane of the sensor; X axis is along the pins and Y axis is in the plane and perpendicular to pins;
import csv
import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt

args=sys.argv[1]
m = sys.argv[2]
n = sys.argv[3]
start = int(m)
end = int(n)

data = pd.read_excel(args+'_Cleaned.xlsx')

f=open(args+'_Answer.txt','w')

AAVY=data.AAVY
SACX=data.SACX
SAVZ=data.SAVZ
SANX=data.SANX
limit=end
a=start
cp0=-8
cp1=-7
cp2=-6
cp3=-5
cp4=-4
cp5=-3
cp6=-2
cp7=-1
cp8=0
AAVY_count=0
flag1=0
TS=[]
TM=[]
TO=[]
MS=[]
sanx=0
savz=0
while (a<limit):
    a=a+1
    Strike=0
    Max=0
    ToeOff=0
    MidSwing=0
    if((cp0<cp7)and(SAVZ[a]<-50)and(SAVZ[a]>SAVZ[a-1])and(abs(SAVZ[a])<500)and(abs(SAVZ[a-1])<500)):
        cp0=a
        Strike=1
        TS.append(cp0)
    if((cp1<cp0)and((abs(SACX[a])>6)or(abs(AAVY[a]-AAVY[a-1])>200)and(abs(AAVY[a])<500)and(abs(AAVY[a-1])<500)or(SAVZ[a]>0))):
        cp1=a
    if((cp2<cp1)and(abs(SACX[a])<1)):
        cp2=a
    if((cp3<cp2)and(SAVZ[a]<SAVZ[a-1])and(abs(SAVZ[a]<500))and(abs(SAVZ[a-1]<500))and(SAVZ[a]<20)):
        cp3=a
        savz=SAVZ[a]
    if((cp4<cp3)and(SAVZ[a]>savz+30)and(abs(SAVZ[a])<500)and(abs(SAVZ[a-1])<500)):
        cp4=a
        Max=1
        TM.append(cp4)
    if((cp5<cp4)and(AAVY[a]>60)and(AAVY[a]>AAVY[a-1])and(abs(AAVY[a])<500)and(abs(AAVY[a-1])<500)):
        cp5=a
    if((cp6<cp5)and((AAVY[a]>220)or(AAVY[a]<AAVY[a-1]))and(abs(AAVY[a])<500)and(abs(AAVY[a-1])<500)):
        cp6=a
        ToeOff=1
        TO.append(cp6)
    if((cp7<cp6)and(SAVZ[a]>50)):
        cp7=a
    if((cp8<cp7)and(SAVZ[a]<0)):
        cp8=a
        MidSwing=1
        MS.append(cp8)

    f.write(str(data.Heel[a]) + ' ' + str(data.Toe[a]) +' '+ str(Strike) + ' ' + str(Max) + ' ' + str(ToeOff) + '\n' )

#    print(a)
#    print()

f.close() 




#################################################################################################################################################

def Actual_ToeStrike (data,count=0):
	flag=0
	while(flag!=1):
		if(((data.Toe[count]>=1)or(data.Heel[count]>=1))and((data.Toe[count-1]<1)or(data.Heel[count-1]<1))and((data.Toe[count+1]>=1)or(data.Heel[count+1]>=1))and((data.Toe[count+2]>=1)or(data.Heel[count+2]>=1))):
			flag=1
		else:
			count=count+1
		if(count>=limit):
			break
	return count 
def Actual_Strike2(data,count=0):
	flag=0
	while(flag!=1):
		if(data.AAVY[count]<-100):
			flag=1
		else:
			count=count+1
		if(count>=limit):
			break
	return count

def Actual_ToeMax (data,count=0):
	flag=0
	limit_TM = count+9
	maxi=0
	maxi_idx=count
	while(count<limit_TM):
		if(data.Toe[count]>=maxi):
			maxi=data.Toe[count]
			maxi_idx = count
			count = count+1
		else:
			count=count+1
		if(count>=limit):
			break
	return maxi_idx

	
def Actual_ToeOff(data,count=0):
	flag=0
	while(flag!=1):
		if((data.Toe[count]<1)and(data.Toe[count+1]<1)and(data.Toe[count+2]<1)):
			flag=1
		else:
			count=count+1
		if(count>=limit):
			break
	return count
	
#################################################################################################################################################
A_TS=[]
A_TM=[]
A_TO=[]
A_MS=[]

j=start
while((data.Toe[j]>0)or(data.Toe[j+1]>0)or(data.Toe[j+2]>0)or(data.Toe[j+3]>0)or(data.Toe[j+4]>0)or(data.Toe[j+5]>0)):
    j=j+1
count = j

while(count<=limit):
	count = Actual_ToeStrike(data,count)
	A_TS.append(count)
	count=count+10
	if(count>limit-10):
		break	
	count=Actual_Strike2(data,count)
	count = count+5
	

i=0
while(i<len(A_TS)):
	count = A_TS[i]
	count=count+10
	while(data.AAVY[count]<100):
		count=count+1
	if(count>limit-10):
		break
	count = Actual_ToeOff(data,count)
	A_TO.append(count)
	i=i+1


i=0
while(i<len(A_TO)):
	count = A_TO[i]-9
	count = Actual_ToeMax(data,count)
	A_TM.append(count)	
	i=i+1

i=0
while(i<len(A_TO)-1):
	A_MS.append((A_TO[i] + A_TS[i+1])/2)
	i=i+1

#############################################################################################################################################


#################################################################################################################################################

#print("Actual HS:")
#print(A_HS)

#print("Actual HM:")
#print(A_HM)

#print("Actual HO:")
#print(A_HO)

#print("Actual TO:")
#print(A_TO)
#################################################################################################################################################

t1 = data.Time[1]
t2 = data.Time[len(data.Time)-1]
t = (t2-t1)/1000   
sampling_time = t/len(data.Time)
    
#################################################################################################################################################

freq = 0
if (len(TS)>=len(A_TS)):
	freq = len(A_TS)
else:
	freq = len(TS)
diff_TS = []
array_TS=[]
count  = 0
total = 0
while(count<freq):
	diff_TS.append(abs(TS[count] - A_TS[count]))
	array_TS.append((TS[count]-A_TS[count])*sampling_time)
	total = total + diff_TS[count]
	count = count+1
print("Actual Toe Strikes:")
print(A_TS)
print("Detected Toe Strikes:")
print(TS)
print("Number of Actual Toe Strikes:")
print(len(A_TS))
print("Number of Detected Toe Strikes:")
print(len(TS))	
print("Difference in Toe Strike Actual and Detected:")
print(diff_TS)
print("Avg Diff in TS (Samples):")
print(total/freq)
print("Avg Diff in TS (Seconds):")
print(total*sampling_time/freq)
TS_error = total*sampling_time/freq

#################################################################################################################################################

freq = 0
if (len(TM)>=len(A_TM)):
	freq = len(A_TM)
else:
	freq = len(TM)
diff_TM = []
count  = 0
total = 0
array_TM=[]
while(count<freq):
	diff_TM.append(abs(TM[count] - A_TM[count]))
	if(data.Toe[TM[count]] == data.Toe[A_TM[count]]):
		diff_TM[count]=0
	array_TM.append((TM[count]-A_TM[count])*sampling_time)
	total = total + diff_TM[count]
	count = count+1

print("Actual ToeMax:")
print(A_TM)
print("Detected ToeMax:")
print(TM)	
print("Number of Actual ToeMax:")
print(len(A_TM))
print("Number of Detected ToeMax:")
print(len(TM))
print("Difference in ToeMax Actual and Detected:")
print(diff_TM)
print("Avg Diff in TM (Samples):")
print(total/freq)
print("Avg Diff in TM (Seconds):")
print(total*sampling_time/freq)
TM_error = total*sampling_time/freq

#################################################################################################################################################

freq = 0
if (len(TO)>=len(A_TO)):
	freq = len(A_TO)
else:
	freq = len(TO)
diff_TO = []
count  = 0
total = 0
array_TO=[]
while(count<freq):
	diff_TO.append(abs(TO[count] - A_TO[count]))
	array_TO.append((TO[count]-A_TO[count])*sampling_time)
	total = total + diff_TO[count]
	count = count+1

print("Actual Toe Offs:")
print(A_TO)
print("Detected Toe Offs:")
print(TO)
print("Number of Actual Toe Offs:")
print(len(A_TO))
print("Number of Detected Toe Offs:")
print(len(TO))	
print("Difference in Toe Offs Actual and Detected:")
print(diff_TO)
print("Avg Diff in TO (Samples):")
print(total/freq)
print("Avg Diff in TO (Seconds):")
print(total*sampling_time/freq)
TO_error = total*sampling_time/freq

#################################################################################################################################################

freq = 0
if (len(MS)>=len(A_MS)):
	freq = len(A_MS)
else:
	freq = len(MS)
diff_MS = []
count  = 0
total = 0
array_MS=[]
while(count<freq):
	diff_MS.append(abs(MS[count] - A_MS[count]))
	array_MS.append((MS[count]-A_MS[count])*sampling_time)
	total = total + diff_MS[count]
	count = count+1

print("Actual MidSwings:")
print(A_MS)
print("Detected MidSwings:")
print(MS)
print("Number of Actual MidSwings:")
print(len(A_MS))
print("Number of Detected MidSwings:")
print(len(MS))	
print("Difference in MidSwings Actual and Detected:")
print(diff_MS)
print("Avg Diff in MS (Samples):")
print(total/freq)
print("Avg Diff in MS (Seconds):")
print(total*sampling_time/freq)
MS_error = total*sampling_time/freq

#################################################################################################################################################

print("Avg Diff in TS (Seconds):")
print(TS_error)
print("Avg Diff in TM (Seconds):")
print(TM_error)
print("Avg Diff in TO (Seconds):")
print(TO_error)
print("Avg Diff in MS (Seconds):")
print(MS_error)


#################################################################################################################################################
#dfa = pd.DataFrame({'HS' : array_HS , 'HM' : array_HM , 'HO' : array_HO , 'TO' : array_TO})

#print(dfa)
#dfa.boxplot()
#plt.show()
#################################################################################################################################################

file=open('Error_Online.txt','a')
file.write(args + ' ' + str(TS_error)+' ' + str(TM_error) +' '+ str(TO_error) + ' ' + str(len(TO)) + '\n')
file.close()
