import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_add_choice_with_invalid_text():
    question = Question(title='Q1')
    with pytest.raises(Exception):
        question.add_choice('')
    with pytest.raises(Exception):
        question.add_choice('a' * 101)

def test_create_question_with_invalid_points():
    with pytest.raises(Exception):
        Question(title='Q1', points=0)
    with pytest.raises(Exception):
        Question(title='Q2', points=101)

def test_adding_multiple_choices_generates_sequential_ids():
    question = Question(title='Q1')
    choice1 = question.add_choice('C1')
    choice2 = question.add_choice('C2')
    choice3 = question.add_choice('C3')
    assert choice1.id == 1
    assert choice2.id == 2
    assert choice3.id == 3

def test_remove_a_specific_choice():
    question = Question(title='Q1')
    choice1 = question.add_choice('C1')
    choice_to_remove = question.add_choice('C2')

    question.remove_choice_by_id(choice_to_remove.id)

    assert len(question.choices) == 1
    assert question.choices[0].id == choice1.id

def test_remove_non_existent_choice():
    question = Question(title='Q1')
    question.add_choice('C1')
    
    with pytest.raises(Exception):
        question.remove_choice_by_id(99)

def test_remove_all_choices():
    question = Question(title='Q1')
    question.add_choice('C1')
    question.add_choice('C2')
    
    question.remove_all_choices()
    
    assert len(question.choices) == 0

def test_set_multiple_correct_choices():
    question = Question(title='Q1', max_selections=2)
    c1 = question.add_choice('C1')
    c2 = question.add_choice('C2')
    c3 = question.add_choice('C3')

    question.set_correct_choices([c2.id, c3.id])

    assert not c1.is_correct
    assert c2.is_correct
    assert c3.is_correct

def test_correct_selected_choices_with_mixed_answers():
    question = Question(title='Q1', max_selections=3)
    c1_incorrect = question.add_choice('C1')
    c2_correct = question.add_choice('C2', is_correct=True)
    c3_correct = question.add_choice('C3', is_correct=True)

    selected_ids = [c1_incorrect.id, c3_correct.id]
    correctly_selected_ids = question.correct_selected_choices(selected_ids)

    assert correctly_selected_ids == [c3_correct.id]

def test_correct_selected_choices_with_no_correct_answers():
    question = Question(title='Q1')
    c1_incorrect = question.add_choice('C1')
    c2_correct = question.add_choice('C2', is_correct=True)

    selected_ids = [c1_incorrect.id]
    result = question.correct_selected_choices(selected_ids)

    assert len(result) == 0

def test_correct_selected_choices_exceeding_max_selections():
    question = Question(title='Q1', max_selections=1)
    question.add_choice('C1')
    question.add_choice('C2')
    
    with pytest.raises(Exception):
        question.correct_selected_choices([1, 2])