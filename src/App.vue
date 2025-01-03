<script setup>
import { ref } from 'vue'

const netstat_data = ref(null)

async function fetchData() {
  netstat_data.value = null
  const res = await fetch('http://localhost:3000')
  console.log(res)
  netstat_data.value = await res.json()
}

fetchData()
</script>

<template>
  <div id="app">
    <table>
      <thead>
        <tr>
          <th>Protocol</th>
          <th>Local Address</th>
          <th>Foreign Address</th>
          <th>State</th>
          <th>Command</th>
          <th>PID</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in netstat_data" :key=item.pid>
          <td>{{ item.protocol }}</td>
          <td>{{ item.local.address+':'+item.local.port }}</td>
          <td>{{ item.remote.address+':'+item.remote.port }}</td>
          <td>{{ item.state }}</td>
          <td>{{ item.processName }}</td>
          <td>{{ item.pid }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
