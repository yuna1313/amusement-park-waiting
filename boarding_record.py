# 탑승 기록 클래스 선언
class BoardingRecord:
    # 탑승 기록에 필요한 속성들을 생성자에서 정의
    # 탑승한 놀이기구 이름, 탑승 시작 시간, 탑승 종료 시간, 대기 시간, 대기 종류 (일반/FastPass)
    def __init__(self, ride_name, start_time, end_time, wait_time, queue_type):
        self.ride_name = ride_name
        self.start_time = start_time
        self.end_time = end_time
        self.wait_time = wait_time
        self.queue_type = queue_type

    # 탑승 기록을 출력하는 메소드를 선언한다.
    def show_record(self):
        print("🎠 놀이기구:", self.ride_name)
        print("⏰ 탑승 시간:", self.start_time, "초 ~", self.end_time, "초")
        print("⏳ 대기 시간:", self.wait_time, "초")
        print("🎫 대기 종류:", self.queue_type)