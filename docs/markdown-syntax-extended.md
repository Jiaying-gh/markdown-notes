# Extended

## Tables
### Create Tables
Use three hyphens or more to create the table head and use pipes to create a column.

The following table shows the rendered output.

|Trees |Growth Cycle|
|------|------------|
|Oak   |Annual      |
|Lemon |Semi-annual |

### Align Columns
To align columns to the left, right, or center, add the colon ":" to the left, right, or on both sides of the hyphen.

|Trees   |Growth Cycle  |Leaf Size|
|:-------|:------------:|--------:|
|Oak     |Annual        |Large    |
|Lemon   |Semi-annual   |Small    |

### Add Other Elements in a Table
You can add code, links, and emphasis.

|Trees   |Growth Cycle  |Link|
|:-------|:------------:|--------:|
|Oak     |Annual        |`This is an exaple code block`|
|Lemon   |Semi-annual   |[lemon tree](https://uscitrusnursery.com/cdn/shop/articles/lemon-tree_1c2bd620-e725-4c4b-afec-d6cb651a6f4c.jpg?v=1765117676)|

!!!tip Tip
    To create tables quickly and with GUI, try [Markdown Tables Generator][].

!!!note Note
    Separate a table with the previous content by at least a blank line, otherwise the table cannot be rendered as a table.

## Fenced Code Blocks
Put three backticks before and after the code block.

```
{
    "name": "jiaying",
    "job": "technical writer",
    "email": "sisuzanel@163.com"
}
```
## Syntax Highlighting
This allows elements in fenced blocks to be rendered in colors for highlighting.

Specify the language after the starting three backticks.

```json
{
    "name": "jiaying",
    "job": "technical writer",
    "email": "sisuzanel@163.com"
}
```

## Footnotes
To add a footnote reference, add a caret and an identifier inside a pair of brackets.
To add the footnote,  use another caret and number inside brackets with a colon and text.

!!!example Example
    This line has a footnote.[^1]

## Heading IDs {#Heading-IDs}
Enclose the custom ID in curly braces on the same line as the heading. 

!!!note Note
    Do not put spaces in heading IDs.

### Link to Heading IDs
Create a standard link with a number sign "#" followed by the heading ID

!!!example Example
    To know how to create a heading ID, see [Heading IDs](#Heading-IDs).

## Definition List
To create a definition list, type the term on the first line. On the next line, type a colon followed by a space and the definition.

!!!example Example
    Markdown
    : a lightweight markup language

    VS code
    : a programming editor

## Strikethrough
Put two tilde symbols "~" before and after the words.

!!!example Example
    You can ~~strikethrough words~~.

## Task List
 To create a task list, add dashes (-) and brackets with a space ([ ]) in front of task list items.

!!!example Example
    - [ ] Push Extended.md to GitHub
    - [ ] Design the structure of my portfolio

### Check a Task List
To check a task list, put an x in between the brackets.

!!!example Example
    - [x] Push Extended.md to GitHub
    - [ ] Design the structure of my portfolio

## Emoji
- Copy and paste the emoji in the md file.
- Enter the emoji shortcode.  
  Refer to the [list of emoji shortcodes][].

!!!example Example
    Glad to meet you!:smiley:  
    Do you think three-body people are real?:alien:  
    How about we go and get our nails done?:nail_care:

## Word Highlighting
 To highlight words, use two equal signs (==) before and after the words.

!!!example Example
    This is a ==very important== note.

## Subscript
To create a subscript, use one tilde symbol (~) before and after the characters.

!!!example Example
    Charge your phone with 5V ~AC~.

!!!note Note
    Some applications use this syntax for strikethrough.

## Superscript
 To create a superscript, use one caret symbol (^) before and after the characters.

!!!example Example
    E=MC^2^.

[^1]: This is a footnote.   
    `This is a footnote`


[Markdown Tables Generator]: (https://www.tablesgenerator.com/markdown_tables#)
[list of emoji shortcodes]: https://www.markdownguide.org/extended-syntax/

