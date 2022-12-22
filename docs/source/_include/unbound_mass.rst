Mass-Manage
===========

If you are mass-managing DNS records or using DNS-Blocklists - you might want to disable ``reload: false`` on single module-calls!

This takes a long time, as the service gets reloaded every time!

You might want to reload it 'manually' after all changes are done => using the :ref:`ansibleguy.opnsense.reload <modules_reload>` module
