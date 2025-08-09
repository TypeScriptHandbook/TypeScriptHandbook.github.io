Create a Python program to fix markdown files.
Use uv and a src directory layout for the repository.

The program should first break the input file into reformattable and non-reformattable parts.
The non-reformattable parts should be passed through unchanged.
The reformattable parts should be reformatted.
Non-reformattable parts include headers, code blocks, lists, and tables.
Reformattable parts include prose paragraphs.

For each paragraph, assemble all sentences so that each sentence is on its own line.
Then remove all trailing spaces.
Then use the standard textwrap module to wrap the each sentence to LINEWIDTH characters.
Translate all tabs to spaces.
Remove double blank lines, and replace them with a single blank line.
Ensure that the file ends with a single blank line.
Translate all non-plain characters to their plain equivalents; for example, round quotes should be converted to straight quotes, and em dashes should be converted to --, etc.
Normalize multiple spaces within sentences to single spaces

The command line should take one of:
- A directory name
- A file name
- A directory name and a file name
- A directory name and a file name pattern

Use argparse to parse the command line, and add any necessary option flags.
LINEWIDTH and any other configurable options should be in config.py.

Create a test suite using pytest and include it in the repository. Use pytest fixtures to produce easy-to-understand test cases.
