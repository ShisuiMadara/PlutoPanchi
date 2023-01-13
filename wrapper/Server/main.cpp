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

using namespace std;

int PORT = 23;
char* IP_ADDR = "192.168.4.1";
//int PORT = 6000;
//char* IP_ADDR = "127.0.0.1";

int SockID;
pthread_mutex_t socketLock, RCbufLock;

class Communication{
public:
    vector<uint8_t> RCBuffer;
    vector<uint8_t> command_buffer;


    Communication(){
        RCBuffer = vector<uint8_t>(22);
        command_buffer = vector<uint8_t>(7);
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
        for (int i = 4; i < 8; i++){
            addRCBuffer(1500, i);
        }
        calcCRC(RCBuffer);
    }

    void init_command_buffer () {
        command_buffer[0] = '$';
        command_buffer[1] = 'M';
        command_buffer[2] = '<';
        command_buffer[3] = (uint8_t) 1;
        command_buffer[4] = (uint8_t) 217;
        command_buffer[5] = (uint8_t) 0;

        calcCRC(command_buffer); 
    }

};

void* sendRCRequests(void* comm){
    Communication* com = (Communication*) comm;
    while(true){
        pthread_mutex_lock(&RCbufLock);
        pthread_mutex_lock(&socketLock);
        //com->connectSocket();
        usleep(500);
        int x = send(SockID, &com->RCBuffer[0], com->RCBuffer.size(), 0);
        cout << x << endl;
        //close(SockID);
        pthread_mutex_unlock(&socketLock);
        pthread_mutex_unlock(&RCbufLock);
    }    
}

void* getRCRequests(void* comm){
    Communication* com = (Communication*) comm;
    while (true){
        //Suscriber Begin
        
        //Subscriber End
        pthread_mutex_lock(&RCbufLock);
        //Edit to add RCBuffer Modification
        
        pthread_mutex_unlock(&RCbufLock);
    }
}

void* get_command_req (void* comm) {

    Communication* com = (Communication*) comm;

    while(true) {

        //call subscriber

        pthread_mutex_lock(&socketLock);
        write(SockID, &com->command_buffer[0], com->command_buffer.size());
        pthread_mutex_unlock(&socketLock);
          
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

    pthread_t RC, Comm;

    sleep(1);

    int RC_ = pthread_create(&RC, NULL, sendRCRequests, (void*) comm);
    //int Comm_ = pthread_create(&Comm, NULL, get_command_req, (void*) comm); 

    pthread_join(RC, NULL);
    pthread_join(Comm, NULL);
    sleep(5);
}