import import_ipynb

from ride import Ride
from visitor import Visitor
from waiting_info import WaitingInfo

# 놀이공원 대기 시스템 클래스를 선언한다.
class AmusementParkSystem:
    # 시스템에 필요한 속성들을 생성자에서 정의한다.
    def __init__(self):
        # 현재 시간을 저장한다. 프로그램은 0초부터 시작한다.
        self.current_time = 0

        # 현재 사용자를 저장할 변수를 선언한다.
        self.current_visitor = None

        # 놀이기구 목록을 저장할 리스트를 선언한다.
        self.ride_list = []

        # 자동으로 추가되는 대기자 번호를 저장한다.
        self.auto_visitor_number = 1

        # 자동 대기자 추가 시 일반 대기열의 최대 인원을 정한다.
        # 이 인원 이상이면 해당 놀이기구에는 자동 대기자를 더 추가하지 않아 무한 증가를 막는다.
        self.max_normal_queue = 20

        # 자동 대기자 추가 시 FastPass 대기열의 최대 인원을 정한다.
        self.max_fastpass_queue = 10

        # 놀이기구 객체를 생성하여 리스트에 추가한다.
        self.ride_list.append(Ride("스톤 익스프레스", 5, 4))
        self.ride_list.append(Ride("아르카나 라이드", 7, 6))
        self.ride_list.append(Ride("에오스 타워", 7, 8))
        self.ride_list.append(Ride("자이로 스핀 메이플 리뉴얼 버전", 7, 10))

        # 프로그램 시작 전에 각 놀이기구마다 기존 대기자 5명을 추가한다.
        self.add_sample_waiting_people()

    # 각 놀이기구마다 기존 대기자 5명을 추가하는 메소드를 선언한다.
    def add_sample_waiting_people(self):
        # 놀이기구 리스트의 길이만큼 반복문을 돌린다.
        for i in range(len(self.ride_list)):
            # 현재 순서의 놀이기구를 가져온다.
            ride = self.ride_list[i]

            # 한 놀이기구마다 5명씩 기존 대기자를 추가한다.
            for j in range(5):
                # 기존 대기자 객체를 생성한다.
                sample_visitor = Visitor("기존대기자" + str(i + 1) + "-" + str(j + 1), 1)

                # 대기 정보 객체를 생성한다.
                waiting_info = WaitingInfo(sample_visitor, ride.ride_name, "일반", self.current_time, 0)

                # 놀이기구 대기열에 대기 정보를 추가한다.
                ride.add_waiting(waiting_info)

            # 기존 대기자 추가 후 예상 탑승 시간을 다시 계산한다.
            ride.update_expected_times(self.current_time)

    # 프로그램을 실행하는 메소드를 선언한다.
    def run(self):
        print("🎢 놀이공원 대기 시스템")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("프로그램은 0초부터 시작합니다.")

        # 프로그램 실행 후 사용자를 먼저 등록한다.
        self.register_visitor()

        # 사용자가 종료를 선택할 때까지 반복한다.
        while True:
            # 메인 메뉴를 출력한다.
            self.show_main_menu()

            # 사용자로부터 메뉴 번호를 입력받는다.
            menu = input("👉 메뉴 번호를 선택하세요: ")

            # 입력한 메뉴에 따라 기능을 실행한다.
            if menu == "1":
                self.show_waiting_status()
            elif menu == "2":
                self.join_ride()
            elif menu == "3":
                self.current_visitor.show_boarding_history()
            elif menu == "4":
                self.show_popular_rides()
            elif menu == "5":
                self.show_my_info()
            elif menu == "6":
                print("프로그램을 종료합니다.")
                break
            else:
                print("잘못된 메뉴입니다.")

            # 종료가 아니라면 메뉴 실행 후 1초가 지난 것으로 처리한다.
            if menu != "6":
                self.time_pass()

    # 사용자 등록 메소드를 선언한다.
    def register_visitor(self):
        print()
        print("👤 사용자 등록")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("놀이공원 대기 시스템을 이용하기 위해 사용자 정보를 입력해주세요.")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        # 사용자로부터 이름을 입력받는다.
        visitor_name = input("👉 사용자 이름을 입력하세요: ")

        # 사용자로부터 티켓 타입을 숫자로 입력받는다.
        ticket_type = self.input_ticket_type()

        # 입력받은 정보로 사용자 객체를 생성한다.
        self.current_visitor = Visitor(visitor_name, ticket_type)

        # 사용자 등록 결과를 출력한다.
        print()
        print("✅ 사용자 등록 완료")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("👤 이름:", self.current_visitor.visitor_name)
        print("🎫 티켓 타입:", self.current_visitor.ticket_name)
        print("⚡ FastPass 잔여 횟수:", self.current_visitor.fastpass_count, "회")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    # 티켓 타입을 입력받는 메소드를 선언한다.
    def input_ticket_type(self):
        # 올바른 입력이 들어올 때까지 반복한다.
        while True:
            print()
            print("🎫 티켓 타입 선택")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print("이용하실 티켓 타입을 선택해주세요.")
            print()
            print("1️⃣  일반")
            print("2️⃣  FastPass 1회")
            print("3️⃣  FastPass 3회")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

            # 사용자로부터 티켓 타입 번호를 입력받는다.
            choice = input("👉 티켓 타입 번호를 입력하세요: ")

            # 1을 입력하면 일반 티켓으로 처리한다.
            if choice == "1":
                return 1

            # 2를 입력하면 FastPass 1회 티켓으로 처리한다.
            elif choice == "2":
                return 2

            # 3을 입력하면 FastPass 3회 티켓으로 처리한다.
            elif choice == "3":
                return 3

            # 그 외 입력은 다시 입력받는다.
            else:
                print()
                print("❌ 잘못된 입력입니다.")
                print("1, 2, 3 중에서 다시 입력해주세요.")

    # 메인 메뉴를 출력하는 메소드를 선언한다.
    def show_main_menu(self):
        print()
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("⏰ 현재 시간:", self.current_time, "초")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("1️⃣  놀이기구 대기 현황 조회")
        print("2️⃣  놀이기구 줄서기")
        print("3️⃣  나의 탑승 내역 조회")
        print("4️⃣  인기 놀이기구 조회")
        print("5️⃣  나의 정보 조회")
        print("6️⃣  종료")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    # 놀이기구 목록을 출력하는 메소드를 선언한다.
    def show_ride_list(self):
        print()
        print("🎡 놀이기구 목록")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        # 놀이기구 리스트의 길이만큼 반복문을 돌린다.
        for i in range(len(self.ride_list)):
            # 현재 순서의 놀이기구를 가져온다.
            ride = self.ride_list[i]

            # 놀이기구 정보를 출력한다.
            print(str(i + 1) + ".", ride.ride_name)

        # 뒤로 가기(메인 메뉴 복귀) 항목을 출력한다.
        print("0. 뒤로 가기")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    # 대기할 놀이기구를 선택하는 메소드를 선언한다.
    def select_ride(self):
        # 놀이기구 목록을 출력한다.
        self.show_ride_list()

        # 사용자로부터 놀이기구 번호를 입력받는다.
        choice = input("👉 대기할 놀이기구 번호를 선택하세요 (0: 뒤로 가기): ")

        # 0을 입력하면 줄서기를 취소하고 메인 메뉴로 돌아간다.
        if choice == "0":
            print("메인 메뉴로 돌아갑니다.")
            return None

        # 입력한 번호가 1~4 중 하나인지 확인한다.
        if choice == "1" or choice == "2" or choice == "3" or choice == "4":
            # 리스트의 인덱스는 0부터 시작하므로 입력값에서 1을 뺀다.
            index = int(choice) - 1

            # 선택한 놀이기구 객체를 반환한다.
            return self.ride_list[index]

        # 잘못 입력했다면 None을 반환한다.
        else:
            print("잘못된 놀이기구 번호입니다.")
            return None

    # 놀이기구 줄서기 메소드를 선언한다.
    def join_ride(self):
        print()
        print("🎢 놀이공원 줄서기")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        # 사용자가 대기할 놀이기구를 선택한다.
        ride = self.select_ride()

        # 잘못된 번호를 입력했다면 메소드를 종료한다.
        if ride == None:
            return

        # 선택한 놀이기구에 이미 대기 중이면 등록을 막는다.
        if ride.get_my_waiting_info(self.current_visitor) != None:
            print("\n이미 해당 놀이기구에 대기 중입니다.")
            return

        # 일반 대기열로 등록할지 FastPass 대기열로 등록할지 결정한다.
        queue_type = self.decide_queue_type()

        # 일반 대기는 한 번에 하나만 가능하므로, 이미 일반 대기 중이면 등록을 막는다.
        # (FastPass 대기는 별도로 하나 더 가질 수 있다.)
        if queue_type == "일반" and self.has_normal_waiting() == True:
            print("\n이미 다른 놀이기구에 일반 대기 중입니다.")
            print("일반 대기는 한 번에 하나만 가능합니다. (FastPass 대기는 별도로 1개 가능)")
            return

        # 예상 탑승 시간을 구한다.
        expected_time = ride.get_expected_time_for_new_waiting(self.current_time, queue_type)

        # 예상 대기 시간을 구한다.
        wait_time = expected_time - self.current_time

        # 대기 정보 객체를 생성한다.
        waiting_info = WaitingInfo(self.current_visitor, ride.ride_name, queue_type, self.current_time, expected_time)

        # 현재 사용자는 5초 전 알림에서 탑승 여부를 확인해야 하므로 False로 변경한다.
        waiting_info.boarding_confirm = False

        # 놀이기구 대기열에 대기 정보를 추가한다.
        ride.add_waiting(waiting_info)

        # 대기열 변경 후 예상 탑승 시간을 다시 계산한다.
        ride.update_expected_times(self.current_time)

        # 대기 등록 결과를 출력한다.
        print()
        print("✅ 대기 등록 완료")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("🎠 놀이기구:", ride.ride_name)
        print("🎫 대기 종류:", queue_type)
        print("⏳ 예상 대기 시간:", wait_time, "초")
        print("⏰ 예상 탑승 시간:", expected_time, "초")
        print("🔔 입장 15초 전 / 5초 전 알림이 등록되었습니다.")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    # 일반 대기와 FastPass 대기 중 어떤 대기열에 등록할지 결정하는 메소드를 선언한다.
    def decide_queue_type(self):
        # 현재 사용자가 FastPass 사용자가 아니면 일반 대기열로 등록한다.
        if self.current_visitor.is_fastpass_user() == False:
            return "일반"

        # 이미 FastPass로 대기 중인 놀이기구가 있으면 일반 대기열로 등록한다.
        if self.has_fastpass_waiting() == True:
            print("\n이미 FastPass로 대기 중인 놀이기구가 있습니다.")
            print("FastPass는 동시에 1개만 등록 가능하므로 일반 대기열로 등록됩니다.")
            return "일반"

        # FastPass 잔여 횟수가 없으면 일반 대기열로 등록한다.
        if self.current_visitor.fastpass_count <= 0:
            print("\nFastPass 잔여 횟수가 없습니다.")
            print("일반 대기열로 등록됩니다.")
            return "일반"

        # FastPass를 사용할지 사용자에게 입력받는다.
        while True:
            print("\nFastPass 잔여 횟수:", self.current_visitor.fastpass_count)
            answer = input("⚡ 이번 탑승에 FastPass를 사용하시겠습니까? (Y/N): ")

            # Y를 입력하면 FastPass 대기열로 등록한다.
            if answer == "Y" or answer == "y":
                return "FastPass"

            # N을 입력하면 일반 대기열로 등록한다.
            elif answer == "N" or answer == "n":
                return "일반"

            # 그 외 입력은 다시 입력받는다.
            else:
                print("Y 또는 N으로 입력해주세요.")

    # 현재 사용자가 FastPass 대기열에 등록되어 있는지 확인하는 메소드를 선언한다.
    def has_fastpass_waiting(self):
        # 놀이기구 리스트의 길이만큼 반복문을 돌린다.
        for i in range(len(self.ride_list)):
            # 현재 순서의 놀이기구를 가져온다.
            ride = self.ride_list[i]

            # FastPass 대기열의 길이만큼 반복문을 돌린다.
            for j in range(len(ride.fastpass_queue)):
                # 현재 순서의 대기 정보를 가져온다.
                waiting_info = ride.fastpass_queue[j]

                # 현재 사용자 객체와 대기 정보의 사용자 객체가 같으면 True를 반환한다.
                if waiting_info.visitor == self.current_visitor:
                    return True

        # 모든 FastPass 대기열에 현재 사용자가 없다면 False를 반환한다.
        return False

    # 현재 사용자가 일반 대기열에 등록되어 있는지 확인하는 메소드를 선언한다.
    def has_normal_waiting(self):
        # 놀이기구 리스트의 길이만큼 반복문을 돌린다.
        for i in range(len(self.ride_list)):
            # 현재 순서의 놀이기구를 가져온다.
            ride = self.ride_list[i]

            # 일반 대기열의 길이만큼 반복문을 돌린다.
            for j in range(len(ride.normal_queue)):
                # 현재 순서의 대기 정보를 가져온다.
                waiting_info = ride.normal_queue[j]

                # 현재 사용자 객체와 대기 정보의 사용자 객체가 같으면 True를 반환한다.
                if waiting_info.visitor == self.current_visitor:
                    return True

        # 모든 일반 대기열에 현재 사용자가 없다면 False를 반환한다.
        return False

    # 전체 놀이기구 대기 현황을 출력하는 메소드를 선언한다.
    def show_waiting_status(self):
        print()
        print("📋 놀이기구 대기 현황")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        # 놀이기구 리스트의 길이만큼 반복문을 돌린다.
        for i in range(len(self.ride_list)):
            # 현재 순서의 놀이기구를 가져온다.
            ride = self.ride_list[i]

            # 하나의 놀이기구 대기 현황을 출력한다.
            self.show_one_ride_status(ride)

    # 하나의 놀이기구 대기 현황을 출력하는 메소드를 선언한다.
    def show_one_ride_status(self, ride):
        # 일반 예상 대기 시간을 구한다.
        normal_wait_time = ride.get_wait_time(self.current_time, "일반")

        # FastPass 예상 대기 시간을 구한다.
        fastpass_wait_time = ride.get_wait_time(self.current_time, "FastPass")

        print()
        print("🎠", ride.ride_name)
        print("──────────────────────────────")
        print("⏱ 탑승 시간:", ride.ride_time, "초")
        print("👥 수용 인원:", ride.capacity, "명")
        print("🚶 일반 대기:", ride.get_normal_count(), "명 / 지금 서면", normal_wait_time, "초")
        print("⚡ FastPass 대기:", ride.get_fastpass_count(), "명 / 지금 서면", fastpass_wait_time, "초")

        # 현재 사용자가 이 놀이기구에 대기 중인지 확인한다.
        my_waiting = ride.get_my_waiting_order(self.current_visitor)

        # 현재 사용자가 대기 중이라면 몇 번째 대기인지와 탑승까지 남은 시간을 출력한다.
        if my_waiting[1] != 0:
            # 현재 사용자의 대기 정보를 가져온다.
            my_info = ride.get_my_waiting_info(self.current_visitor)

            # 예상 탑승 시간에서 현재 시간을 빼서 남은 시간을 구한다.
            remain_time = my_info.expected_time - self.current_time

            # 음수가 나오지 않도록 0 미만이면 0으로 맞춘다.
            if remain_time < 0:
                remain_time = 0

            print("✅ 나의 대기:", my_waiting[0], "대기열", my_waiting[1], "번째 / 탑승까지", remain_time, "초 남음")

        print("──────────────────────────────")

    # 나의 정보를 출력하는 메소드를 선언한다.
    def show_my_info(self):
        print()
        print("👤 나의 정보")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("이름:", self.current_visitor.visitor_name)
        print("티켓 타입:", self.current_visitor.ticket_name)
        print("FastPass 잔여 횟수:", self.current_visitor.fastpass_count, "회")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
    # 인기 놀이기구 TOP 3를 출력하는 메소드를 선언한다.
    def show_popular_rides(self):
        print()
        print("🔥 인기 놀이기구 TOP 3")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("누적 대기 인원이 많은 놀이기구를 순서대로 보여드립니다.")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        # 정렬된 놀이기구를 저장할 리스트를 선언한다.
        sorted_list = []

        # 기존 놀이기구 리스트를 정렬용 리스트에 복사한다.
        for i in range(len(self.ride_list)):
            sorted_list.append(self.ride_list[i])

        # 누적 대기 인원이 많은 순서대로 정렬한다.
        for i in range(len(sorted_list)):
            for j in range(i + 1, len(sorted_list)):
                # 뒤쪽 놀이기구의 누적 대기 인원이 더 많으면 위치를 바꾼다.
                if sorted_list[i].total_wait_count < sorted_list[j].total_wait_count:
                    temp = sorted_list[i]
                    sorted_list[i] = sorted_list[j]
                    sorted_list[j] = temp

        # 상위 3개의 놀이기구만 출력한다.
        for i in range(3):
            ride = sorted_list[i]

            # 순위에 따라 이모지를 다르게 출력한다.
            if i == 0:
                rank_icon = "🥇"
            elif i == 1:
                rank_icon = "🥈"
            else:
                rank_icon = "🥉"

            print(rank_icon, i + 1, "위")
            print("🎠 놀이기구:", ride.ride_name)
            print("👥 누적 대기 인원:", ride.total_wait_count, "명")
            print("──────────────────────────────")

    # 시간이 지나가는 것을 처리하는 메소드를 선언한다.
    def time_pass(self):
        # 현재 시간을 1초 증가시킨다.
        self.current_time = self.current_time + 1

        # 5초마다 자동 대기자를 추가한다.
        if self.current_time % 5 == 0:
            self.add_auto_waiting_people()

        # 전체 놀이기구의 예상 탑승 시간을 다시 계산한다.
        self.update_all_expected_times()

        # 입장 알림을 확인한다.
        self.check_alert()

        # 놀이기구 탑승 처리를 확인한다.
        self.process_all_rides()

    # 전체 놀이기구의 예상 탑승 시간을 다시 계산하는 메소드를 선언한다.
    def update_all_expected_times(self):
        # 놀이기구 리스트의 길이만큼 반복문을 돌린다.
        for i in range(len(self.ride_list)):
            # 현재 순서의 놀이기구 예상 탑승 시간을 다시 계산한다.
            self.ride_list[i].update_expected_times(self.current_time)

    # 5초마다 대기열에 자동 대기자를 추가하는 메소드를 선언한다.
    def add_auto_waiting_people(self):
        # 한 놀이기구마다 FastPass 대기열에 추가할 자동 대기자 수를 저장한다.
        fastpass_add_count = 1

        print()
        print("👥 자동 대기자 추가")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("⏰", self.current_time, "초가 되어 모든 놀이기구에 자동 대기자가 추가됩니다.")
        print("(5초마다 일반 대기는 수용 인원에 비례해서, FastPass는", fastpass_add_count, "명 추가. 단 대기열이 상한 이상이면 추가하지 않음)")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        # 놀이기구 리스트의 길이만큼 반복문을 돌린다.
        for i in range(len(self.ride_list)):
            # 현재 순서의 놀이기구를 가져온다.
            ride = self.ride_list[i]

            # 일반 대기열에 추가할 자동 대기자 수를 수용 인원에 비례해 정한다.
            # 수용 인원이 큰(인기 많은) 놀이기구일수록 더 많은 대기자가 몰린다고 본다.
            normal_add_count = ride.capacity // 2

            # 일반 대기열에 자동 대기자를 추가한다.
            for j in range(normal_add_count):
                # 일반 대기 인원이 상한 이상이면 더 이상 추가하지 않는다.
                if ride.get_normal_count() >= self.max_normal_queue:
                    break

                # 자동 대기자 객체를 생성한다.
                auto_visitor = Visitor("자동대기자" + str(self.auto_visitor_number), 1)

                # 일반 대기 정보 객체를 생성한다.
                waiting_info = WaitingInfo(auto_visitor, ride.ride_name, "일반", self.current_time, 0)

                # 놀이기구 일반 대기열에 자동 대기자를 추가한다.
                ride.add_waiting(waiting_info)

                # 다음 자동 대기자 번호를 증가시킨다.
                self.auto_visitor_number = self.auto_visitor_number + 1

            # FastPass 대기열에 자동 대기자를 추가한다.
            for j in range(fastpass_add_count):
                # FastPass 대기 인원이 상한 이상이면 더 이상 추가하지 않는다.
                if ride.get_fastpass_count() >= self.max_fastpass_queue:
                    break

                # FastPass 자동 대기자 객체를 생성한다. (FastPass 보유자로 생성한다.)
                auto_visitor = Visitor("자동FastPass대기자" + str(self.auto_visitor_number), 2)

                # FastPass 대기 정보 객체를 생성한다.
                waiting_info = WaitingInfo(auto_visitor, ride.ride_name, "FastPass", self.current_time, 0)

                # 놀이기구 FastPass 대기열에 자동 대기자를 추가한다.
                ride.add_waiting(waiting_info)

                # 다음 자동 대기자 번호를 증가시킨다.
                self.auto_visitor_number = self.auto_visitor_number + 1

            # 현재 놀이기구의 예상 탑승 시간을 다시 계산한다.
            ride.update_expected_times(self.current_time)

        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    # 입장 15초 전 / 5초 전 알림을 확인하는 메소드를 선언한다.
    def check_alert(self):
        # 놀이기구 리스트의 길이만큼 반복문을 돌린다.
        for i in range(len(self.ride_list)):
            # 현재 순서의 놀이기구를 가져온다.
            ride = self.ride_list[i]

            # FastPass 대기열과 일반 대기열을 합쳐서 전체 대기열을 만든다.
            all_queue = ride.fastpass_queue + ride.normal_queue

            # 전체 대기열의 길이만큼 반복문을 돌린다.
            for j in range(len(all_queue)):
                # 현재 순서의 대기 정보를 가져온다.
                waiting_info = all_queue[j]

                # 현재 사용자의 대기 정보인지 확인한다.
                if waiting_info.visitor == self.current_visitor:
                    # 예상 탑승 시간에서 현재 시간을 빼서 남은 시간을 구한다.
                    remain_time = waiting_info.expected_time - self.current_time

                    # 남은 시간이 15초 이하이고 아직 15초 전 알림을 하지 않았다면 이동 안내를 출력한다.
                    if remain_time <= 15 and remain_time > 5 and waiting_info.alert_15 == False:
                        print()
                        print("🔔 이동 안내")
                        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                        print("🚶 이제", waiting_info.ride_name, "(으)로 이동해주세요 (탑승까지", remain_time, "초)")
                        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                        waiting_info.alert_15 = True

                    # 남은 시간이 5초 이하이고 아직 5초 전 알림을 하지 않았다면 도착 여부를 입력받는다.
                    if remain_time <= 5 and remain_time >= 0 and waiting_info.alert_5 == False:
                        print()
                        print("🚪 도착 확인")
                        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                        print("🎠", waiting_info.ride_name)
                        print("⏰ 입장 5초 전입니다.")
                        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                        waiting_info.alert_5 = True

                        # 사용자에게 도착 여부를 입력받는다.
                        while True:
                            answer = input("👉 " + waiting_info.ride_name + "에 도착하셨나요? (Y/N): ")

                            # Y를 입력하면 탑승 확인 상태로 변경한다.
                            if answer == "Y" or answer == "y":
                                print("✅ 탑승 확인이 완료되었습니다.")
                                waiting_info.boarding_confirm = True
                                break

                            # N을 입력하면 대기열에서 제거한다.
                            elif answer == "N" or answer == "n":
                                print("❌ 탑승하지 않는 것으로 처리되어 대기열에서 제거됩니다.")
                                ride.remove_waiting_info(waiting_info)

                                # 대기열이 변경되었으므로 예상 탑승 시간을 다시 계산한다.
                                ride.update_expected_times(self.current_time)
                                break

                            # Y 또는 N이 아니면 다시 입력받는다.
                            else:
                                print("Y 또는 N으로 입력해주세요.")

    # 모든 놀이기구의 탑승 처리를 확인하는 메소드를 선언한다.
    def process_all_rides(self):
        # 놀이기구 리스트의 길이만큼 반복문을 돌린다.
        for i in range(len(self.ride_list)):
            # 현재 순서의 놀이기구를 가져온다.
            ride = self.ride_list[i]

            # 현재 놀이기구에서 탑승 처리된 사용자 리스트를 가져온다.
            boarding_list = ride.process_boarding(self.current_time)

            # 탑승 처리된 사용자 리스트의 길이만큼 반복문을 돌린다.
            for j in range(len(boarding_list)):
                # 현재 순서의 대기 정보를 가져온다.
                waiting_info = boarding_list[j]

                # 현재 사용자가 탑승 처리되었다면 탑승 완료 문구를 출력한다.
                if waiting_info.visitor == self.current_visitor:
                    print("\n[탑승 처리 완료]")
                    print("놀이기구:", waiting_info.ride_name)
                    print("대기 종류:", waiting_info.queue_type)
                    print("FastPass 잔여 횟수:", self.current_visitor.fastpass_count)