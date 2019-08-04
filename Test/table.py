from init import Orm
import orm

TestTable = Orm.define('test', {
    'name':{
        'type':orm.STRING,
        'isPrimaryKey': True,
        'notNull':True
    },
    'start_date':{
        'type':orm.DATE,
        'notNull':True
    },
    'duration':{
        'type':orm.INTEGER,
        'notNull':True
    },
    'end_date':{
        'type':orm.DATE,
        'notNull':True
    },
    'whom':{
        'type':orm.STRING,
        'notNull':True
    },
    'count':{
        'type':orm.INTEGER,
        'notNull':True
    },
    'Type':{
        'type':orm.STRING
    }
})
