# 364 Assignment 2 - Chatting Program

Author: Siqi(Mike) Ma

ID: 2623324

UPI: sma148

## <1> Install / Testing Environment

* ### Please Run the program in the Windows OS Environment
* Make sure Python 3.7 or above is installed.


* Make sure Pyqt5 is installed.


## <2> How to Run

* Server End:

   1) Open A Command Prompt (cmd) and change directory to the top level directory (where the all .py files are located) of the unzipped folder.

  2) Type In following command to start the server:
  
          python Server.py --name=server --port=9900

        where you can replace the `9900` port number to other port numbers if you prefer. 

* Client Side GUI:

  1) Depending on how many clients GUI you would like to open, Open corresponding number of Command Prompt (cmd), and and change directory to the top level directory (where the all .py files are located) of the unzipped folder.

  2) Type in each Command Prompt to start each Client GUI:
  
          python Connection.py
  3) Fill in the same Port number as specified in the Server above, i.e. `9900`
  4) Choose a nickname for each client, **MAKE SURE NO TWO CLIENTS HAVE THE SAME NAME !**
  5) Click the button - `connect`
  6) Enjoy ! ^_^