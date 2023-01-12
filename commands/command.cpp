#include <command.h>
#include <unistd.h>
#include <string>

using namespace std;

vector<uint8_t>command_buffer[7];

void command::sendRequestMSP_SET_COMMAND(int commandType)
{
  vector<int8_t> payload(1);
  payload[0] = (int8_t) (commandType & 0xFF);

  sendRequestMSP(createPacketMSP(MSP_SET_COMMAND, payload));
}


