% this script checks for new modes, and updates the mode number

% check for voice input
% newestWord = checkForNewWord;

% Brandon Hung
axes = zeros(1,4);
buttons = zeros(1,12);
povs = -1;

if useVoiceInput % if we have voice input, use instead of joystick
newestWord = checkForNewWord(conn);
disp(newestWord);
    switch newestWord
        case 'stay'
            buttons(11) = 1;
        case 'free'
            buttons(12) = 1;
        case '1'
            buttons(1) = 1;
        case '2'
            buttons(2) = 1;
        case '3'
            buttons(3) = 1;
        case '4'
            buttons(4) = 1;
        case 'track'
            buttons(7) = 1;
            buttons(8) = 1;
        case 'quit'
            buttons(10) = 1;
        otherwise
            disp('None')
    end
%     read the joystick
else
[axes,buttons,povs] = read(joy);
end

% Brandon Hung

% check if still running
running = ~any(buttons(9:10));
if ~running
    remainInMode = 0;
end

% check if switching to goal poses
if any(buttons(1:numGoals))
    socketPoint = 0;
    newGoalNum = find(buttons(1:numGoals));
    if newGoalNum ~= lastGoalNum
        goalNum = newGoalNum(1); % only take the lowest number pressed
        mode = 'goalPoses';
        remainInMode = 0;
    end
end
running = ~any(buttons(9:10));


% check if switching to grav comp
if buttons(12) % if button 12 is pressed, go into grav comp
    socketPoint = 0;
    mode = 'gravComp';
    disp('grav Comp mode')
    remainInMode = 0;
    goalNum = 0;
    lastGoalNum =0;
end

% check if switching to hold pose
if buttons(11)
    socketPoint = 0;
    remainInMode = 0;
    mode = 'holdPose';
    disp('Hold pose mode');
    goalNum = 0;
    lastGoalNum =0;
    lastPos = fbk.position;
end

% check if switching to push mode
% d-pad will make it push in a direction
if (povs~=-1)
    socketPoint = 0;
    mode = 'push';
    pos = lastPos;
    switch povs
        case 0
            directionToPush = [0;0;1]; % this will be relative to base frame, not gravity
            pushString = 'up';
        case 180
            directionToPush = [0;0;-1];
            pushString = 'down';
        case 90
            directionToPush = [1;0;0];
            pushString = 'forward';
    end
    goalNum = 0;
    lastGoalNum =0;
    remainInMode = 0;
    
end

% check to see if entering IK mode
if buttons(7)&&buttons(8)
    socketPoint = 1;
    mode = 'follow';
    remainInMode = 0;
    goalNum = 0;
    lastGoalNum =0;
end
disp(socketPoint)
if (abs(axes(3))>.05)&&(withGripper)
    cmdGripper.position = cmdGripper.position + .05*axes(3);
    cmdGripper.position = max(cmdGripper.position, gripperMin);
    cmdGripper.position = min(cmdGripper.position, gripperMax);
    gripper.set(cmdGripper);
    
end
