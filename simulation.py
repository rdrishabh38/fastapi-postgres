#!/usr/bin/env python3
import requests
import time
import threading
import random
import string
import sys

# Configuration: number of requests per minute
USERS_PER_MINUTE = 20
DRIVERS_PER_MINUTE = 20
CARS_PER_MINUTE = 20
RIDES_PER_MINUTE = 15

# Upper limits
MAX_USERS = 200
MAX_DRIVERS = 200
MAX_CARS = 500
MAX_RIDES = 500

# Simulated ride duration in seconds
RIDE_DURATION_SECONDS = 30

# Endpoints (adjust these URLs if needed)
USER_REGISTRATION_URL = "http://localhost:8000/users/register"
DRIVER_REGISTRATION_URL = "http://localhost:8000/drivers/register"
CAR_REGISTRATION_URL = "http://localhost:8000/cars/register"
RIDE_REQUEST_URL = "http://localhost:8000/rides/book"
RIDE_COMPLETE_URL_TEMPLATE = "http://localhost:8000/rides/{ride_id}/complete"

# Global lists to store registered user and driver IDs
available_users = []
available_drivers = []

# Global counters
user_count = 0
driver_count = 0
car_count = 0
ride_count = 0

# Locks for thread safety
users_lock = threading.Lock()
drivers_lock = threading.Lock()
count_lock = threading.Lock()


def random_string(length=8):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


def random_password(length=10):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def simulate_user_registration():
    global user_count
    sleep_interval = 60.0 / USERS_PER_MINUTE
    while True:
        with count_lock:
            if user_count >= MAX_USERS:
                print("Reached maximum user registrations.")
                break
        email = f"user_{random_string()}@example.com"
        data = {
            "email": email,
            "password": random_password(),
            "name": random_string(6),
            "phone_number": "".join(random.choice("0123456789") for _ in range(10))
        }
        try:
            response = requests.post(USER_REGISTRATION_URL, json=data)
            response.raise_for_status()
            user = response.json()
            print("User registration response:", user)
            with users_lock:
                available_users.append(user["user_id"])
            with count_lock:
                user_count += 1
        except Exception as e:
            print("Error in user registration:", e)
        time.sleep(sleep_interval)


def simulate_driver_registration():
    global driver_count
    sleep_interval = 60.0 / DRIVERS_PER_MINUTE
    while True:
        with count_lock:
            if driver_count >= MAX_DRIVERS:
                print("Reached maximum driver registrations.")
                break
        email = f"driver_{random_string()}@example.com"
        data = {
            "email": email,
            "password": random_password(),
            "name": random_string(6),
            "phone_number": "".join(random.choice("0123456789") for _ in range(10)),
            "driver_license": random_string(10).upper()
        }
        try:
            response = requests.post(DRIVER_REGISTRATION_URL, json=data)
            response.raise_for_status()
            driver = response.json()
            print("Driver registration response:", driver)
            with drivers_lock:
                available_drivers.append(driver["driver_id"])
            with count_lock:
                driver_count += 1
        except Exception as e:
            print("Error in driver registration:", e)
        time.sleep(sleep_interval)


def simulate_car_registration():
    global car_count
    sleep_interval = 60.0 / CARS_PER_MINUTE
    while True:
        with count_lock:
            if car_count >= MAX_CARS:
                print("Reached maximum car registrations.")
                break
        with drivers_lock:
            if not available_drivers:
                print("No drivers available for car registration; waiting...")
                time.sleep(2)
                continue
            driver_id = random.choice(available_drivers)
        data = {
            "driver_id": driver_id,
            "make": random.choice(["Toyota", "Honda", "Ford", "Chevrolet", "BMW"]),
            "model": random_string(4).upper(),
            "year": random.randint(2000, 2023),
            "license_plate": f"{random_string(3).upper()}{random.randint(1000, 9999)}",
            "color": random.choice(["Blue", "Red", "Black", "White", "Green"])
        }
        try:
            response = requests.post(CAR_REGISTRATION_URL, json=data)
            response.raise_for_status()
            car = response.json()
            print("Car registration response:", car)
            with count_lock:
                car_count += 1
        except Exception as e:
            print("Error in car registration:", e)
        time.sleep(sleep_interval)


def complete_ride_after_delay(ride_id, user_id, driver_id):
    time.sleep(RIDE_DURATION_SECONDS)
    complete_url = RIDE_COMPLETE_URL_TEMPLATE.format(ride_id=ride_id)
    try:
        response = requests.post(complete_url)
        response.raise_for_status()
        completed_ride = response.json()
        print("Ride completion response:", completed_ride)
        # Mark user and driver as available again
        with users_lock:
            if user_id not in available_users:
                available_users.append(user_id)
        with drivers_lock:
            if driver_id not in available_drivers:
                available_drivers.append(driver_id)
    except Exception as e:
        print("Error completing ride:", e)


def simulate_ride_request():
    global ride_count
    sleep_interval = 60.0 / RIDES_PER_MINUTE
    while True:
        with count_lock:
            if ride_count >= MAX_RIDES:
                print("Reached maximum ride requests.")
                break
        with users_lock:
            if not available_users:
                print("No available users for ride request; waiting...")
                time.sleep(2)
                continue
            user_id = random.choice(available_users)
        with drivers_lock:
            if not available_drivers:
                print("No available drivers for ride request; waiting...")
                time.sleep(2)
                continue
            driver_id = random.choice(available_drivers)
        with users_lock:
            if user_id in available_users:
                available_users.remove(user_id)
        with drivers_lock:
            if driver_id in available_drivers:
                available_drivers.remove(driver_id)
        # Generate random coordinates for pickup and dropoff
        pickup_lon = random.uniform(-74, -73)
        pickup_lat = random.uniform(40, 41)
        dropoff_lon = random.uniform(-74, -73)
        dropoff_lat = random.uniform(40, 41)
        data = {
            "user_id": user_id,
            "pickup_location": f"POINT({pickup_lon} {pickup_lat})",
            "dropoff_location": f"POINT({dropoff_lon} {dropoff_lat})"
        }
        try:
            response = requests.post(RIDE_REQUEST_URL, json=data)
            response.raise_for_status()
            ride = response.json()
            print("Ride request response:", ride)
            with count_lock:
                ride_count += 1
            # Spawn a thread to complete the ride after delay
            threading.Thread(target=complete_ride_after_delay, args=(ride["ride_id"], user_id, driver_id),
                             daemon=True).start()
        except Exception as e:
            print("Error in ride request:", e)
            with users_lock:
                if user_id not in available_users:
                    available_users.append(user_id)
            with drivers_lock:
                if driver_id not in available_drivers:
                    available_drivers.append(driver_id)
        time.sleep(sleep_interval)


def main():
    threads = []
    # Start registration threads first
    t_user = threading.Thread(target=simulate_user_registration, daemon=True)
    t_driver = threading.Thread(target=simulate_driver_registration, daemon=True)
    t_user.start()
    t_driver.start()

    # Wait for 10 seconds to accumulate some registrations
    print("Waiting 10 seconds for initial user and driver registrations...")
    time.sleep(10)

    # Now start the dependent threads
    t_car = threading.Thread(target=simulate_car_registration, daemon=True)
    t_ride = threading.Thread(target=simulate_ride_request, daemon=True)
    threads.append(t_car)
    threads.append(t_ride)
    t_car.start()
    t_ride.start()

    # Optionally join all threads to wait until all reach their limit
    t_user.join()
    t_driver.join()
    t_car.join()
    t_ride.join()

    print("Simulation complete.")
    sys.exit(0)


if __name__ == "__main__":
    main()
