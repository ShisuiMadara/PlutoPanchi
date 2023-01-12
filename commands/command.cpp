#include <command.h>
#include <unistd.h>
#include <string>

using namespace std;

vector<uint8_t> command_buffer;


void init_command_buffer () {
	command_buffer[0] = '$';
    command_buffer[1] = 'M';
    command_buffer[2] = '<';
    command_buffer[3] = (uint8_t) 1;
    command_buffer[4] = (uint8_t) 217;
    command_buffer[5] = (uint8_t) 0;

    calcCRC(command_buffer) 
}

void* get_command_req (void* com) {

	Communication* comm = (Communication*) com;

	while(true) {

		//call subscriber

		pthread_mutex_lock(&socketLock);
	    write(SockID, &com->command_buffer[0], com->command_buffer.size());
	    pthread_mutex_unlock(&socketLock);
	      
	}
 }





