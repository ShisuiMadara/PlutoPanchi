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

int PORT = 6000;
char* IP_ADDR = "127.0.0.1";
int SockID;

class Communication{
public:
    vector<uint8_t> RCBuffer;
    Communication(){
        RCBuffer = vector<uint8_t>(22);
    }
    void calcCRC(vector<uint8_t>& buf){
        uint8_t crc = 0;
        for (int i = 4; i < buf.size() - 1; i++){
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
        
        // if ((arg = fcntl(SockID, F_GETFL, NULL)) < 0){
        //     cout << "Connection Failure!" << endl;
        //     return false;
        // }
        // arg |= O_NONBLOCK;
        // if (fcntl(SockID, F_SETFL, arg) < 0){
        //     cout << "Connection Failure!" << endl;
        //     return false;
        // }

        int res = connect(SockID, (struct sockaddr *) &sockaddr, sizeof(sockaddr));
        if (res < 0){
            cout << "Connection Faillure!" << endl;
            if (errno == EINPROGRESS) cout << "bb";
            return false;
        }
        if ((arg = fcntl(SockID, F_GETFL, NULL)) < 0){
            cout << "Connection Failure!" << endl;
            return false;
        }
        arg &= (~O_NONBLOCK);
        if (fcntl(SockID, F_SETFL, arg) < 0){
            cout << "Connection Failure!" << endl;
            return false;
        }

        int optval;
        socklen_t optlen;
        // if(getsockopt(SockID, SOL_SOCKET, SO_KEEPALIVE, &optval, &optlen) < 0){
        //     cout << "Connection Failure!" << endl;
        //     close(SockID);
        //     return false;
        // }
        // optval = 1;
        // optlen = sizeof(optval);
        // if (setsockopt(SockID, SOL_SOCKET, SO_KEEPALIVE, &optval, optlen) < 0){
        //     cout << "Connection Failure!" << endl;
        //     close(SockID);
        //     return false;
        // }
        // if(getsockopt(SockID, SOL_SOCKET, SO_KEEPALIVE, &optval, &optlen) < 0){
        //     cout << "Connection Failure!" << endl;
        //     close(SockID);
        //     return false;
        // }
        // int error = 0;
        // socklen_t len = sizeof(error);
        // int retval = getsockopt(SockID, SOL_SOCKET, SO_ERROR, &error, &len);

        // if (retval != 0){
        //     cout << "Connection Failure!" << endl;
        //     close(SockID);
        //     return false;
        // }
        // if (error != 0){
        //     cout << "Connection Failure!" << endl;
        //     close(SockID);
        //     return false;
        // }
        // else {
        //     cout << "Pluto Connected" << endl;
        // }
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
        calcCRC(RCBuffer);
    }
};

void* sendRCRequests(void* comm){
    Communication* com = (Communication*) comm;
    write(SockID, &com->RCBuffer[0], com->RCBuffer.size());
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
    pthread_t RC, Comm;
    int RC_ = pthread_create(&RC, NULL, sendRCRequests, (void*) comm);
    pthread_join(RC, NULL);
    sleep(5);
}