import doctest
import os
import paragraph

doctest.testfile(os.path.join(os.path.dirname(paragraph.__file__),'..',"README.md"))