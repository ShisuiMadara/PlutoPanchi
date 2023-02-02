# PlutoPanchi
This program is responsible for establishing a fast and stable channel of communication between the python wrapper and Pluto. It is very easy to set-up and customise as per need but is powerful enough out-of-box that it can handle drone controls easily. It implements the MSP protocol over a TCP connection and sends the commands as specified by the wrapper and also sends packets periodically to maintain a persistent connection between Pluto and the python wrapper. It should also be noted that it is an essential component of the wrapper package and is required for the wrapper to work.
<br>
The complete documentation can be found <a href = "https://docs.google.com/document/d/1g0mEcBW1Y69Aj0LcN4L1GlqutJQJiYZ8/edit?usp=sharing&ouid=107777261984550371902&rtpof=true&sd=true"> HERE </a>.

<br>
<h1>Installation and building</h1>
The program is available as a downloadable standalone executable for Linux systems; however, we recommend you build/compile it from the source code which is easy to do. There are some pre-requisites that you should note:
<ul>
<li>Operating System: Linux/Unix or POSIX-Compliant</li>
<li>Compiler: G++ 9.4.0 or above</li>
<li>Libraries: ZeroMQ</li>
<b>Note: </b>
<p>The compilation process may work for G++ versions < 9.4.0 but there is no guarantee.
ZeroMQ is not required for running the program and is only required for building.</p>
<br>
For Debian users, if you do not have ZeroMQ you can install it using the following command:

	$ sudo apt-get install libzmq3-dev
  
Non-Debian users can refer to: https://zeromq.org/download/
<br>
To obtain the source code you should clone the git repository and we are assuming at this point you have already cloned the repo. You will find the code in the [repository]/wrapper/Server folder. Inside the folder, there must be a main.cpp file which contains the source code. To proceed with the build open a terminal and change the directory to the above-mentioned.
<br>
To build the program you simply need to run the following command:

	$ g++ -o Server.out -lzmq -lpthread main.cpp
  
After the execution of the command, if successful, you must see a file named Server.out and it is the compiled program. In case of an error please make sure you followed the instructions correctly. In case the error persists please take a look at the troubleshooting section.

<br>
<h1>How To Use</h1>
To use this program, you should follow simple steps:
<ol>
  <li>Make sure you are connected to the Pluto’s Wi-Fi Hotspot</li>
  <li>Run the executable and wait for the program to print “Connected”</li>
  <li>Command to run the executable:  
  
  ```$ ./Server.out```
  
  </li>
</ol>
These are the only steps to run this program. Once the “Connected” message is printed, the backend program is actively communicating with Drone and is ready to receive commands from the wrapper.
If you encounter errors like connection failed or ZMQ error please take a look at the Troubleshooting section.

Further sections will cover details about the working of the program and are of great importance if you want to modify the program or to understand how it works. If you are not interested in the internal working, I would suggest you to skip to Troubleshooting at the end.

<h1>Controlling</h1>

| Parameter | Type     | 
| :-------- | :------- | 
| `W` | `Go forward` | 
| `S` | `Go backward` | 
| `A` | `Go towards left` | 
| `D` | `Go towards right` | 
| `1` | `Take Off` | 
| `2` | `Land` | 
| `3` | `Back Flip` | 
| `4` | `Front Flip` | 
| `5` | `Right Flip` | 
| `6` | `Left Flip` | 
| `Arrow Key UP` | `Increase Height` | 
| `Arrow Key DOWN` | `Decrease Height` | 
| `Q` | `Quit` | 

<h1>Dependencies</h1>
<ul>
  <li>C/C++ compiler</li>
  <li>Python3 </li>
  <li>pthread library</li>
  <li>zmq</li>
  <li>curses</li>
</ul>

<h1>Troubleshooting</h1>
Possible Errors:
<ul>
<li>Drone Connection Error: The most probable cause for this error is that you are not connected to the Pluto’s Wi-Fi. Generally connecting/re-connecting to Wi-Fi fixes this issue.
<li>ZMQ Port Already Used: This error happens when you restart the application few times. The fix is to kill the process running on that port. You can run the command:

```$  fuser -k 6000/tcp```

</li>
<li>-1 on Console: It usually means drone has closed the Socket on its end. You need to rerun the program.</li>
</ul>

