instal virtualenv for windows
create a virtualenv in this dir
execute command "pip install -r requirements.txt"
install psql
then open two terminals

clone kafka repo.

cd into kafka folder and run these commands in seperate terminals

./bin/windows/zookeeper-server-start.bat ./config/zookeeper.properties
./bin/windows/kafka-server-start.bat ./config/server.properties
./bin/windows/kafka-server-start.bat ./config/server_1.properties

after starting kafka start all the server

for now run all the server in single system it will withstand



**in init.py change the db password**

Terminal 1:
    execute "python app.py"

Terminal 2:
    cd Tests
    npm i
    node consumer.js

clone the WSS repo also
