<template>
  <div class="call-container">
    <div class="remote-video-container" ref="remoteVideo"></div>
    <div class="local-video-container" ref="localVideo"></div>
    <div class="call-controls-container">
      <button v-if="!inCall" @click="startCall">Start Call</button>
      <button v-if="inCall" @click="endCall">End Call</button>
    </div>
  </div>
</template>

<script>
import io from 'socket.io-client'

export default {
  name: 'VideoCall',
  data() {
    return {
      socket: null,
      inCall: false,
      localStream: null,
      remoteStream: null,
    }
  },
  mounted() {
    this.socket = io('http://localhost:3000')
    this.socket.on('callAccepted', this.callAccepted)
    this.socket.on('incomingStream', this.addRemoteStream)
    this.socket.on('callEnd', this.endCall)
  },
  methods: {
    async startCall() {
      this.inCall = true
      this.localStream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: true,
      })
      this.socket.emit('startCall')
      this.$refs.localVideo.srcObject = this.localStream
    },
    endCall() {
      this.inCall = false
      this.socket.emit('endCall')
      this.localStream.getTracks().forEach((track) => track.stop())
      this.$refs.localVideo.srcObject = null
      this.$refs.remoteVideo.srcObject = null
    },
    callAccepted() {
      this.localStream.getTracks().forEach((track) => {
        this.socket.emit('sendStream', { track, room: this.roomId })
      })
    },
    addRemoteStream(stream) {
      this.remoteStream = new MediaStream()
      stream.forEach((track) => {
        this.remoteStream.addTrack(track)
      })
      this.$refs.remoteVideo.srcObject = this.remoteStream
    },
  }
}
</script>

<style>
.call-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.remote-video-container,
.local-video-container {
  width: 100%;
  height: 0;
  padding-bottom: 75%;
  background-color: #ccc;
}

.local-video-container {
  position: absolute;
  right: 10px;
  bottom: 10px;
  width: 20%;
  height: 20%;
}

.call-controls-container {
  display: flex;
  justify-content: center;
}

button {
  margin: 10px;
 
}
</style>
