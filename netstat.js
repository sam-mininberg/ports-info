//must apt-get install net-tools
import netstat from 'node-netstat'
import express from 'express'
import cors from 'cors'

const app = express()
const port = 3000
let netstat_data = []

netstat.parsers.linux = netstat.parserFactories.linux({
  parseName: true
})

netstat({ sync: true }, data => {
  console.log(data)
  netstat_data.push(data)
})

app.use(cors())

app.get('/', (req,res) => res.json(netstat_data))

app.listen(port)
