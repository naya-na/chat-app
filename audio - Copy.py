import socket
import pyaudio
import threading

# Audio Configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100  # Sampling rate
CHUNK = 1024  # Buffer size
PORT = 5000   # UDP Port
IP = "127.0.0.1"  # Change this for different clients

# Setup UDP Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, PORT))

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Setup Stream for Listening
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, 
                    input=True, output=True, frames_per_buffer=CHUNK)

def receive_audio():
    """ Receive and Play Audio """
    while True:
        try:
            data, addr = sock.recvfrom(CHUNK * 2)
            stream.write(data)
        except:
            break

def send_audio():
    """ Capture and Send Audio """
    while True:
        try:
            data = stream.read(CHUNK, exception_on_overflow=False)
            sock.sendto(data, (IP, PORT))
        except:
            break

# Start Threads for Sending and Receiving
threading.Thread(target=receive_audio, daemon=True).start()
threading.Thread(target=send_audio, daemon=True).start()

print("🔊 Audio Chat Started... Press Ctrl+C to Exit")

# Keep the script running
try:
    while True:
        pass
except KeyboardInterrupt:
    print("\n🛑 Audio Chat Stopped")
    sock.close()
    stream.stop_stream()
    stream.close()
    audio.terminate()
[]