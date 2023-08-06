
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

import unittest

import re
import os
import os.path
import unicodedata
import logging

from pylatexenc.latexwalker import LatexWalker
from pylatexenc.latex2text import LatexNodes2Text


class TestLatexNodes2Text(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestLatexNodes2Text, self).__init__(*args, **kwargs)
        self.maxDiff = None
    
    def test_basic(self):

        self.assertEqual(
            LatexNodes2Text().nodelist_to_text(LatexWalker(r'\textbf{A}').get_latex_nodes()[0]),
            'A'
        )

        latex = r'''\textit{hi there!} This is {\em an equation}:
\begin{equation}
    x + y i = 0
\end{equation}

where $i$ is the ``imaginary unit.''
'''
        self.assertEqualUpToWhitespace(
            LatexNodes2Text().nodelist_to_text(LatexWalker(latex).get_latex_nodes()[0]),
            u'''hi there! This is an equation:

    x + y i = 0

where i is the “imaginary unit.”
'''
        )
        self.assertEqualUpToWhitespace(
            LatexNodes2Text(math_mode='with-delimiters').nodelist_to_text(LatexWalker(latex).get_latex_nodes()[0]),
            u'''hi there! This is an equation:
\\begin{equation}
    x + y i = 0
\\end{equation}
where $i$ is the “imaginary unit.”
'''
        )

        self.assertEqual(
            LatexNodes2Text().nodelist_to_text(LatexWalker(latex).get_latex_nodes()[0]),
            LatexNodes2Text().latex_to_text(latex)
        )
        
    def test_accents(self):
        self.assertEqual(
            LatexNodes2Text().nodelist_to_text(LatexWalker(r"Fran\c cais").get_latex_nodes()[0]),
            '''Fran\N{LATIN SMALL LETTER C WITH CEDILLA}ais'''
        )
        self.assertEqual(
            LatexNodes2Text().nodelist_to_text(LatexWalker(r"Fr\'en{\'{e}}tique").get_latex_nodes()[0]),
            '''Fr\N{LATIN SMALL LETTER E WITH ACUTE}n\N{LATIN SMALL LETTER E WITH ACUTE}tique'''
        )
        self.assertEqual(
            LatexNodes2Text(math_mode='with-delimiters')
            .nodelist_to_text(LatexWalker(r"$1 \not= 2$").get_latex_nodes()[0]),
            '''$1 {} 2$'''.format(unicodedata.normalize('NFC', "=\N{COMBINING LONG SOLIDUS OVERLAY}"))
        )
        

    def test_keep_braced_groups(self):
        self.assertEqual(
            LatexNodes2Text(keep_braced_groups=True)
            .nodelist_to_text(
                LatexWalker(
                    r"\textit{Voil\`a du texte}. Il est \'{e}crit {en fran{\c{c}}ais}"
                ).get_latex_nodes()[0]
            ),
            '''Voil\N{LATIN SMALL LETTER A WITH GRAVE} du texte. Il est \N{LATIN SMALL LETTER E WITH ACUTE}crit {en fran\N{LATIN SMALL LETTER C WITH CEDILLA}ais}'''
        )

        self.assertEqual(
            LatexNodes2Text(keep_braced_groups=True, keep_braced_groups_minlen=4)
            .nodelist_to_text(LatexWalker(r"A{XYZ}{ABCD}").get_latex_nodes()[0]),
            '''AXYZ{ABCD}'''
        )
        self.assertEqual(
            LatexNodes2Text(keep_braced_groups=True, keep_braced_groups_minlen=0)
            .nodelist_to_text(LatexWalker(r"{A}{XYZ}{ABCD}").get_latex_nodes()[0]),
            '''{A}{XYZ}{ABCD}'''
        )


    def test_spaces_strictlatex(self):

        def do_test(tex, uni, math_mode=None):
            kwargs = {}
            if math_mode is not None:
                kwargs['math_mode'] = math_mode
            self.assertEqual(
                LatexNodes2Text(strict_latex_spaces=True, **kwargs).latex_to_text(tex),
                uni,
                msg="For TeX=r'{}'".format(tex)
            )

        # from https://github.com/phfaist/pylatexenc/issues/11

        from itertools import combinations_with_replacement
        chars = ((r'\"{o} ', 'ö '),
                 (r'{\"o} ', 'ö '),
                 (r'\L ', 'Ł'),
                 (r'{\L} ', 'Ł '),
                 ('u ', 'u '))

        for cc in combinations_with_replacement(chars, 3):
            ttex, uuni = list(zip(*cc))

            tex = ''.join(ttex).strip()
            uni = ''.join(uuni).strip()

            do_test(tex, uni)

        # from https://github.com/phfaist/pylatexenc/issues/15

        do_test(r'$\alpha$ $\beta$ $\gamma$', r'$\alpha$ $\beta$ $\gamma$', math_mode='verbatim')
        do_test(r'$\gamma$ detector', r'$\gamma$ detector', math_mode='verbatim')
        do_test(r'$\gamma$ $\gamma$ coincidence', r'$\gamma$ $\gamma$ coincidence',
                math_mode='verbatim')


    def test_spaces_strictlatex_options(self):

        def do_test(tex, uni, strict_latex_spaces=None, keep_comments=None, **kwargs):
            self.assertEqual(
                LatexNodes2Text(strict_latex_spaces=strict_latex_spaces, keep_comments=keep_comments,
                                **kwargs)
                .latex_to_text(tex, **kwargs),
                uni
            )

        testlatex = r'''{A} {B} \L \AA xyz:
inline math $\alpha\beta \gamma = x + i y$
line with comment % comment here
	  indented line.
\begin{equation}
    \zeta = a + i b
\end{equation}
the end.'''

        do_test(testlatex, r'''ABŁÅ xyz:
inline math αβγ = x + i y
line with comment % comment here
	  indented line.

    ζ = a + i b

the end.''',
                strict_latex_spaces=False, keep_comments=True)
        do_test(testlatex, r'''ABŁÅ xyz:
inline math αβγ = x + i y
line with comment 
	  indented line.

    ζ = a + i b

the end.''',
                strict_latex_spaces=False, keep_comments=False)
        
        do_test(testlatex, r'''ABŁÅ xyz:
inline math αβγ = x + i y
line with comment % comment here
	  indented line.

    ζ = a + i b

the end.''',
                strict_latex_spaces='based-on-source', keep_comments=True)
        do_test(testlatex, r'''ABŁÅ xyz:
inline math αβγ = x + i y
line with comment 
	  indented line.

    ζ = a + i b

the end.''',
                strict_latex_spaces='based-on-source', keep_comments=False)
        
        do_test(testlatex, r'''A B ŁÅxyz:
inline math αβγ = x + i y
line with comment % comment here
	  indented line.

    ζ = a + i b

the end.''',
                strict_latex_spaces='macros', keep_comments=True)
        do_test(testlatex, r'''A B ŁÅxyz:
inline math αβγ = x + i y
line with comment 
	  indented line.

    ζ = a + i b

the end.''',
                strict_latex_spaces='macros', keep_comments=False)
        
        do_test(testlatex, r'''A B ŁÅxyz:
inline math αβγ = x + i y
line with comment % comment here
indented line.

    ζ = a + i b

the end.''',
                strict_latex_spaces='except-in-equations', keep_comments=True)
        do_test(testlatex, r'''A B ŁÅxyz:
inline math αβγ = x + i y
line with comment indented line.

    ζ = a + i b

the end.''',
                strict_latex_spaces='except-in-equations', keep_comments=False)

        do_test(testlatex, r'''A B ŁÅxyz:
inline math αβγ= x + i y
line with comment % comment here
indented line.

    ζ= a + i b

the end.''',
                strict_latex_spaces=True, keep_comments=True)
        do_test(testlatex, r'''A B ŁÅxyz:
inline math αβγ= x + i y
line with comment indented line.

    ζ= a + i b

the end.''',
                strict_latex_spaces=True, keep_comments=False)
        


    def test_spaces_default(self):

        # from https://github.com/phfaist/pylatexenc/issues/11 --- ensure previous behavior

        def do_test(tex, uni):
            self.assertEqual(LatexNodes2Text().latex_to_text(tex), uni,
                             msg="For TeX=r'{}'".format(tex))

        do_test(r'\"{o} \"{o} \"{o}', 'ööö')
        do_test(r'\"{o} \"{o} {\"o}', 'ööö')
        do_test(r'\"{o} \"{o} \L', 'ööŁ')
        do_test(r'\"{o} \"{o} {\L}', 'ööŁ')
        do_test(r'\"{o} \"{o} u', 'öö u')
        do_test(r'\"{o} {\"o} {\"o}', 'ööö')
        do_test(r'\"{o} {\"o} \L', 'ööŁ')
        do_test(r'\"{o} {\"o} {\L}', 'ööŁ')
        do_test(r'\"{o} {\"o} u', 'öö u')
        do_test(r'\"{o} \L \L', 'öŁŁ') #
        do_test(r'\"{o} \L {\L}', 'öŁŁ') #
        do_test(r'\"{o} \L u', 'öŁ u')
        do_test(r'\"{o} {\L} {\L}', 'öŁŁ')
        do_test(r'\"{o} {\L} u', 'öŁ u')
        do_test(r'\"{o} u u', 'ö u u')
        do_test(r'{\"o} {\"o} {\"o}', 'ööö')
        do_test(r'{\"o} {\"o} \L', 'ööŁ')
        do_test(r'{\"o} {\"o} {\L}', 'ööŁ')
        do_test(r'{\"o} {\"o} u', 'öö u')
        do_test(r'{\"o} \L \L', 'öŁŁ') #
        do_test(r'{\"o} \L {\L}', 'öŁŁ') #
        do_test(r'{\"o} \L u', 'öŁ u')
        do_test(r'{\"o} {\L} {\L}', 'öŁŁ')
        do_test(r'{\"o} {\L} u', 'öŁ u')
        do_test(r'{\"o} u u', 'ö u u')
        do_test(r'\L \L \L', 'ŁŁŁ') #
        do_test(r'\L \L {\L}', 'ŁŁŁ') #
        do_test(r'\L \L u', 'ŁŁ u') #
        do_test(r'\L {\L} {\L}', 'ŁŁŁ') #
        do_test(r'\L {\L} u', 'ŁŁ u') #
        do_test(r'\L u u', 'Ł u u')
        do_test(r'{\L} {\L} {\L}', 'ŁŁŁ')
        do_test(r'{\L} {\L} u', 'ŁŁ u')
        do_test(r'{\L} u u', 'Ł u u')
        do_test(r'u u u', 'u u u')




    def test_input(self):
        latex = r'''ABCDEF fdksanfkld safnkd anfklsa

\input{test_input_1.tex}

MORENKFDNSN'''
        correct_text = r'''ABCDEF fdksanfkld safnkd anfklsa

hi there! This is an equation:

    x + y i = 0

where i is the imaginary unit.

MORENKFDNSN'''

        testdir = os.path.realpath(os.path.abspath(os.path.dirname(__file__)))

        l2t = LatexNodes2Text()
        l2t.set_tex_input_directory(testdir)

        output = l2t.nodelist_to_text(LatexWalker(latex).get_latex_nodes()[0])

        self.assertEqualUpToWhitespace(
            output,
            correct_text
        )

        latex = r'''ABCDEF fdksanfkld safnkd anfklsa

\input{test_input_1}

MORENKFDNSN'''

        self.assertEqualUpToWhitespace(
            l2t.nodelist_to_text(LatexWalker(latex).get_latex_nodes()[0]),
            correct_text
        )

        latex = r'''ABCDEF fdksanfkld safnkd anfklsa

\input{../test_input_1}

MORENKFDNSN'''

        correct_text_unsafe = correct_text # as before
        correct_text_safe = r'''ABCDEF fdksanfkld safnkd anfklsa

MORENKFDNSN'''

        # make sure that the \input{} directive failed to include the file.
        l2t = LatexNodes2Text()
        l2t.set_tex_input_directory(os.path.join(testdir, 'dummy'))
        self.assertEqualUpToWhitespace(
            l2t.nodelist_to_text(LatexWalker(latex).get_latex_nodes()[0]),
            correct_text_safe
        )
        # but without the strict_input flag, it can access it.
        l2t.set_tex_input_directory(os.path.join(testdir, 'dummy'), strict_input=False)
        self.assertEqualUpToWhitespace(
            l2t.nodelist_to_text(LatexWalker(latex).get_latex_nodes()[0]),
            correct_text_unsafe
        )


    def test_mathmodes_00(self):
        latex = r"""
If $\alpha=1$ and \(\beta=2\), then
\[
  \beta=2\alpha\ ,
\]
or, equivalently,
$$ \alpha = \frac1{\beta}\ .$$
"""
        correct_text = r"""
If α=1 and β=2, then

    β=2α ,

or, equivalently,

    α = 1/β .

"""
        l2t = LatexNodes2Text(math_mode='text')
        self.assertEqualUpToWhitespace(
            l2t.latex_to_text(latex),
            correct_text
        )

    def test_mathmodes_01(self):
        latex = r"""
If $\alpha=1$ and \(\beta=2\), then
\[
  \beta=2\alpha\ ,
\]
or, equivalently,
$$ \alpha = \frac1{\beta}\ .$$
"""
        correct_text = r"""
If $α=1$ and \(β=2\), then
\[
    β=2α ,
\]
or, equivalently,
$$
    α = 1/β .
$$
"""
        l2t = LatexNodes2Text(math_mode='with-delimiters')
        self.assertEqualUpToWhitespace(
            l2t.latex_to_text(latex),
            correct_text
        )

    def test_mathmodes_02(self):
        latex = r"""
If $\alpha=1$ and \(\beta=2\), then
\[
  \beta=2\alpha\ ,
\]
or, equivalently,
$$ \alpha = \frac1{\beta}\ .$$
"""
        
        l2t = LatexNodes2Text(math_mode='verbatim')
        self.assertEqualUpToWhitespace(
            l2t.latex_to_text(latex),
            latex # math stays verbatim
        )





    def assertEqualUpToWhitespace(self, a, b):
        a2 = re.sub(r'\s+', ' ', a).strip()
        b2 = re.sub(r'\s+', ' ', b).strip()
        self.assertEqual(a2, b2)




if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
#

