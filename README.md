# N-node-distributed-system-that-implements-a-vector-clock-
**N-node distributed system that implements a vector  clock** 

**Project 2** 

N-node distributed system that implements a vector 
clock 

**Introduction** 
This project is implemented on Python language. We have used python’s socket library for 
communicating between different clients. In this project we explored how a vector clock is used 
to determine the order of events in a distributed system. 

**Implementation:**

We have 3 major functionalities implemented for each client 

**1. When a client is created**
   
- Client broadcasts its name along with a string “NEW_CONNECTION==” with it.
  
- Then it creates a vector with its name and set it to 0.
  
- When an existing client receives this message, it will create a new entry for the new 
client in its vector and set it to 0. After this the existing client will broadcast its name to 
the new client along with a string “EXISTING_CONNECTION==”.

- When the new client receives existing connection message, it will create a new entry for 
each existing client in its vector and set it to 0.

- After the client is created it generates 2 threads, one for sending messages and one for 
receiving messages.

**2. When client sends a message**
   
- Before sending a message, the client prints it existing vector.
  
- It increments its own vector by 1 and the sends the message along with new vector 
data.

- After sending message, the client prints the new vector.
  
**3. When client receives a message**
   
- Before receiving a message, the client prints it existing vector.
  
- Once the client receives a message and vector, it compares the received vector with its 
own vector and updates its own vector with the latest data.

- After receiving message, the client prints the new vector. 

**What we learned:** 

- How to use sockets to communicate between clients.
  
- How to create a thread in python.
  
- How vector clock works. 


**What issues we faced**: 

- While running multiple clients on mac machine, the program was throwing an exception 
that the port is already in use. We resolved the issue by setting the socket option to 
‘SO_REUSEPORT’ instead of ‘SO_RESUEADDR’.
 
- Since the clients were running independently of each other there was no easy way to 
store the name of each client in a central place. This was an issue because a new client 
will not have the knowledge of the existing clients. To resolve this, we implemented a 
logic where when a new client is created it will broadcast its name to every other 
existing client and in response each existing client will broadcast their name to the new 
client. This way all the clients can easily sync their names with each other.

**Screenshots:** 

![image](https://github.com/NehaMore2202/N-node-distributed-system-that-implements-a-vector-clock-/assets/154467395/5b49116f-c31a-4a21-9853-54467ad94371)

**Readme to run N-node distributed system that implements a vector  clock**

Required python version >= 3.10.

This project uses pythons `sockets` library to send and receive messages between clients.

**NOTE:**

If there is a error saying "Port is already in use" while running the code:

Please comment line number 19 and uncomment line 21.


**Steps to run the program:**

- Open a terminal on the project directory
  
- Run command `python3 vector_clock.py` # or python vector_clock.py
  
- You will see a prompt to enter client name
  
- After which you can send message from this to other client

To run a new client open a new terminal on the project directory and follow the above steps

**References:**

1. https://www.tutorialspoint.com/python/index.htm
   
2. https://www.w3schools.com/python/
   
3. https://docs.python.org/3/howto/sockets.html
   
4. https://wiki.python.org/moin/UdpCommunication
 

 

 

 

 

 
