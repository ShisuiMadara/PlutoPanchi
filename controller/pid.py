import time

def pid(curr_pos, req_pos, current_time=None):
        
        Kp = 5
        Ki = 0
        Kd = 0

        sample_time = 5  #5 milli second 
        current_time = current_time if current_time is not None else time.time()
        last_time = current_time
        
        error = req_pos - curr_pos

        current_time = current_time if current_time is not None else time.time()
        delta_time = current_time - last_time
        delta_error = error - last_error

        if (delta_time >= sample_time):

            P_Term = Kp * error
            I_Term += error * delta_time

            D_Term = 0.0
            if delta_time > 0:
                D_Term = delta_error / delta_time

            # Remember last time and last error for next calculation
            last_time = current_time
            last_error = error

            output = P_Term + (Ki * I_Term) + (Kd * D_Term)

            if output > 600:
                output = 600

            if output < -600:
                output = -600  

            ouput += 1500      

        return output    