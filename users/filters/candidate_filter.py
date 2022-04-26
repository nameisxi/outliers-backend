import django_filters as filters

from ..models import *
from technologies.models import ProgrammingLanguage, Technology, Topic


class  CandidateFilter(filters.FilterSet):
    # choices = ['asp.net', 'hack', 'idris', 'sourcepawn', 'nginx', 'matlab', 'lua', 'tcl', 'handlebars', 'dart', 'hcl', 'python', 'ruby', 'plsql', 'groovy', 'jinja', 'codeql', 'io', 'rescript', 'starlark', 'roff', 'mustache', 'php', 'stylus', 'common lisp', 'tsql', 'solidity', 'go', 'rich text format', 'crystal', 'visual basic .net', 'assembly', 'vue', 'thrift', 'verilog', 'standard ml', 'haxe', 'lilypond', 'classic asp', 'maxscript', 'zig', 'scheme', 'julia', 'ejs', 'pug', 'swig', 'v', 'java', 'groff', 'reason', 'basic', 'viml', 'autohotkey', 'vim snippet', 'scala', 'apacheconf', 'openedge abl', 'brainfuck', 'powershell', 'nim', 'c#', 'yacc', 'glsl', 'jupyter notebook', 'less', 'smali', 'webassembly', 'makefile', 'coffeescript', 'tex', 'arduino', 'applescript', 'objective-c++', 'objective-c', 'zephir', 'bicep', 'kotlin', 'clojure', 'r', 'css', 'xslt', 'shaderlab', 'shell', 'javascript', 'perl', 'html', 'dockerfile', 'd', 'svelte', 'sage', 'c++', 'cmake', 'digital command language', 'vba', 'c', 'racket', 'typescript', 'rust', 'elixir', 'ec', 'actionscript', 'scss', 'vim script', 'haskell', 'sass', 'elm', 'f#', 'ocaml', 'batchfile', 'processing', 'cobol', 'emacs lisp', 'swift']
    # programming_languages = filters.MultipleChoiceFilter(
    #     field_name='github_accounts__programming_languages',
    #     lookup_expr='icontains',
    #     conjoined=True,
    #     choices=[(choice, choice) for choice in ProgrammingLanguage.objects.all().distinct('name')],
    # )
    # technologies = filters.CharFilter(field_name='technologies', lookup_expr='icontains')
    
    # class Meta:
    #     model = Candidate
    #     fields = ['programming_languages', 'technologies']
    
    language_choices = [(language, language) for language in ProgrammingLanguage.objects.values_list('name', flat=True).distinct()]
    language_filter = filters.MultipleChoiceFilter(
        field_name='programming_languages__language__name',
        lookup_expr='icontains',
        conjoined=True,
        choices=language_choices,
    )

    class Meta:
        model = Candidate
        exclude = ['work_score', 'popularity_score', 'hireability_score', 'fit_score']
    
    @property
    def qs(self):
        queryset = super().qs
        print("Queryset length:", len(queryset))

    # pass
