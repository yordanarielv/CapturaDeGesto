import cv2
import mediapipe as mp
import pygame
import threading

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mpDraw = mp.solutions.drawing_utils
cap=cv2.VideoCapture(0)
anterior=None
video_run= False
pygame.init()
video = cv2.VideoCapture("Hajime no Ippo.mp4")
clock = pygame.time.Clock()
ventana = pygame.display.set_mode((640, 480))


while True:
   bol,frame=cap.read()
   frame_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
   resultado = hands.process(frame_rgb)


   if resultado.multi_hand_landmarks:
       for handLms in resultado.multi_hand_landmarks:
           mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)
           indiceP=handLms.landmark[8].y
           indiceN=handLms.landmark[6].y
           medioP=handLms.landmark[12].y
           medioN=handLms.landmark[10].y
           anularP=handLms.landmark[16].y
           anularN=handLms.landmark[14].y
           meP=handLms.landmark[20].y
           meN=handLms.landmark[18].y
           if indiceP > indiceN and medioP > medioN and anularP > anularN and meP > meN:
               video_run = True  # 👈 activa el video
           else:
               video_run = False
               ventana.fill((0, 0, 0))
               pygame.display.update()

           if video_run == True:  # 👈 esto va FUERA del if del gesto
               bol_video, frame_video = video.read()
               if bol_video:
                   frame_rgb_video = cv2.cvtColor(frame_video, cv2.COLOR_BGR2RGB)
                   frame_rgb_video = cv2.resize(frame_rgb_video, (640, 480))
                   superficie = pygame.surfarray.make_surface(frame_rgb_video)
                   superficie = pygame.transform.rotate(superficie, -90)
                   ventana.blit(superficie, (0, 0))
                   pygame.display.update()
               else:
                   video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                   video_run = False




   if cv2.waitKey(1) & 0xFF == ord('q'):
       break


