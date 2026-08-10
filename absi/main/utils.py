GROUP_NAME = 'transcribe_updates'


def get_word(text: str, idx: int = 0) -> str:
    """
    Split the given piece of text in a fail-safe manner, splitting
    on '-' if a dash is present, otherwise on space.
    """
    if text is None:
        return None

    if '-' in text:
        pair = text.split('-')
    else:
        pair = text.split()

    if len(pair) > idx:
        return pair[idx].strip()
