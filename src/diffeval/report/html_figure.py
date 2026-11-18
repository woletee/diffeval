"""One escaped figure for one sample."""

from html import escape


def html_figure(sample: dict) -> str:
    src = escape(sample["path"], quote=True)
    label = escape(f"seed {sample['seed']}")
    return f'<figure><img src="{src}" alt="{label}"><figcaption>{label}</figcaption></figure>'
