hold on;
clear;

file = readtable('DeepakDown.xlsx', 'Sheet',1,'Range','A1:Z1000');


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
A=diff(AANY)
A(end+1)=0.0004

%plot(Time,Heel);
%plot(Time,Heel);
Toe=smooth(Toe)
AAVY=smooth(SANX)
SAVZ=smooth(SACX)
plot(Time,Toe);
plot(Time,AAVY);
%plot(Time,10*SAVZ);
legend('Toe','SACX','SANX');
%savefig('Toe_AACY.fig');