from controller import Robot
import socket

# Create the Robot instance and get timestep
robot = Robot()
timestep = int(robot.getBasicTimeStep())

# Get wheel motors and initialize
left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

# Socket setup for gesture communication
HOST = '127.0.0.1'  # Localhost
PORT = 12345        # Arbitrary port number

try:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    server_socket.settimeout(0.1)  # Set to non-blocking mode
    print("✅ Socket setup complete. Waiting for gesture connection...")
except Exception as e:
    print(f"❌ Socket error: {e}")

conn = None  # Connection object

# Main control loop
while robot.step(timestep) != -1:
    if conn is None:
        # Try to accept a connection from gesture program
        try:
            conn, addr = server_socket.accept()
            print("🎉 Gesture program connected!")
        except socket.timeout:
            continue  # No connection yet, keep trying
    else:
        # Connection established - receive and process commands
        try:
            data = conn.recv(1024).decode().strip()
            if data:
                if data.startswith("Command: "):
                    command = data.replace("Command: ", "")
                    print(f"Executing: {command}")
                    
                    # Execute the command
                    if command == "W":  # Forward
                        left_motor.setVelocity(2.0)
                        right_motor.setVelocity(2.0)
                    elif command == "S":  # Stop
                        left_motor.setVelocity(0.0)
                        right_motor.setVelocity(0.0)
                    elif command == "A":  # Turn left
                        left_motor.setVelocity(-1.0)
                        right_motor.setVelocity(1.0)
                    elif command == "D":  # Turn right
                        left_motor.setVelocity(1.0)
                        right_motor.setVelocity(-1.0)
        except:
            # Maintain connection even if no data received
            pass