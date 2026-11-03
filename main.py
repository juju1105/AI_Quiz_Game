
import json
import os


class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer


class QuizGame:
    def __init__(self):
        self.score = 0
        self.high_score = 0

        self.state_file = "state.json"
        self.quiz_file = "quiz.json"

        self.quizzes = []

        self.load_quizzes()
        self.load_state()

    # JSON 파일에서 퀴즈 읽기
    def load_quizzes(self):
        try:
            with open(self.quiz_file, "r", encoding="utf-8") as file:
                data = json.load(file)

            for item in data:
                quiz = Quiz(
                    item["question"],
                    item["choices"],
                    item["answer"]
                )
                self.quizzes.append(quiz)

            if not self.quizzes:
                print("퀴즈가 없습니다.")

        except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError):
            print("퀴즈 파일을 읽을 수 없습니다.")

    # 최고 점수 읽기
    def load_state(self):
        if not os.path.exists(self.state_file):
            return

        try:
            with open(self.state_file, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.high_score = data.get("high_score", 0)

        except (json.JSONDecodeError, OSError, AttributeError):
            print("저장 파일을 읽을 수 없습니다. 새 기록으로 시작합니다.")
            self.high_score = 0

    # 최고 점수 저장
    def save_state(self):
        data = {
            "high_score": self.high_score
        }

        with open(self.state_file, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    # 메뉴 표시
    def show_menu(self):
        print("\n=== AI Quiz Game ===")
        print("1. 퀴즈 시작")
        print("2. 퀴즈 목록 보기")
        print("3. 점수 확인")
        print("4. 종료")
        print("5. 퀴즈 추가")

    # 메뉴 실행
    def run(self):
        while True:
            self.show_menu()
            choice = input("메뉴를 선택하세요: ").strip()

            if choice == "1":
                self.start_quiz()
            elif choice == "2":
                self.show_quizzes()
            elif choice == "3":
                print("현재 점수:", self.score)
                print("최고 점수:", self.high_score)
            elif choice == "4":
                print("게임을 종료합니다.")
                break
            elif choice == "5":
                self.add_quiz()
            else:
                print("잘못된 입력입니다.")

    # 퀴즈 시작
    def start_quiz(self):
        if not self.quizzes:
            print("실행할 퀴즈가 없습니다.")
            return

        self.score = 0

        for quiz in self.quizzes:
            print("\n" + quiz.question)

            for option in quiz.choices:
                print(option)

            while True:
                answer = input("정답 번호를 입력하세요: ").strip()

                if not answer:
                    print("입력이 비어 있습니다.")
                    continue

                if not answer.isdigit():
                    print("숫자만 입력해주세요.")
                    continue

                answer = int(answer)

                if answer < 1 or answer > len(quiz.choices):
                    print("선택지 범위 안의 숫자를 입력해주세요.")
                    continue

                break

            if answer == quiz.answer:
                print("정답입니다!")
                self.score += 1
            else:
                print("오답입니다.")

        print("\n최종 점수:", self.score, "/", len(self.quizzes))

        if self.score > self.high_score:
            self.high_score = self.score
            self.save_state()
            print("최고 점수가 갱신되었습니다!")

    # 퀴즈 목록 보기
    def show_quizzes(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"{index}. {quiz.question}")

    # 새로운 퀴즈 추가
    def add_quiz(self):
        print("\n=== 퀴즈 추가 ===")

        question = input("문제를 입력하세요: ").strip()

        if not question:
            print("문제는 비워둘 수 없습니다.")
            return

        choices = []

        for i in range(3):
            choice = input(f"{i + 1}번 선택지를 입력하세요: ").strip()

            if not choice:
                print("선택지는 비워둘 수 없습니다.")
                return

            choices.append(f"{i + 1}. {choice}")

        while True:
            answer = input("정답 번호를 입력하세요 (1~3): ").strip()

            if not answer.isdigit():
                print("숫자를 입력해주세요.")
                continue

            answer = int(answer)

            if answer < 1 or answer > 3:
                print("1부터 3까지 입력해주세요.")
                continue

            break

        new_quiz = Quiz(question, choices, answer)
        self.quizzes.append(new_quiz)

        data = []

        for quiz in self.quizzes:
            data.append({
                "question": quiz.question,
                "choices": quiz.choices,
                "answer": quiz.answer
            })

        with open(self.quiz_file, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print("새로운 퀴즈가 추가되었습니다!")


if __name__ == "__main__":
    try:
        game = QuizGame()
        game.run()

    except (KeyboardInterrupt, EOFError):
        print("\n게임을 종료합니다.")
