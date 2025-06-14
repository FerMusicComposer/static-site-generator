import unittest
import textwrap
from application import *

class TestApplication(unittest.TestCase):
    
    def test_extract_title_extracts_h1_header(self) -> str:
        md = textwrap.dedent("""
        # This Is The Main Title
        
        Some random text     

        ## Subsection
        This is a paragraph of the subsection.
        """)
        title = extract_title(md)
        self.assertEqual(title, "This Is The Main Title")