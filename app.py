import random
import math
import numpy as np

# Set the value of lambda as an input (rate parameter)

def generate_random_numbers(lam):
    # Generate a random number between 0 and 1
    r = random.random()
    # Calculate the inter-arrival time
    x = -math.log(1 - r) / lam
    res = round(x)
    # res = np.random.poisson(lam)
    return res




# Import necessary modules
import random
from dataclasses import dataclass

# Create a data class for rows that will hold simulation data
@dataclass
class Row:
    iat: int = 0  # inter-arrival time
    st: int = 0  # service time
    arrival: int = 0  # time of arrival
    sstart: int = 0  # service start time
    send: int = 0  # service end time
    waiting: int = 0  # time spent waiting in queue
    qlen: int = 0  # length of queue at time of arrival
    idle: int = 0  # time server is idle

# Set initial values for variables and constants
sim_table = []  # list to hold simulation data
NUM_OF_CUSTOMERS = 500  # number of simulated customers
NUM_OF_RUNS = 10 # number of times to run simulation
num_of_cust_waiting=0
service_time=0
time_between_arrivals=0
waiting_time_in_quene=0

grand_avg_waiting = 0  # average waiting time across all runs
grand_max_qlen = 0  # maximum queue length across all runs

LAMDAIAT = 0.2
LAMDAST = 0.33

# Run simulation NUM_OF_RUNS times
for i in range(NUM_OF_RUNS):

    avg_waiting = 0  # initialize average waiting time for this run
    max_qlen = 0  # initialize maximum queue length for this run
    server_idle = 0  # initialize amount of time server is idle for this run
    c1 = Row()  # create first customer object
    c1.iat = generate_random_numbers(LAMDAIAT)  # generate random inter-arrival time
    c1.st = generate_random_numbers(LAMDAST)  # generate random service time
    c1.arrival = c1.iat  # set arrival time equal to inter-arrival time
    c1.sstart = c1.arrival  # set service start time equal to arrival time
    c1.send = c1.sstart+c1.st  # calculate service end time
    c1.waiting = c1.qlen = 0  # first customer does not wait in queue
    c1.idle = c1.iat  # server is idle until first customer arrives
    server_idle += c1.idle  # add idle time for this customer to total
    sim_table.append(c1)  # add customer object to simulation table at index 0

    # Create remaining customer objects and calculate their simulation data
    for i in range(1,NUM_OF_CUSTOMERS):
        c = Row()  # create new customer object
        c.iat = generate_random_numbers(LAMDAIAT)  # generate random inter-arrival time
        c.st = generate_random_numbers(LAMDAST)  # generate random service time
        c.arrival = c.iat + sim_table[i-1].arrival  # calculate arrival time based on previous customer's arrival time
        if c.arrival >= sim_table[i-1].send:
            # if the customer arrives after the previous customer's service has finished,
            # they can begin service immediately with no waiting
            c.sstart = c.arrival
            c.qlen = 0
            c.idle = c.sstart - sim_table[i-1].send
        else:
            # if the customer arrives before the previous customer's service has finished,
            # they must wait in the queue before beginning service themselves
            c.sstart = sim_table[i-1].send
            c.idle = 0
            q = i
            while q > 0 and c.arrival < sim_table[q-1].send:
                # calculate the length of the queue at the time of this customer's arrival
                c.qlen+=1
                q-=1
        
        c.send = c.sstart + c.st  # calculate service end time
        c.waiting = c.sstart - c.arrival  # calculate time spent waiting in queue
        if(c.waiting>0):
            num_of_cust_waiting +=1
            waiting_time_in_quene+=c.waiting
        
        avg_waiting += c.waiting  # add waiting time for this customer to total
        max_qlen = max(c.qlen,max_qlen)  # update max queue length if necessary
        server_idle += c.idle  # add idle time for this customer to total
        sim_run_time=c.send
        service_time+=c.st
        time_between_arrivals +=c.iat

        sim_table.append(c)  # add customer object to simulation table

    avg_waiting /= NUM_OF_CUSTOMERS  # calculate average waiting time for this run
   # server_idle /= sim_table[NUM_OF_CUSTOMERS-1].send  # calculate server idle time for this run

    grand_avg_waiting += avg_waiting  # add average waiting time for this run to total for all runs
    grand_max_qlen = max(max_qlen,grand_max_qlen)  # update max queue length across all runs if necessary

    # calculate overall average waiting time across all runs

    # Print out simulation data table
    prob_that_cust_has_wait=num_of_cust_waiting/NUM_OF_CUSTOMERS #probability that customer has to wait 
    prob_of_server_idleness=server_idle/sim_run_time #proportion of server idleness
    avg_service_time = service_time/NUM_OF_CUSTOMERS #average srevice time
    avg_time_bet_arrivals= time_between_arrivals / (NUM_OF_CUSTOMERS-1) #average time between arrivals
    avg_waiting_time_who_wait= waiting_time_in_quene/num_of_cust_waiting #average waiting time of those who wait
    avg_cust_spend_in_system = avg_waiting +avg_service_time #average time a customer spends in system

    print("cust\t\tiat\t\tst\t\tarrival\t\tsstart\t\tsend\t\twaiting\t\tqlen\t\tidle")
    for i in range(NUM_OF_CUSTOMERS):
        print("C"+str(i+1),'\t\t',sim_table[i].iat,'\t\t',sim_table[i].st,'\t\t',sim_table[i].arrival,'\t\t',sim_table[i].sstart,'\t\t',sim_table[i].send,'\t\t',sim_table[i].waiting,'\t\t',sim_table[i].qlen,'\t\t',sim_table[i].idle)
    print('avg_waiting:= ',avg_waiting)
    print('max_qlen:= ',max_qlen)   
    print('server_idle:= ',server_idle)
    print('probability that customer has to wait:= ',prob_that_cust_has_wait) 
    print('proportion of server idleness:= ',prob_of_server_idleness)
    print('average srevice time:= ',avg_service_time)
    print('average time between arrivals:= ',avg_time_bet_arrivals)
    print('average waiting time of those who wait:= ',avg_waiting_time_who_wait)
    print('average time a customer spends in system:= ',avg_cust_spend_in_system)
    print('\n\n')
    sim_table.clear()  # clear simulation table for next run
    

grand_avg_waiting /= NUM_OF_RUNS    # calculate overall average waiting time across all runs

print('grand_avg_waiting:= ',grand_avg_waiting) # print overall average waiting time across all runs
print('grand_max_qlen:= ',grand_max_qlen) # print max queue length across all runs

