import string


def get_clean_text_of_answer(answer_text: str) -> str:
    """Gets the question text cleared of punctuation marks."""
    clean_text_of_answer = answer_text.translate(
        str.maketrans(
            '',
            '',
            string.punctuation,
        ),
    )
    return clean_text_of_answer.strip().lower()
