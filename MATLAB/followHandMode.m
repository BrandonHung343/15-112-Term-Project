% follow with IK, use leap controller


% tts('Follow Mode','Microsoft Zira Desktop - English (United States)');
pos = lastPos;
fk = kin.getFK('EndEffector', pos);
xyz = fk(1:3,4);
thLast = pos;
xyzMax = sum(lengths) + rb;
xyzMin = rb - sum(lengths);
xyzMin(1) = .25;
firstTime = 1;

utilPath = 'C:\Users\Brandon\Documents\GitHub\backpackArmControl\utils';
%if count(py.sys.path,utilPath) == 0
%   insert(py.sys.path,int32(0),utilPath);
% end
% controller = py.leapPythonTest.getController;

R = [ [0; 1; 0], [1; 0; 0], [0;0;-1] ];% [xnew ynew znew]
p = [0; -.07; .25];


remainInMode = 1;
while remainInMode
    if sendCommands
        try
            fbk = robot.getNextFeedback();
        catch err
            disp(err.message)
        end
    end
    
    
    % Brandon Hung
    disp(socketPoint);
    %         axes(abs(axes)<.1) = 0;
    %     xyz = xyz + [-axes(2); axes(1); -axes(4)] * .01/2;
    %     xyz = max(xyz, xyzMin);
    %     xyz = min(xyz, xyzMax);
    
    % frame = py.leapPythonTest.getFrame(controller);
    
        %         frame.hands.rightmost.palm_position
%         point = [10;...
%             10;...
%             10;]/1000; % measures in mm
     if socketPoint == 1
%         disp(pointTransformed(1:3).')
%         xyz = pointTransformed(1:3);
%          disp(newPoint)
            newPoints = checkForNewWord(conn);
         if strlength(newPoints) > 10
             xyz = cell2mat(transpose(textscan(strrep(newPoints, '_', ' '), '%f %f %f')));
             disp(xyz)
             pointTransformed = [R p; 0 0 0 1]*[xyz; 1];
             disp(pointTransformed(1:3).')
             xyz = max(xyz, xyzMin);
             xyz = min(xyz, xyzMax);
        % x = z, y = x, z = y
       % xyz = [0.5;-0.3;0.4];
        if sendCommands
            pos = kin.getInverseKinematics('Xyz', xyz, 'InitialPositions', fbk.position);
        else
            pos = kin.getInverseKinematics('Xyz', xyz, 'InitialPositions', lastPos);
        end
        end
     end
    % Brandon Hung
    
    if any( abs(pos-lastPos) > ones(size(pos))*.5)
        firstTime = 1; % if too far, treat as if first time
    end
    
    
    if firstTime
        firstTime = 0;
        positionEnd = pos;
        moveArmToTheta;
    elseif sendCommands
        
        %% gravity comp torques
        % Compensate gravity at current position
        %         fbk = robot.getNextFeedback();
        % automatically determine direction of gravity
        gravityVec = [fbk.accelX(1) fbk.accelY(1) fbk.accelZ(1)].';
        % dealing with non identity base frames
        baseFrame = kin.getBaseFrame();
        gravityVec = baseFrame(1:3,1:3)' * gravityVec;
        efforts = kin.getGravCompEfforts(fbk.position, gravityVec);
        
        cmd.position = pos;
        cmd.velocity = NaN(1,n);
        cmd.effort = efforts;
        try
            robot.set(cmd);
        catch err
            disp(err.message);
        end
    end
    
    if buttons(numGoals+1)
        numGoals = numGoals+1;
        th = [th, pos.'];
        disp(['added goal: ',num2str(numGoals)]);
        goalNum = numGoals;
        lastGoalNum = goalNum;
        
    end
    
    
    if animate
        plt.plot(pos)
    else
        pause(.01);
    end
    lastPos = pos;
    
end
lastPos = pos;
