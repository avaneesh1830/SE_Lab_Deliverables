from spam_scoring import score_message


def test_known_sender_reduction_keeps_positive_score():
    # The known-sender adjustment runs, but the score is not clamped at zero.
    assert score_message("FREE! prize", True, 0) == 1
