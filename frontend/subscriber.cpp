#include <thread>
#include <zmq.hpp>
#include <iostream>
#include <signal.h>
#include <unistd.h>

using namespace std;

static int s_interrupted = 0;

const string TOPIC = "";


void startSubscriber()
{
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
    while(true)
    {
        int rc = 0;
        zmq::message_t topic;
        zmq::message_t msg;
        zmq::poll (&items [0], 2, -1);
        if (items [0].revents & ZMQ_POLLIN)
        {
            cout << "waiting on recv..." << endl;
            rc = zmq_socket.recv(&topic, ZMQ_RCVMORE);  
            rc = zmq_socket.recv(&msg) && rc;
            if(rc > 0) 
            {
                cout << "topic:\"" << string(static_cast<char*>(topic.data()), topic.size()) << "\"" << endl;
                cout << "msg:\"" << string(static_cast<char*>(msg.data()), msg.size()) << "\"" << endl;
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

int main() {
    thread t_sub(startSubscriber);
    sleep(1);
   
    t_sub.join();
}