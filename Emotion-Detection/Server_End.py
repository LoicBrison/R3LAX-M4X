from vidgear.gears import VideoGear
from vidgear.gears import NetGear

stream = VideoGear(enablePiCamera=True).start()

while True:
    try: 
        frame = stream.read()

        if frame is None:
            break

        server.send(frame)
    
    except KeyboardInterrupt:
        break

stream.stop()
writer.close()