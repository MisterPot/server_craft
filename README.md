# Server_craft module

### Instalation

    git clone https://github.com/MisterPot/server_craft.git

Double click to `install.bat`, if use Windows.
`sh install.bat`, if use Linux.
### How to use

With this packed was installed simple utility `craft` to create and
control server.

    craft [option]
        
        -v                  view all available versions of servers
        -r                  run jar file in current dir
        -d [version]        download and unpack server to current dir 
        -c [config_file]    use config file to run server, if not used
                            default config file
        -c create           to create default config file in current dir 


For example:
    
    craft -c create
    craft -d 1.17.1 -c settings.conf -r

This commands create default `settings.conf`, download server of
version 1.17.1 and use config `settings.conf`, then run it.

After run `craft` with argument `-r` pops up new console , in which
you must input this

    from server_craft.starter import server
    server.start()

After this , server will start completely. 
