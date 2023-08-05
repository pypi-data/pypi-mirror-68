#!/usr/bin/python
# -*- coding: utf-8 -*-
# rdiffweb, A web interface to rdiff-backup repositories
# Copyright (C) 2019 rdiffweb contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import
from __future__ import unicode_literals

from builtins import str
import grp
import logging
import os
import platform
import pwd
import subprocess
import sys

import cherrypy
import psutil

from rdiffweb.controller import Controller, validate_int, validate
from rdiffweb.core import RdiffError, RdiffWarning
from rdiffweb.core.config import Option
from rdiffweb.core.i18n import ugettext as _
from rdiffweb.core.rdw_templating import do_format_filesize as filesize
from rdiffweb.core.store import ROLES

# Define the logger
logger = logging.getLogger(__name__)


def get_pyinfo():
    if platform.dist()[0] != '' and platform.dist()[1] != '':
        yield _('OS Version'), '%s %s (%s %s)' % (platform.system(), platform.release(), platform.dist()[0].capitalize(), platform.dist()[1])
    else:
        yield _('OS Version'), '%s %s' % (platform.system(), platform.release())
    if hasattr(os, 'path'): yield _('OS Path'), os.environ['PATH']
    if hasattr(sys, 'version'): yield _('Python Version'), ''.join(sys.version)
    if hasattr(sys, 'subversion'): yield _('Python Subversion'), ', '.join(sys.subversion)
    if hasattr(sys, 'prefix'): yield _('Python Prefix'), sys.prefix
    if hasattr(sys, 'executable'): yield _('Python Executable'), sys.executable
    if hasattr(sys, 'path'): yield _('Python Path'), ', '.join(sys.path)


def get_osinfo():

    def gr_name(gid):
        try:
            return grp.getgrgid(gid).gr_name
        except:
            return

    def pw_name(uid):
        try:
            return pwd.getpwuid(os.getuid()).pw_name
        except:
            return

    if hasattr(sys, 'getfilesystemencoding'): yield _('File System Encoding'), sys.getfilesystemencoding()
    if hasattr(os, 'getcwd'):
        yield _('Current Working Directory'), os.getcwd()
    if hasattr(os, 'getegid'):
        yield _('Effective Group'), '%s (%s)' % (os.getegid(), gr_name(os.getegid()))
    if hasattr(os, 'geteuid'):
        yield _('Effective User'), '%s (%s)' % (os.geteuid(), pw_name(os.geteuid))
    if hasattr(os, 'getgid'):
        yield _('Group'), '%s (%s)' % (os.getgid(), gr_name(os.getgid()))
    if hasattr(os, 'getuid'):
        yield _('User'), '%s (%s)' % (os.getuid(), gr_name(os.getuid()))
    if hasattr(os, 'getgroups'):
        yield _('Group Membership'), ', '.join(['%s (%s)' % (gid, gr_name(gid)) for gid in os.getgroups()])
    try:
        if hasattr(os, 'getpid') and hasattr(os, 'getppid'):
            yield _('Process ID'), ('%s (parent: %s)' % (os.getpid(), os.getppid()))
    except:
        pass


def get_hwinfo():
    if hasattr(os, 'getloadavg'):
        yield _('Load Average'), ', '.join(map(str, map(lambda x: round(x, 2), os.getloadavg())))
    yield _('CPU Count'), psutil.cpu_count()
    meminfo = psutil.virtual_memory()
    yield _('Memory usage'), '%s / %s' % (filesize(meminfo.used), filesize(meminfo.total))


def get_pkginfo():
    import jinja2
    yield _('Jinja2 Version'), getattr(jinja2, '__version__')
    yield _('CherryPy Version'), getattr(cherrypy, '__version__')
    from rdiffweb.core.store_sqlite import sqlite3  # @UnresolvedImport
    yield _('SQLite Version'), getattr(sqlite3, 'version')
    try:
        import ldap
        yield _('LDAP Version'), getattr(ldap, '__version__')
        yield _('LDAP SASL Support (Cyrus-SASL)'), ldap.SASL_AVAIL  # @UndefinedVariable
        yield _('LDAP TLS Support (OpenSSL)'), ldap.TLS_AVAIL  # @UndefinedVariable
    except:
        pass


@cherrypy.tools.is_admin()
class AdminPage(Controller):
    """Administration pages. Allow to manage users database."""

    logfile = Option('logfile')
    logaccessfile = Option('logaccessfile')

    def _check_user_root_dir(self, directory):
        """Raised an exception if the directory is not valid."""
        if not os.access(directory, os.F_OK) or not os.path.isdir(directory):
            raise RdiffWarning(_("User root directory %s is not accessible!") % directory)

    def _get_log_files(self):
        """
        Return a list of log files to be shown in admin area.
        """
        logfiles = [self.logfile, self.logaccessfile]
        logfiles = [fn for fn in logfiles if fn]
        return [os.path.basename(fn) for fn in logfiles]

    def _get_log_data(self, logfile, num=2000):
        """
        Return a list of log files to be shown in admin area.
        """
        logfiles = [self.logfile, self.logaccessfile]
        logfiles = [fn for fn in logfiles if fn]
        for fn in logfiles:
            if logfile == os.path.basename(fn):
                try:
                    return subprocess.check_output(['tail', '-n', str(num), fn], stderr=subprocess.STDOUT).decode('utf-8')
                except:
                    logging.exception('fail to get log file content')
                    return "Error getting file content"

    @cherrypy.expose
    def default(self):
        params = {"user_count": self.app.store.count_users(),
                  "repo_count": self.app.store.count_repos()}

        return self._compile_template("admin.html", **params)

    @cherrypy.expose
    def logs(self, filename=u""):

        # Check if the filename is valid.
        data = ""
        logfiles = self._get_log_files()
        if logfiles:
            if not filename:
                filename = logfiles[0]

            if filename not in logfiles:
                raise cherrypy.HTTPError(404)

            data = self._get_log_data(filename)

        params = {
            "filename": filename,
            "logfiles": logfiles,
            "data":  data,
        }
        return self._compile_template("admin_logs.html", **params)

    @cherrypy.expose
    def users(self, criteria=u"", search=u"", action=u"", username=u"",
              email=u"", password=u"", user_root=u"", role=u""):

        # If we're just showing the initial page, just do that
        params = {}
        if self._is_submit():
            try:
                params = self._users_handle_action(action, username,
                                                   email, password, user_root,
                                                   role)
            except RdiffWarning as e:
                params['warning'] = str(e)
            except RdiffError as e:
                params['error'] = str(e)

        params.update({
            "criteria": criteria,
            "search": search,
            "users": list(self.app.store.users(search=search, criteria=criteria))})

        # Build users page
        return self._compile_template("admin_users.html", **params)

    @cherrypy.expose
    def repos(self, criteria=u"", search=u""):
        params = {
            "criteria": criteria,
            "search": search,
            "repos": list(self.app.store.repos(search=search, criteria=criteria))
        }
        return self._compile_template("admin_repos.html", **params)

    @cherrypy.expose
    def sysinfo(self):

        params = {
            "version": self.app.version,
            "plugins": self.app.plugins,
            # Config
            "cfg": {
                k: '********' if 'password' in k else v
                for k, v in self.app.cfg.items()},
            # System Info entries
            "pyinfo": list(get_pyinfo()),
            "osinfo": list(get_osinfo()),
            "hwinfo": list(get_hwinfo()),
            "ldapinfo": list(get_pkginfo()),
        }

        return self._compile_template("admin_sysinfo.html", **params)

    def _users_handle_action(self, action, username, email, password,
                             user_root, role):

        success = ""

        # We need to change values. Change them, then give back that main
        # page again, with a message
        if username == self.app.currentuser.username:
            # Don't allow the user to changes it's "role" state.
            role = self.app.currentuser.role

        # Fork the behaviour according to the action.
        if action == "edit":
            # Validation
            validate_int(role, 'role should be an integer')
            validate(int(role) in ROLES, 'invalid role')

            user = self.app.store.get_user(username)
            logger.info("updating user [%s] info", user)
            if password:
                user.set_password(password, old_password=None)
            user.user_root = user_root
            user.role = role
            # Avoid updating the email fields is it didn'T changed. see pdsl/minarca#187
            if email != user.email:
                user.email = email
            success = _("User information modified successfully.")

            # Check and update user directory
            if user.user_root:
                self._check_user_root_dir(user.user_root)
                user.update_repos()

        elif action == "add":
            # Validation
            validate_int(role, 'role should be an integer')
            validate(int(role) in ROLES, 'invalid role')
            
            if username == "":
                raise RdiffWarning(_("The username is invalid."))
            logger.info("adding user [%s]", username)

            user = self.app.store.add_user(username, password)
            if user_root:
                user.user_root = user_root
            user.role = role
            user.email = email

            # Check and update user directory
            if user.user_root:
                self._check_user_root_dir(user.user_root)
                user.update_repos()
            success = _("User added successfully.")

        if action == "delete":
            if username == self.app.currentuser.username:
                raise RdiffWarning(_("You cannot remove your own account!"))
            user = self.app.store.get_user(username)
            if not user:
                raise RdiffWarning(_("User doesn't exists!"))
            try:
                user.delete()
            except ValueError as e:
                raise RdiffWarning(e)
            success = _("User account removed.")

        # Return messages
        return {'success': success}
