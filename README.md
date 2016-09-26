# caspython-centera

EMC Centera Python Wrapper with a user-friendly CenteraConnection interface.


## Usage

Connecting to Centera is easy thanks to CenteraConnection.

    from Filepool.connector import CenteraConnection
    
    # Connect to a pool.
    pool = CenteraConnection('192.168.1.1,192.168.1.2')

    # Get pool info.
    infos = pool.info()
    print("You have still {freeSpace} bytes".format(**infos))
    
    # Put many files.
    clip_id = pool.put("put_one_file", files=["file1.txt", "file2.txt"], retention_sec=10)
    
    # Get clip metadata.
    clip = self.connection.get(clip_id, tag=True)
    print(clip.attributes)
    
    # Close pool.
    pool.close()



## Installing

On RHEL7 you need:
 
    #yum -y install compat-libstdc++-33

Download and unpack the Centera SDK 3.1 or above.

    export CENTERA_HOME=/opt/centera
    export PYTHONPATH+=:$(echo $PWD/src/build/lib.*)
    (cd src && python setup.py install; )

If using sudo, run:

    (cd src && sudo CENTERA_HOME=$CENTERA_HOME python setup.py install; )


## Develop

Setup the enviroment for using the local build and your test environment

    export CENTERA_PEA_LOCATION=$PWD/stage_pool.pea
    tox


## Centera Garbage collection & shredding

https://community.emc.com/message/518033
https://community.emc.com/docs/DOC-7853
