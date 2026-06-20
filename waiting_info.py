# 대기 정보를 저장하는 클래스 선언
class WaitingInfo:
    # 대기 정보에 필요한 속성들을 생성자에서 정의
    # 사용자 정보, 놀이기구 이름, 대기 타입(일반/FastPass), 대기 등록 시간, 예상 탑승 시간, 15초 전 알림 출력 여부, 5초 전 알림 출력 여부, 탑승 여부
    def __init__(self, visitor, ride_name, queue_type, register_time, expected_time):
        self.visitor = visitor
        self.ride_name = ride_name
        self.queue_type = queue_type
        self.register_time = register_time
        self.expected_time = expected_time
        self.alert_15 = False
        self.alert_5 = False
        self.boarding_confirm = True