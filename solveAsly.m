

%[Ts B A Hr Hs dist P Bm Am]=
c=clock;
BW=0; %rad/s
%GET PLANT PTF
if (contplant)  %continuous plant
   
    sysc=tf(num, den, 'iodelay', delay);
    sysd=c2d(sysc, Ts, 'zoh');
    [B A]=tfdata(sysd, 'v');
    
    %get bandwidth
    BW=max(abs(roots(den)));
    
    B=padarray(B', sysd.ioDelay, 0, 'pre')';

else  %discrete plant
    B=Bp;
    A=Ap;
end
%GET REGULATION P(z) & TRACKING Bm(z)/Am(z)
if (contdesign)%continuous design criteria

    P=z_polynomial(w0reg, zetareg, Ts);

    BW=max([BW w0reg]);
    
   
    Am=z_polynomial(w0track, zetatrack, Ts);

    BW=max([BW w0track]);
    
    Bm=sum(Am) ;%Bm(z)=Am(1)

else  %discrete design criteria
    P = P;
    Am=Am;
	Bm=Bm;
end

Hr=Hr;
Hs=Hs;

if distfreq==0
    distfreq=[1 -1];
else
    distfreq=[1, -2*cos(2*pi*distfreq*Ts), 1]
end

solvee(Ts,B,A,Hr,Hs,distfreq,P,Bm,Am,removestablezeroes);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function solvee(Ts,Bp,Ap,Hr,Hs,dist,P,Bm,Am,removestablezeroes)

Bps=[]; Bpu=[];

if (removestablezeroes)  %cancel stable zeros
    [Bps Bpu]=separate_B(Bp);
else                                %don't cancel
    Bps=1; Bpu=Bp;
end

%SOLUTION
%Ap Hs S + Bp Hr R = P      (no zeros cancelled)
S_has_integrator=has_no_integrator(Ap);
Hs_full=[];
if S_has_integrator
    Hs_full=conv(Hs, [1 -1]);   
else
    Hs_full=Hs;
end
A=conv(Ap, Hs_full)';
B=conv(Bpu, Hr)';
nA=size(A); nA=nA(1)-1; %vertical vector size, power of z = size-1
nB=size(B); nB=nB(1)-1;
A=padarray(A, nB-1, 0, 'post');
B=padarray(B, nA-1, 0, 'post');
M=[];
for k=1:nB
    M=[M A];
    A=circshift(A, 1);
end
for k=(nB+1):(nB+nA)
    M=[M B];
    B=circshift(B, 1);
end
%M
n=size(M);  n=n(1);%M is a square matrix
nP=size(P); nP=nP(2);
P_full=padarray(P', n-nP, 0, 'post');
SR=M\P_full;

%Extract R, S, T
R=SR((nB+1):(nB+nA))';
S=SR(1:nB)';
if S_has_integrator
    S=conv(S, [1, -1]);
end
S=conv(S, Bps);


R=conv(R, Hr)
S=conv(S, Hs)
T=P/sum(Bpu)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function no_int=has_no_integrator(A)%finds if A has no integrator
r=roots(A);
sr=size(r);
no_int=true;
for k=1:sr(1)
    if r(k)==1
        no_int=false;
    end
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [B_stable B_unstable]=separate_B(B)
lz=count_leading_zeros(B);
gain=B(lz+1);%find polynomial gain
r=roots(B);
B_stable=1; B_unstable=1;
sr=size(r);
for k=1:sr(1)
    if abs(r(k))>=1 %unstable & critical zeros
        B_unstable=conv(B_unstable, [1 -r(k)]);
    else            %stable zeros
        B_stable=conv(B_stable, [1 -r(k)]);
    end
    B_stable=B_stable*gain; %put the gain in the cancelled part
    %B_unstable
B_unstable=padarray(B_unstable', lz, 0, 'pre')'; %put the delays in non-cancelled par
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function lz=count_leading_zeros(v)
size_v=size(v) ;

if size_v(1)<size_v(2)%horizontal vector
    v=v';
end
size_v=size(v);
lz=0;

for k=1:size_v(1)
    if v(k)==0
        lz=lz+1;
        
    else
        break;
    end
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function P=z_polynomial(w0, zeta, Ts)
s=w0*(-zeta+1i*sqrt(1-zeta*zeta));
z=exp(s*Ts);
rez=real(z); imz=imag(z);
P=[1, -2*rez, rez*rez+imz*imz];

