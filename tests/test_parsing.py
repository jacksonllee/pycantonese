import pytest

from pycantonese import parse_text


@pytest.mark.parametrize(
    "text, pos_tag_kwargs, participant, expected",
    [
        ("", None, None, ""),
        (None, None, None, ""),
        (
            # The canonical case
            "學廣東話",
            None,
            None,
            (
                "@Begin\n"
                "@Participants:\tX Other\n"
                "*X:\t學 廣東話\n"
                "%mor:\tVERB|hok6 PROPN|gwong2dung1waa2\n"
                "@End\n"
            ),
        ),
        (
            # Custom participant
            "學廣東話",
            None,
            "Foo",
            (
                "@Begin\n"
                "@Participants:\tFoo Other\n"
                "*Foo:\t學 廣東話\n"
                "%mor:\tVERB|hok6 PROPN|gwong2dung1waa2\n"
                "@End\n"
            ),
        ),
        (
            # Unseen "word", so no jyutping in the output
            "135",
            None,
            None,
            (
                "@Begin\n"
                "@Participants:\tX Other\n"
                "*X:\t135\n"
                "%mor:\tX|\n"
                "@End\n"
            ),
        ),
        (
            # Custom POS tagging
            "學廣東話",
            {"tagset": "hkcancor"},
            None,
            (
                "@Begin\n"
                "@Participants:\tX Other\n"
                "*X:\t學 廣東話\n"
                "%mor:\tv|hok6 nz|gwong2dung1waa2\n"
                "@End\n"
            ),
        ),
        (
            # Extra whitespace characters should be ignored
            "學廣東話\n\n\n\n\n\n學廣東話",
            None,
            None,
            (
                "@Begin\n"
                "@Participants:\tX Other\n"
                "*X:\t學 廣東話\n"
                "%mor:\tVERB|hok6 PROPN|gwong2dung1waa2\n"
                "*X:\t學 廣東話\n"
                "%mor:\tVERB|hok6 PROPN|gwong2dung1waa2\n"
                "@End\n"
            ),
        ),
        (
            # Let utterance segmentation do its thing
            "廣東話好難學？都唔係吖！",
            None,
            None,
            (
                "@Begin\n"
                "@Participants:\tX Other\n"
                "*X:\t廣東話 好 難學 ？\n"
                "%mor:\tPROPN|gwong2dung1waa2 ADV|hou2 ADJ|naan4hok6 ？\n"
                "*X:\t都 唔係 吖 ！\n"
                "%mor:\tADV|dou1 VERB|m4hai6 PART|aa1 ！\n"
                "@End\n"
            ),
        ),
        (
            # User-specified utterance segmentation with a list
            ["廣東話好難學？都唔係吖！"],
            None,
            None,
            (
                "@Begin\n"
                "@Participants:\tX Other\n"
                "*X:\t廣東話 好 難學 ？ 都 唔係 吖 ！\n"
                "%mor:\tPROPN|gwong2dung1waa2 ADV|hou2 ADJ|naan4hok6 ？ ADV|dou1 VERB|m4hai6 PART|aa1 ！\n"  # noqa: E501
                "@End\n"
            ),
        ),
        (
            # User-specified utterance segmentation with a list, with an empty utterance
            ["廣東話好難學？都唔係吖！", None],
            None,
            None,
            (
                "@Begin\n"
                "@Participants:\tX Other\n"
                "*X:\t廣東話 好 難學 ？ 都 唔係 吖 ！\n"
                "%mor:\tPROPN|gwong2dung1waa2 ADV|hou2 ADJ|naan4hok6 ？ ADV|dou1 VERB|m4hai6 PART|aa1 ！\n"  # noqa: E501
                "*X:\n"
                "@End\n"
            ),
        ),
        (
            # User-specified participants
            [("小芬", "你食咗飯未呀？"), ("小明", "我食咗喇。")],
            None,
            None,
            (
                "@Begin\n"
                "@Participants:\t小明 Other, 小芬 Other\n"
                "*小芬:\t你 食 咗 飯 未 呀 ？\n"
                "%mor:\tPRON|nei5 VERB|sik6 PART|zo2 NOUN|faan6 ADV|mei6 PART|aa4 ？\n"
                "*小明:\t我 食 咗 喇 。\n"
                "%mor:\tPRON|ngo5 VERB|sik6 PART|zo2 PART|laa3 。\n"
                "@End\n"
            ),
        ),
    ],
)
def test_parse_text(text, pos_tag_kwargs, participant, expected):
    corpus = parse_text(
        text,
        pos_tag_kwargs=pos_tag_kwargs,
        participant=participant,
    )
    actual = "\n".join(corpus.to_strs())
    assert actual == expected
