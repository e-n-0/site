from django.utils.translation import ugettext_lazy as _

from prologin.utils import ChoiceEnum


class LanguageDef:
    """
    Represent a programming language and its properties.
    """
    identity = lambda e: e

    def __init__(self, name, extensions, camisole=None, doc=None, time=identity, memory=identity):
        """
        :param name: the language full, human name
        :param extensions: file extension(s) accepted for this language
        :param camisole: the corresponding camisole language name, if correctable
        :param doc: the documentation name for this language
        :param time: a callable giving the maximum user time limit given the raw user time limit
        :param memory: a callable giving the maximum memory limit given the raw memory limit
        """
        self.name = name
        self.extensions = extensions
        self.doc = doc
        self.camisole_name = camisole
        self.time_limit = time
        self.memory_limit = memory

    def __str__(self):
        return str(self.name)  # force gettext resolution

    def serialize(self):
        return str(self)

    @property
    def correctable(self):
        return self.camisole_name is not None


@ChoiceEnum.sort()
class Language(ChoiceEnum):
    """
    Machine-name (member name, left of equal sign) must be less than
    16 character long.
    """
    c = LanguageDef("C", ['.c'], doc='c',
        camisole='c', memory=lambda m: m * 10 + 1024)
    cpp = LanguageDef("C++", ['.cc', '.c++', '.cpp'], doc='cpp',
        camisole='c++', memory=lambda m: m * 10 + 3000)
    pascal = LanguageDef("Pascal", ['.pas', '.pascal'], doc='pascal',
        camisole='pascal', memory=lambda m: m + 1024)
    ocaml = LanguageDef("OCaml", ['.ml', '.ocaml'], doc='ocaml',
        camisole='ocaml', memory=lambda m: 2 * m + 1024)
    scheme = LanguageDef("Scheme", ['.scm'], doc='scheme',
        camisole='scheme', memory=lambda m: m + 36384, time=lambda t: 3 * t)
    haskell = LanguageDef("Haskell", ['.hs'], doc='haskell',
        camisole='haskell', memory=lambda m: 5 * m + 15000, time=lambda t: 4 * t + 1024)
    java = LanguageDef("Java", ['.java'], doc='java',
        camisole='java', memory=lambda m: 5 * m + 22000, time=lambda t: 4 * t + 36000)
    python2 = LanguageDef("Python 2", ['.py', '.py2'], doc='python2')  # memory=lambda m: 5 * m + 7500, time=lambda t: 15 * t)
    python3 = LanguageDef("Python 3", ['.py3'], doc='python3',
        camisole='python', memory=lambda m: 5 * m + 7500, time=lambda t: 15 * t)
    ada = LanguageDef("Ada", ['.adb'], doc='ada',
        camisole='ada', memory=lambda m: m + 4096)
    php = LanguageDef("PHP", ['.php'], doc='php',
        camisole='php', memory=lambda m: 5 * m + 36384, time=lambda t: 8 * t)
    js = LanguageDef("Javascript", ['.js'],
        camisole='javascript', memory=lambda m: 5 * m + 100000, time=lambda t: 5 * t)
    vb = LanguageDef("Visual Basic", ['.vb'],
        camisole='visualbasic', memory=lambda m: m + 16384, time=lambda t: 2 * t)
    perl = LanguageDef("Perl", ['.pl', '.perl'],
        camisole='perl', memory=lambda m: m + 5000, time=lambda t: 10 * t)
    lua = LanguageDef("Lua", ['.lua'],
        camisole='lua', memory=lambda m: m + 5000, time=lambda t: 10 * t)
    csharp = LanguageDef("C#", ['.cs'],
        camisole='c#', memory=lambda m: m + 16384, time=lambda t: t + 38)
    fsharp = LanguageDef("F#", ['.fs'],
        camisole='f#', memory=lambda m: m + 17408)
    brainfuck = LanguageDef("Brainfuck", ['.bf'],
        camisole='brainfuck', memory=lambda m: 10 * m + 50000, time=lambda t: 8 * t)
    pseudocode = LanguageDef(_("Pseudocode"), ['.txt'])

    def name_display(self):
        return self.value.name

    def extensions(self):
        return self.value.extensions

    def doc(self):
        return self.value.doc

    def correctable(self):
        return self.value.correctable

    def ace_lexer(self):
        return ACE_LEXER_MAPPING.get(self.name, 'text')

    def pygments_lexer(self):
        return PYGMENTS_LEXER_MAPPING.get(self.name, 'text')

    def __str__(self):
        return self.name_display()

    def __repr__(self):
        return '<{}.{}>'.format(self.__class__.__name__, self.name)

    @classmethod
    def guess(cls, obj):
        if isinstance(obj, cls):
            return obj
        if isinstance(obj, LanguageDef):
            return cls(obj)
        # assume string
        obj = obj.lower().strip()
        # some special cases
        obj = {
            'python': 'python2',
            'caml': 'ocaml',
        }.get(obj, obj)
        try:
            # 'cpp', 'PYTHON'
            return cls[obj]
        except KeyError:
            pass
        # try harder
        for lang in cls:
            if lang.name_display().lower() == obj:
                return lang
            if obj in lang.extensions() or '.' + obj in lang.extensions():
                return lang
        return None

    @classmethod
    def _get_choices(cls):
        # We hacked the member values to put LanguageDef-s instead of DB values
        # so we fix this here.
        # (("c", "C"), ("cpp", "C++"), ("csharp", "C#"), …)
        return tuple((member.name, member.name_display()) for member in cls)


ACE_LEXER_MAPPING = {
    'c': 'c_cpp',
    'cpp': 'c_cpp',
    'pascal': 'pascal',
    'ocaml': 'ocaml',
    'scheme': 'scheme',
    'haskell': 'haskell',
    'java': 'java',
    'ada': 'ada',
    'php': 'php',
    'perl': 'perl',
    'lua': 'lua',
    'csharp': 'csharp',
    'python2': 'python',
    'python3': 'python',
    'vb': 'vbscript',
    'js': 'javascript',
}

PYGMENTS_LEXER_MAPPING = {
    'c': 'c',
    'cpp': 'cpp',
    'pascal': 'pascal',
    'ocaml': 'ocaml',
    'scheme': 'scheme',
    'haskell': 'haskell',
    'java': 'java',
    'python2': 'python',
    'python3': 'python',
    'ada': 'ada',
    'php': 'php',
    'js': 'javascript',
    'vb': 'vb.net',
    'perl': 'perl',
    'lua': 'lua',
    'csharp': 'csharp',
    'fsharp': 'fsharp',
    'brainfuck': 'brainfuck',
}
