import pytest

from pycantonese import parse_text
from pycantonese.word_segmentation import Segmenter


@pytest.mark.parametrize(
    "text, segment_kwargs, pos_tag_kwargs, participant, expected",
    [
        ("", None, None, None, ""),
        (None, None, None, None, ""),
        (
            # The canonical case
            "學廣東話",
            None,
            None,
            None,
            "*X:    學         廣東話\n%mor:  VERB|hok6  NOUN|gwong2dung1waa2\n",
        ),
        (
            # Custom participant
            "學廣東話",
            None,
            None,
            "Foo",
            "*Foo:  學         廣東話\n%mor:  VERB|hok6  NOUN|gwong2dung1waa2\n",
        ),
        (
            # Unseen "word", so no jyutping in the output
            "135",
            None,
            None,
            None,
            "*X:    135\n%mor:  VERB|\n",
        ),
        (
            # Custom POS tagging
            "學廣東話",
            None,
            {"tagset": "hkcancor"},
            None,
            "*X:    學      廣東話\n%mor:  V|hok6  NG|gwong2dung1waa2\n",
        ),
        (
            # Custom word segmentation
            "學廣東話",
            {"segmenter": Segmenter(disallow={"廣東話"})},
            None,
            None,
            (
                "*X:    學         廣東               話\n"
                "%mor:  VERB|hok6  PROPN|gwong2dung1  VERB|waa6\n"
            ),
        ),
        (
            # Extra whitespace characters should be ignored
            "學廣東話\n\n\n\n\n\n學廣東話",
            None,
            None,
            None,
            (
                "*X:    學         廣東話\n"
                "%mor:  VERB|hok6  NOUN|gwong2dung1waa2\n"
                "*X:    學         廣東話\n"
                "%mor:  VERB|hok6  NOUN|gwong2dung1waa2\n"
            ),
        ),
        (
            # Let utterance segmentation do its thing
            "廣東話好難學？都唔係吖！",
            None,
            None,
            None,
            (
                "*X:    廣東話                 好        難         學         ？\n"
                "%mor:  PROPN|gwong2dung1waa2  ADV|hou2  ADJ|naan4  VERB|hok6  ？\n"
                "*X:    都        唔係         吖        ！\n"
                "%mor:  ADV|dou1  VERB|m4hai6  PART|aa1  ！\n"
            ),
        ),
        (
            # User-specified utterance segmentation with a list
            ["廣東話好難學？都唔係吖！"],
            None,
            None,
            None,
            (
                "*X:    廣東話                 好        難         學         ？  都        唔係         吖        ！\n"  # noqa: E501
                "%mor:  PROPN|gwong2dung1waa2  ADV|hou2  ADJ|naan4  VERB|hok6  ？  ADV|dou1  VERB|m4hai6  PART|aa1  ！\n"  # noqa: E501
            ),
        ),
        (
            # User-specified utterance segmentation with a list, with an empty utterance
            ["廣東話好難學？都唔係吖！", None],
            None,
            None,
            None,
            (
                "*X:    廣東話                 好        難         學         ？  都        唔係         吖        ！\n"  # noqa: E501
                "%mor:  PROPN|gwong2dung1waa2  ADV|hou2  ADJ|naan4  VERB|hok6  ？  ADV|dou1  VERB|m4hai6  PART|aa1  ！\n"  # noqa: E501
                "*X:\t\n"
            ),
        ),
        (
            # User-specified participants
            [("小芬", "你食咗飯未呀？"), ("小明", "我食咗喇。")],
            None,
            None,
            None,
            (
                "*小芬:  你         食         咗        飯          未        呀        ？\n"  # noqa: E501
                "%mor:   PRON|nei5  VERB|sik6  PART|zo2  NOUN|faan6  ADV|mei6  PART|aa4  ？\n"  # noqa: E501
                "*小明:  我         食         咗        喇         。\n"
                "%mor:   PRON|ngo5  VERB|sik6  PART|zo2  PART|laa1  。\n"
            ),
        ),
    ],
)
def test_parse_text(text, segment_kwargs, pos_tag_kwargs, participant, expected):
    corpus = parse_text(
        text,
        segment_kwargs=segment_kwargs,
        pos_tag_kwargs=pos_tag_kwargs,
        participant=participant,
    )
    actual = "\n".join(corpus.to_strs())
    assert actual == expected
