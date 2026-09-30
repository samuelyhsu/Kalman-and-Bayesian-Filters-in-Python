import io
import os
import unittest
from unittest.mock import patch

import nb_translate as translation


class TranslationCheckTests(unittest.TestCase):
    def test_matrix_row_separator_loss_is_reported(self):
        source = r'$$\begin{bmatrix}1&0\\0&1\end{bmatrix}$$'
        damaged = source.replace('\\\\', '\\')
        files = {
            os.path.join(translation.SRC, 'sample.ipynb.txt'): source,
            os.path.join(translation.TR, 'sample.ipynb.txt'): damaged,
        }
        def open_sample(path, **kwargs):
            return io.StringIO('=====CELL 0=====\n' + files[path])
        with patch('builtins.open', side_effect=open_sample), \
                patch.object(translation.os.path, 'exists', side_effect=files.__contains__):
            errors, missing = translation.check('sample.ipynb')
        self.assertIn('cell 0: formulas changed', errors)
        self.assertEqual(missing, [])

    def test_formula_value_change_is_detected(self):
        self.assertNotEqual(translation.formulas_of('$x=1$'),
                            translation.formulas_of('$x=2$'))

    def test_formula_reordering_and_trailing_spaces_are_accepted(self):
        self.assertEqual(translation.formulas_of('$x$ and $$ \ny\n$$'),
                         translation.formulas_of('$$\ny\n$$ then $x$'))

    def test_repeated_formula_loss_is_detected(self):
        self.assertNotEqual(translation.formulas_of('$x$ and $x$'),
                            translation.formulas_of('$x$'))

    def test_formula_text_and_command_boundaries_are_preserved(self):
        for source, changed in [(r'$\text{Mean}$', r'$\text{Average}$'),
                                (r'$\alpha x$', r'$\alphax$')]:
            with self.subTest(source=source):
                self.assertNotEqual(translation.formulas_of(source),
                                    translation.formulas_of(changed))

    def test_link_followed_by_prose_has_same_target(self):
        self.assertEqual(translation.urls_of('[article](https://example.org/a)for'),
                         translation.urls_of('[article](https://example.org/a) text'))

    def test_balanced_parentheses_in_url_are_retained(self):
        url = 'https://example.org/a_(b_(c))'
        self.assertEqual(translation.urls_of('[article](' + url + ')for'), [url])

    def test_changed_url_is_detected(self):
        self.assertNotEqual(translation.urls_of('[a](https://example.org/a)'),
                            translation.urls_of('[a](https://example.org/b)'))


if __name__ == '__main__':
    unittest.main()
