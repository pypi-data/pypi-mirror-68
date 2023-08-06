from markdown import Extension
from markdown.inlinepatterns import InlineProcessor
import xml.etree.ElementTree as etree

DEFAULT_COLOR = '#999'
RE_TYPEHINT_INLINE = r'\[@([a-zA-Z]+)\s?([^\]]*)?\]'

def getTypeColor( ty, config ):

	uniformedType = ty.lower()
	found = None
	
	try:
		found = config[ 'types'][0][ uniformedType ]
	except:
		pass

	if ( found is not None ):
		return found
	else:
		return config[ 'default_color' ][0]

def generateTag( innerText, color, config ):

	attributes = {
		'style': "background:%s;"
			"display:inline-block;"
			"padding:.4em .6em;"
			"font-size:75%%;"
			"font-weight:700;"
			"line-height:1;"
			"color:%s;"
			"text-align:center;"
			"white-space:nowrap;"
			"vertical-align:baseline;"
			"border-radius:.25em;"
			% (
				color,
				config[ 'text_color' ][0]
			)
	}

	el = etree.Element( 'span', attributes )
	el.text = innerText

	return el

class TypeHintPattern( InlineProcessor ):
	def __init__( self, pattern, md, config ):

		self.config = config

		InlineProcessor.__init__( self, pattern, md )

	def handleMatch( self, m, data ):

		el = m.group( 0 )

		matchedType = m.group( 1 )
		customText = m.group( 2 )
		innerText = customText if customText else matchedType

		if matchedType:
			el = generateTag( innerText, getTypeColor( matchedType, self.config ), self.config )

		return el, m.start( 0 ), m.end( 0 )

class TypeHintExtension( Extension ):
	def __init__( self, *args, **kwargs ):

		self.config = {
			'text_color': [
				'#FFF',
				'Text color to be used for type hint bubbles'
			],
			'default_color': [
				DEFAULT_COLOR,
				'Default background color for unregistered types'
			],
			'types': [
				{
					'any': DEFAULT_COLOR,
					'array': '#F90',
					'boolean': '#000',
					'class': '#F1C40F',
					'date': '#FFC0CB',
					'element': '#95BD42',
					'float': '#BDC581',
					'function': '#008000',
					'int': '#3F42BD',
					'number': '#BD3F42',
					'object': '#999',
					'regexp': '#D35400',
					'string': '#3A87AD'
				},
				'Dictionary of Types mapped to hex colors'
			]
		}

		super( TypeHintExtension, self ).__init__( *args, **kwargs )
	
	def extendMarkdown( self, md ):

		md.registerExtension( self )
		md.inlinePatterns.register( TypeHintPattern( RE_TYPEHINT_INLINE, md, self.config ), 'typehint', 175 )

def makeExtension( *args, **kwargs ):
	return TypeHintExtension( *args, **kwargs )