import random
import time


# 제목을 시각적으로 출력하는 함수
def header(title):
    print("\n" + "#" * 50)
    print(f"{title.center(50)}")
    print("#" * 50 + "\n")
    time.sleep(0.5)

# ============================== 문제 1. 퍼즐 암호 생성 함수 ==============================
class Puzzle:
    def __init__(self, rule, is_real=False):
        self.rule = rule                        # 퍼즐 규칙 (예: fibonacci, square 등)
        self.is_real = is_real                  # 이 퍼즐이 진짜 암호인지 여부
        self.password = self.generate_password()# 규칙에 따라 암호 생성
        self.hint_stage = 0                     # 힌트 단계 (0부터 시작)
        self.revealed_indices = set([0])        # 공개된 문자 인덱스 (처음엔 첫 글자만 공개)


    # 규칙에 따라 암호 문자열 생성, 처음 숫자 랜덤하게 생성
    def generate_password(self):
        ##### 퍼즐의 규칙에 따라 비밀번호(숫자 문자열)를 생성하세요. #####
        ##### 퍼즐의 규칙은 예시에 있는 걸 해도 되고 자유롭게 만들어도 됩니다. 창의성을 보여주세요! #####
        ##### 비밀번호는 매번 달라져야 합니다. #####
        
        # 암호 길이를 5~7 사이로 무작위로 설정
        length = random.randint(5, 7)
        # 수열의 시작 숫자도 무작위 설정(1~10 사이)
        start = random.randint(1, 10)

        # 퍼즐 규칙에 따라 서로 다른 방식으로 숫자 수열 생성
        if self.rule == "even":
            # 짝수 수열: 시작 숫자의 2배부터 시작해 2씩 증가
            order = [start * 2 + i * 2 for i in range(length)]
        elif self.rule == "fibonacci":
            # 피보나치 수열: 앞 두 수의 합으로 다음 수 생성
            a, b = start, start + 1
            order = [a, b]
            while len(order) < length:
                length.append(order[-1] + order[-2])
        elif self.rule == "square":
            # 제곱근 수열: (start + i)의 제곱값 생성
            order = [(start + i) ** 2 for i in range(length)] 
        elif self.rule == "real": 
            # 진짜 복구 암호: 규칙이 없는 무작위 숫자 나열
            order = [random.randint(0, 9) for _ in range(length)]
        else:
            # 정의도지 않은 규칙일 경우 예외 처리: 무작위 숫자열
            order = [random.randint(0,9) for _ in range(length)] 

        # 숫자 리스트를 문자열로 이어붙여 최종 암호 생성
        return ''.join(str(n) for n in order)          



    # ============================== 문제 2. 힌트 제공 함수 ==============================
    def get_hint(self):
        ##### 힌트 단계를 1 증가시키고, 규칙에 맞는 힌트를 반환하세요. #####
        ##### 힌트는 규칙별로 최대 3단계까지 존재합니다. #####
        
        # 힌트 단계를 1 올립니다.(최대 3까지만 증가)
        if self.hint_stage <= 3:
            self.hint_stage += 1

        # 퍼즐 규칙에 따른 힌트 반환
        if self.rule == "even":
            if self.hint_stage == 1:
                return "수열이 전부 짝수네요."
            elif self.hint_stage == 2:
                return "2씩 증가하고 있습니다."
            elif self.hint_stage == 3:
                return "예: 2, 4, 6, 8, 10의 흐름입니다."
            
        elif self.rule == "fibonacci":
            if self.hint_stage == 1:
                return "수들이 일정한 규칙으로 증가해요."
            elif self.hint_stage == 2:
                return "앞의 두 수를 더하면 다음 수가 됩니다."
            elif self.hint_stage == 3:
                return "예: 1,2,3,5,8,13처럼요."
            
        elif self.rule == "square":
            if self.hint_stage == 1:
                return "수들이 꽤 크게 증가합니다."
            elif self.hint_stage == 2:
                return "어떤 수들을 제곱한 값들이에요."
            elif self.hint_stage >= 3:
                return "예: 1,4,9 처럼요."

        elif self.rule == "real":
            if self.hint_stage == 1:
                return "규칙이 잘 보이지 않습니다..."
            elif self.hint_stage == 2:
                return "여러 숫자가 혼합된 것 같습니다."   
            elif self.hint_stage == 3:
                return "무작위로 보이는 숫자들의 나열입니다."

        # 힌트
        return "특정한 패턴이 있는 것 같아요."

    # ============================== 문제 3. 랜덤한 인덱스 공개 ==============================
    def reveal_random(self):
        ##### 아직 공개되지 않은 인덱스를 찾아서, 그 중 하나를 무작위로 선택해 공개하세요. #####
        
        # 아직 공개되지 않은 인덱스 찾기
        hidden_indices = [i for i in range(len(self.password)) if i not in self.revealed_indices]

        # 숨겨진 인덱스가 존재할 경우
        if hidden_indices:
            # 그 중 하나를 무작위로 선택하여 공개 리스트에 추가
            index_to_reveal = random.choice(hidden_indices)
            self.revealed_indices.add(index_to_reveal)

    # 공개된 인덱스를 제외한 부분을 *로 마스킹하여 반환
    def get_masked_password(self):
        return ''.join(
            self.password[i] if i in self.revealed_indices else '*'
            for i in range(len(self.password))
        )

# ============================== 문제 4. 플레이어 생성 ==============================
class Player:
    def __init__(self, name):
        ##### 플레이어 이름(name)과 체력(lives)을 초기화하세요. 체력은 3으로 시작합니다. #####
        
        self.name = name.strip()
        self.lives = 3

# ============================== 문제 5. 게임 초기화 ==============================
class ForensicGame:
    def __init__(self):
        ##### 게임 시작 시 필요한 요소들을 초기화하세요. #####
        ##### 퍼즐 리스트(puzzles), 이미 푼 퍼즐 인덱스(solved_indices), 진짜 암호의 인덱스(real_answer_index), 플레이어(player), 퍼즐 초기화 함수 호출 #####
        
        # 플레이어는 show_intro에서 입력받고 이후 설정됨
        self.player = None

        # 퍼즐 리스트와 이미 푼 퍼즐 목록
        self.puzzles = []
        self.solved_indices = set()

        # 진짜 복구 암호 퍼즐의 인덱스를 무작위로 설정
        self.real_answer_index = random.randint(0,3)

        # 퍼즐 초기화 함수 호출
        self.init_puzzles()

    # ============================== 문제 6. 퍼즐 초기화 함수 ==============================
    def init_puzzles(self):
        ##### 퍼즐 4개를 랜덤한 규칙으로 생성하세요. #####
        ##### 정답에 해당하는 퍼즐만 is_real=True로 설정하세요. #####
        
        possible_rules = ["even", "fibonacci", "square"]
        random.shuffle(possible_rules)

        for i in range(4):
            if i == self.real_answer_index:
                # 진짜 복구 암호: is_real= True, 규칙은 "real"
                puzzle = Puzzle(rule="real", is_real=True)

            else:
                # 나머지 퍼즐은 규칙 기반 가짜 암호
                rule = possible_rules[i % len(possible_rules)]
                puzzle = Puzzle(rule=rule, is_real=False)

            self.puzzles.append(puzzle)
            
    #show_intro인트로 추가
    def show_intro(self):
        header("디지털 포렌식 암호 추적자")
    
        # 오프닝 시나리오
        print("피로그래밍 23기 해커톤이 한창 진행 중이던 어느 날...")
        time.sleep(1.0)
        print("한 참가자의 노트북 화면이 갑자기 이상한 숫자 암호로 뒤덮였습니다.")
        time.sleep(1.0)
        print("“이건 단순한 버그가 아니야…” 누군가 시스템에 침투한 흔적.")
        time.sleep(1.0)
        print("해커톤 시스템을 해킹하려는 의도적인 암호 공격!")
        time.sleep(1.0)
        print("복구의 실마리는 단 4개의 숫자 퍼즐.")
        time.sleep(1.0)
        print("하지만, 이 중 진짜 암호키는 단 하나.")
        time.sleep(1.0)
        print("시간은 많지 않습니다... 시스템이 완전히 무너지기 전에 복구 키를 찾아야 합니다.")
        time.sleep(1.0)
        print("당신은 이 해커톤의 마지막 희망, 디지털 보안 분석가.")
        time.sleep(1.0)
        print("당신의 임무는 단 하나 — 퍼즐 속 숫자 패턴을 해독하고, 진짜 암호를 밝혀내는 것!\n")
        time.sleep(1.0)
        
        print(" 게임 규칙 안내")
        time.sleep(0.8)
        print("- 퍼즐은 총 4개로 구성되어 있습니다.")
        time.sleep(1.0)
        print("- 단, 그 중 단 하나만이 해킹을 푸는 진짜 암호입니다.")
        time.sleep(1.0)
        print("- 나머지 퍼즐도 풀 수는 있지만 점수만 얻고 사건 해결은 불가능합니다.")
        time.sleep(1.0)
        print("- 플레이어는 체력이 3이며, 암호 입력에 실패할 때마다 1씩 감소합니다.")
        time.sleep(1.0)
        print("- 퍼즐을 선택하면 첫 글자만 공개되며, 틀릴 때마다 추가로 글자가 공개됩니다.")
        time.sleep(1.0)
        print("- 힌트는 최대 3단계까지 주어집니다.\n")
        time.sleep(1.0)
    
        # 탐정 이름 입력
        print("이제, 분석가님의 이름을 입력해주세요.")
        time.sleep(0.5)
        # ============================== 문제 7. 이름 입력 받기 ==============================
        ##### 사용자로부터 탐정 이름을 입력받고, 입력 시 양 옆에 공백을 제거하여 저장하세요. #####
        
        self.detective_namee = input("탐정 이름: ").strip()
        print(f"\n{self.detective_name} 분석가님, 당신의 두뇌와 직감이 이 해커톤을 구할 열쇠입니다!\n")
        time.sleep(1.0)

    # 아직 시도하지 않은 퍼즐 목록 출력
    def display_choices(self):
        print("\n 선택 가능한 암호 퍼즐 목록:")
        for i, puzzle in enumerate(self.puzzles):
            # ============================== 문제 8. 푼 퍼즐 제외 출력 ==============================
            ##### 이미 푼 퍼즐(i in self.solved_indices)은 제외하고 출력하세요. #####
            
            # 이미 푼 퍼즐은 건너뛴다.
            if i in self.solved_indices:
                continue

            # 퍼즐 rule과 마스킹된 암호 표시
            print(f" [{i + 1}] {puzzle.rule}{puzzle.get_masked_password()}")



    # 사용자로부터 선택 입력 받기
    def choose_puzzle(self):
        while True:
            try:
                choice = int(input("\n풀 퍼즐 번호를 선택하세요: ")) - 1
                if choice < 0 or choice >= len(self.puzzles):
                    raise ValueError
                return choice
            except ValueError:
                print("올바른 번호를 입력하세요.")

    # 선택한 퍼즐을 실제로 플레이 (정답 입력 받고 피드백 제공)
    def play_puzzle(self, index):
        puzzle = self.puzzles[index]
        header(f"{index + 1}번 퍼즐 도전!")
        print(f"첫 힌트: {puzzle.get_hint()}")

        # ============================== 문제 9. 시도 횟수 & 체력 처리 ==============================
        ##### 퍼즐 시도 횟수를 3으로 설정하고, 오답일 경우 체력을 감소시키세요. #####
        
        attempts = 3 

        while attempts > 0:
            guess = input("암호를 입력하세요: ").strip().upper()
            if guess == puzzle.password:
                print("정답입니다!")
                time.sleep(1.0)
                if puzzle.is_real:
                    header("암호 해독 성공!")
                    print(f"진짜 암호는 바로 {puzzle.password} 이었습니다.")
                    time.sleep(1.0)
                    print("시스템 복구 키 입력 완료")
                    time.sleep(1.0)
                    print("데이터 복원 진행 중...  ")
                    time.sleep(1.0)
                    print("해킹 시도 차단 완료")
                    time.sleep(1.0)
                    print("당신의 판단력과 추리력, 그리고 끈기가 이번 해킹 시도를 막아냈습니다.")
                    time.sleep(1.0)
                    return True  # 게임 종료
                else:
                    print("이 퍼즐은 진짜 암호가 아니었습니다... 하지만 해독 성공!")
                    time.sleep(1.0)
                    break
            else:
                attempts -= 1
                puzzle.reveal_random()
                print(f"오답입니다. 남은 시도: {attempts}")
                time.sleep(1.0)
                if puzzle.hint_stage < 3:
                    print(f"추가 힌트: {puzzle.get_hint()}")
                print(f"현재 상태: {puzzle.get_masked_password()}")

        ##### 만약 남은 기회가가 0이 되면 체력을 1 줄이고, 플레이어의 체력이 0이면 게임 오버를 출력하세요. #####
        
        # 시도 모두 실패한 경우
        if attempts == 0:
            self.player.lives -= 1
            print(f"\n 퍼즐 실패! 남은 생명: {self.player.lives}")
            print(f"퍼즐의 답은 {puzzle.password} 였습니다.\n")
            time.sleep(1.0)

            # 체력이 0이 되면 게임 오버 처리
            if self.player.lives == 0:
                header("게임 오버")
                print("체력을 모두 소진했습니다. game over!...\n")
                print(f"진짜 암호는: {self.puzzles[self.real_answer_index].password}")
                return True
            

        self.solved_indices.add(index)
        return False  # 계속 진행


    # 전체 게임 실행 루프
    def play(self):
        self.show_intro()
        self.player = Player(self.detective_name)
        
        print("""
---------------------------------------------------------------------------------------------------------------------
  _______      ___      .___  ___.  _______            _______..___________.     ___      .______      .___________.
 /  _____|    /   \\     |   \\/   | |   ____|          /       ||           |    /   \\     |   _  \\     |           |
|  |  __     /  ^  \\    |  \\  /  | |  |__            |   (----``---|  |----`   /  ^  \\    |  |_)  |    `---|  |----`
|  | |_ |   /  /_\\  \\   |  |\\/|  | |   __|            \\   \\        |  |       /  /_\\  \\   |      /         |  |     
|  |__| |  /  _____  \\  |  |  |  | |  |____       .----)   |       |  |      /  _____  \\  |  |\\  \\----.    |  |     
 \\______| /__/     \\__\\ |__|  |__| |_______|      |_______/        |__|     /__/     \\__\\ | _| `._____|    |__|     
      
---------------------------------------------------------------------------------------------------------------------      
                                                                                                                    
""")


        while True:
            if len(self.solved_indices) == len(self.puzzles):
                print("\n모든 퍼즐을 시도했지만 진짜 암호는 해독하지 못했습니다.")
                time.sleep(1.0)
                print(f"진짜 암호는: {self.puzzles[self.real_answer_index].password}")
                break

            self.display_choices()
            index = self.choose_puzzle()
            game_over = self.play_puzzle(index)
            if game_over:
                # 게임 재시작 여부 확인
                self.ask_restart()
                break
                
    def ask_restart(self):
        print()
        retry = input("게임을 다시 시작하시겠습니까? (네/아니오): ").strip()
        if retry == "네":
            # ============================== 문제 10. 게임 재시작 처리 ==============================
            ##### 게임을 재시작하려면 self를 초기화하고, 다시 play()를 호출해야 합니다. #####
            
            self.__init__()
            self.play()
        else:
            print("게임을 종료합니다. 감사합니다!")



# 실행부: 게임 시작
if __name__ == "__main__":
    game = ForensicGame()
    game.play()


