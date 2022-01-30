#Note: In this code (x,y,z) == (z,y,x) for IMU readings;
#IMU[0] = IMU z component; IMU[1] = IMU y component; IMU[2] = IMU x component;
#Z Axis is perpendicular to the plane of the sensor; X axis is along the pins and Y axis is in the plane and perpendicular to pins;
import csv
import numpy
import pandas as pd
import sys

args=sys.argv[1]

data = pd.read_excel(args+'_Cleaned.xlsx')

f=open(args+'_Answer.txt','w')

AAVY=data.AAVY
SACX=data.SACX
AANY=data.AANY
SAVZ=data.SAVZ
AAVX=data.AAVX
AACX=data.AACX
limit=2000
a=200
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
HeelStrikeOne=0
while (a<limit):
    a=a+1
    Strike=0
    Max=0
    HeelOff=0
    ToeOff=0
    
    if((cp1<cp7)and(AAVY[a]<-50)):
        cp1=a
    elif((cp2<cp1)and(AAVY[a]>0)):
        cp2=a
    elif((cp3<cp2)and(abs(SACX[a]>0))):
        cp3=a
        Strike=1
        HS.append(cp3)
    elif((cp4<cp3)and(AANY[a]>AANY[a-1])):
        cp4=a
        flag=1   
    if((cp5<=cp4)and(abs(AAVY[a])<10)and(flag==1)):
        cp5=a
        Max=1
        flag=0
        HM.append(cp5)
    elif((cp6<cp5)and((AAVY[a]>0)and(SAVZ[a]-SAVZ[a-1])>0)):
        cp6=a
        HeelOff=1
        HO.append(cp6)
    elif((cp7<cp6)and(((AAVY[a]<AAVY[a-1])and(AAVY[a]>0)) or (AAVY[a]>200))):
        cp7=a
        ToeOff=1
        TO.append(cp7)

    f.write(str(data.Heel[a]) + ' ' + str(data.Toe[a]) +' '+ str(Strike) + ' ' + str(Max) + ' ' + str(HeelOff) +' ' + str(ToeOff) + '\n' )

#    print(a)
#    print()

f.close() 

print(HS)
print(HM)
print(HO)
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
count = 220

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


#############################################################################################################################################


#################################################################################################################################################

print("Actual HS:")
print(A_HS)

print("Actual HM:")
print(A_HM)

print("Actual HO:")
print(A_HO)

print("Actual TO:")
print(A_TO)
#################################################################################################################################################
   
sampling_time = 60/len(data.Time)
    
#################################################################################################################################################

freq = 0
if (len(HS)>=len(A_HS)):
	freq = len(A_HS)
else:
	freq = len(HS)
diff_HS = []
count  = 0
total = 0
while(count<freq):
	diff_HS.append(abs(HS[count] - A_HS[count]))
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
while(count<freq):
	diff_HM.append(abs(HM[count] - A_HM[count]))
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
if (len(HO)>=len(A_HO)):
	freq = len(A_HO)
else:
	freq = len(HO)
diff_HO = []
count  = 0
total = 0
while(count<freq):
	diff_HO.append(abs(HO[count] - A_HO[count]))
	total = total + diff_HO[count]
	count = count+1

print("Actual Heel Offs:")
print(A_HO)
print("Detected Heel Offs:")
print(HO)	
print("Number of Actual Heel Offs:")
print(len(A_HO))
print("Number of Detected Heel Offs:")
print(len(HO))
print("Difference in Heel Offs Actual and Detected:")
print(diff_HO)
print("Avg Diff in HO (Samples):")
print(total/freq)
print("Avg Diff in HO (Seconds):")
print(total*sampling_time/freq)
HO_error = total*sampling_time/freq
#################################################################################################################################################

freq = 0
if (len(TO)>=len(A_TO)):
	freq = len(A_TO)
else:
	freq = len(TO)
diff_TO = []
count  = 0
total = 0
while(count<freq):
	diff_TO.append(abs(TO[count] - A_TO[count]))
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
print("Avg Diff in HO (Seconds):")
print(HO_error)
print("Avg Diff in TO (Seconds):")
print(TO_error)

#################################################################################################################################################
file=open('Error_Online.txt','a')
file.write(args + ' ' + str(HS_error)+' ' + str(HM_error) + ' ' + str(HO_error) +' '+ str(TO_error) + '\n')
file.close()
