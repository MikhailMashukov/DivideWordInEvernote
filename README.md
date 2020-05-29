Small utility for exporting Word documents into Evernote. Just a pre-alpha version and not polished at all ("make yourself"), but maybe will be useful for somebody. It took almost a work day for me to implement-debug it.

You can have your notes in Word with structure like
(heading 1) To read/watch
  (heading 2) Books to read
    (heading 3) Programming
    Psychology
    Other
  Movies to watch
    ... 
Useful Linux utilities
  Related to processes
  ...

But you can only copy-paste entire document into Evernote. Or to cut separate blocks manually.
I had about 1000 notes in 6 main Word documents until recently decided to move to something else (and have chosen Evernote).
So I have written this script. The script looks at headings at levels 2, 3 and 4 and generates notes' titles of the form <parent heading 2> / <heading 3> or <parent heading 3> / <heading 4>. I.e. you will get Books to read / Programming, Books to read / Psychology and so on.

In order to cut you need

* Take Evernote notebook with at least one note (the first one will be used as template for generated notes),
* create new Evernote note in this notebook,
* paste Word document into it,
* export the notebook to a .enex file (hopefully the new note will be last in exported .enex file, since the script always divide the last one),
* write path to this file into divideEvernoteWordFile() call at the end of the script,
* write your desired output file path near,
* run the script,
* import the produced .enex file.
  
TODO: it would be nice to support proper division of embedded images and so on. They are stored near the source XML content block and are linked by hashes from it. So this is quite easy. But I have been too lazy to implement this yet.