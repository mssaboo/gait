hold on;
clear;

file = readtable('Walk1701_Cleaned.xlsx', 'Sheet',1,'Range','A1:Z600');


Time = file.Time;
Heel = file.Heel;
Toe = file.Toe;
SAVZ = file.SAVZ;
SAVY = file.SAVY;
SAVX = file.SAVX;
SANZ = file.SANZ;
SANY = file.SANY;
SANX = file.SANX;
SACZ = file.SACZ;
SACY = file.SACY;
SACX = file.SACX;
AAVZ = file.AAVZ;
AAVY = file.AAVY;
AAVX = file.AAVX;
AANZ = file.AANZ;
AANY = file.AANY;
AANX = file.AANX;
AACZ = file.AACZ;
AACY = file.AACY;
AACX = file.AACX;

%plot(Time,Heel);
%plot(Time,Heel);
%Heel = smooth(AAVY)
%AAVY = smooth(AANY)
plot(Time,Heel);
plot(Time,SACX);
legend('Heel','SAVZ');
%savefig('Toe_AACY.fig');