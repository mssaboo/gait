hold on;
clear;

file = readtable('MaheshWalk001_Cleaned.xlsx', 'Sheet',1,'Range','A1:Z600');


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
Heel = smooth(Heel)
AAVY = smooth(AAVY)
plot(Time,Heel);
plot(Time,AAVY);
legend('Heel','SAVZ');
%savefig('Toe_AACY.fig');