from recatch_recipient_groups.prefixes import (
    build_exact_size_title_prefixes,
    cover_numeric_range_with_prefixes,
)


def test_cover_numeric_range_with_prefixes_for_100000() -> None:
    assert cover_numeric_range_with_prefixes(0, 100000, width=7) == ["00", "0100000"]


def test_cover_numeric_range_with_prefixes_for_500000() -> None:
    assert cover_numeric_range_with_prefixes(0, 500000, width=7) == [
        "00",
        "01",
        "02",
        "03",
        "04",
        "0500000",
    ]


def test_build_exact_size_title_prefixes_adds_title_prefix() -> None:
    assert build_exact_size_title_prefixes(230000, title_prefix="QA_DYN_") == [
        "QA_DYN_00",
        "QA_DYN_01",
        "QA_DYN_020",
        "QA_DYN_021",
        "QA_DYN_022",
        "QA_DYN_0230000",
    ]
