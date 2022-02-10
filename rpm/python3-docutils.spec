# Adapted from Fedora's packaging (2014-02-17)
# http://pkgs.fedoraproject.org/cgit/python-docutils.git/tree/python-docutils.spec

Name:           python3-docutils
Version:        0.18.1
Release:        1
Summary:        System for processing plaintext documentation
# See COPYING.txt for information
License:        Public Domain and BSD and Python and GPLv3+
URL:            http://docutils.sourceforge.net
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3-imaging

%description
The Docutils project specifies a plaintext markup language, reStructuredText,
which is easy to read and quick to write.  The project includes a python
library to parse rST files and transform them into other useful formats such
as HTML, XML, and TeX as well as commandline tools that give the enduser
access to this functionality.

Currently, the library supports parsing rST that is in standalone files and
PEPs (Python Enhancement Proposals).  Work is underway to parse rST from
Python inline documentation modules and packages.

%prep
%autosetup -n %{name}-%{version}/docutils

# Remove shebang from library files
for file in docutils/utils/{code_analyzer.py,punctuation_chars.py,error_reporting.py,smartquotes.py} docutils/utils/math/{latex2mathml.py,math2html.py} docutils/writers/xetex/__init__.py; do
    sed -i -e '/#! *\/usr\/bin\/.*/{1D}' $file
done

iconv -f ISO88592 -t UTF8 tools/editors/emacs/IDEAS.rst > tmp
mv tmp tools/editors/emacs/IDEAS.rst

%build
%py3_build

%install
%py3_install

for file in %{buildroot}/%{_bindir}/*.py; do
    mv $file `dirname $file`/`basename $file .py`
done

# We want the licenses but don't need this build file
rm -f licenses/docutils.conf

# Flash file shouldn't be in the installed package.
rm -f docs/user/rst/images/biohazard.swf

%files
%defattr(-,root,root,-)
%license COPYING.txt licenses/*
%{_bindir}/*
%{python3_sitelib}/*
