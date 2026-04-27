import cv2
import mediapipe as mp
from rules import analisar_postura

camera = cv2.VideoCapture(0)
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

img = cv2.imread("imagem.jpg")
while True:
    ret, frame = camera.read()    
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultado = pose.process(rgb)
    if resultado.pose_landmarks:
        mp_drawing.draw_landmarks(frame, resultado.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    if resultado.pose_landmarks:
        pontos = resultado.pose_landmarks.landmark
        nariz = pontos[mp_pose.PoseLandmark.NOSE]
        quadril_esquerdo = pontos[mp_pose.PoseLandmark.LEFT_HIP]
        quadril_direito = pontos[mp_pose.PoseLandmark.RIGHT_HIP]
        joelho_esquerdo = pontos[mp_pose.PoseLandmark.LEFT_KNEE]
        joelho_direito = pontos[mp_pose.PoseLandmark.RIGHT_KNEE]

        postura_analisada = analisar_postura(nariz, quadril_esquerdo, quadril_direito, joelho_esquerdo, joelho_direito)           
        cv2.putText(frame, postura_analisada, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Tela", frame)
    if cv2.waitKey(1) == 27:
        break
camera.release()
cv2.destroyAllWindows()