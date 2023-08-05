# coding=utf-8
import logging

__author__ = 'ThucNC'
_logger = logging.getLogger(__name__)


from dataclasses import dataclass, field
from enum import Enum
from typing import List


class QuestionType(Enum):
    multiple_choice = "multiple_choice"
    short_answer = "short_answer"
    long_answer = "long_answer"


@dataclass
class QuestionOption:
    content: str = ""
    # index: str = ""
    # question_id: str = ""
    # option_id: str = ""
    is_correct: bool = False


@dataclass
class Question:
    src_name: str = ""
    src_id: str = ""
    src_index: int = 0
    src_ans_id: str = ""
    src_url: str = ""
    answer: str = ""
    type: QuestionType = QuestionType.short_answer
    src_ans_tag: str = ""
    statement: str = ""
    statement_format: str = "html"  # html | markdown
    statement_language: str = 'en'  # en \ vi
    options: List[QuestionOption] = field(default_factory=list) # for multiple choice question
    solution: str = ""
    tags: List[str] = field(default_factory=list)
