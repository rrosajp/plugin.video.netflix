# -*- coding: utf-8 -*-
# Author: asciidisco
# Module: default
# Created on: 13.01.2017
# License: MIT https://goo.gl/5bMj3H
# pylint: disable=broad-except

"""Kodi plugin for Netflix (https://netflix.com)"""
from __future__ import unicode_literals

import sys

import xbmcplugin

import resources.lib.cache as cache
import resources.lib.common as common
import resources.lib.kodi.ui as ui
import resources.lib.kodi.library as library
import resources.lib.navigation as nav
import resources.lib.navigation.directory as directory
import resources.lib.navigation.hub as hub
import resources.lib.navigation.player as player
import resources.lib.navigation.actions as actions

def route(pathitems):
    """Route to the appropriate handler"""
    common.debug('Routing navigation request')
    root_handler = pathitems[0]
    pass_on_params = (pathitems[1:], common.REQUEST_PARAMS)
    if not common.PATH or root_handler == nav.MODE_DIRECTORY:
        directory.build(*pass_on_params)
    elif root_handler == nav.MODE_HUB:
        hub.browse(*pass_on_params)
    elif root_handler == nav.MODE_PLAY:
        player.play(pathitems=pathitems[1:],
                    needs_pin=common.REQUEST_PARAMS.get('pin', False))
    elif root_handler == nav.MODE_ACTION:
        actions.execute(*pass_on_params)
    elif root_handler == nav.MODE_LIBRARY:
        library.execute(*pass_on_params)
    else:
        raise nav.InvalidPathError(
            'No root handler for path {}'.format('/'.join(pathitems)))

if __name__ == '__main__':
    # Initialize variables in common module scope
    # (necessary when reusing language invoker)
    common.init_globals(sys.argv)
    common.info('Started (Version {})'.format(common.VERSION))
    common.info('URL is {}'.format(common.URL))

    try:
        route(common.PATH.split('/'))
    except Exception as exc:
        import traceback
        common.error(traceback.format_exc())
        ui.show_notification(msg='Error: {}'.format(exc))
        xbmcplugin.endOfDirectory(handle=common.PLUGIN_HANDLE, succeeded=False)

    cache.commit()
    library.save_library()
