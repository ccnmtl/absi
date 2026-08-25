GROUP_NAME_PREFIX = 'transcribe_job'


def get_group_name(job_id: str) -> str:
    """
    Get group name based on job id.
    """
    return f'{GROUP_NAME_PREFIX}_{job_id}'


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


def get_ssml_phoneme(arabic_word: str, ipa: str):
    return '<phoneme alphabet="ipa" ph="{ipa}">{s}</phoneme>'.format(
        s=arabic_word, ipa=ipa)


def get_ssml_polly(arabic_word: str, ipa: str) -> str:
    """
    Given an Arabic word, and optionally its IPA notation, return an
    SSML string which can be passed to speech systems.
    """
    if ipa:
        # Strip surrounding slashes in IPA notation.
        ipa = ipa.strip('/')
        ssml = """
        <speak>
            <lang xml:lang="arb">
                {phoneme}
            </lang>
        </speak>
        """.format(phoneme=get_ssml_phoneme(arabic_word, ipa))
    else:
        ssml = """
        <speak>
            <lang xml:lang="arb">{s}</lang>
        </speak>
        """.format(s=arabic_word)

    return ssml


def get_ssml_azure(arabic_word: str, ipa: str, voice: str) -> str:
    """
    Given an Arabic word, and optionally its IPA notation, return an
    SSML string which can be passed to speech systems.

    ar-SA refers to Saudi Arabian Arabic, not Modern Standard Arabic
    (MSA). But I am using this instead of lang="arb" because Microsoft
    only supports these regional voices. In Amazon Polly above, all
    voices are regional as well, but the lang="arb" denotation is
    supported.
    """
    if ipa:
        # Strip surrounding slashes in IPA notation.
        ipa = ipa.strip('/')
        ssml = """
        <speak version="1.0"
               xmlns="http://www.w3.org/2001/10/synthesis"
               xml:lang="ar-SA">
            <voice name="{voice}">
                {phoneme}
            </voice>
        </speak>
        """.format(voice=voice, phoneme=get_ssml_phoneme(arabic_word, ipa))
    else:
        ssml = """
        <speak version="1.0"
               xmlns="http://www.w3.org/2001/10/synthesis"
               xml:lang="ar-SA">
            <voice name="{voice}">
                {s}
            </voice>
        </speak>
        """.format(voice=voice, s=arabic_word)

    return ssml
