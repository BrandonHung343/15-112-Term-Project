#############################################
ROBOTIC ARM SETUP
#############################################
Note: 
This program runs in Python 2.7.14. It will not compile with Python 3.6

Project:
This project is an attempt to provide a headless UI through voice control and hand tracking to a robotic arm. It
explores making robots more ergonomic for the everyday user and is easily modifiable to allow users to input their 
own functionality.

Installation:
You'll need to have the following external libraries installed
	- OpenCV (cv2)
	- SpeechRecognition
	- PyAudio
	- HEBI Module Optimization
	- MATLAB_SEA

	1. OpenCV:
		a) Navigate to https://opencv.org/releases.html and download opencv 3.3.1. 
		For Windows, run the installer and extract the files in opencv/build/python/2.7 to 
		C://Python27//Lib//site-packages. 
		b) For Mac and Linux, to build from source refer to
		https://docs.opencv.org/2.4/doc/tutorials/introduction/linux_install/linux_install.html and
		https://blogs.wcode.org/2014/10/howto-install-build-and-use-opencv-macosx-10-10/
		c) Althernatively, you can open command prompt and type 
		'pip install opencv_python-3.3.1.0-cp27-cp27m-win32.whl' which should auto-install 
		for you.  

	2. SpeechRecognition:
		a) Open command prompt and 
		type in '(include sudo for Linux) pip install SpeechRecognition'

	3. PyAudio
		a) Open command prompt and 
		type in '(include sudo for Linux) pip install PyAudio'

	4. HEBI
		a) Navigate to http://docs.hebi.us/ and download the HEBI MATLAB API
		b) Extract the API into the directory from where you plan on running the arm control code
		c) Make sure to properly change the 'addpath' statements at the beginning of the mainStartup.m 
		script to include the exact file path you extracted the files to
	
	5. MATLAB
		a) Navigate to https://github.com/biorobotics/matlab_SEA
		b) If you have installed git, open git shell or terminal and run 
		'git clone https://github.com/biorobotics/matlab_SEA.git'
		c) Otherwise, download as zip and extract into your robotic arm MATLAB directory

Operation:

	1) Start the Python file term_project.py
	2) Start the MATLAB script mainStartup.m
	3) The two files should automatically connect, and windows showing video camera 
	feed will appear. 
	4) Line up a tag 1 foot from the camera, in the middle of the camera window. Say 'calibrate' clearly.
	The filtered image will appear on the 'draw' pane. If the filter is incorrect, then you can calibrate
	it again using this step. ALternatively, you can right click on the object in the 'Window' pane to set
	it as the tag.
	5) You can now begin switching modes using voice control. The keywords are 1, 2, 3, (poses), track (follow tag),
	stay (hold in place), free (gravity compensation/moveable mode), and calibrate (sets tag). NOTICE: Before 
	running 'track', ensure that your tag is set or the program may not run correctly
	6) To exit, open the 'Window' pane and click the ESC key

Happy Cyborging!

PHOTO CREDITS:

Credits to the images used in the video go to:
https://en.wikipedia.org/wiki/Mobile_Servicing_System
http://www.gmanetwork.com/news/scitech/technology/364318/mit-builds-real-life-doc-ock-bionic-arms/story/

Credits for most of the robotic arm construction and mainStartup.m script go to Julian Whitman