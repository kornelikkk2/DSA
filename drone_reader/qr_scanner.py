import cv2
import numpy as np
import requests
import time
from django.conf import settings

def draw_qr(frame, qr_points):
    n = len(qr_points)
    for j in range(n):
        cv2.line(frame, tuple(qr_points[j]), tuple(qr_points[(j+1) % n]), (0, 255, 0), 3)
    return frame

def send_to_server(qr_data):
    """Функция для отправки данных на сервер"""
    server_url = "http://localhost:8000/api/qr_codes/"  # URL вашего Django сервера
    print(qr_data)
    try:
        response = requests.post(
            server_url,
            json={"qr_data": qr_data, "timestamp": time.time()},
            timeout=2
        )
        if response.status_code == 200:
            print(f"Data sent successfully: {qr_data}")
        else:
            print(f"Server returned status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data to server: {e}")

def do_smth_with_qr_result(qr_text):
    if qr_text:
        print(f"QR Code Detected: {qr_text}")
        send_to_server(qr_text)

def show_video(frame):     
    cv2.imshow('QR Code Scanner', frame)

def scan_qr_code(frame, qr_detector):
    results = []
    retval, decoded_info, points, _ = qr_detector.detectAndDecodeMulti(frame)
    if retval:
        for decoded_text, qr_points in zip(decoded_info, points):
            results.append({
                'data': decoded_text,
                'points': qr_points.astype(int)
            })
    return results

def main():

    stream_url = "http://192.168.2.137:8080/stream?topic=/webcam/image_raw"

    qr_detector = cv2.QRCodeDetector()
    cap = cv2.VideoCapture(stream_url)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    
    sent_qrs = {}
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Could not read frame.")
            break

        qr_results = scan_qr_code(frame, qr_detector)

        for result in qr_results:
            qr_text = result['data']
            
            if qr_text not in sent_qrs:
                do_smth_with_qr_result(qr_text)
                sent_qrs[qr_text] = time.time()
                frame = draw_qr(frame, result['points'])
            
            current_time = time.time()
            sent_qrs = {k: v for k, v in sent_qrs.items() if current_time - v < 600}
        
        show_video(frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
