from vidgear.gears import NetGear
import cv2

client = NetGear(receive_mode = True)

# infinite loop
while True:
    frame = client.recv()

    if frame is None:
        break


    cv2.imshow("Output Frame", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# close output window
cv2.destroyAllWindows()
client.close()