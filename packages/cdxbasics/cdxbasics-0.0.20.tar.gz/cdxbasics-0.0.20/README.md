# cdxbasics

Collection of basic tools for Python development. Highlights are

<ul>
    <li><tt>Generic()</tt>: object which operates both like a dictionary and like an object, e.g. one can write<br>
        <tt><code>
            &nbsp;&nbsp;&nbsp;&nbsp;from cdxbasics import Generic<br>
            &nbsp;&nbsp;&nbsp;&nbsp;g = Generic(a=1, b=2)  # construction with nice keywords<br>
            &nbsp;&nbsp;&nbsp;&nbsp;g.c = 3<br>
            &nbsp;&nbsp;&nbsp;&nbsp;a = g.a<br>
            &nbsp;&nbsp;&nbsp;&nbsp;a = g['a'] <br>
            &nbsp;&nbsp;&nbsp;&nbsp;d = g.get('d',None)  # with default<br>
            &nbsp;&nbsp;&nbsp;&nbsp;e = g('e',None)  # with default<br>
            &nbsp;&nbsp;&nbsp;&nbsp;del g.c<br>
            &nbsp;&nbsp;&nbsp;&nbsp;del ....
            </code>
        </tt>
    <li><tt>Logger</tt>: classic C++ style defensive programming VERIFY tools, e.g.<br>
        <tt>
            &nbsp;&nbsp;&nbsp;&nbsp;from cdxbasics import Logger<br>
            &nbsp;&nbsp;&nbsp;&nbsp;_log = Logger(__file__)<br>
            &nbsp;&nbsp;&nbsp;&nbsp;_log.verify( a==1, "'a' is not one but %s", a)<br>
            &nbsp;&nbsp;&nbsp;&nbsp;_log.warn_if( a!=1, "'a' was not one but %s", a)
        </tt><br> and other features.
    <li><tt>dctkwargs</tt>: tool to capture misspelled **kwargs.<br>
           Use<br>
            <tt>
            &nbsp;&nbsp;&nbsp;&nbsp;    from cdxbasics import dctkwargs<br>
            &nbsp;&nbsp;&nbsp;&nbsp;    def f(**kwargs):<br>
            &nbsp;&nbsp;&nbsp;&nbsp;    &nbsp;&nbsp;&nbsp;&nbsp;kwargs = dctkwargs(kwargs)<br>
            &nbsp;&nbsp;&nbsp;&nbsp;    &nbsp;&nbsp;&nbsp;&nbsp;a = kwargs('a')         # standard <br>
            &nbsp;&nbsp;&nbsp;&nbsp;    &nbsp;&nbsp;&nbsp;&nbsp;b = kwargs('b', None)   # with default <br>
            &nbsp;&nbsp;&nbsp;&nbsp;    &nbsp;&nbsp;&nbsp;&nbsp;assert kwargs.isDone(), "Unknown keywords: %s" % str(kwargs)
        </tt>
    <li><tt>fmt()</tt>: C++ style format function.
    <li><tt>uniqueHash()</tt>: runs a standard hash over most combinations of standard elements or objects.
    <li><tt>plain()</tt>: converts most combinations of standards elements or objects into plain list/dict structures.
</ul>

Version 0.20 also contains a few tools to handle file i/o in a transparent way in the new <tt>subdir</tt> module. For the time being this is experimental.
Please share any bugs with the author in case you do end up using them.


