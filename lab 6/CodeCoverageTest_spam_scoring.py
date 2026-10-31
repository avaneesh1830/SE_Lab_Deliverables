from spam_scoring import classify, filter_inbox, inbox_status, score_message


def test_plain_message_scores_zero():
    assert score_message("hello there", False, 0) == 0


def test_empty_text_scores_zero():
    assert score_message("", False, 0) == 0


def test_spam_word_is_case_insensitive_and_strips_punctuation():
    assert score_message("FREE! prize,", False, 0) == 4


def test_uppercase_word_adds_a_point():
    assert score_message("ALERT", False, 0) == 1


def test_short_uppercase_word_does_not_add_a_point():
    assert score_message("OK", False, 0) == 0


def test_link_count_branches():
    assert score_message("hello", False, 1) == 1
    assert score_message("hello", False, 3) == 1
    assert score_message("hello", False, 4) == 4


def test_known_sender_clamps_negative_score_to_zero():
    assert score_message("FREE!", True, 0) == 0


def test_classify_thresholds():
    assert classify(1) == "clean"
    assert classify(3) == "clean"
    assert classify(4) == "suspicious"
    assert classify(7) == "suspicious"
    assert classify(8) == "spam"


def test_filter_inbox_counts_each_classification():
    messages = [
        ("hello", False, 0),
        ("FREE! prize", False, 0),
        ("FREE! prize urgent cash", False, 0),
    ]
    assert filter_inbox(messages) == {"spam": 1, "suspicious": 1, "clean": 1}


def test_filter_inbox_empty():
    assert filter_inbox([]) == {"spam": 0, "suspicious": 0, "clean": 0}


def test_inbox_status_empty():
    assert inbox_status({"spam": 0, "suspicious": 0, "clean": 0}) == "empty"


def test_inbox_status_spam_ratio_thresholds():
    assert inbox_status({"spam": 1, "suspicious": 0, "clean": 4}) == "healthy"
    assert inbox_status({"spam": 1, "suspicious": 0, "clean": 3}) == "noisy"
    assert inbox_status({"spam": 3, "suspicious": 0, "clean": 2}) == "flooded"
