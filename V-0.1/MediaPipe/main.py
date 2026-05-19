import cv2
import mediapipe as mp
from Bodyrules import analisar_postura
from HandRules import calcular_mao
from HandActivityMonitor import HandMonitor
from LightControl import LightControl
from LightControl import brightControl

camera = cv2.VideoCapture(0)
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)

while True:
    ret, frame = camera.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultado = pose.process(rgb)
    resultado_maos = hands.process(rgb)
    estado_mao_direita = None
    estado_mao_esquerda = None

    if resultado.pose_landmarks:
        mp_drawing.draw_landmarks(frame, resultado.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        pontos = resultado.pose_landmarks.landmark
        nariz = pontos[mp_pose.PoseLandmark.NOSE]
        quadril_esquerdo = pontos[mp_pose.PoseLandmark.LEFT_HIP]
        quadril_direito = pontos[mp_pose.PoseLandmark.RIGHT_HIP]
        joelho_esquerdo = pontos[mp_pose.PoseLandmark.LEFT_KNEE]
        joelho_direito = pontos[mp_pose.PoseLandmark.RIGHT_KNEE]
        pe_esquerdo = pontos[mp_pose.PoseLandmark.LEFT_ANKLE]
        pe_direito = pontos[mp_pose.PoseLandmark.RIGHT_ANKLE]
        ombro_direito = pontos[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        ombro_esquerdo = pontos[mp_pose.PoseLandmark.LEFT_SHOULDER]
        cotovelo_direito = pontos[mp_pose.PoseLandmark.RIGHT_ELBOW]
        cotovelo_esquerdo = pontos[mp_pose.PoseLandmark.LEFT_ELBOW]
        pulso_direito = pontos[mp_pose.PoseLandmark.RIGHT_WRIST]
        pulso_esquerdo = pontos[mp_pose.PoseLandmark.LEFT_WRIST]

        postura_analisada = analisar_postura(nariz, quadril_esquerdo, quadril_direito, joelho_esquerdo, joelho_direito, pe_esquerdo, pe_direito)
        cv2.putText(frame, postura_analisada, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    if resultado_maos.multi_hand_landmarks and resultado_maos.multi_handedness:
        for i, hand_landmarks in enumerate(resultado_maos.multi_hand_landmarks):
            label = resultado_maos.multi_handedness[i].classification[0].label
            
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            pontos_mao = hand_landmarks.landmark
            

            pulso         = pontos_mao[mp_hands.HandLandmark.WRIST]
            polegar_cmc   = pontos_mao[mp_hands.HandLandmark.THUMB_CMC]
            polegar_mcp   = pontos_mao[mp_hands.HandLandmark.THUMB_MCP]
            polegar_ip    = pontos_mao[mp_hands.HandLandmark.THUMB_IP]
            polegar_tip   = pontos_mao[mp_hands.HandLandmark.THUMB_TIP]
            indicador_mcp = pontos_mao[mp_hands.HandLandmark.INDEX_FINGER_MCP]
            indicador_pip = pontos_mao[mp_hands.HandLandmark.INDEX_FINGER_PIP]
            indicador_dip = pontos_mao[mp_hands.HandLandmark.INDEX_FINGER_DIP]
            indicador_tip = pontos_mao[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            medio_mcp     = pontos_mao[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
            medio_pip     = pontos_mao[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
            medio_dip     = pontos_mao[mp_hands.HandLandmark.MIDDLE_FINGER_DIP]
            medio_tip     = pontos_mao[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            anelar_mcp    = pontos_mao[mp_hands.HandLandmark.RING_FINGER_MCP]
            anelar_pip    = pontos_mao[mp_hands.HandLandmark.RING_FINGER_PIP]
            anelar_dip    = pontos_mao[mp_hands.HandLandmark.RING_FINGER_DIP]
            anelar_tip    = pontos_mao[mp_hands.HandLandmark.RING_FINGER_TIP]
            mindinho_mcp  = pontos_mao[mp_hands.HandLandmark.PINKY_MCP]
            mindinho_pip  = pontos_mao[mp_hands.HandLandmark.PINKY_PIP]
            mindinho_dip  = pontos_mao[mp_hands.HandLandmark.PINKY_DIP]
            mindinho_tip  = pontos_mao[mp_hands.HandLandmark.PINKY_TIP]

            estado_mao = calcular_mao(pulso, polegar_cmc, polegar_mcp, polegar_ip, polegar_tip, indicador_mcp, indicador_pip, indicador_dip, indicador_tip, medio_mcp, medio_pip, medio_dip, medio_tip, anelar_mcp, anelar_pip, anelar_dip, anelar_tip, mindinho_mcp, mindinho_pip, mindinho_dip, mindinho_tip)
            estado_mao.lado = label
            
            if label == "Right":
                estado_mao_esquerda = estado_mao
            elif label == "Left":
                estado_mao_direita = estado_mao

    if resultado.pose_landmarks and estado_mao_direita:
        handMonitor = HandMonitor(estado_mao_direita.lado,estado_mao_direita.aberta, ombro_esquerdo, ombro_direito, cotovelo_esquerdo, cotovelo_direito, pulso_direito, pulso_esquerdo)
        handMonitor
        
        LightControl(handMonitor)
        brightControl(estado_mao_direita, handMonitor)
    cv2.imshow("Tela", frame)
    if cv2.waitKey(1) == 27:
        break

camera.release()
cv2.destroyAllWindows()
