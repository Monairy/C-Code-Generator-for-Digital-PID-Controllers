




BW=0;
if (contdesign)%continuous design

    P=z_polynomial(w0reg, zetareg, Ts);
    BW=max([BW w0reg]);

    Am=z_polynomial(w0track, zetatrack, Ts);
    BW=max([BW w0track]);
    
    Bm=sum(Am) ;%Bm(z)=Am(1)

else %discrete design
    P = P;
    Am=Am;
	Bm=Bm;
end


name=sprintf('SystemSimulation');

sim_time=100; t_ref=5; t_dist=50;
str_Ts=num2str(Ts);
x=0; y=0;
sys=new_system(name);
set_param(name, 'stoptime',num2str(sim_time));
x=x+0; y=y+40;%step position
add_block('simulink/Sources/Step', [name '/Reference'], 'position',[x, y, x+30, y+30],...
    'time',num2str(t_ref*Ts), 'sampletime',str_Ts);
x=x+60;%step width

add_block('simulink/Discrete/Discrete Filter', [name '/Bm(z)//Am(z)'], 'position',[x, y, x+150, y+30],...
    'numerator',['[' num2str(Bm) ']'], 'denominator',['[' num2str(Am) ']'], 'sampletime',str_Ts);
x=x+160;%tracking width
add_line(name, 'Reference/1', 'Bm(z)//Am(z)/1');

T_block=add_block('simulink/Discrete/Discrete Filter', [name '/T(z)'], 'position',[x, y, x+100, y+30],...
    'numerator',['[' num2str(T) ']'], 'denominator','[1]', 'sampletime',str_Ts);
x=x+150;%T width
add_line(name, 'Bm(z)//Am(z)/1', 'T(z)/1');

firstsum_block=add_block('simulink/Math Operations/Sum', [name '/Sum1'], 'position',[x, y+5, x+20, y+5+20],...
    'inputs','|+-');
x=x+40;%sum width
add_line(name, 'T(z)/1', 'Sum1/1');

%Hs_block=add_block('simulink/Discrete/Discrete Filter', [name '/1//Hs(z)'], 'position',[x, y, x+100, y+30],...
  %  'numerator','[1]', 'denominator',['[' num2str(Hs) ']'], 'sampletime',str_Ts);
%Hr_block=add_block('simulink/Discrete/Discrete Filter', [name '/Hr(z)'], 'position',[x, y+100, x+100, y+130],...
  %  'numerator',['[' num2str(Hr) ']'], 'denominator','[1]', 'sampletime',str_Ts, 'orientation','left');

x=x+130;%Hs width

R_block=add_block('simulink/Discrete/Discrete Filter', [name '/R(z)'], 'position',[x, y+100, x+100, y+130],...
    'numerator',['[' num2str(R) ']'], 'denominator','[1]', 'sampletime',str_Ts, 'orientation','left');

%add_line(name, 'Sum1/1', '1//Hs(z)/1');%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


S_block=add_block('simulink/Discrete/Discrete Filter', [name '/1//S(z)'], 'position',[x, y, x+100, y+30],...
    'numerator','[1]', 'denominator',['[' num2str(S) ']'], 'sampletime',str_Ts);

x=x+130;%S width
add_line(name, 'Sum1/1', '1//S(z)/1');
%add_line(name, '1//Hs(z)/1', '1//S(z)/1');

x=x+330;%make space for possible continuous plant
secondsum_block=add_block('simulink/Math Operations/Sum', [name '/Sum2'], 'position',[x, y+70, x+20, y+90],...
    'inputs','++|');
x=x+20;%sum width

x=x-285;%return till after S
if (contplant)%continuous plant
    add_block('simulink/Discrete/Zero-Order Hold', [name '/Zero-Order Hold'], 'position',[x, y, x+35, y+30]);
    x=x+35;%ZOH width
    add_line(name, '1//S(z)/1', 'Zero-Order Hold/1');
    
    x=x+35;%spacing
    add_block('simulink/Continuous/Transport Delay', [name '/Plant Delay'], 'position',[x, y, x+30, y+30],...
        'delaytime',delay);
    x=x+30;%delay width
    add_line(name, 'Zero-Order Hold/1', 'Plant Delay/1');
    
    x=x+35;%spacing
    add_block('simulink/Continuous/Transfer Fcn', [name '/Gp(s)'], 'position',[x, y, x+120, y+30],...
        'numerator',num, 'denominator',den);
    x=x+120;%Gp width
    add_line(name, 'Plant Delay/1', 'Gp(s)/1');
    add_line(name, 'Gp(s)/1', 'Sum2/2');
else%discrete plant
    add_block('simulink/Discrete/Discrete Filter', [name '/Bp(z)//Ap(z)'], 'position',[x, y+40, x+150, y+75],...
        'numerator',['[' num2str(Bp) ']'], 'denominator',['[' num2str(Ap) ']'], 'sampletime',str_Ts);
    x=x+200;%plant width
    add_line(name, '1//S(z)/1', 'Bp(z)//Ap(z)/1');
    add_line(name, 'Bp(z)//Ap(z)/1', 'Sum2/2');
end

x=x+35;%spacing till sum2
x=x-135;%new branch
add_block('simulink/Sources/Sine Wave', [name '/Disturbance'], 'position',[x+40, 0, x+80, 0+30],...
    'amplitude','-0.25', 'Frequency',num2str(distfreq), 'phase','pi/2', 'sampletime',str_Ts);
x=x+30;%disturbance width

x=x+40;%spacing
add_block('simulink/Continuous/Transport Delay', [name '/Disturbance Delay'], 'position',[x+40, 0, x+70, 0+30],...
    'delaytime',num2str(t_dist*Ts));
x=x+30;%delay width
add_line(name, 'Disturbance/1', 'Disturbance Delay/1');
add_line(name, 'Disturbance Delay/1', 'Sum2/1');

x=x+125;%spacing from dist. delay till mux
add_block('simulink/Signal Routing/Mux', [name '/Mux'], 'position',[x, y+15, x+5, y+15+38]);
x=x+5;%mux width

x=x+35;%spacing
add_block('simulink/Sinks/Scope', [name '/Scope'], 'position',[x, y+15, x+30, y+60]);
add_line(name, '1//S(z)/1', 'Mux/1');
add_line(name, 'Sum2/1', 'Mux/2');
add_line(name, 'Mux/1', 'Scope/1');
%add_line(name, 'Sum2/1', 'Scope/1');

%feedback blocks
x=x-600; y=y+150;%from scope left edge to R

%all=get(get_param(block_R, 'handle'))
x=x-50;%R width

add_line(name, 'Sum2/1', 'R(z)/1');

x=x-190;%spacing

x=x-195;
add_line(name, 'R(z)/1)', 'Sum1/2');
%add_line(name, 'R(z)/1', 'Hr(z)/1');
%add_line(name, 'Hr(z)/1)', 'Sum1/2');

 Simulink.BlockDiagram.createSubSystem([firstsum_block, R_block,S_block,T_block]);
%convert2subsys([H_block, block_R]);
open_system(sys);
%clear;

