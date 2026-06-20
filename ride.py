import import_ipynb

from visitor import Visitor
from waiting_info import WaitingInfo
from boarding_record import BoardingRecord

# 놀이기구 클래스를 선언한다.
class Ride:
    # 놀이기구에 필요한 속성들을 생성자에서 정의한다.
    def __init__(self, ride_name, ride_time, capacity):
        # 놀이기구 이름을 저장한다.
        self.ride_name = ride_name

        # 코드에서 사용할 탑승 시간을 초 단위로 저장한다.
        # 예: 스톤 익스프레스는 5초, 아르카나 라이드는 7초
        self.ride_time = ride_time

        # 한 번에 탑승 가능한 인원을 저장한다.
        # 예: 스톤 익스프레스는 2명, 에오스 타워는 6명
        self.capacity = capacity

        # 일반 대기열을 저장할 리스트를 선언한다.
        self.normal_queue = []

        # FastPass 대기열을 저장할 리스트를 선언한다.
        self.fastpass_queue = []

        # 누적 대기 인원을 저장한다.
        self.total_wait_count = 0

        # 다음 탑승 처리 시간을 저장한다.
        # 프로그램은 0초부터 시작하고, 첫 운행은 ride_time초 뒤에 시작한다고 가정한다.
        self.next_boarding_time = ride_time

    # 대기열에 사용자를 추가하는 메소드를 선언한다.
    def add_waiting(self, waiting_info):
        # FastPass 대기이면 FastPass 대기열에 추가한다.
        if waiting_info.queue_type == "FastPass":
            self.fastpass_queue.append(waiting_info)

        # 일반 대기이면 일반 대기열에 추가한다.
        else:
            self.normal_queue.append(waiting_info)

        # 대기 등록이 되었으므로 누적 대기 인원을 1 증가시킨다.
        self.total_wait_count = self.total_wait_count + 1

    # 일반 대기 인원을 반환하는 메소드를 선언한다.
    def get_normal_count(self):
        return len(self.normal_queue)

    # FastPass 대기 인원을 반환하는 메소드를 선언한다.
    def get_fastpass_count(self):
        return len(self.fastpass_queue)

    # 같은 사용자가 이미 해당 놀이기구에 대기 중인지 확인하는 메소드를 선언한다.
    def has_same_visitor(self, visitor):
        # 일반 대기열에서 같은 사용자 객체가 있는지 확인한다.
        for i in range(len(self.normal_queue)):
            if self.normal_queue[i].visitor == visitor:
                return True

        # FastPass 대기열에서 같은 사용자 객체가 있는지 확인한다.
        for i in range(len(self.fastpass_queue)):
            if self.fastpass_queue[i].visitor == visitor:
                return True

        # 같은 사용자가 없으면 False를 반환한다.
        return False

    # 한 번 운행할 때 탑승할 대기자를 선택하는 메소드를 선언한다.
    def make_boarding_group(self, fastpass_queue, normal_queue):
        # 이번 운행에서 탑승할 대기 정보를 저장할 리스트를 선언한다.
        boarding_group = []

        # FastPass 대기 인원이 수용 가능 인원보다 많고 일반 대기자도 있으면 반반으로 탑승시킨다.
        # 예: 수용 가능 인원 6명, FastPass 7명, 일반 5명이면 FastPass 3명 + 일반 3명 탑승
        if len(fastpass_queue) > self.capacity and len(normal_queue) > 0:
            # FastPass가 가져갈 좌석 수를 구한다.
            fastpass_limit = self.capacity // 2

            # 일반 대기가 가져갈 좌석 수를 구한다.
            normal_limit = self.capacity - fastpass_limit

            # FastPass 제한 인원만큼 탑승 그룹에 추가한다.
            fastpass_count = 0
            while fastpass_count < fastpass_limit and len(fastpass_queue) > 0:
                boarding_group.append(fastpass_queue.pop(0))
                fastpass_count = fastpass_count + 1

            # 일반 제한 인원만큼 탑승 그룹에 추가한다.
            normal_count = 0
            while normal_count < normal_limit and len(normal_queue) > 0:
                boarding_group.append(normal_queue.pop(0))
                normal_count = normal_count + 1

            # 일반 대기자가 부족해서 자리가 남으면 FastPass 대기자를 추가로 탑승시킨다.
            while len(boarding_group) < self.capacity and len(fastpass_queue) > 0:
                boarding_group.append(fastpass_queue.pop(0))

            # FastPass 대기자가 부족해서 자리가 남으면 일반 대기자를 추가로 탑승시킨다.
            while len(boarding_group) < self.capacity and len(normal_queue) > 0:
                boarding_group.append(normal_queue.pop(0))

        # FastPass 대기 인원이 수용 가능 인원보다 많지 않으면 FastPass를 먼저 태운다.
        else:
            # 탑승 가능 인원만큼 반복한다.
            while len(boarding_group) < self.capacity and (len(fastpass_queue) > 0 or len(normal_queue) > 0):
                # FastPass 대기자가 있으면 먼저 탑승시킨다.
                if len(fastpass_queue) > 0:
                    boarding_group.append(fastpass_queue.pop(0))

                # FastPass 대기자가 없으면 일반 대기자를 탑승시킨다.
                elif len(normal_queue) > 0:
                    boarding_group.append(normal_queue.pop(0))

        # 이번 운행에서 탑승할 대기 정보 리스트를 반환한다.
        return boarding_group

    # 예상 탑승 시간을 다시 계산하는 메소드를 선언한다.
    def update_expected_times(self, current_time):
        # 계산용 FastPass 대기열 복사 리스트를 선언한다.
        fastpass_copy = []

        # 계산용 일반 대기열 복사 리스트를 선언한다.
        normal_copy = []

        # FastPass 대기열을 계산용 리스트에 복사한다.
        for i in range(len(self.fastpass_queue)):
            fastpass_copy.append(self.fastpass_queue[i])

        # 일반 대기열을 계산용 리스트에 복사한다.
        for i in range(len(self.normal_queue)):
            normal_copy.append(self.normal_queue[i])

        # 예상 탑승 계산을 시작할 시간을 정한다.
        board_time = self.next_boarding_time

        # 다음 탑승 시간이 현재 시간보다 작으면 현재 시간부터 계산한다.
        if board_time < current_time:
            board_time = current_time

        # 계산용 대기열에 사람이 남아있는 동안 반복한다.
        while len(fastpass_copy) > 0 or len(normal_copy) > 0:
            # 이번 운행에 탑승할 그룹을 구한다.
            boarding_group = self.make_boarding_group(fastpass_copy, normal_copy)

            # 이번 운행에 탑승할 사람들의 예상 탑승 시간을 저장한다.
            for i in range(len(boarding_group)):
                boarding_group[i].expected_time = board_time

            # 다음 운행 시간으로 이동한다.
            board_time = board_time + self.ride_time

    # 특정 대기열에 새로 등록했을 때 예상 탑승 시간을 구하는 메소드를 선언한다.
    def get_expected_time_for_new_waiting(self, current_time, queue_type):
        # 임시 사용자 객체를 생성한다.
        temp_visitor = Visitor("임시사용자", 1)

        # 임시 대기 정보를 생성한다.
        temp_waiting = WaitingInfo(temp_visitor, self.ride_name, queue_type, current_time, 0)

        # 대기 종류에 따라 임시로 대기열에 넣는다.
        if queue_type == "FastPass":
            self.fastpass_queue.append(temp_waiting)
        else:
            self.normal_queue.append(temp_waiting)

        # 예상 탑승 시간을 다시 계산한다.
        self.update_expected_times(current_time)

        # 임시 대기자의 예상 탑승 시간을 저장한다.
        expected_time = temp_waiting.expected_time

        # 임시로 넣었던 대기 정보를 제거한다.
        if queue_type == "FastPass":
            self.fastpass_queue.pop()
        else:
            self.normal_queue.pop()

        # 임시 대기자를 제거했으므로 다시 예상 탑승 시간을 계산한다.
        self.update_expected_times(current_time)

        # 예상 탑승 시간을 반환한다.
        return expected_time

    # 예상 대기 시간을 구하는 메소드를 선언한다.
    def get_wait_time(self, current_time, queue_type):
        # 새로 등록했을 때 예상 탑승 시간을 구한다.
        expected_time = self.get_expected_time_for_new_waiting(current_time, queue_type)

        # 예상 탑승 시간에서 현재 시간을 빼서 대기 시간을 구한다.
        wait_time = expected_time - current_time

        # 예상 대기 시간을 반환한다.
        return wait_time

    # 현재 사용자가 몇 번째로 대기 중인지 확인하는 메소드를 선언한다.
    def get_my_waiting_order(self, visitor):
        # FastPass 대기열에서 현재 사용자를 찾는다.
        for i in range(len(self.fastpass_queue)):
            if self.fastpass_queue[i].visitor == visitor:
                return ["FastPass", i + 1]

        # 일반 대기열에서 현재 사용자를 찾는다.
        for i in range(len(self.normal_queue)):
            if self.normal_queue[i].visitor == visitor:
                return ["일반", i + 1]

        # 대기 중이 아니라면 빈 값을 반환한다.
        return ["", 0]

    # 현재 사용자의 대기 정보 객체를 반환하는 메소드를 선언한다.
    def get_my_waiting_info(self, visitor):
        # FastPass 대기열에서 현재 사용자를 찾는다.
        for i in range(len(self.fastpass_queue)):
            if self.fastpass_queue[i].visitor == visitor:
                return self.fastpass_queue[i]

        # 일반 대기열에서 현재 사용자를 찾는다.
        for i in range(len(self.normal_queue)):
            if self.normal_queue[i].visitor == visitor:
                return self.normal_queue[i]

        # 대기 중이 아니라면 None을 반환한다.
        return None

    # 특정 대기 정보를 대기열에서 제거하는 메소드를 선언한다.
    def remove_waiting_info(self, waiting_info):
        # 일반 대기열에서 해당 대기 정보를 찾는다.
        for i in range(len(self.normal_queue)):
            if self.normal_queue[i] == waiting_info:
                self.normal_queue.pop(i)
                return True

        # FastPass 대기열에서 해당 대기 정보를 찾는다.
        for i in range(len(self.fastpass_queue)):
            if self.fastpass_queue[i] == waiting_info:
                self.fastpass_queue.pop(i)
                return True

        # 제거하지 못했다면 False를 반환한다.
        return False

    # 탑승 시간이 되었을 때 탑승 처리를 하는 메소드를 선언한다.
    def process_boarding(self, current_time):
        # 탑승 처리된 대기 정보를 저장할 리스트를 선언한다.
        boarding_list = []

        # 현재 시간이 다음 탑승 시간 이상이면 운행을 처리한다.
        while current_time >= self.next_boarding_time:
            # 대기자가 없으면 다음 탑승 시간을 현재 시간 + 탑승 시간으로 변경하고 반복을 종료한다.
            if len(self.fastpass_queue) == 0 and len(self.normal_queue) == 0:
                self.next_boarding_time = current_time + self.ride_time
                break

            # 이번 운행의 탑승 시작 시간을 저장한다.
            start_time = self.next_boarding_time

            # 이번 운행에 탑승할 그룹을 구한다.
            boarding_group = self.make_boarding_group(self.fastpass_queue, self.normal_queue)

            # 탑승 확인을 하지 않은 사용자는 다시 대기열 앞쪽에 넣기 위한 리스트를 선언한다.
            not_confirm_list = []

            # 실제 탑승할 사람만 저장할 리스트를 선언한다.
            real_boarding_group = []

            # 탑승 그룹의 길이만큼 반복문을 돌린다.
            for i in range(len(boarding_group)):
                # 현재 순서의 대기 정보를 가져온다.
                waiting_info = boarding_group[i]

                # 탑승 확인이 되어 있으면 실제 탑승 그룹에 추가한다.
                if waiting_info.boarding_confirm == True:
                    real_boarding_group.append(waiting_info)

                # 탑승 확인이 되어 있지 않으면 다시 대기열에 넣을 리스트에 추가한다.
                else:
                    not_confirm_list.append(waiting_info)

            # 탑승 확인이 되지 않은 대기자를 원래 대기열 앞쪽에 다시 넣는다.
            for i in range(len(not_confirm_list)):
                waiting_info = not_confirm_list[i]

                if waiting_info.queue_type == "FastPass":
                    self.fastpass_queue.insert(0, waiting_info)
                else:
                    self.normal_queue.insert(0, waiting_info)

            # 실제 탑승 그룹만 탑승 처리하도록 변경한다.
            boarding_group = real_boarding_group

            # 탑승 그룹의 길이만큼 반복문을 돌린다.
            for i in range(len(boarding_group)):
                # 현재 순서의 대기 정보를 가져온다.
                waiting_info = boarding_group[i]

                # 탑승 종료 시간을 구한다.
                end_time = start_time + self.ride_time

                # 대기 시간을 구한다.
                wait_time = start_time - waiting_info.register_time

                # FastPass로 탑승했다면 FastPass 잔여 횟수를 1 차감한다.
                if waiting_info.queue_type == "FastPass":
                    if waiting_info.visitor.fastpass_count > 0:
                        waiting_info.visitor.fastpass_count = waiting_info.visitor.fastpass_count - 1

                # 탑승 기록 객체를 생성한다.
                record = BoardingRecord(self.ride_name, start_time, end_time, wait_time, waiting_info.queue_type)

                # 사용자의 탑승 기록 리스트에 탑승 기록을 추가한다.
                waiting_info.visitor.add_boarding_record(record)

                # 탑승 처리된 대기 정보를 리스트에 추가한다.
                boarding_list.append(waiting_info)

            # 다음 탑승 시간을 현재 탑승 시간만큼 증가시킨다.
            self.next_boarding_time = self.next_boarding_time + self.ride_time

        # 탑승 처리 후 남은 대기자의 예상 탑승 시간을 다시 계산한다.
        self.update_expected_times(current_time)

        # 탑승 처리된 대기 정보 리스트를 반환한다.
        return boarding_list