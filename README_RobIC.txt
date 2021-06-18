RobIC installation guide:

programmation language : pyhton 3.7
Database : MongoDB version 4.4.6

Step:
1 - Create robic_dev repository
 > mkdir robic_dev

2 - Create the virtual environment
 robic_dev > cd robic_dev
 robic_dev > pip3 install virtualenv
 robic_dev > python3 -m venv venv

NB: The venv repository must be created

3 - Active the virtual environnement
 robic_dev > source venv/Scripts/activate
 (venv) robic_dev >

NB: in command prompt, you must see something like this: (venv) robic_dev>

4 - Install all package via command :
 (venv) robic_dev > pip3 install -r requirement.txt

NB: the file "requirement.txt" must be in the robic_dev repository

5 - To make RobIC accessible via web
 (venv) robic_dev >./run_server.sh
6 - To make RobIC accessible via chatbots
 (venv) robic_dev >py socketServer.py

7 - Copy all files sent to you
************** Structure of RobIC repository **********
Look at pictures from whatsapp

robic_dev
	|
	|
	Complaints_call
	|
	|
	Complaints_internet
	|
	|
	Complaints_sms
	|
	|
	static
	|
	|
	templates
	|
	|
	venv
	|
	|
	(some files)
	
