# Python Markdown Extension: typehint

An extension for [Python-Markdown](https://python-markdown.github.io). Replaces `[@TYPENAME]` text with styled "bubble" with a unique color.

## Example Input

```
## Uppercase

[@ANY]
[@ARRAY]
[@BOOLEAN]
[@CLASS]
[@DATE]
[@ELEMENT]
[@FLOAT]
[@FUNCTION]
[@INT]
[@NUMBER]
[@OBJECT]
[@REGEXP]
[@STRING]

## Title Case

[@Any]
[@Array]
[@Boolean]
[@Class]
[@Date]
[@Element]
[@Float]
[@Function]
[@Int]
[@Number]
[@Object]
[@RegExp]
[@String]

## Lower Case

[@any]
[@array]
[@boolean]
[@class]
[@date]
[@element]
[@float]
[@function]
[@int]
[@number]
[@object]
[@regexp]
[@string]

## Custom

[@any any]
[@array \[\]]
[@boolean true]
[@class MyClass]
[@date myDate]
[@element HTMLElement]
[@float 4.32]
[@function myFunction]
[@int 32]
[@number myNumber]
[@object {}]
[@regexp myRegex]
[@string 'testing']
```

## Example Output

![example_output](docs/images/example_output.png)