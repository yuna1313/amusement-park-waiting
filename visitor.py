# 사용자 클래스 선언
class Visitor:
    # 사용자에게 필요한 속성들을 생성자에서 정의
    # 사용자 이름, 티켓 타입, 티켓 이름, 탑승 기록 리스트, FastPass 사용 가능 횟수
    # 티켓 타입: 1은 일반, 2는 FastPass 1회, 3은 FastPass 3회를 의미
    def __init__(self, visitor_name, ticket_type):
        self.visitor_name = visitor_name
        self.ticket_type = ticket_type
        self.ticket_name = ""
        self.fastpass_count = 0
        self.boarding_history = []

        # 티켓 타입에 따라 티켓 이름과 FastPass 사용 가능 횟수를 저장한다.
        if ticket_type == 1:
            self.ticket_name = "일반"
            self.fastpass_count = 0
        elif ticket_type == 2:
            self.ticket_name = "FastPass 1회"
            self.fastpass_count = 1
        elif ticket_type == 3:
            self.ticket_name = "FastPass 3회"
            self.fastpass_count = 3
        else:
            self.ticket_name = "일반"
            self.fastpass_count = 0

    # FastPass 사용자인지 확인하는 메소드 선언
    def is_fastpass_user(self):
        # 티켓 타입이 2 또는 3이면 FastPass 사용자이므로 True 반환
        if self.ticket_type == 2 or self.ticket_type == 3:
            return True
        # 티켓 타입이 1이면 일반 사용자이므로 False 반환
        else:
            return False

    # 탑승 기록을 추가하는 메소드 선언
    def add_boarding_record(self, record):
        # 사용자의 탑승 기록 리스트에 탑승 기록 추가
        self.boarding_history.append(record)

    # 사용자의 탑승 기록을 출력하는 메소드를 선언한다.
    def show_boarding_history(self):
        print()
        print("🎠 나의 놀이기구 탑승 내역")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        # 탑승 기록이 없으면 안내 문구를 출력한다.
        if len(self.boarding_history) == 0:
            print("아직 탑승 내역이 없습니다.")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        # 탑승 기록이 있으면 반복문을 이용해 전체 탑승 기록을 출력한다.
        else:
            for i in range(len(self.boarding_history)):
                print()
                print("📌", i + 1, "번째 탑승 기록")
                print("──────────────────────────────")
                self.boarding_history[i].show_record()

            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")