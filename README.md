# The pythonic way

The aim of this site is to provide a cookbook (working examples)
or courses on specific topics programming with the best programming language: Python ;-)

# Licence

The source code is under [GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html).
The result is under http://creativecommons.org/licenses/by-nc-sa/4.0/

# Contributing, Bug Reports

If you are interested to contribute to this web site, fork this project and submit a pull request.

I use sphinx to generate html (in a directory named *docs*) and use github pages functionality
to publish the content of *docs* directory (in master branch) as web site (see
[project pages](https://help.github.com/articles/user-organization-and-project-pages/) ).

To contribute, fix bugs (typos, error), create new pages

 1. install (sphinx)[http://www.sphinx-doc.org/].
 2. fork the project.
 3. create a new branch.
 3. create new page or fix an existing one.
 4. check the result locally (make html)
 5. ask for a pull request on the source code, not on the generated html (do not commit anything in docs directory).

Project Structure

* docs -- The html generate by sphinx. The content of this directory is pushed publish on github pages
* doctrees -- Generate by sphinx not directly used
* source
 * *.rst -- The source files in Restructured Text.
 * _static
    * figs -- The figure used in the site.
    * code -- The python code files used.
 * _templates -- The files to customize the *classic* css.
 * _themes -- The custom theme used for this site (inherit from *classic*).
* LICENSE -- What you can do with the code.
* Makefile -- to automate the html generation, *make html*.
* REAMDE.md -- This file.
