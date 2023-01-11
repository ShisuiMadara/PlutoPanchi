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

using namespace std;

int PORT = 23;
char* IP_ADDR = "192.168.4.1";
int SockID;

class Communication{
    bool ConnectSocket(){
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
        
        if ((arg = fcntl(SockID, F_GETFL, NULL)) < 0){
            cout << "Connection Failure!" << endl;
            return false;
        }
        arg |= O_NONBLOCK;
        if (fcntl(SockID, F_SETFL, arg) < 0){
            cout << "Connection Failure!" << endl;
            return false;
        }

        int res = connect(SockID, (struct sockaddr *) &sockaddr, sizeof(sockaddr));
        if (res < 0){
            cout << "Connection Failure!" << endl;
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
        if(getsockopt(SockID, SOL_SOCKET, SO_KEEPALIVE, &optval, &optlen) < 0){
            cout << "Connection Failure!" << endl;
            close(SockID);
            return false;
        }
        
    }
};