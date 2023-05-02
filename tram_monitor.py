import threading
import time
import random
class Tram:
    def __init__(self, capacity, stops):
        self.capacity = capacity
        self.stops = stops
        self.current_stop = 0
        self.passengers = []
        self.lock = threading.Lock()
        self.full = threading.Condition(self.lock)
        self.empty = threading.Condition(self.lock)
    def get_on(self, passenger):
        with self.lock:
            while len(self.passengers) == self.capacity:
                self.full.wait()
            self.passengers.append(passenger)
            self.empty.notify()
    def get_off(self, passenger):
        with self.lock:
            self.passengers.remove(passenger)
            self.empty.notify()
    def run(self):
        while True:
            print(f'Tram is arriving at stop {self.current_stop}')
            with self.lock:
                for passenger in self.passengers:
                    passenger.notify(self.current_stop)
                self.current_stop = (self.current_stop + 1) % self.stops
                time.sleep(1)
class Passenger:
    def __init__(self, tram):
        self.tram = tram
    def notify(self, stop):
        if stop == self.tram.current_stop:
            self.tram.get_off(self)
    def ride(self):
        with self.lock:
            self.tram.get_on(self)
            print(f'Passenger got on at stop {self.tram.current_stop}')
            self.empty.wait()
if __name__ == '__main__':
    capacity = 10
    stops = 5
    tram = Tram(capacity, stops)
    passengers = [Passenger(tram) for _ in range(capacity * 2)]
    tram_thread = threading.Thread(target=tram.run)
    tram_thread.start()
    passenger_threads = []
    for passenger in passengers:
        t = threading.Thread(target=passenger.ride)
        passenger_threads.append(t)
        t.start()
    tram_thread.join()
    for t in passenger_threads:
        t.join() 