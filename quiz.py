from abc import ABCMeta, abstractmethod
from random import shuffle
import itertools



class quiz():

    __metaclass__ = ABCMeta

    newid = itertools.count().next

    def __init__(self):
        self.question = ""
        self.answers = {}
        self.id = quiz.newid()


    @abstractmethod
    def check_answer(self, user_answer):
        return self.check_answer(user_answer)

    @abstractmethod
    def set_answers(self, input_correct_answers, answer_list):
        return self.set_answers(input_correct_answers, answer_list)

    def get_question(self):
        return self.get_question()

    def shuffle_answers(self, unshuffled_answers):
        shuffle(unshuffled_answers)
        question_number = 1
        for q in unshuffled_answers:
            self.answers[question_number] = q
            question_number += 1

    def set_question(self, user_question):
        self.question = user_question


class multipleChoice(quiz):

    def __init__(self):
        super(quiz, self).__init__()
        self.correctAnswer = ""
        self.answer_list = []

    def set_answers(self, input_correct_answer, input_list):
        self.correctAnswer = input_correct_answer
        self.answer_list = [str(answer) for answer in input_list]
        self.answer_list.append(input_correct_answer)

    def check_answer(self, user_answer):
        try:
            intAnswer = int(user_answer)
            if self.answers.get(intAnswer) == self.correctAnswer:
                return True
        except ValueError:
            if user_answer == self.correctAnswer:
                return True

        return False


class checkBox(quiz):

    def __init__(self):
        super(quiz, self).__init__()
        self.correct_answers = []
        self.answer_list = []

    def set_answers(self, input_correct_answers, input_list):
        self.correct_answers = [answer for answer in input_correct_answers]
        self.answer_list = [answer for answer in input_list]
        for answer in self.correct_answers:
            if answer not in self.answer_list:
                self.answer_list.append(answer)

    def check_answer(self, user_answer):
        count = 0
        for answer in user_answer:
            try:
                intAnswer = int(answer)
                if self.answers.get(intAnswer) in self.correct_answers:
                    count += 1
                else:
                    return False

            except ValueError:

                if answer in self.correct_answers:
                    count += 1
                else:
                    return False

        if len(self.correct_answers) == count:
            return True
        else:
            return False


class TrueFalse(quiz):
    def __init__(self):
        super(quiz, self).__init__()
        self.correct_answers = bool

    def set_answers(self, input_correct_answers, answer_list={"1": "True", "2": "False"}):
        if input_correct_answers == "True":
            self.correct_answers = True
        elif input_correct_answers == "False":
            self.correct_answers = False
        else:
            return False

        self.correct_answers = input_correct_answers
        self.answers = answer_list

    def check_answer(self, user_answer):
        if user_answer == "True":
            boolAnswer = True
        elif user_answer == "False":
            boolAnswer = False
        else:
            return False

        return self.correct_answers == boolAnswer


def main():
        check_box_obj = checkBox()
        check_box_obj.set_question("What is your favorite color?")
        check_box_obj.set_answers(["blue", "purple"], ["red", "black", "green"])
        check_box_obj.shuffle_answers(unshuffled_answers=check_box_obj.answer_list)
        print(check_box_obj.question)
        for key, value in check_box_obj.answers.items():
            print(str(key) + '. ' + value)
        print()
        notRightAnswer = True
        while notRightAnswer:
            my_input = input("Enter an answer: ")
            split_input = my_input.split()
            if check_box_obj.check_answer(split_input):
                print("good job")
                notRightAnswer = False
            else:
                print("incorrect")


if __name__ == '__main__':
        main()


