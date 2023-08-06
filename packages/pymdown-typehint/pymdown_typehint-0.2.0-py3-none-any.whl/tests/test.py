import markdown
import os
from ..typehint.typehint import TypeHintExtension

CURRENT_DIR = os.path.abspath( os.path.dirname( __file__ ) )

class TestMarkdown():
	def __init__( self, *args, **kwargs ):

		self.md = markdown.Markdown( extensions = [ TypeHintExtension() ], extension_configs = {} )

		for subdir, dirs, files in os.walk( os.path.join( CURRENT_DIR, 'fixtures' ) ):
			for file in files:
				if ( file.endswith( '.md' ) ):
					self.md.convertFile( input = os.path.join( CURRENT_DIR, 'fixtures', file ), output = os.path.join( CURRENT_DIR, 'fixtures', (file + '.html') ) )

# run test
test = TestMarkdown()