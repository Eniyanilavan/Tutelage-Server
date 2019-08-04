import orm
from orm import ORM

Orm = ORM.ORM({
    'db_name':'tutelage',
    'host':'127.0.0.1',
    'port':5432,
    'user_name':'postgres',
    'password':'Eniyan007!'
},'psql').app()