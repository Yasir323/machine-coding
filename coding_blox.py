"""
CODING BLOX

Coding Blox is an Online Coding Platform that allows a user to Sign Up, Create Contests and participate in Contests
hosted by Others.

Each contest can have a level (LOW, MEDIUM, HIGH) and will contain a set of questions.

Each question will have different levels of difficulty(LOW, MEDIUM, HIGH) and score.

Based on the contest level, the question set is going to be decided. Contest level with LOW difficulty will have
questions with LOW difficulty level.

Final score will be decided based on the difficulty LEVEL chosen for a contest

Users solve problems and get points based on the difficulty of the problems and after the contests scores of the users
are updated.

You have to design the Coding Blox platform with the following functionalities.

Command : CreateUser <user_name> : Provided a user name register a user with a default score of 1500.
    Eg: CreateUser Ross CreateUser Monica CreateUser Joey CreateUser Chandler

Command: CreateQuestion <difficulty_level> Eg: CreateQuestion “LOW” 10 AutoIncrement QuestionId should be assigned
starting with 1.

Command: ListQuestion <difficulty_level> difficulty_level is optional if nothing is passed it’ll show all the questions.
If difficulty_level is passed then list all the questions with that difficulty level.
    Eg: ListQuestion LOW or ListQuestion

Command : CreateContest <contest_name> <contest_level> <contest_creator_user_name>:
    Eg: CreateContest “diwali_contest” LOW “Ross”. It means Ross is creating a contest with name “diwali_contest”
The contest_creator_user_name will always attend the contest. AutoIncrement ContestId should be assigned starting
with 1. Question list is made independent of the contest and it is decided based on the contest difficulty level.
For eg: If the contest difficulty level is LOW then all questions with LOW difficulty level can be used in the
contest.

Command : ListContest <difficulty_level>: difficulty_level is optional if nothing is passed it’ll show all the contests.
If difficulty_level is passed then list all the contests with that difficulty level.
    Eg: ListContest LOW or ListContest

Command: AttendContest <contest_id>  <user_name> : The contest_creator will attend the contest automatically.
    Eg: AttendContest 1 Monica AttendContest 1 Joey

Command: RunContest <contest_id> <contest_creator_user_name>:
    Eg: RunContest 1 Ross The user who has created the contest can only start the contest.
Question list is made independent of the contest and it is decided based on the contest difficulty level.
For eg: If the contest difficulty level is LOW then all questions with LOW difficulty level can be used in this contest.

It should generate random questions solved by the users based on the contest difficulty level chosen.

“Ross” : 1,3,5
“Monica” : 1,6,3
“Joey” : 2,4,6 Should update User Score based on the score secured according to the Problems solved.
currentContestPoints = Sum of scores of all question solved Final Score should be calculated based on the difficulty
level of contest
For LOW level → newScore = currentScore + (currentContestPoints - 50)

For MEDIUM level → newScore = currentScore + (currentContestPoints - 30)

For HIGH level → newScore = currentScore + (currentContestPoints)

Command : LeaderBoard <sorting order asc/desc> Should display a leaderboard with userIds and Score. Eg: LeaderBoard score desc

“Joey” : 1515
“Ross” : 1485
“Monica” : 1475
Bonus Functionality : Implement a functionality where contest history can be displayed, given a contest id.
Command : ContestHistory <contest_id>: Should display a contest leaderboard with userName, points Secured and questions
solved. Eg: ContestHistory 1

“Joey” : 65 [2,4,6]
“Ross” : 35 [1,3,5]
“Monica”: 25 [1,3,6]
Implement Contest Withdraw functionality where users can withdraw from a contest before the RunContest has executed.
Command: WithdrawContest <contest_id> <username>:
Eg: WithdrawContest 1 “Joey” The user who created the contest can’t withdraw from the contest.

Expectations: Create the sample data yourself. You can put it into a file, test case or main driver program itself.
Code should be demoable. Either by using a main driver program or test cases. Code should be modular. Code should have
basic OO design. Please do not jam in responsibilities of one class into another. Code should be extensible. Wherever
applicable, use interfaces and contracts between different methods. It should be easy to add/remove functionality
without re-writing the entire codebase. Code should handle edge cases properly and fail gracefully. Code should be
legible, readable and DRY.

Guidelines: Please do not access internet for anything EXCEPT syntax You are free to use the language of your choice
All work should be your own.

LLD/leetcode-lld-flipkart-coding-blox
"""
import itertools
from enum import Enum
import random
from typing import List, Dict, Optional, Set, Tuple


class Difficulty(Enum):
    Low = 10
    Medium = 20
    High = 30


class IdGenerator:

    def __init__(self, start: int = 0):
        self.id = start

    def generator(self):
        while True:
            yield self.id
            self.id += 1


class User:
    id_gen = IdGenerator().generator()

    def __init__(self, name: str):
        self.name = name


class Question:
    id_gen = IdGenerator(1).generator()

    def __init__(self, statement: str, difficulty: Difficulty):
        self.id = next(Question.id_gen)
        self.difficulty = difficulty
        self.statement = statement


class Contest:
    id_gen = IdGenerator(1).generator()

    def __init__(self, name: str, difficulty: Difficulty, creator: User):
        self.id = next(Contest.id_gen)
        self.name = name
        self.difficulty = difficulty
        self.creator = creator
        self.participants: Set[User] = {creator}
        self.scores: Dict[User, int] = {}
        self.leaderboard: List[Tuple[str, int, List[int]]] = []  # Fixed length: 10

    def add_participant(self, user: User):
        self.participants.add(user)

    def remove_participant(self, user: User):
        self.participants.remove(user)

    def update_scores(self, solved: Dict[User, List[Question]]):
        all_questions_solved = set(itertools.chain(solved.values()))
        contest_score = len(all_questions_solved) * self.difficulty.value
        sub = 0
        if self.difficulty == Difficulty.Low:
            sub = 50
        elif self.difficulty == Difficulty.Medium:
            sub = 30
        for participant, questions_solved in solved.items():
            score = ((contest_score - sub) + self.difficulty.value) * len(questions_solved)
            if participant in self.participants:
                self.scores[participant] += score
            self.update_leaderboard(score, participant, [ques.id for ques in questions_solved])

    def update_leaderboard(self, score: int, participant: User, questions_solved: List[int]):
        self.leaderboard.append((participant.name, score, questions_solved))
        self.leaderboard = list(sorted(self.leaderboard, key=lambda x: x[1], reverse=True))[:10]


class CodingPlatform:

    def __init__(self):
        self.questions: Dict[int, Question] = {}
        self.contests: Dict[int, Contest] = {}
        self.users: Dict[str, User] = {}

    def create_user(self, username: str) -> Optional[User]:
        if username in self.users:
            print("Username already taken!")
        else:
            user = User(username)
            self.users[username] = user
            return user

    def create_question(self, statement: str, difficulty: Difficulty) -> Question:
        question = Question(statement, difficulty)
        self.questions[question.id] = question
        return question

    def create_contest(self, name: str, difficulty: Difficulty, creator: str) -> Optional[Contest]:
        user = self.users.get(creator)
        if user:
            contest = Contest(name, difficulty, user)
            self.contests[contest.id] = contest
            return contest

    def list_questions(self, difficulty: Optional[Difficulty]) -> List[Question]:
        if difficulty:
            return list(filter(lambda x: x.difficulty == difficulty, self.questions.values()))
        return list(self.questions.values())

    def list_contests(self, difficulty: Optional[Difficulty]) -> List[Contest]:
        if difficulty:
            return list(filter(lambda x: x.difficulty == difficulty, self.contests.values()))
        return list(self.contests.values())

    def attend_contest(self, contest_id: int, user_name: str):
        contest = self.contests.get(contest_id)
        user = self.users.get(user_name)
        if contest and user:
            contest.add_participant(user)

    def withdraw_contest(self, contest_id: int, user_name: str):
        contest = self.contests.get(contest_id)
        user = self.users.get(user_name)
        if contest and user and user.name != contest.creator.name:
            contest.remove_participant(user)

    def run_contest(self, contest_id: int, creator: str, num_questions: Optional[int]):
        # The user who has created the contest can only start the contest
        user = self.users.get(creator)
        if not user:
            print("User not found!")
        else:
            contest = self.contests.get(contest_id)
            if not contest:
                print("Contest not found!")
            else:
                if user != contest.creator:
                    print("You are not authorized to start this contest!")
                else:
                    # Get random questions
                    questions = list(filter(
                        lambda x: x.difficulty == contest.difficulty, self.questions.values()
                    ))
                    if num_questions:
                        questions = questions[:num_questions]
                    random.shuffle(questions)
                    solved = {}
                    for participant in contest.participants:
                        questions_solved_by_participant = random.choices(questions, k=random.randint(0, len(questions)))
                        solved[participant] = questions_solved_by_participant
                    contest.update_scores(solved)


def main():
    user1 = User("John")
    user2 = User("Jane")

    ques1 = Question("What?", Difficulty.Low)
    ques2 = Question("When?", Difficulty.Medium)
    ques3 = Question("How?", Difficulty.High)

    print(ques1.id, ques2.id, ques3.id)


if __name__ == "__main__":
    main()
