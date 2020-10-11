from pycantonese import segment


def test_segment():
    assert segment("廣東話容唔容易學？") == ["廣東話", "容", "唔", "容易", "學", "？"]
