% Julian Whitman
% main file for controlling the backpack arm in multiple modes

% Brandon Hung
conn = tcpip('127.0.0.1', 5000);
conn.InputBufferSize = 1024;
conn.Timeout = 1;
conn.Terminator = '~';


% Flags:
sendCommands = 1;
animate = ~sendCommands;
withGripper = 0; % use the gripper
useVoiceInput = 1;
input = 1;

% paths:
addpath('C:\Users\Brandon\Downloads\hebi-matlab-api\hebi');
addpath('C:\Users\Brandon\Documents\GitHub\backpack_arm_control\data')
addpath('C:\Users\Brandon\Documents\GitHub\backpack_arm_control\setup')
addpath('C:\Users\Brandon\Documents\GitHub\backpack_arm_control\modes')
addpath('C:\Users\Brandon\Documents\GitHub\backpack_arm_control\voiceInput')
addpath('C:\Users\Brandon\Documents\GitHub\backpack_arm_control\utils')
% addpath(genpath(pwd));
addpath(genpath('C:\Users\Brandon\Documents\GitHub\matlab_SEA'));
% Brandon Hung

% load armData.mat;
% close all;
% % lengths = [ 0.0250 +  0.0245*11.5 ,  0.0250 +  0.0245*8 , 0.0250/2 +  0.0245* 7.75]
% lengths = [ 0.0250 +  0.0245*11.5 ,  0.0250 +  0.0245*8 , 0.0250/2 + .01 ]
% lengths = [.23;.15;.16;.1]; rb = [.17; 0; .0065];
% a = [ 0, -1.6247    0.0182      ].'
% th = [0, -pi/4, pi/4; 0, -pi/4, pi/4; 0, -pi/4, pi/4];
% S= load('overheadConstrainedD_3.mat');
S= load('armData4J.mat');
a = S.a;
th = S.th;
rb = S.rb;
lengths = S.lengths;
% conditioning angles
th = mod(th, 2*pi);
th(th>pi) = th(th>pi) - 2*pi;
a = mod(a, 2*pi);
a(a>pi) = a(a>pi) - 2*pi;

n = length(a);
if input == 1
   fopen(conn);
end
%% Create animation
if animate
    links = {};
    for i = 1:n-1
        links = [links, {{'X5-9'},...
            {'X5Link','ext',lengths(i),'twist',a(i+1)}  }];
    end
    links = [links, {{'X5-9'},...
        {'X5Link','ext',lengths(n),'twist',0}  }];
    %     if withGripper
    %          links = [links, {{'FieldableGripper'}}]; % this mounts wrong, so I'll leave it off
    %     end
    plt = HebiPlotter('JointTypes', links,'resolution','low');
    plt.setBaseFrame( [R_x(a(1) ), rb; 0 0 0 1] );
    plt.plot(th(:,1))
end

%% create kinematics object
kin = HebiKinematics();
for i =  1:n-1
    kin.addBody('X5-4', 'PosLim', [-pi pi]);
    kin.addBody('X5Link', 'ext', lengths(i), 'twist', a(i+1));
end
kin.addBody('X5-4', 'PosLim', [-pi pi]);
kin.addBody('X5Link', 'ext', lengths(n), 'twist', 0);
kin.setBaseFrame( [R_x(a(1) ), rb; 0 0 0 1] );
trajGen = HebiTrajectoryGenerator(kin);


%% create arm group, gains and command structures
if sendCommands
    if n==4
    makeRobotGroup4;
    else
    makeRobotGroup;
    end
    %     setDefaultGains_XSeries;
            setGainsBackpack;

end

if withGripper
    setupGripper;
end

%% start joystick
joy = vrjoystick(1);
[axes,buttons,povs] = read(joy);


if ~sendCommands
    lastPos = zeros(1,n);
    pos = lastPos;
else
    
    try
        fbk = robot.getNextFeedback();
    catch err
        disp(err.message)
    end
    lastPos =fbk.position;
    disp(['Mean voltage: ' num2str(mean(fbk.voltage), '%2.1f'), ' V']);
    
end




numGoals = size(th, 2);
goalNum = 0;
lastGoalNum = NaN;
running = 1;
mode = 'gravComp';

while running
    
    % grab most recent fbk` c
    if sendCommands
        try
            fbk = robot.getNextFeedback();
        catch err
            disp(err.message)
        end
        % check if voltage is too low
        if mean(fbk.voltage)<30
            disp(['Low voltage: ' num2str(mean(fbk.voltage), 1), ' V']);
        end
    end
    
    
    
    % Look to see if there is a new mode to go to:
    checkForNewMode;
    
    % move to a new goal pose
    if ((goalNum~=lastGoalNum)&&running&&(strcmp(mode, 'goalPoses') ))
        lastGoalNum = goalNum;
        disp(['go to goal: ',num2str(goalNum)]);
        positionEnd = th(:,goalNum).';
        if sendCommands
            try
                fbk = robot.getNextFeedback();
            catch err
                disp(err.message)
            end
            lastPos =fbk.position;
        end
        moveArmToTheta;
        %         moveToThetaBumpStop; % not working well yet
    end
    
    % go to grav. comp
    if strcmp(mode,'gravComp')
        disp('gravity comp mode')
        gravityCompMode;
    end
    
    % hold the pose its at
    if strcmp(mode, 'holdPose')
        % this mode will hold lastPos until a different button pressed.
        holdPoseMode;
    end % endif strcmp(mode, 'holdPose')
    
    % push in a direction
    if strcmp(mode,'push')
        disp([mode ' ' pushString]);
        pushImpedanceMode;
    end
    
    % follow with IK
    if strcmp(mode,'follow')
        disp('Following mode');
        followHandMode;
    end
    
    if animate
        drawnow;
    end
end

if sendCommands
    setToNaN;
end

