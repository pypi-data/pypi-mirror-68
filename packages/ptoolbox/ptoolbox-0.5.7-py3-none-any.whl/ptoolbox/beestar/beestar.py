# coding=utf-8
import copy
import logging

__author__ = 'ThucNC'

import configparser
import os
import time
from typing import List

import requests
from bs4 import BeautifulSoup, NavigableString
from ptoolbox.helpers.clog import CLog
from ptoolbox.models.question import Question, QuestionOption, QuestionType

_logger = logging.getLogger(__name__)


def strip_br(s):
    while s.strip().endswith("<br/>"):
        s = s.strip()[:-5]
    return s.strip()


class Beestar:
    def __init__(self):
        self.username = None
        self.csrf_token = None
        self.s = requests.session()
        self._headers = {
            'host': 'beestar.org',
            'origin': 'https://beestar.org',
            'referer': 'https://beestar.org/user?cmd=getLogin',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/70.0.3538.77 Safari/537.36',
        }

    def login(self, username, password):
        """
        login, return student list
        [
            (id, email, name, url),
            (id, email, name, url),
        ]
        :param username:
        :param password:
        :return:
        """
        login_url = "https://beestar.org/user?cmd=login"

        headers = copy.deepcopy(self._headers)
        data = {
            "loginID": username,
            "password": password,
            "Login": ""
        }
        r = self.s.post(login_url, headers=headers, data=data)

        print(r.status_code)
        # print(r.headers)
        # print(r.text)

        soup = BeautifulSoup(r.text, 'html.parser')
        students = soup.select("table.edgeblue tr")
        if students:
            titles = students[0].select("td")
            if len(titles) == 4 and titles[1].text == "Student":
                CLog.info(f"Found {len(students)-1} students: ")
                res = []
                for student in students[1:]:
                    # print(student)
                    tds = student.select("td")
                    a_tag = tds[1].select("a")[0]
                    res.append((tds[2].text, tds[3].text, a_tag.text, "https://beestar.org" + a_tag['href']))
                return res

        CLog.error("Login failed!")
        return []

    @staticmethod
    def read_credential(credential_file):
        config = configparser.ConfigParser()
        config.read(credential_file)
        if not config.has_section('BEESTAR'):
            CLog.error(f'Section `BEESTAR` should exist in {credential_file} file')
            return None
        if not config.has_option('BEESTAR', 'cookie'):
            CLog.error(f'cookie are missing in {credential_file} file')
            return None

        return config.get('BEESTAR', 'cookie')

    def login_by_cookie(self, cookie):
        self._headers['cookie'] = cookie

    def get_review_detail(self, review_url, output_folder):
        CLog.info(f"Getting quiz {review_url}")
        headers = copy.deepcopy(self._headers)
        r = self.s.get(review_url, headers=headers)
        # print(r.status_code)
        # print(r.headers)
        # print(r.text)

        test_url = "https://beestar.org/exam?cmd=reviewresult"
        r = self.s.get(test_url, headers=headers)
        # print(r.status_code)
        # print(r.headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        body = soup.select("body")[0]

        centers = soup.select("center")
        title = centers[0].select("h2")[0]
        CLog.warn(f"Got quiz: {title.text}")
        file_name = "-".join(title.text.lower().replace(":", "").replace(",", "").replace(".", "").split())

        centers[0].replaceWith(title)
        centers[-1].decompose()

        scripts = soup.select("script")
        for script in scripts:
            script.decompose()

        bookmarks = soup.select("span.bm")
        for bookmark in bookmarks:
            bookmark.decompose()

        inputs = soup.select("input")
        for input_tag in inputs:
            input_tag.decompose()

        body.attrs = {}
        imgs = soup.select("image")
        for img in imgs:
            if "white_diam.gif" in img['src']:
                img.decompose()
            elif "or_diam.gif" in img['src']:
                img['src'] = "https://beestar.org/images/or_diam.gif"

        with_ans = soup.prettify()

        imgs = soup.select("image")
        for img in imgs:
            if "diam.gif" in img['src']:
                img.decompose()

        fonts = soup.select("font")
        for font in fonts:
            if font['size'] == "2":
                font.decompose()

        without_ans = soup.prettify()

        output_file = os.path.join(output_folder, file_name + ".html")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(without_ans)
        out_file_with_ans = os.path.join(output_folder, file_name + "_ans.html")
        with open(out_file_with_ans, "w", encoding="utf-8") as f:
            f.write(with_ans)

        return without_ans, with_ans

    @staticmethod
    def read_quiz_from_file(html_file_with_ans) -> (str, List[Question]):
        CLog.info(f"Reading beestar quiz from file {html_file_with_ans}")
        questions = []
        with open(html_file_with_ans, "r") as f:
            quiz_html = f.read()
            soup = BeautifulSoup(quiz_html, 'html.parser')
            title = soup.select("h2")[0].text.strip()
            CLog.info(f"Quiz title: {title}")
            hr_tags = soup.select("hr")  # mỗi hr là một nhóm câu hỏi
            for hr_tag in hr_tags:
                next_tag = hr_tag.next_sibling
                hr_tag.extract()
                question_soup = BeautifulSoup("", 'html.parser')
                while next_tag and next_tag.name != 'hr':
                    if next_tag:
                        question_soup.append(copy.copy(next_tag))
                    # print(next_tag)
                    tmp = next_tag
                    next_tag = next_tag.next_sibling
                    tmp.extract()
                if question_soup.select("b"):
                    # print("Question:", question_soup.prettify())
                    question_number_tags = []
                    for b_tag in question_soup.select("b"):
                        s = b_tag.text.strip()
                        if s.endswith('.') and s[:-1].isdigit() and 1 <= int(s[:-1]) <= 10:
                            # b_tag.decompose()
                            question_number_tags.append(b_tag)
                    if len(question_number_tags) <= 1:
                        questions.append(Beestar.parse_question(question_soup))
                    else:
                        CLog.warn("Multiple questions found!")
                        a_question_soup = BeautifulSoup("", 'html.parser')
                        for child in question_soup.children:
                            # print("child", child)
                            if child in question_number_tags[1:]:
                                questions.append(Beestar.parse_question(a_question_soup))
                                # print("HOHOOH", a_question_soup.decode_contents())
                                # print("HOHOOH HOHO")
                                a_question_soup = BeautifulSoup("", 'html.parser')

                            a_question_soup.append(copy.copy(child))
                        questions.append(Beestar.parse_question(a_question_soup))
                        # print("HOHOOH", a_question_soup.decode_contents())
                        # print("HOHOOH HOHO")
        CLog.info("Done")
        return title, questions

    @staticmethod
    def parse_question(question_soup) -> Question:
        """
        parse một nhóm câu hỏi ngăn cách bởi <hr/>
        :param question_soup:
        :return:
        """
        # print("Question: ", question_soup)
        for p_tag in question_soup.select("p"):
            if not p_tag.text.strip():
                p_tag.decompose()

        solution = None
        for solution_tag in question_soup.select("font"):
            if solution_tag['size'] == "2":
                solution = solution_tag.decode_contents().strip()
                solution_tag.decompose()
                break

        options = []
        to_be_extracted = []
        for b_tag in question_soup.select("b"):
            if b_tag.text.strip() in ["A.", "B.", "C.", "D.", "E.", "F."]:
                is_correct = False
                if b_tag.previous_sibling.name == "image" or b_tag.previous_sibling.previous_sibling.name == "image":
                    # and "or_diam.gif" in next_tag["src"]:
                    if b_tag.previous_sibling.name == "image":
                        b_tag.previous_sibling.decompose()
                    else:
                        b_tag.previous_sibling.previous_sibling.decompose()
                    is_correct = True

                option_soup = BeautifulSoup("", 'html.parser')
                for next_sib in b_tag.next_siblings:
                    if next_sib.name == 'b' and next_sib.text.strip() in ["A.", "B.", "C.", "D.", "E.", "F."]:
                        break
                    if next_sib.name != "image":
                        option_soup.append(copy.copy(next_sib))
                        to_be_extracted.append(next_sib)

                # next_tag = b_tag.next_sibling
                # next_tag.extract()
                #
                # option_soup = BeautifulSoup("", 'html.parser')
                # while next_tag and not (next_tag.name == 'b'
                #                         and next_tag.text.strip() in ["A.", "B.", "C.", "D.", "E.", "F."]):
                #     print("next sibling:", next_tag)
                #     option_soup.append(copy.copy(next_tag))
                #     tmp = next_tag
                #     next_tag = next_tag.next_sibling
                #     tmp.extract()
                b_tag.extract()

                # print("Option found", option_soup.decode_contents().strip(), is_correct)
                options.append(QuestionOption(content=strip_br(option_soup.decode_contents().strip()), is_correct=is_correct))
                print('option', options[-1])

                for tag in to_be_extracted:
                    tag.extract()

        for b_tag in question_soup.select("b"):
            s = b_tag.text.strip()
            if s.endswith('.') and s[:-1].isdigit() and 1 <= int(s[:-1]) <= 10:
                b_tag.decompose()

        # print("Question:", question_soup.prettify())
        # print("Options:", options)
        # print("Solution:", solution)

        question = Question(statement_format="html",
                            statement_language="en",
                            statement=question_soup.decode_contents().strip(),
                            options=options,
                            type=QuestionType.multiple_choice,
                            solution=solution
                            )

        # print("statement:", question.statement)
        return question

    def get_student_quiz_list(self, student):
        student_url = student[3]
        headers = copy.deepcopy(self._headers)
        r = self.s.get(student_url, headers=headers)

        print(r.status_code)
        # print(r.headers)
        # print(r.text)

        soup = BeautifulSoup(r.text, 'html.parser')
        quiz_tags = soup.select("a")
        quizzes = []
        for quiz_tag in quiz_tags:
            href = quiz_tag['href']
            if "startexerciseconfirm" in href:
                quizzes.append("https://beestar.org" + href)

        return quizzes

    def start_exercise(self, quiz_url):
        CLog.info(f"Starting quiz {quiz_url}")
        headers = copy.deepcopy(self._headers)
        r = self.s.get(quiz_url, headers=headers)
        # print(r.status_code)
        # print(r.headers)
        # print(r.text)

        test_url = "https://beestar.org/exam?cmd=startexercise&status=NSTART"
        r = self.s.get(test_url, headers=headers)
        print(r.status_code)
        # print(r.headers)
        print("Start exercise:")
        # print(r.text)
        soup = BeautifulSoup(r.text, 'html.parser')
        input_tags = soup.select("form input")

        cmd = exam_id = student_id = start_dt = em_type = trace_num = submitExam = ""
        for input_tag in input_tags:
            if input_tag["name"] == "cmd":
                cmd = input_tag["value"]
            if input_tag["name"] == "exam_id":
                exam_id = input_tag["value"]
            if input_tag["name"] == "student_id":
                student_id = input_tag["value"]
            if input_tag["name"] == "start_dt":
                start_dt = input_tag["value"]
            if input_tag["name"] == "em_type":
                em_type = input_tag["value"]
            if input_tag["name"] == "trace_num":
                trace_num = input_tag["value"]
            if input_tag["name"] == "submitExam":
                submitExam = input_tag["value"]

        submit_url = "https://beestar.org/exam"

        data = {
            "cmd": cmd,
            "submitExam": submitExam,
            "exam_id": exam_id,
            "student_id": student_id,
            "start_dt": start_dt,
            "em_type": em_type,
            "trace_num": trace_num

        }
        print(data)
        r = self.s.post(submit_url, headers=headers, data=data)

        print(r.status_code)
        print(r.headers)
        # print(r.text)

    def get_all_quizzes(self, username, password, output_folder):
        students = self.login(username, password)
        if not students:
            return []

        for student in students:
            CLog.warn(f"Getting quizzes for student {student}")
            quizzes = self.get_student_quiz_list(student)
            for quiz_url in quizzes:
                if "status=FINISH" in quiz_url:
                    # pass
                    self.get_review_detail(quiz_url, output_folder)
                else:
                    CLog.info(
                        f"Exercise not Finished yet. Trying to submit it first before getting result: {quiz_url}...")
                    self.start_exercise(quiz_url)
                    time.sleep(1)
                    self.get_review_detail(quiz_url.replace("status=NSTART", "status=FINISH"), output_folder)
                    # break
            # break


if __name__ == "__main__":
    beestar = Beestar()
    # output_folder = "../../problems/beestar"
    # students = beestar.get_all_quizzes(username="gthuc.nguyen@gmail.com", password="pxnv84",
    #                                    output_folder=output_folder)

    title, quiz = beestar.read_quiz_from_file("../../problems/beestar/beestar-grade-3-math-exercise-results-week-17-ex-1-spring-2020_ans.html")
    for question in quiz:
        print(question)
