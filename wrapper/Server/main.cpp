#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 
#include <pthread.h>
#include <arpa/inet.h>
#include<fcntl.h>
#include <vector>
#include <thread>
#include <zmq.hpp>
#include <signal.h>

using namespace std;

static int s_interrupted = 0;

// int PORT = 23;
// char* IP_ADDR = "192.168.4.1";
int PORT = 12000;
char* IP_ADDR = "127.0.0.1";

int SockID;
pthread_mutex_t socketLock, RCbufLock;
void* get_command_req (void*);
class Communication{
public:
    vector<uint8_t> RCBuffer;
    vector<uint8_t> command_buffer;


    Communication(){
        RCBuffer = vector<uint8_t>(22);
        command_buffer = vector<uint8_t>(8);
    }
    void calcCRC(vector<uint8_t>& buf){
        uint8_t crc = 0;
        for (int i = 3; i < buf.size() - 1; i++){
            crc ^= buf[i];
        }
        buf[buf.size() - 1] = crc;
    }
    void addRCBuffer(int num, int pos){
        int apos = (pos * 2) + 5;
        RCBuffer[apos] = (uint8_t)(num & UINT8_MAX);
        RCBuffer[apos + 1] = (uint8_t)((num >> 8) & UINT8_MAX);
    }
    bool connectSocket(){
        struct sockaddr_in sockaddr;
        SockID = socket(AF_INET, SOCK_STREAM, 0);
        if (SockID < 0){
            cout << "Connection Failure!" << endl;
            return false;
        }
        sockaddr.sin_family = AF_INET;
        sockaddr.sin_port = htons(PORT);
        sockaddr.sin_addr.s_addr = inet_addr(IP_ADDR);
        long arg;
        
        int res = connect(SockID, (struct sockaddr *) &sockaddr, sizeof(sockaddr));
        if (res < 0){
            cout << "Connection Faillure!" << endl;
            if (errno == EINPROGRESS) cout << "bb";
            return false;
        }
        int optval = 1;
        int optlen = sizeof(optval);

        if(setsockopt(SockID, SOL_SOCKET, SO_KEEPALIVE, &optval, optlen) < 0) {
            return false;
        }

        int error = 0 ;
        socklen_t len = sizeof(error);


        int retval = getsockopt(SockID, SOL_SOCKET, SO_ERROR, &error, &len);

        if(error != 0) {
            return false;
        }

        cout << "Pluto Connected" << endl;
        return true;
    }
    void initRCBuffer(){
        RCBuffer[0] = '$';
        RCBuffer[1] = 'M';
        RCBuffer[2] = '<';
        RCBuffer[3] = (uint8_t) 16;
        RCBuffer[4] = (uint8_t) 200;
        for (int i = 0; i < 4; i++){
            addRCBuffer(1500, i);
        }
        for (int i = 4; i < 8; i++){
            addRCBuffer(1000, i);
        }
        calcCRC(RCBuffer);
    }
    void readyBuffer(){
        for (int i = 4; i < 7; i++){
            addRCBuffer(1500, i);
        }
        //addRCBuffer(1600, 2);
        calcCRC(RCBuffer);
    }

    void init_command_buffer () {
        command_buffer[0] = '$';
        command_buffer[1] = 'M';
        command_buffer[2] = '<';
        command_buffer[3] = (uint8_t) 2;
        command_buffer[4] = (uint8_t) 217;
        command_buffer[5] = (uint8_t) 0;
        command_buffer[6] = (uint8_t) 0;


        calcCRC(command_buffer); 
    }

};

void* sendRCRequests(void* comm){
    Communication* com = (Communication*) comm;
    int i = 0;
    while(true){
        
        // if (i == 55){
        //     com->command_buffer[5] = (uint8_t)1;
        //     com->calcCRC(com->command_buffer);

        //     get_command_req(comm);
        // }
        // if (i == 300){
        //     com->command_buffer[5] = (uint8_t)2;
        //     com->addRCBuffer(1500, 2);
        //     com->calcCRC(com->command_buffer);
        //     com->calcCRC(com->RCBuffer);
        //     get_command_req(comm);
        // }
        pthread_mutex_lock(&RCbufLock);
        pthread_mutex_lock(&socketLock);
        usleep(50000);
        int x = send(SockID, &com->RCBuffer[0], com->RCBuffer.size(), 0);
        cout << x << endl;
        pthread_mutex_unlock(&socketLock);
        usleep(500);
        pthread_mutex_unlock(&RCbufLock);
        i++;
    }    
}

void* getRCRequests(void* comm){
    Communication* com = (Communication*) comm;

    //Sub init
    const string TOPIC = "front";
    zmq::context_t zmq_context(1);
    zmq::socket_t zmq_socket(zmq_context, ZMQ_SUB);
    zmq_socket.connect("tcp://127.0.0.1:6000");

    zmq::socket_t killer_socket(zmq_context, ZMQ_PAIR); 
    killer_socket.bind("ipc://killmebaby");

    zmq_socket.setsockopt(ZMQ_SUBSCRIBE, TOPIC.c_str(), TOPIC.length()); 
    zmq::pollitem_t items [] = {
        { zmq_socket, 0, ZMQ_POLLIN, 0 },
        { killer_socket, 0, ZMQ_POLLIN, 0 }
    };
    while (true){
        //Suscriber Begin
        int rc = 0;
        zmq::message_t topic;
        zmq::message_t msg;
        zmq::poll (&items [0], 2, -1);
        cout << "AA" << endl;
        if (items [0].revents & ZMQ_POLLIN)
        {
            cout << "waiting on recv..." << endl;
            rc = zmq_socket.recv(&topic, ZMQ_RCVMORE);  
            rc = zmq_socket.recv(&msg) && rc;
            if(rc > 0) 
            {
                cout << "topic:\"" << string(static_cast<char*>(topic.data()), topic.size()) << "\"" << endl;
                string dat = string(static_cast<char*>(msg.data()), msg.size());
                stringstream ss(dat);
                pthread_mutex_lock(&RCbufLock);
                int temp;
                for (int i = 0; i < 4; i++){                    
                    ss >> temp;
                    com->addRCBuffer(temp, i);
                }
                for (int i = 4; i < 8; i++){                    
                    ss >> temp;
                    if (temp) temp = 1500;
                    else temp = 1100;
                    com->addRCBuffer(temp, i);
                }
                com->calcCRC(com->RCBuffer);
                pthread_mutex_unlock(&RCbufLock);
            }
        }
        else if (items [1].revents & ZMQ_POLLIN)
        {
            if(s_interrupted == 1)
            {
                cout << "break" << endl;
                break;
            }
        }
        //Subscriber End
    }
}

void* get_command_req (void* comm) {
    Communication* com = (Communication*) comm;

    const string TOPIC = "cmd";
    zmq::context_t zmq_context(1);
    zmq::socket_t zmq_socket(zmq_context, ZMQ_SUB);
    zmq_socket.connect("tcp://127.0.0.1:6000");

    zmq::socket_t killer_socket(zmq_context, ZMQ_PAIR); 
    killer_socket.bind("ipc://killmebaby");

    zmq_socket.setsockopt(ZMQ_SUBSCRIBE, TOPIC.c_str(), TOPIC.length()); 
    zmq::pollitem_t items [] = {
        { zmq_socket, 0, ZMQ_POLLIN, 0 },
        { killer_socket, 0, ZMQ_POLLIN, 0 }
    };

    while(true) {
        int rc = 0;
        zmq::message_t topic;
        zmq::message_t msg;
        zmq::poll (&items [0], 2, -1);
        cout << "AA" << endl;
        if (items [0].revents & ZMQ_POLLIN)
        {
            cout << "waiting on recv..." << endl;
            rc = zmq_socket.recv(&topic, ZMQ_RCVMORE);  
            rc = zmq_socket.recv(&msg) && rc;
            if(rc > 0) 
            {
                cout << "topic:\"" << string(static_cast<char*>(topic.data()), topic.size()) << "\"" << endl;
                string dat = string(static_cast<char*>(msg.data()), msg.size());
                com->command_buffer[5] = (uint8_t)stoi(dat);
                com->calcCRC(com->command_buffer);
                cout<<"ll";                
                pthread_mutex_lock(&socketLock);
                usleep(50000);
                send(SockID, &com->command_buffer[0], com->command_buffer.size(), 0);
                pthread_mutex_unlock(&socketLock);
            }
        }
        else if (items [1].revents & ZMQ_POLLIN)
        {
            if(s_interrupted == 1)
            {
                cout << "break" << endl;
                break;
            }
        }  
    }
 }


int main(){
    Communication* comm = new Communication;
    if(comm->connectSocket() != true){
        cout << "Retrying" << endl;
        sleep(1);
        if (comm->connectSocket() != true){
            exit(1);
        }
    }
    comm->initRCBuffer();
    comm->init_command_buffer();
    comm->readyBuffer();

    if (pthread_mutex_init(&socketLock, NULL) != 0){
        cout << "Mutex failure!" << endl;
        exit(1);
    }
    if (pthread_mutex_init(&RCbufLock, NULL) != 0){
        cout << "Mutex failure!" << endl;
        exit(1);
    }

    pthread_t RC, Comm, RCR;

    sleep(1);

    int RC_ = pthread_create(&RC, NULL, sendRCRequests, (void*) comm);
    int Comm_ = pthread_create(&Comm, NULL, get_command_req, (void*) comm);
    int RCR_ = pthread_create(&RCR, NULL, getRCRequests, (void*) comm); 

    pthread_join(RC, NULL);
    pthread_join(Comm, NULL);
    pthread_join(RCR, NULL);
    sleep(5);
}