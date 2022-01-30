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
data = pd.read_excel(args+'_Cleaned.xlsx')

f=open(args+'_Answer.txt','w')

AAVY=data.AAVY
SACX=data.SACX
AANY=data.AANY
SAVZ=data.SAVZ
AAVX=data.AAVX
AACX=data.AACX
SANX=data.SANX
limit=1800
a=int(m)
cp1=-7
cp2=-6
cp3=-5
cp4=-4
cp5=-3
cp6=-2
cp7=-1
Strike=0
HS=[]
HM=[]
HO=[]
TO=[]
TM=[]
sanx=0
while (a<limit):
    a=a+1
    Strike=0
    Max=0
    ToeMax=0
    ToeOff=0
    
    if((cp1<cp7)and(AAVY[a]<-50)):
        cp1=a
    elif((cp2<cp1)and(AAVY[a]>0)):
        cp2=a
    elif((cp3<cp2)and(abs(SACX[a]>1))):
        cp3=a
        Strike=1
        HS.append(cp3)
        sanx=SANX[cp3]
    elif((cp4<cp3)and((AANY[a]>AANY[a-1])or(SANX[a]<(sanx-10)))):
        cp4=a
        flag=1   
    elif((cp5<=cp4)and(abs(AAVY[a])<10)and(flag==1)):
        cp5=a
        Max=1
        flag=0
        HM.append(cp5)
    elif((cp6<cp5)and(SAVZ[a]>SAVZ[a-1])and((abs(AANY[a]-AANY[a-1])>1)or(SANX[a]<(sanx-30))or(AAVY[a]>31))):
        cp6=a
        ToeMax=1
        TM.append(cp6)
    elif((cp7<cp6)and(((AAVY[a]<AAVY[a-1])and(AAVY[a]>10)and(SAVZ[a]>SAVZ[a-1])) or (AAVY[a]>200) or (SANX[a]<(sanx-50)))):
        cp7=a
        ToeOff=1
        TO.append(cp7)

    f.write(str(data.Heel[a]) + ' ' + str(data.Toe[a]) +' '+ str(Strike) + ' ' + str(Max) + ' ' + str(ToeMax) +' ' + str(ToeOff) + '\n' )

#    print(a)
#    print()

f.close() 

print(HS)
print(HM)
print(TM)
print(TO)



#################################################################################################################################################

def Actual_HeelStrike (data,count=0):
	flag=0
	while(flag!=1):
		if((data.Heel[count]>=1)and(data.Heel[count-1]<1)and(data.Heel[count+1]>=1)and(data.Heel[count+2]>=1)and(data.Heel[count+3]>=1)):
			flag=1
		else:
			count=count+1
		if(count>=limit):
			break
	return count

def Actual_HeelMax (data,count=0):
	flag=0
	limit_HM = count+40
	maxi=0
	maxi_idx=count
	while(count<limit_HM):
		if(data.Heel[count]>maxi):
			maxi=data.Heel[count]
			maxi_idx = count
			count = count+1
		else:
			count=count+1
		if(count>=limit):
			break
	return maxi_idx

def Actual_HeelOff(data,count=0):
	flag=0
	while(flag!=1):
		if((data.Heel[count]==0)):
			flag=1
		else:
			count=count+1
		if(count>=limit):
			break
	return count

def Actual_ToeMax(data,count=0):
	flag=0
	limit_TM = count+50
	maxi=0
	maxi_idx=count
	while(count<limit_TM):
		if(data.Toe[count]>maxi):
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
		if((data.Toe[count]<1)and(data.Toe[count+1]<1)):
			flag=1
		else:
			count=count+1
		if(count>=limit):
			break
	return count
	
#################################################################################################################################################
A_HS=[]
A_HM=[]
A_HO=[]
A_TO=[]
A_TM=[]
count = int(m)

while(count<=limit):
	count = Actual_HeelStrike(data,count)
	A_HS.append(count)
	count=count+30
	

i=0
while(i<len(A_HS)):
	count = A_HS[i]
	count = Actual_HeelOff(data,count)
	A_HO.append(count)
	i=i+1

i=0
while(i<len(A_HO)):
	count = A_HO[i]+5
	if(count>=limit):
		break
	count = Actual_ToeOff(data,count)
	A_TO.append(count)
	i=i+1

i=0
while(i<len(A_HO)):
	count = A_HS[i]
	count = Actual_HeelMax(data,count)
	A_HM.append(count)	
	i=i+1

i=0
while(i<len(A_HO)):
	count = A_HS[i]
	count = Actual_ToeMax(data,count)
	A_TM.append(count)	
	i=i+1


#############################################################################################################################################


#################################################################################################################################################

print("Actual HS:")
print(A_HS)
print("Actual HM:")
print(A_HM)
print("Actual TM:")
print(A_TM)
print("Actual TO:")
print(A_TO)
#################################################################################################################################################
   
sampling_time = 60/len(data.Time)
    
#################################################################################################################################################
#################################################################################################################################################

freq = 0
if (len(HS)>=len(A_HS)):
	freq = len(A_HS)
else:
	freq = len(HS)
diff_HS = []
array_HS=[]
count  = 0
total = 0
while(count<freq):
	diff_HS.append(abs(HS[count] - A_HS[count]))
	array_HS.append((HS[count]-A_HS[count])*sampling_time)
	total = total + diff_HS[count]
	count = count+1
print("Actual Heel Strikes:")
print(A_HS)
print("Detected Heel Strikes:")
print(HS)
print("Number of Actual Heel Strikes:")
print(len(A_HS))
print("Number of Detected Heel Strikes:")
print(len(HS))	
print("Difference in Heel Strike Actual and Detected:")
print(diff_HS)
print("Avg Diff in HS (Samples):")
print(total/freq)
print("Avg Diff in HS (Seconds):")
print(total*sampling_time/freq)
HS_error = total*sampling_time/freq

#################################################################################################################################################

freq = 0
if (len(HM)>=len(A_HM)):
	freq = len(A_HM)
else:
	freq = len(HM)
diff_HM = []
count  = 0
total = 0
array_HM=[]
while(count<freq):
	diff_HM.append(abs(HM[count] - A_HM[count]))
	array_HM.append((HM[count]-A_HM[count])*sampling_time)
	total = total + diff_HM[count]
	count = count+1

print("Actual HeelMax:")
print(A_HM)
print("Detected HeelMax:")
print(HM)	
print("Number of Actual HeelMax:")
print(len(A_HM))
print("Number of Detected HeelMax:")
print(len(HM))
print("Difference in HeelMax Actual and Detected:")
print(diff_HM)
print("Avg Diff in HM (Samples):")
print(total/freq)
print("Avg Diff in HM (Seconds):")
print(total*sampling_time/freq)
HM_error = total*sampling_time/freq

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
	array_TM.append((TM[count]-A_TM[count])*sampling_time)
	total = total + diff_TM[count]
	count = count+1

print("Actual Heel Offs:")
print(A_TM)
print("Detected Heel Offs:")
print(TM)	
print("Number of Actual Heel Offs:")
print(len(A_TM))
print("Number of Detected Heel Offs:")
print(len(TM))
print("Difference in Heel Offs Actual and Detected:")
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

print("Avg Diff in HS (Seconds):")
print(HS_error)
print("Avg Diff in HM (Seconds):")
print(HM_error)
print("Avg Diff in TM (Seconds):")
print(TM_error)
print("Avg Diff in TO (Seconds):")
print(TO_error)

#################################################################################################################################################
#dfa = pd.DataFrame({'HS' : array_HS , 'HM' : array_HM , 'TM' : array_TM , 'TO' : array_TO})

#print(dfa)
#dfa.boxplot()
#plt.show()
#################################################################################################################################################

file=open('Error_Online.txt','a')
file.write(args + ' ' + str(HS_error)+' ' + str(HM_error) + ' ' + str(TM_error) +' '+ str(TO_error) + '\n')
file.close()
