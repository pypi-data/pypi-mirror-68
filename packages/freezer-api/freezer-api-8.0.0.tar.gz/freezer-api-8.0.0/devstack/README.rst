This directory contains the Freezer-API DevStack plugin.

To configure the Freezer API with DevStack, you will need to
enable this plugin by adding one line to the [[local|localrc]]
section of your local.conf file.

To enable the plugin, add a line of the form::

    enable_plugin freezer-api <GITURL> [GITREF]

where::

    <GITURL> is the URL of a freezer-api repository
    [GITREF] is an optional git ref (branch/ref/tag).  The default is master.

For example::

    enable_plugin freezer-api https://git.openstack.org/openstack/freezer-api master


The plugin makes use of apache2 by default.
To use the uwsgi server set the following environment variable::

    export FREEZER_API_SERVER_TYPE=uwsgi

The default port is 9090. To configure the api to listen on a different port
set the variable FREEZER_API_PORT.
For example to make use of port 19090 use::

    export FREEZER_API_PORT=19090

The plugin makes use of elasticsearch as db backend by default.
To use the sqlachemy set the following environment variable::

    export FREEZER_BACKEND='sqlalchemy'

This is a sample local.conf file for freezer developer::
    
    [[local|localrc]]
    ADMIN_PASSWORD=stack
    DATABASE_PASSWORD=stack
    RABBIT_PASSWORD=stack
    SERVICE_PASSWORD=$ADMIN_PASSWORD

    DEST=/opt/stack
    LOGFILE=$DEST/logs/stack.sh.log
    
    # only install keystone/horizon/swift in devstack
    # disable_all_services
    # enable_service key mysql s-proxy s-object s-container s-account horizon

    enable_plugin freezer http://git.openstack.org/openstack/freezer master
    enable_plugin freezer-api http://git.openstack.org/openstack/freezer-api.git master
    enable_plugin freezer-tempest-plugin http://git.openstack.org/openstack/freezer-tempest-plugin.git master
    enable_plugin freezer-web-ui http://git.openstack.org/openstack/freezer-web-ui.git master
    
    export FREEZER_BACKEND='sqlalchemy'

For more information, see:
 https://docs.openstack.org/devstack/latest/index.html
