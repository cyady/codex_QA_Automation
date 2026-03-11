from __future__ import annotations


def _cover_numeric_range(
    start: int,
    end: int,
    width: int,
    prefix: str,
    low: int,
    high: int,
    output: list[str],
) -> None:
    if end < low or high < start:
        return
    if start <= low and high <= end:
        output.append(prefix)
        return
    if len(prefix) == width:
        output.append(prefix)
        return

    step = 10 ** (width - len(prefix) - 1)
    for digit in range(10):
        child_low = low + digit * step
        child_high = child_low + step - 1
        _cover_numeric_range(
            start=start,
            end=end,
            width=width,
            prefix=f"{prefix}{digit}",
            low=child_low,
            high=child_high,
            output=output,
        )


def cover_numeric_range_with_prefixes(
    start: int,
    end: int,
    *,
    width: int,
) -> list[str]:
    if width < 1:
        raise ValueError(f"width must be >= 1: {width}")
    if start < 0 or end < 0:
        raise ValueError(f"range must be >= 0: {start}..{end}")
    if end < start:
        raise ValueError(f"invalid range: {start}..{end}")

    max_value = (10**width) - 1
    if end > max_value:
        raise ValueError(f"end exceeds width {width}: {end} > {max_value}")

    output: list[str] = []
    _cover_numeric_range(
        start=start,
        end=end,
        width=width,
        prefix="",
        low=0,
        high=max_value,
        output=output,
    )
    return output


def build_exact_size_title_prefixes(
    count: int,
    *,
    title_prefix: str,
    number_width: int = 7,
    internal_start: int = 0,
) -> list[str]:
    if count < 1:
        raise ValueError(f"count must be >= 1: {count}")
    if internal_start < 0:
        raise ValueError(f"internal_start must be >= 0: {internal_start}")
    if count < internal_start:
        raise ValueError(f"count must be >= internal_start: {count} < {internal_start}")

    numeric_prefixes = cover_numeric_range_with_prefixes(
        start=internal_start,
        end=count,
        width=number_width,
    )
    return [f"{title_prefix}{prefix}" for prefix in numeric_prefixes]
