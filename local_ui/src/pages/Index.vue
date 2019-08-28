<template>
  <!--<q-page class="flex flex-center">
    <img alt="Quasar logo" src="~assets/quasar-logo-full.svg">
  </q-page> -->
  <q-page class="q-pa-md row items-start q-gutter-md flex flex-center">

    <div class="q-pa-md q-gutter-md">

      <!-- CPU INFO -->
      <div class="q-pa-md row q-gutter-md">
        <!-- A72 temperatures  -->
        <q-card class="my-card text-white">
          <q-item>
            <q-item-section avatar>
              <q-avatar
                square
                size="48px"
              >
                <img src="~assets/thermometer.svg">
              </q-avatar>
            </q-item-section>

            <q-item-section>
              <q-item-label>A72 Temperature</q-item-label>
              <q-item-label
                style="color: white;"
                caption
              >iMX8 ARM Dual Core</q-item-label>
            </q-item-section>
          </q-item>

          <q-knob
            readonly
            v-model="tempA72"
            show-value
            font-size="25px"
            size="200px"
            :thickness="0.25"
            track-color="grey-3"
            class="text-white q-ma-md"
            :color="gauge_tempA72Color"
          >
            {{ tempA72 }} ºC
          </q-knob>
        </q-card>

        <!-- A53 temperatures  -->
        <q-card class="my-card text-white">
          <q-item>
            <q-item-section avatar>
              <q-avatar
                square
                size="48px"
              >
                <img src="~assets/thermometer.svg">
              </q-avatar>
            </q-item-section>

            <q-item-section>
              <q-item-label>A53 Temperature</q-item-label>
              <q-item-label
                style="color: white;"
                caption
              >
                iMX8 ARM Quad Core
              </q-item-label>
            </q-item-section>
          </q-item>

          <q-knob
            readonly
            v-model="tempA53"
            show-value
            font-size="25px"
            size="200px"
            :thickness="0.25"
            track-color="grey-3"
            :color="gauge_tempA53Color"
            class="text-white q-ma-md"
          >
            {{ tempA53 }} ºC
          </q-knob>
        </q-card>

        <!-- GPU Core1 temperature  -->
        <q-card class="my-card text-white">
          <q-item>
            <q-item-section avatar>
              <q-avatar
                square
                size="48px"
              >
                <img src="~assets/thermometer.svg">
              </q-avatar>
            </q-item-section>

            <q-item-section>
              <q-item-label>GPU Temperature</q-item-label>
              <q-item-label
                style="color: white;"
                caption
              >Vivante GC7000 </q-item-label>
            </q-item-section>
          </q-item>

          <q-knob
            readonly
            v-model="gpuTemp"
            show-value
            font-size="25px"
            size="200px"
            :thickness="0.25"
            track-color="grey-3"
            class="text-white q-ma-md"
            :color="gauge_gpuTempColor"
          >
            {{ gpuTemp }} ºC
          </q-knob>
        </q-card>

        <!-- CPU USAGE  -->
        <q-card class="my-card text-white">
          <q-item>
            <q-item-section avatar>
              <q-avatar
                square
                size="48px"
              >
                <img src="~assets/cpu.svg">
              </q-avatar>
            </q-item-section>

            <q-item-section>
              <q-item-label>CPU Usage</q-item-label>
              <q-item-label
                style="color: white;"
                caption
              >
                iMX8 Quad Max
              </q-item-label>
            </q-item-section>
          </q-item>

          <q-knob
            readonly
            v-model="cpu_usage"
            show-value
            font-size="25px"
            size="200px"
            :thickness="0.25"
            track-color="grey-3"
            :color="gauge_cpuColor"
            class="text-white q-ma-md"
          >
            {{ cpu_usage }} %
          </q-knob>
        </q-card>

      </div>

      <!-- CARDS FOR CHARTS USAGE -->
      <div class="q-pa-md row q-gutter-md">
        <!-- RAM memory usage  -->
        <q-card class="my-card text-white">
          <q-item>
            <q-item-section avatar>
              <q-avatar
                square
                size="48px"
              >
                <img src="~assets/ram-memory.svg">
              </q-avatar>
            </q-item-section>

            <q-item-section>
              <q-item-label>RAM Memory</q-item-label>
              <q-item-label
                style="color: white;"
                caption
              >Usage per time </q-item-label>
            </q-item-section>
          </q-item>

          <div class="chartRAM">
            <IEcharts
              :option="rambar"
              :loading="loading"
              @ready="onReady"
              theme="macarons2"
            />
          </div>
        </q-card>

        <!-- GPU memory usage  -->
        <q-card class="my-card text-white">
          <q-item>
            <q-item-section avatar>
              <q-avatar
                square
                size="48px"
              >
                <img src="~assets/graphics-card.svg">
              </q-avatar>
            </q-item-section>

            <q-item-section>
              <q-item-label>GPU Memory</q-item-label>
              <q-item-label
                style="color: white;"
                caption
              >Usage per time </q-item-label>
            </q-item-section>
          </q-item>

          <div class="chartRAM">
            <IEcharts
              :option="rambar"
              :loading="loading"
              @ready="onReady"
              theme="macarons2"
            />
          </div>
        </q-card>

      </div>
    </div>

    <div
      class="q-pa-md row q-gutter-md"
      style="max-width: 600px"
    >
      <!-- camera -->
      <q-card class="my-card text-white">
        <q-item>
          <q-item-section avatar>
            <q-avatar
              square
              size="48px"
            >
              <img src="~assets/camera.svg">
            </q-avatar>
          </q-item-section>

          <q-item-section>
            <q-item-label>Camera</q-item-label>
            <q-item-label
              style="color: white;"
              caption
            >
              Let's see some pasta
            </q-item-label>
          </q-item-section>
        </q-item>

        <web-cam
          ref="webcam"
          :device-id="deviceId"
          width="100%"
          @started="onStarted"
          @stopped="onStopped"
          @error="onError"
          @cameras="onCameras"
          @camera-change="onCameraChange"
        />

      </q-card>
    </div>

  </q-page>
</template>

<style lang="stylus" scoped>
/* .my-card {
  background: radial-gradient(circle, #444444 0%, #232323 100%);
}

.dash-card {
  width: 100%;
  max-width: 250px;
} */
.chartRAM {
  width: 480px;
  height: 300px;
}
</style>

<script>
import axios from 'axios'
import IEcharts from 'vue-echarts-v3/src/full.js'
import '../components/macarons2.js'
import { WebCam } from 'vue-web-cam'

export default {
  name: 'PageIndex',
  components: {
    WebCam,
    IEcharts
  },
  data () {
    return {
      tempA72: 0.0,
      tempA53: 0.0,
      cpu_usage: 0.0,
      gpuTemp: 0.0,
      gauge_tempA72Color: 'positive',
      gauge_tempA53Color: 'positive',
      gauge_gpuTempColor: 'positive',
      gauge_cpuColor: 'positive',
      camera: null,
      deviceId: null,
      devices: [],
      // memory chart
      loading: true,
      rambar_maxpoints: 20,
      rambar_localpoint: 0,
      rambar: {
        title: {
          text: ''
        },
        tooltip: {},
        xAxis: {
          data: [0, 1, 2]
        },
        yAxis: {},
        series: [{
          name: 'usage',
          type: 'line',
          data: [0, 1, 2]
        }]
      }
    }
  },
  computed: {
    device: function () {
      return this.devices.find(n => n.deviceId === this.deviceId)
    }
  },
  watch: {
    camera: function (id) {
      this.deviceId = id
    },
    devices: function () {
      // Once we have a list select the first one
      const list = this.devices
      console.log('Devices listed by electron')
      list.forEach(element => {
        console.log(element.label)
      })
      var first = list[0]
      if (first) {
        this.camera = first.deviceId
        this.deviceId = first.deviceId
      }
    }
  },
  methods: {
    setDynamicGaugeColor (tmp, color) {
      if (tmp > 80.0) {
        this[color] = 'negative'
      } else if (tmp > 50) {
        this[color] = 'warning'
      } else {
        this[color] = 'positive'
      }
    },
    monitorCPUTemperature () {
      setInterval(() => {
        const me = this
        // rest for gpu info
        axios.get('http://10.42.0.248:5001/gpu')
          .then(response => {
            if (response.data.temperatures !== undefined) {
              me.gpuTemp = response.data.temperatures.GPU0

              me.rambar_localpoint++
              if (me.rambar_localpoint >= me.rambar_maxpoints) {
                me.rambar_localpoint = 0
              }

              me.rambar.xAxis.data[me.rambar_localpoint] = me.rambar_localpoint
              me.rambar.series[0].data[me.rambar_localpoint] = response.data.memoryUsage

              // react
              me.rambar.series[0].data.push(0)
              me.rambar.series[0].data.splice(me.rambar.series[0].data.length - 1, 1)
              console.log(response.data.memoryUsage)

              me.setDynamicGaugeColor(me.gpuTemp, 'gauge_gpuTempColor')
            }
          })

        // rest for cpu
        axios.get('http://10.42.0.248:5001/cpu')
          .then(response => {
            if (response.data.temperatures !== undefined) {
              me.tempA72 = response.data.temperatures.A72
              me.tempA53 = response.data.temperatures.A53
              me.cpu_usage = response.data.usage

              me.setDynamicGaugeColor(me.tempA72, 'gauge_tempA72Color')
              me.setDynamicGaugeColor(me.tempA53, 'gauge_tempA53Color')
              me.setDynamicGaugeColor(me.cpu_usage, 'gauge_cpuColor')
            }
          })
      }, 1000)
    },
    /* camera methods */
    onCapture () {
      this.img = this.$refs.webcam.capture()
    },
    onStarted (stream) {
      console.log('On Started Event', stream)
    },
    onStopped (stream) {
      console.log('On Stopped Event', stream)
    },
    onStop () {
      this.$refs.webcam.stop()
    },
    onStart () {
      this.$refs.webcam.start()
    },
    onError (error) {
      console.log('On Error Event')
      console.error(error)
    },
    onCameras (cameras) {
      this.devices = cameras
      console.log('On Cameras Event', cameras)
    },
    onCameraChange (deviceId) {
      this.deviceId = deviceId
      this.camera = deviceId
      console.log('On Camera Change Event', deviceId)
    },
    // charts
    onReady (instance, ECharts) {
      console.log(instance, ECharts)
      this.loading = false
    },
    onClick (event, instance, ECharts) {
      console.log(arguments)
    }
  },
  created () {
    try {
      // try fullscreen stuff
      const electron = require('electron')
      var window = electron.remote.getCurrentWindow()
      window.setFullScreen(true)
    } catch (err) {
      console.warn(err)
    }

    this.monitorCPUTemperature()
  }
}
</script>
