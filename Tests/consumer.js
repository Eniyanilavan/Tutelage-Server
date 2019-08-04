const kafka = require('kafka-node');
const axios = require('axios')
var spawn = require('child_process').spawn;
var spawnSync = require('child_process').spawnSync;
var fs = require('fs');

var Client = new kafka.KafkaClient({ kafkaHost: "localhost:9092" });
var PyClient = new kafka.KafkaClient({ kafkaHost: "localhost:9093" });
var CClient = new kafka.KafkaClient({ kafkaHost: "localhost:9092" });
var JavaClient = new kafka.KafkaClient({ kafkaHost: "localhost:9092" });

completed = (id, result) => {
    axios({
        method: 'post',
        url: 'http://localhost:4040',
        data: {
            id: id,
            result: result
        }
    })
}

writeFile = (content, name)=>{
    fs.writeFileSync(`./code/${name}`, content)
}

const ConsumerInit = () => {

    console.log("Inited");
    var CComsumer = new kafka.Consumer(CClient, [
        {
            topic: 'c',
            partition: 0
        },
        {
            topic: 'c',
            partition: 1
        },
    ])
    var PyComsumer = new kafka.Consumer(PyClient, [
        {
            topic: 'python',
            partition: 0
        },
        {
            topic: 'python',
            partition: 1
        },
    ])
    var JavaComsumer = new kafka.Consumer(JavaClient, [
        {
            topic: 'java',
            partition: 0
        },
        {
            topic: 'java',
            partition: 1
        },
    ])

    CComsumer.on('message', async (message) => {
        body = JSON.parse(message.value);
        console.log('c');
        var results = {
            outputs:[],
            success: 0,
            failed: 0,
            error: [],
            total: 0,
            isRun: body.isRun 
        };
        writeFile(body.code, `${body.id}.c`)
        var num_testcases = fs.readdirSync(`./${body.test}/${body.ques_no}/Testcases`)
        if (body.isRun){
            num_testcases = [num_testcases[0]]
        }
        for (var test_case in num_testcases){
            results.total++;
            console.log(test_case)
            var input = fs.readFileSync(`./${body.test}/${body.ques_no}/Testcases/${test_case}/input.txt`)+""
            var exoutput = fs.readFileSync(`./${body.test}/${body.ques_no}/Testcases/${test_case}/output.txt`)+""
            var output = '', error= ''
            var obj = spawnSync(`gcc`, [`./code/${body.id}.c`, `-o`, `./code/${body.id}.o`])
            var err = (obj.output[2]+"")
            if (err !== "" && err.indexOf('error: ') !== -1){
                var results = {
                    outputs:[err],
                    success: 0,
                    failed: 1,
                    error: [0],
                    total: 1 
                };
                return completed(body.id, results)
            }
            var code = await new Promise((resolve, reject)=>{
                var run = spawn(`./code/${body.id}.o`, [])
                run.stdin.write(input)
                run.stdout.on('data',(data)=>{
                    output += data
                })
                run.stderr.on('data',(data)=>{
                    error += data
                    results.error.push(results.total-1)
                })
                run.on('error',(err)=>{
                    console.log(err)
                })
                run.on('close', (code)=>{
                    resolve(code)
                })
            })
            if(code !== 0){
                results.failed++;
                results.outputs.push(error)
            }
            else{
                console.log(exoutput)
                console.log(output)
                if(exoutput === output){
                    results.success++;
                    results.outputs.push(output)
                }
                else{
                    results.failed++;
                    results.error.push(results.total-1)
                    results.outputs.push('test case failed')
                }
            }
        }
        completed(body.id, results)
    })

    JavaComsumer.on('message', async (message) => {
        body = JSON.parse(message.value);
        console.log('java');
        console.log(message.offset);
        console.log(message.partition);
        completed(body.id)
    })

    PyComsumer.on('message', async (message) => {
        var body = JSON.parse(message.value);
        console.log('py');
        var results = {
            outputs:[],
            success: 0,
            failed: 0,
            error: [],
            total: 0,
            isRun: body.isRun 
        };
        writeFile(body.code, `${body.id}.py`)
        var num_testcases = fs.readdirSync(`./${body.test}/${body.ques_no}/Testcases`)
        if (body.isRun){
            console.log("run")
            num_testcases = [num_testcases[0]]
        }
        for (var test_case in num_testcases){
            results.total++;
            var input = fs.readFileSync(`./${body.test}/${body.ques_no}/Testcases/${test_case}/input.txt`)
            var exoutput = fs.readFileSync(`./${body.test}/${body.ques_no}/Testcases/${test_case}/output.txt`)+""
            var output = '', error= ''
            var code = await new Promise((resolve, reject)=>{
                var run = spawn(`python3`, [`./code/${body.id}.py`])
                run.stdin.write(input)
                run.stdout.on('data',(data)=>{
                    output += data
                })
                run.stderr.on('data',(data)=>{
                    error += data
                    results.error.push(results.total-1)
                })
                run.on('error',(err)=>{
                    console.log(err)
                })
                run.on('close', (code)=>{
                    resolve(code)
                })
            })
            if(code !== 0){
                results.failed++;
                results.outputs.push(error)
            }
            else{
                if(exoutput === output){
                    results.success++;
                    results.outputs.push(output)
                }
                else{
                    results.failed++;
                    results.outputs.push('test case failed')
                }
            }
        }
        completed(body.id, results)
    })

    PyComsumer.on('error', (err) => {
        console.log(err);
    })

    JavaComsumer.on('error', (err) => {
        console.log(err);
    })

    CComsumer.on('error', (err) => {
        console.log(err);
    })

}

var topics = [
    {
        topic: "c",
        partitions: 2,
        replicationFactor: 2
    },
    {
        topic: "python",
        partitions: 2,
        replicationFactor: 2
    },
    {
        topic: "java",
        partitions: 2,
        replicationFactor: 2
    },
]

Client.createTopics(topics, (err, res) => {
    if (err) {
        console.log(err);
        return;
    }
    ConsumerInit();
})


