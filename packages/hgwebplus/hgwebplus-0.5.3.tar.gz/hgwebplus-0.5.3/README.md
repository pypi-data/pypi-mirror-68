# hgwebplus

hgwebplus is a [mercurial](https://mercurial-scm.org/) extension that enhances
the normal hgweb tooling so that theme authors can create more robust themes.

It's built as an extension mainly to try out new things before attempting to
get them upstreamed.  Also, due to the Bitbucket death clock, I couldn't wait
for an upstream release.

All screen shots are from my
[hgkeeper-theme](https://keep.imfreedom.org/grim/hgkeeper-theme).

# Features

hgwebplus was created during the development of
[hgkeeper-theme](https://keep.imfreedom.org/grim/hgkeeper-theme) as a way to
make the theme look more like current code hosting sites.

Everything has been built to be backwards compatible, to keep existing themes
working.  However, this code has only been tested on Python3 and Python2 is
considered unsupported right now.

## Readme Rendering

Readme rendering is supported via a template keyword named `readme`. Since
this is a keyword, it can be used in any template.  It will look for files
named `README.md`, `README.txt`, and `README` in a case insensitive fashion,
and return their contents rendered with a Markdown renderer.

The Markdown rendering uses [mistune](https://pypi.org/project/mistune/) to
support Markdown.  However, there is no styling associated with this renderer.
To do that, I recommend you use [sindresorhus's
github-markdown-css](https://github.com/sindresorhus/github-markdown-css/) in
your theme and adjust it accordingly.

## Gravatar Support

This is a bit of a misnomer as there isn't actually a
[Gravatar](https://gravatar.com/) filter/keyword, but hgwebplus adds an `md5`
filter that allows you to create Gravatar links.

With the `md5` filter you can then display a Gravatar for an author with the
example below:

```
<img src="https://www.gravatar.com/avatar/{author|email|mailmap|strip|lower|md5}?s=36" decoding="async">
```

At some point, we'll probably build a proper function where you don't need to
know the specifics of the Gravatar API, but for now this works.

## Diff Rendering

The stock diff rendering in hgweb leaves a bit to be desired.  When rendering
the lines of the diffs, you don't have the correct line numbers, nor the file
names, nor the file revisions all of which make it impossible to link to the
original revision for further viewing.

Therefore, hgwebplus exposes all of these to the diffs templates and allows
you to create something similar to the screenshot below.

![diff screenshot](images/diff.png)

## Diffstat

The diffstat template has been modified to give you the number of lines added
and removed as well as a boolean telling you if the file is binary or not.

With these changes you can create something like the below screen shot:

![diffstat example](images/diffstat.png)

## Title

`title` is a new tempate keyword that will output the value of the `web.title`
configuration setting.  This allows users to customize a title that themes
can then render.

There is also a `sub_title` keyword that can be used to add a secondary text to
be displayed with the title.

## Clone URLS

Previously there was no way for an administrator to tell a theme how to clone
the repositories.  This meant that there was no interface a theme could build
to tell users how to clone a repository.

To fix this, hgwebplus adds two new template keywords `http_clone_url` and
`ssh_clone_url`.  These are controlled via the `web.http_clone_url` and
`web.ssh_clone_url` configuration settings.

# Issues

If you have any issues with this extension, please file them at
[https://issues.imfreedom.org/issues/HGWEBPLUS](https://issues.imfreedom.org/issues/HGWEBPLUS).

# Installation

Release are done purely via [pypi](https://pypi.org/project/hgwebplus/) and
can be installed a few ways.

## Mercurial Installed via Package Manager

If your Mecurial is installed via your package manager, you may choose to
install hgwebplus to the system path, but this typically requires sudo access.
If you choose to go this route, you can use the following command to install
hgwebplus.

```
pip3 install hgwebplus
```

Once it's done installing, you can modify your `~/.hgrc` and add the make
sure your `[extensions]` section contains the following:

```
[extensions]
hgext3rd.hgwebplus =
```

If you would rather not install hgwebplus system wide, you can instead install
it to your user directory with the following command:

```
pip3 install --user hgwebplus
```

Once this is installed, you'll have to update your `~/.hgrc` to look something
like the following replacing the `?` with your version of Python:

```
[extensions]
hgext3rd.evolve = ~/.local/lib/python3.?/site-packages/hgext3rd/
```

## Mercurial Installed Via pip

If you've installed mercurial via `pip3 --user` then you can just install
hgwebplus in the same manner with

```
pip3 install --user hgwebplus
```

After installation you just need to tell Mercurial about it by making sure
that your `~/.hgrc` `[extensions]` section contains the following:

```
[extensions]
hgext3rd.hgwebplus =
```
