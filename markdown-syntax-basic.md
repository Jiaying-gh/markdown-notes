# Basic Syntax

## Italic  
  Put two underlines "_" around the text.  
  
  !!! example Example:  
      I _will_ get a good job.

## Bold  
  Put two asterisks "*" (preferred) or underlines "_" around the text.

  !!! example Example:  
      I **will** get a good job.

  >[!Note]
  If you need to make texts both italic and bold, put two asterisks on the outside to make it more legible.  
  For example, I **_will_** get a good job.


## Headers  
  Put the same number of hash masks "#" as the size of the header level.  
  Six levels are available.   
  
  !!! example Example:
      # Header 1  
      ## Header 2  
      ### Header 3
      #### Header 4
      ##### Header 5
      ###### Header 6

## Link  
### Inline link  

Inline links attach the links right after the link text in the Markdown file.  
Put a pair of square brackets "[]" around the link text and a pair of parenthesis "()" around the link.   

> [!Note]
Do not place a space between the link text and the link, otherwise the square brackets show in the rendered content. 

!!!example Example
    I will get a good job on [LinkIn](https://www.linkedin.com/).  

### Reference link  
Reference links allow you to put links at the end of the Markdown file so as to manage them in a unified way.  
The link is actually a reference to another place in the file.  

Put a pair of square brackets around the link text and reference text. At the end of the file, copy and paste the reference text with brackets, and then follow the right bracket with a colon and the link.  
    
!!! example Example:  
    I will get a good job on [LinkIn][job website].
    
[job website]: https://www.linkedin.com/  

> [!Note]
> Both types of links are rendered the same way.

## Image  
### Inline image
Put an exclamation mark "!" before the alt  text, and follow the alt text with the link in a pair of parenthesis.  

> [!Note] Why we need alx text
> Users may use screen readers.
> Users may have limited network speed to load an image.  

<div class="markdown-alert markdown-alert-example">
  <p class="markdown-alert-title">Example</p>
  <p>The following table shows how the image is displayed in markdown.</p>
</div>

![a tree](https://www.bing.com/images/search?view=detailV2&ccid=zaltdJrk&id=593B06C3D6868D35297494C3CAD315970D67A85A&thid=OIP.zaltdJrkPdMPHulBBhkitwHaFj&mediaurl=https%3A%2F%2Fcdn.britannica.com%2F95%2F156695-131-FF89C9FA%2Foak-tree.jpg&cdnurl=https%3A%2F%2Fth.bing.com%2Fth%2Fid%2FR.cda96d749ae43dd30f1ee941061922b7%3Frik%3DWqhnDZcV08rDlA%26pid%3DImgRaw%26r%3D0&exph=675&expw=900&q=tree&FORM=IRPRST&ck=FD7AEF948C89334357AC8C5C86D15BB3&selectedIndex=3&itb=1&cw=1343&ch=781&ajaxhist=0&ajaxserp=0)

### Reference image
1. Put an exclamation mark "!" before the link  text.
2. Put a pair of square brackets around the link text and reference text.
3. At the end of the file, copy and paste the reference text with brackets, and then follow the right bracket with a colon and the link.

> [!Note]Note  
> Do not place a space between the exclamation mark and the left square bracket.

!!! example Example
    ![example tree][a tree]  
    [a tree]: https://www.bing.com/images/search?view=detailV2&ccid=zaltdJrk&id=593B06C3D6868D35297494C3CAD315970D67A85A&thid=OIP.zaltdJrkPdMPHulBBhkitwHaFj&mediaurl=https%3A%2F%2Fcdn.britannica.com%2F95%2F156695-131-FF89C9FA%2Foak-tree.jpg&cdnurl=https%3A%2F%2Fth.bing.com%2Fth%2Fid%2FR.cda96d749ae43dd30f1ee941061922b7%3Frik%3DWqhnDZcV08rDlA%26pid%3DImgRaw%26r%3D0&exph=675&expw=900&q=tree&FORM=IRPRST&ck=FD7AEF948C89334357AC8C5C86D15BB3&selectedIndex=3&itb=1&cw=1343&ch=781&ajaxhist=0&ajaxserp=0

## Block quote
Put a greater than ">" caret before the quote.  
This is to indicate that the content is from somewhere else.
After rendering, it will be dented and has a colored line at the left of the content.
You can place other markdown elements in a block quote.

!!! example Example
    The following sentence is a quote.
    > The only thing we have to fear is fear itself.  

To quote multiple paragraphs in a single block quote, place > before each paragraph, including the blank line.

To end a quote block, leave a blank line after it.

## Line break  
### Hard break  
Press Enter, and put a space before the new line. 

### Soft break  
 Put two spaces after the previous line, and then press Enter.  

## List
### Unordered list
Place a asterisk "*" before each item.  

!!! example Example
    * Sun
    * Moon
    * Venus

To insert a lower-level list, indent one asterisk more before the preceding item.  

!!! example Example
    * Fruit  
      * Lemon
      * Apple
      * Blueberry

### Ordered list
Place the number before the step.

!!! example Example
    1. Write markdown files.
    2. Upload file to Github.  

### List text
Start a new line, and then indent the line by at least one space.

!!! example Example
    1. Upload markdown files to  Github.  
       Make sure the files are closed.




