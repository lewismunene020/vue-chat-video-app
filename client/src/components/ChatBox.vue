<template>
  <div>
    <div v-for="message in messages" :key="message.id">
      {{ message.text }}
    </div>
    <form @submit.prevent="sendMessage">
      <input v-model="messageText" type="text" placeholder="Enter message here" />
      <button type="submit">Send</button>
    </form>
  </div>
</template>

<script>
import io from 'socket.io-client'
import axios from 'axios'

export default {
  data() {
    return {
      messages: [],
      messageText: '',
      socket: io('http://localhost:3000')
    }
  },
  created() {
    this.socket.on('new message', message => {
      this.messages.push(message)
    })

    axios.get('/api/messages').then(response => {
      this.messages = response.data
    })
  },
  methods: {
    sendMessage() {
      axios.post('/api/messages', {
        text: this.messageText
      }).then(() => {
        this.messageText = ''
      })
    }
  }
}
</script>
