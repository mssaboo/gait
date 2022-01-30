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
AANY=data.AANY
SAVZ=data.SAVZ
#AAVX=data.AAVX
#AACX=data.AACX
SANX=data.SANX
limit=end
a=start
cp1=-7
cp2=-6
cp3=-5
cp4=-4
cp5=-3
cp6=-2
cp7=-1
cp8=0
cp9=1
cp10=2
cp11=3
cp12=4
Strike=0
EHS=[]
HS=[]
EHM=[]
HM=[]
EHO=[]
HO=[]
ETO=[]
TO=[]
MS=[]
sanx=0
while (a<limit):
    a=a+1
    Strike=0
    Max=0
    HeelOff=0
    ToeOff=0
    
    if((cp1<cp7)and(SAVZ[a]<-50)and(SAVZ[a]>SAVZ[a-1])):
        cp1=a
    elif((cp2<cp1)and(SAVZ[a]>-100)):
        cp2=a
        EHS.append(cp1)
    elif((cp3<cp2)and(AAVY[a]>0)):
        cp3=a
    elif((cp4<cp3)and(abs(SACX[a]>1))):
        cp4=a
        Strike=1
        HS.append(cp4)
        sanx=SANX[cp4]
    elif((cp6<cp4)and(AAVY[a]<50)and(AAVY[a]<AAVY[a-1])):
        cp6=a
        EHM.append(cp6)   
    elif((cp7<cp6)and(abs(AAVY[a])<10)and(abs(AAVY[a-1])<10)and(abs(AAVY[a-2])<10)):
        cp7=a
        Max=1
        flag=0
        HM.append(cp7)
    elif((cp8<cp7)and(SAVZ[a]>SAVZ[a-1])):
        cp8=a
        EHO.append(cp8)
    elif((cp9<cp8)and(((SAVZ[a]>SAVZ[a-1])and(AAVY[a]>1)and(AAVY[a-1]>1)and(SANX[a]<0))or(SANX[a]<(sanx-25)))):
        cp9=a
        HeelOff=1
        HO.append(cp9)
    elif((cp10<cp9)and(AAVY[a]>AAVY[a-1])and(AAVY[a]>50)):
        cp10=a
        ETO.append(cp10)
    elif((cp11<cp10)and(((AAVY[a]<AAVY[a-1])and(AAVY[a]>10)and(SAVZ[a]>SAVZ[a-1])) or (AAVY[a]>200) or (SANX[a]<(sanx-50)))):
        cp11=a
        ToeOff=1
        TO.append(cp11)
    elif((cp12<cp11)and(SAVZ[a]<0)):
        cp12=a
        MS.append(cp12)

    f.write(str(data.Heel[a]) + ' ' + str(data.Toe[a]) +' '+ str(Strike) + ' ' + str(Max) + ' ' + str(HeelOff) +' ' + str(ToeOff) + '\n' )

#    print(a)
#    print()

f.close() 



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
A_MS=[]
count = start

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
while(i<len(A_TO)-1):
	A_MS.append((A_TO[i]+A_HS[i+1])/2)
	i=i+1

A_EHS = A_HS
A_EHM = A_HM
A_EHO = A_HO
A_ETO = A_TO

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
if (len(EHS)>=len(A_EHS)):
	freq = len(A_EHS)
else:
	freq = len(EHS)
diff_EHS = []
array_EHS=[]
count  = 0
total = 0
while(count<freq):
	diff_EHS.append(abs(EHS[count] - A_EHS[count]))
	array_EHS.append((EHS[count]-A_EHS[count])*sampling_time)
	total = total + diff_EHS[count]
	count = count+1
print("Actual Early Heel Strikes:")
print(A_EHS)
print("Detected Early Heel Strikes:")
print(EHS)
print("Number of Actual Early Heel Strikes:")
print(len(A_EHS))
print("Number of Detected Early Heel Strikes:")
print(len(EHS))	
print("Difference in Early Heel Strike Actual and Detected:")
print(diff_EHS)
print("Avg Diff in EHS (Samples):")
print(total/freq)
print("Avg Diff in EHS (Seconds):")
print(total*sampling_time/freq)
EHS_error = total*sampling_time/freq

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
if (len(EHM)>=len(A_EHM)):
	freq = len(A_EHM)
else:
	freq = len(EHM)
diff_EHM = []
count  = 0
total = 0
array_EHM=[]
while(count<freq):
	diff_EHM.append(abs(EHM[count] - A_EHM[count]))
	array_EHM.append((EHM[count]-A_EHM[count])*sampling_time)
	total = total + diff_EHM[count]
	count = count+1

print("Actual Early HeelMax:")
print(A_EHM)
print("Detected Early HeelMax:")
print(EHM)	
print("Number of Actual Early HeelMax:")
print(len(A_EHM))
print("Number of Detected Early HeelMax:")
print(len(EHM))
print("Difference in Early HeelMax Actual and Detected:")
print(diff_EHM)
print("Avg Diff in EHM (Samples):")
print(total/freq)
print("Avg Diff in EHM (Seconds):")
print(total*sampling_time/freq)
EHM_error = total*sampling_time/freq

#################################################################################################################################################
freq = 0
if (len(HO)>=len(A_HO)):
	freq = len(A_HO)
else:
	freq = len(HO)
diff_HO = []
count  = 0
total = 0
array_HO=[]
while(count<freq):
	diff_HO.append(abs(HO[count] - A_HO[count]))
	array_HO.append((HO[count]-A_HO[count])*sampling_time)
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
if (len(EHO)>=len(A_EHO)):
	freq = len(A_EHO)
else:
	freq = len(EHO)
diff_EHO = []
count  = 0
total = 0
array_EHO=[]
while(count<freq):
	diff_EHO.append(abs(EHO[count] - A_EHO[count]))
	array_EHO.append((EHO[count]-A_EHO[count])*sampling_time)
	total = total + diff_EHO[count]
	count = count+1

print("Actual Early Heel Offs:")
print(A_EHO)
print("Detected Early Heel Offs:")
print(EHO)	
print("Number of Actual Early Heel Offs:")
print(len(A_EHO))
print("Number of Detected Early Heel Offs:")
print(len(EHO))
print("Difference in Early Heel Offs Actual and Detected:")
print(diff_EHO)
print("Avg Diff in EHO (Samples):")
print(total/freq)
print("Avg Diff in EHO (Seconds):")
print(total*sampling_time/freq)
EHO_error = total*sampling_time/freq
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
if (len(ETO)>=len(A_ETO)):
	freq = len(A_ETO)
else:
	freq = len(ETO)
diff_ETO = []
count  = 0
total = 0
array_ETO=[]
while(count<freq):
	diff_ETO.append(abs(ETO[count] - A_ETO[count]))
	array_ETO.append((ETO[count]-A_ETO[count])*sampling_time)
	total = total + diff_ETO[count]
	count = count+1

print("Actual Early Toe Offs:")
print(A_ETO)
print("Detected Early Toe Offs:")
print(ETO)
print("Number of Actual Early Toe Offs:")
print(len(A_ETO))
print("Number of Detected Early Toe Offs:")
print(len(ETO))	
print("Difference in Early Toe Offs Actual and Detected:")
print(diff_ETO)
print("Avg Diff in ETO (Samples):")
print(total/freq)
print("Avg Diff in ETO (Seconds):")
print(total*sampling_time/freq)
ETO_error = total*sampling_time/freq

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

print("Actual Early Mid Swings:")
print(A_MS)
print("Detected Early Mid Swings:")
print(MS)
print("Number of Actual Early Mid Swings:")
print(len(A_MS))
print("Number of Detected Early Mid Swings:")
print(len(MS))	
print("Difference in Early Mid Swings Actual and Detected:")
print(diff_MS)
print("Avg Diff in MS (Samples):")
print(total/freq)
print("Avg Diff in MS (Seconds):")
print(total*sampling_time/freq)
MS_error = total*sampling_time/freq

#################################################################################################################################################

print("Avg Diff in HS (Seconds):")
print(HS_error)
print("Avg Diff in HM (Seconds):")
print(HM_error)
print("Avg Diff in HO (Seconds):")
print(HO_error)
print("Avg Diff in TO (Seconds):")
print(TO_error)
print("Avg Diff in EHS (Seconds):")
print(EHS_error)
print("Avg Diff in EHM (Seconds):")
print(EHM_error)
print("Avg Diff in EHO (Seconds):")
print(EHO_error)
print("Avg Diff in ETO (Seconds):")
print(ETO_error)
print("Avg Diff in MS (Seconds):")
print(MS_error)


#################################################################################################################################################

savz_HS=[]
savz_HS_time=[]
for i in HS:
        savz_HS.append(data.Heel[HS])
        savz_HS_time.append(data.Time[HS])

#plt.plot(data.Time,data.SAVZ)
plt.ylim(-15,60)
plt.plot(data.Time,data.Heel,label='Heel')
plt.plot(savz_HS_time,savz_HS,'ro',markersize=7)
plt.plot(savz_HS_time[0],savz_HS[0],'ro',markersize=7,label='HS')

savz_HM=[]
savz_HM_time=[]
for i in HM:
        savz_HM.append(data.Heel[HM])
        savz_HM_time.append(data.Time[HM])

#plt.plot(data.Time,data.SAVZ)
plt.ylim(-15,60)
plt.plot(savz_HM_time,savz_HM,'g^',markersize=7)
plt.plot(savz_HM_time[0],savz_HM[0],'g^',markersize=7,label='HM')

savz_HO=[]
savz_HO_time=[]
for i in HO:
        savz_HO.append(data.Heel[HO])
        savz_HO_time.append(data.Time[HO])

#plt.plot(data.Time,data.SAVZ)
plt.ylim(-15,60)
plt.plot(savz_HO_time,savz_HO,'ys',markersize=7)
plt.plot(savz_HO_time[0],savz_HO[0],'ys',markersize=7,label='HO')


plt.legend()
plt.show()

###################################################################################################




###################################################################################################




###################################################################################################




###################################################################################################



###################################################################################################





###################################################################################################




###################################################################################################




###################################################################################################


###################################################################################################

file=open('Error_Online.txt','a')
file.write(args + ' ' + str(HS_error)+' ' + str(HM_error) + ' ' + str(HO_error) +' '+ str(TO_error) + ' ' + str(EHS_error)+' ' + str(EHM_error) + ' ' + str(EHO_error) +' '+ str(ETO_error) + ' ' + str(MS_error) + ' ' + str(len(TO)) + '\n')
file.close()
