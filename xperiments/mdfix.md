Create a Python program to fix markdown files.
Use uv and a src directory layout for the repository.

The program should first assemble all sentences so that each sentence is on its own line.
Then it should remove all trailing spaces.
Then it should use the standard textwrap module to wrap the each sentence to LINEWIDTH characters.
It should translate all tabs to spaces.
It should remove double blank lines, and replace them with a single blank line.
It should ensure that the file ends with a single blank line.
It should translate all non-plain characters to their plain equivalents; for example, round quotes should be converted to straight quotes, and em dashes should be converted to --, etc.
The command line should take one of:
- A directory name
- A file name
- A directory name and a file name
- A directory name and a file name pattern

Use argparse to parse the command line, and add any necessary option flags.
LINEWIDTH and any other configurable options should be in config.py.
