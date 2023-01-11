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

int PORT = 6000;
char* IP_ADDR = "127.0.0.1";
int SockID;

class Communication{
public:
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
};

int main(){
    Communication comm;
    if(comm.ConnectSocket() == true){
        char buffer[8];
        for (int i = 0; i < 8; i++){
            buffer[i] = 'a';
        }
        int n = write(SockID, buffer, strlen(buffer));
        if (n < 0) cout << "error";
    }
    sleep(5);
}