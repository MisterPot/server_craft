# Server_craft module

### Instalation

    git clone https://github.com/MisterPot/server_craft.git
    
Recommends use python 3.8.2

Double click to `install.bat`, if use Windows.
`sh install.bat`, if use Linux.
### How to use

You need to use admin mode in your console for commands below. 

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

If needed version of Java not installed in your computer, this installed automatically.

After run `craft` with argument `-r` pops up new console , in which
you must input this

    from server_craft.starter import server
    server.start()

After this , server will start completely. 

### Other content

Simple utility `exw` can be used in exchanging worlds with another users

    exw [-option]
                 
        -s send             send world from current server directory
        -r ip:port          for receive world, need to write from who going world

For example

In server directory:
    
    exw -s send

Your friend, which want to get current server world:

    exw -r 123.34.54.23:5000

All worlds, which you received, save automatically by the `world_storage_path` variable.
In the future, these worlds can be used in config files with prefix `%` or 
just copy to anywhere