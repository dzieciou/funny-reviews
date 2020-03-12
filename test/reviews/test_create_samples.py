from reviews.create_samples import sample_multiple


def test_sample_multiple():
    sample1, sample2, sample3 = tuple(sample_multiple(10, 3, 2, 4))
    sample1, sample2, sample3 = set(sample1), set(sample2), set(sample3)
    assert len(sample1) + len(sample2) + len(sample3) == 3+2+4
    assert sample1.isdisjoint(sample2)
    assert sample2.isdisjoint(sample3)
    assert sample3.isdisjoint(sample1)
