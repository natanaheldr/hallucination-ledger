from app.services.claim_extractor import extract_claims, classify_initial_status


class TestClaimExtractor:
    def test_extract_factual_sentences(self):
        text = "The Eiffel Tower was built in 1889. It is the tallest structure in Paris."
        claims = extract_claims(text)
        assert len(claims) == 2
        assert "1889" in claims[0]
        assert "Paris" in claims[1]

    def test_extract_with_dates_and_numbers(self):
        text = "In 2023, over 2 million people visited the museum. The company reported $500 million in revenue."
        claims = extract_claims(text)
        assert len(claims) == 2

    def test_extract_superlative_claims(self):
        text = "Mount Everest is the highest mountain on Earth. It was first climbed in 1953."
        claims = extract_claims(text)
        assert len(claims) == 2

    def test_extract_empty_string(self):
        claims = extract_claims("")
        assert claims == []

    def test_extract_pure_opinion(self):
        text = "I think that movie was great. The pasta tasted delicious. It feels like a nice day."
        claims = extract_claims(text)
        for c in claims:
            assert len(c) > 0

    def test_extract_short_sentences_filtered(self):
        text = "Yes. No. It is."
        claims = extract_claims(text)
        assert len(claims) == 0

    def test_classify_initial_status(self):
        assert classify_initial_status("any text") == "unreviewed"
