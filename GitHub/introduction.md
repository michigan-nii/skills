# Version control, Git, and GitHub

GitHub is built on top of Git, and Git is version control, so we should
start by explaining what is version control software and why would we
want it.

## Version control

Most people who have written scripts have made changes to a script only
to find that it doesn't work any more. Some amount of time then gets
spent restoring its old working order, then you remember to make a
copy and work on that.  This is not just about scripts, either, it's
about anything written: a jointly authored paper, a recipe, directions
to your grandmother's house.

Version control was invented to _track_ the changes -- that is, to keep
a record of what changes were made, by whom, and when.  This is quite
fundamental to writing; so fundamental that Microsoft Word has it.

Let's say Jane and John are working on a project together, and they
both work on how to make a script do something new.  They each have
their own copy of the original, and over coffee they discover that
they're both working on the same problem independently.  How can
they take what they've _both_ done, put it into one new version of the
script, and then divide up the remaining work?

First, what steps were taken?

1.  Jane made her copy
1.  Jane made changes to her copy
1.  John made his copy
1.  John made changes to his copy

Now, what do they want to do?

1.  Want to see how Jane's version differs from the original
1.  Want to see how John's version differs from the original
1.  See how Jane's version and John's versions differ from
    each other
1.  Combine Jane's and John's changes into _the_ changed version

This is basically the scenario that all version control software tries
to make better/easier.

There are _four_ versions of the file implied in the outline above:
Jane's copy, John's copy, the original, and the copy with the final
combination of Jane's and John's changes, which is called the _merged_
copy.

How do version control systems work?

All of them have some sort of checkout system.  Jane will _checkout_ a copy
of the file(s) she wants to work on, make changes to them, then check them
in (also called _committing_ changes).  That happens to Jane's copies.
John will do something similar.  They will both then try to put their
changes back into the One True version.  If they worked on separate parts
of the file(s) and there is no overlap, then it goes swimmingly and life
is rosy.  If not, then they will have to resolve the conflicts, and save
the combined result to the One True version.  Then they both copy the
One True version back to where they work and start over.

The exact details of the above outline vary.  Sometimes the software
requires that there be One True version, some don't.  People who use
software that doesn't require One True version learned by hard
experience that they still need one, and that's where GitHub came
in.  It is The Place to put your One True version (and, of course,
all your private copies).

## Creating the One True version

We will assume here that you want to do this the _easy way_, so we'll
use GitHub to create the One True version.  You do this in GitHub by
creating a repo (repository:  The name for a collection of files that
travel together).


