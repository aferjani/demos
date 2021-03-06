# This file is part of the Hotwire Shell project API.

# Copyright (C) 2007 Colin Walters <walters@verbum.org>

# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
# of the Software, and to permit persons to whom the Software is furnished to do so, 
# subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE X CONSORTIUM BE 
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR 
# THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os, sys, shutil, stat

import hotwire
from hotwire.fs import FilePath, unix_basename

from hotwire.builtin import BuiltinRegistry, MultiArgSpec
from hotwire.builtins.fileop import FileOpBuiltin

class MvBuiltin(FileOpBuiltin):
    __doc__ = _("""Rename initial arguments to destination.""")
    def __init__(self):
        super(MvBuiltin, self).__init__('mv', aliases=['move'],
                                        hasstatus=True,
                                        argspec=MultiArgSpec('paths', min=2))

    def execute(self, context, args):
        target = FilePath(args[-1], context.cwd)
        try:
            target_is_dir = stat.S_ISDIR(os.stat(target).st_mode)
            target_exists = True
        except OSError, e:
            target_is_dir = False
            target_exists = False
        
        sources = args[:-1]
        if (not target_is_dir) and len(sources) > 1:
            raise ValueError(_("Can't move multiple items to non-directory"))

        sources_total = len(sources)
        self._status_notify(context, sources_total, 0)

        if target_is_dir:
            for i,source in enumerate(sources):
                target_path = FilePath(unix_basename(source), target)
                shutil.move(FilePath(source, context.cwd), target_path)
                self._status_notify(context, sources_total, i+1)
        else:
            shutil.move(FilePath(sources[0], context.cwd), target)
            self._status_notify(context,sources_total,1)
            
        return []
BuiltinRegistry.getInstance().register_hotwire(MvBuiltin())
