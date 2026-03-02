import heapq, random, math 
from collections import deque

# --- Parameters (These will be getting edited) ---
LAM = 3      # arrivals per minute (λ)
MU = 1       # service per minute per lane (μ)
C = 4        # number of lanes (c)
T_END = 60   # minutes to simulate

# --- Passenger Entity  ---
class Passenger:
    def __init__(self, arrival_time):
        self.arrival_time = arrival_time

def exp_time(rate):
    return -math.log(random.random()) / rate

def main():
    t = 0.0
    fel = []              # future event list (min-heap by time)
    q = deque()           # FIFO queue (stores arrival times)
    busy = 0              # busy lanes
    served = 0
    total_wait = 0.0

    # schedule first arrival
    heapq.heappush(fel, (exp_time(LAM), "A"))

    while fel and t < T_END:
        t, typ = heapq.heappop(fel)

        if typ == "A":  # Arrival
            q.append(t)
            heapq.heappush(fel, (t + exp_time(LAM), "A"))  # next arrival

            if busy < C:                 # start service immediately
                busy += 1
                a = q.popleft()
                total_wait += (t - a)
                heapq.heappush(fel, (t + exp_time(MU), "D"))

        else:       # Departure
            served += 1
            if q:                        # take next from queue
                a = q.popleft()
                total_wait += (t - a)
                heapq.heappush(fel, (t + exp_time(MU), "D"))
            else:
                busy -= 1

    print("served =", served)
    if served:
        print("avg_wait =", total_wait / served)

if __name__ == "__main__":
    main()
