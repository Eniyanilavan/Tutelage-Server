from init import Orm
import orm

Users = Orm.define('users', {
    'regno':{
        'type':orm.STRING,
        'isPrimaryKey': True,
        'notNull':True
    },
    'uname':{
        'type':orm.STRING,
        'notNull':True
    },
    'dept':{
        'type':orm.STRING,
        'notNull':True
    },
    'year':{
        'type':orm.STRING,
        'notNull':True
    },
    'section':{
        'type':orm.STRING,
        'notNull':True
    },
    'isAdmin':{
        'type': orm.BOOLEAN,
        'notNull': True
    },
    'password':{
        'type':orm.STRING,
        'notNull':True
    },
})