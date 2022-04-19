import django_filters as filters

from .models import *


class  CandidateFilter(filters.FilterSet):
    choices = ['asp.net', 'hack', 'idris', 'sourcepawn', 'nginx', 'matlab', 'lua', 'tcl', 'handlebars', 'dart', 'hcl', 'python', 'ruby', 'plsql', 'groovy', 'jinja', 'codeql', 'io', 'rescript', 'starlark', 'roff', 'mustache', 'php', 'stylus', 'common lisp', 'tsql', 'solidity', 'go', 'rich text format', 'crystal', 'visual basic .net', 'assembly', 'vue', 'thrift', 'verilog', 'standard ml', 'haxe', 'lilypond', 'classic asp', 'maxscript', 'zig', 'scheme', 'julia', 'ejs', 'pug', 'swig', 'v', 'java', 'groff', 'reason', 'basic', 'viml', 'autohotkey', 'vim snippet', 'scala', 'apacheconf', 'openedge abl', 'brainfuck', 'powershell', 'nim', 'c#', 'yacc', 'glsl', 'jupyter notebook', 'less', 'smali', 'webassembly', 'makefile', 'coffeescript', 'tex', 'arduino', 'applescript', 'objective-c++', 'objective-c', 'zephir', 'bicep', 'kotlin', 'clojure', 'r', 'css', 'xslt', 'shaderlab', 'shell', 'javascript', 'perl', 'html', 'dockerfile', 'd', 'svelte', 'sage', 'c++', 'cmake', 'digital command language', 'vba', 'c', 'racket', 'typescript', 'rust', 'elixir', 'ec', 'actionscript', 'scss', 'vim script', 'haskell', 'sass', 'elm', 'f#', 'ocaml', 'batchfile', 'processing', 'cobol', 'emacs lisp', 'swift']
    programming_languages = filters.MultipleChoiceFilter(
        field_name='github_account__programming_languages',
        lookup_expr='icontains',
        conjoined=True,
        choices=[(choice, choice) for choice in choices],
    )
    technologies = filters.CharFilter(field_name='github_account__technologies', lookup_expr='icontains')
    
    class Meta:
        model = Candidate
        fields = ['programming_languages', 'technologies']