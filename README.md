caspython-centera
=================

EMC Centera Python Wrapper. See LICENSE.txt for further details.

## Centera Garbage collection & shredding

https://community.emc.com/message/518033
https://community.emc.com/docs/DOC-7853



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
    pip install requirements.txt
    nosetest -v -w test


