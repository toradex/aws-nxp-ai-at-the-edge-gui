<template>
  <q-page class="q-pa-md row items-start q-gutter-md flex flex-center">

    <q-img
      src="statics/partneraws2.png"
      class="fixed-top"
      style="height: 215px; width: 705px;"
    />

    <div class="q-pa-md q-gutter-md fallback">

      <!-- PASTA DETECTION INFO -->
      <div class="q-pa-md row items-start q-gutter-md justify-center">
        <!-- pasta1  -->
        <q-card class="my-pasta text-white">
          <q-img
            src="statics/farfalle.png"
            style="height: 212px; width: 212px;"
          >
            <div class="absolute-top text-subtitle2 text-center">
              <q-linear-progress
                dark
                rounded
                style="height: 20px"
                :value="progress1"
                color="positive"
              />
              <div class="text-white set-position">Confidence {{ (progress1 * 100).toFixed(0) }} %</div>
            </div>
          </q-img>
        </q-card>

        <!-- pasta2  -->
        <q-card class="my-pasta text-white">
          <q-img
            src="statics/fusine.png"
            style="height: 212px; width: 212px;"
          >
            <div class="absolute-top text-subtitle2 text-center">
              <q-linear-progress
                dark
                rounded
                style="height: 20px"
                :value="progress2"
                color="warning"
              />
              <div class="text-white set-position">Confidence {{ (progress2 * 100).toFixed(0) }} %</div>
            </div>
          </q-img>
        </q-card>

        <!-- pasta3  -->
        <q-card class="my-pasta text-white">
          <q-img
            src="statics/shell.png"
            style="height: 212px; width: 212px;"
          >
            <div class="absolute-top text-subtitle2 text-center">
              <q-linear-progress
                dark
                rounded
                style="height: 20px"
                :value="progress3"
                color="negative"
              />
              <div class="text-white set-position">Confidence {{ (progress3 * 100).toFixed(0) }} %</div>
            </div>
          </q-img>
        </q-card>

        <!-- pasta4  -->
        <q-card class="my-pasta text-white">
          <q-img
            src="statics/elbow.png"
            style="height: 212px; width: 212px;"
          >
            <div class="absolute-top text-subtitle2 text-center">
              <q-linear-progress
                dark
                rounded
                style="height: 20px"
                :value="progress4"
                color="negative"
              />
              <div class="text-white set-position">Confidence {{ (progress4 * 100).toFixed(0) }} %</div>
            </div>
          </q-img>
        </q-card>

      </div>

      <!-- CPU INFO -->
      <div class="q-pa-md row q-gutter-md justify-center">

        <!-- Conveyor belt  -->
        <q-card
          class="my-card text-white"
        >
          <q-item>
            <q-item-section avatar>
              <q-avatar
                square
                size="48px"
              >
                <img src="~assets/speedometer.svg">
              </q-avatar>
            </q-item-section>

            <q-item-section>
              <q-item-label>Conveyor Belt</q-item-label>
              <q-item-label
                style="color: white;"
                caption
              >
                Motor Speed
              </q-item-label>
            </q-item-section>
          </q-item>

          <div class="row justify-center no-gauge-distance">
            <q-linear-progress
              dark
              rounded
              style="height: 40px"
              :value="motorSpeed"
              :color="gauge_motorSpee"
            />
            <div class="text-white no-gauge">{{ (motorSpeed * 100).toFixed(0) }} %</div>
          </div>
        </q-card>

        <!-- A72 temperatures  -->
        <q-card class="my-card text-white">
          <q-item>
            <q-item-section avatar>
              <q-avatar
                square
                size="48px"
              >
                <img src="~assets/lamp.svg">
              </q-avatar>
            </q-item-section>

            <q-item-section>
              <q-item-label>Conveyor Belt</q-item-label>
              <q-item-label
                style="color: white;"
                caption
              >LED Brightness</q-item-label>
            </q-item-section>
          </q-item>

          <div class="row justify-center no-gauge-distance">
            <q-linear-progress
              dark
              rounded
              style="height: 40px"
              :value="tempA72"
              :color="gauge_tempA72Color"
            />
            <div class="text-white no-gauge">{{ (tempA72 * 100).toFixed(0) }} %</div>
          </div>
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
              <q-item-label>i.MX 8QM CPUs</q-item-label>
              <q-item-label
                style="color: white;"
                caption
              >
                Temperature
              </q-item-label>
            </q-item-section>
          </q-item>

          <div class="row justify-center no-gauge-distance">
            <q-linear-progress
              dark
              rounded
              style="height: 40px"
              :value="tempA53"
              :color="gauge_tempA53Color"
            />
            <div class="text-white no-gauge">{{ (tempA53 * 100).toFixed(0) }} °C</div>
          </div>
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
              <q-item-label>GPU GC7000</q-item-label>
              <q-item-label
                style="color: white;"
                caption
              >Temperature </q-item-label>
            </q-item-section>
          </q-item>

          <div class="row justify-center no-gauge-distance">
            <q-linear-progress
              dark
              rounded
              style="height: 40px"
              :value="gpuTemp"
              :color="gauge_gpuTempColor"
            />
            <div class="text-white no-gauge">{{ (gpuTemp * 100).toFixed(0) }} °C</div>
          </div>
        </q-card>

      </div>

      <!-- CARDS FOR CHARTS USAGE -->
      <div class="q-pa-md row q-gutter-md justify-center">

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
              <q-item-label>i.MX 8QM</q-item-label>
              <q-item-label
                style="color: white;"
                caption
              >
                CPU AVG Usage
              </q-item-label>
            </q-item-section>
          </q-item>

          <div class="row justify-center no-gauge-distance">
            <q-linear-progress
              dark
              rounded
              class="notransition"
              style="height: 40px"
              :value="cpu_usage"
              :color="gauge_cpuColor"
            />
            <div class="text-white no-gauge">{{ (cpu_usage * 100).toFixed(0) }} %</div>
          </div>
        </q-card>

        <!-- RAM memory usage  -->
        <q-card class="text-white my-card">
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
              >Usage percent </q-item-label>
            </q-item-section>
          </q-item>

          <div class="row justify-center no-gauge-distance">
            <q-linear-progress
              dark
              rounded
              style="height: 40px"
              :value="ramMem"
              :color="ramMemColor"
            />
            <div class="text-white no-gauge">{{ (ramMem * 100).toFixed(0) }} %</div>
          </div>
        </q-card>

        <!-- GPU memory usage  -->
        <q-card class="text-white my-card">
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
              >Usage percent </q-item-label>
            </q-item-section>
          </q-item>

          <div class="row justify-center no-gauge-distance">
            <q-linear-progress
              dark
              rounded
              style="height: 40px"
              :value="gpuMem"
              :color="gpuMemColor"
            />
            <div class="text-white no-gauge">{{ (gpuMem * 100).toFixed(0) }} %</div>
          </div>
        </q-card>

      </div>
    </div>

    <div
      class="q-pa-md row q-gutter-md fallback"
      style="max-width: 800px"
    >
      <!-- camera -->
      <q-card class="text-white">
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
          width="800"
          height="640"
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
.my-card {
  height: 150px;
  width: 212px;
  max-height: 212px !important;
}

.my-pasta {
  height: 212px;
  width: 212px;
  max-height: 212px !important;
}

.chartRAM {
  width: 480px;
  height: 200px;
}

.progressRAM {
  width: 440px;
  height: 98px;
}

.fallback {
  margin-top: 130px;
}

.q-pa-md {
  padding: 0px !important;
}

.set-position {
  position: inherit;
  bottom: 15px;
  text-align: center;
  width: 90%;
}

.no-gauge {
  margin-top: -35px;
  z-index: 99;
}

.no-chart {
  margin-top: -50px;
  z-index: 99;
}

.no-gauge-distance {
  padding: 15px;
  font-weight: bold;
  font-size: 20px;
}

.notransition {
  -webkit-transition: none !important;
  -moz-transition: none !important;
  -o-transition: none !important;
  transition: none !important;
}
</style>

<script>
import axios from 'axios'
import '../components/macarons2.js'
import { WebCam } from 'vue-web-cam'

export default {
  name: 'PageIndex',
  components: {
    WebCam
  },
  data () {
    return {
      restAddr: 'localhost',
      restAddr2: 'localhost',
      statusInfoPort: '5001',
      controlPort: '5002',
      tempA72: 0.0,
      tempA53: 0.0,
      cpu_usage: 0.0,
      gpuTemp: 0.0,
      gpuMem: 0.0,
      ramMem: 0.0,
      motorSpeed: 0.0,
      gauge_tempA72Color: 'positive',
      gauge_tempA53Color: 'positive',
      gauge_gpuTempColor: 'positive',
      gauge_cpuColor: 'positive',
      gauge_motorSpee: 'positive',
      gpuMemColor: 'positive',
      ramMemColor: 'positive',
      progress1: 0.8,
      progress2: 0.5,
      progress3: 0.3,
      progress4: 0.5,
      camera: null,
      deviceId: null,
      devices: []
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
      if (tmp > 0.8) {
        this[color] = 'negative'
      } else if (tmp > 0.5) {
        this[color] = 'warning'
      } else {
        this[color] = 'positive'
      }
    },
    setDynamicGaugeColorInvert (tmp, color) {
      if (tmp > 0.8) {
        this[color] = 'positive'
      } else if (tmp > 0.5) {
        this[color] = 'warning'
      } else {
        this[color] = 'negative'
      }
    },
    monitorCPUTemperature () {
      setInterval(() => {
        const me = this
        // rest cpu, gpu info
        axios.get('http://' + this.restAddr + ':' + me.statusInfoPort + '/all')
          .then(response => {
            if (response.data.gpu.temperatures !== undefined) {
              me.gpuTemp = (response.data.gpu.temperatures.GPU0 / 100.0).toFixed(2)
              let tempA72 = (response.data.cpu.temperatures.A72 / 100.0).toFixed(2)
              me.tempA53 = (response.data.cpu.temperatures.A53 / 100.0).toFixed(2)
              me.cpu_usage = (response.data.cpu.usage / 100.0).toFixed(2)
              me.gpuMem = (response.data.gpu.memoryUsage / 100).toFixed(2)
              me.ramMem = (response.data.ram.usage / 100).toFixed(2)

              me.tempA53 = Math.max(me.tempA53, tempA72)

              me.setDynamicGaugeColor(me.gpuTemp, 'gauge_gpuTempColor')
              me.setDynamicGaugeColor(me.tempA53, 'gauge_tempA53Color')
              me.setDynamicGaugeColor(me.cpu_usage, 'gauge_cpuColor')
              me.setDynamicGaugeColor(me.ramMem, 'ramMemColor')
              me.setDynamicGaugeColor(me.gpuMem, 'gpuMemColor')
            }
          })

        // rest for the conveyor belt speed
        axios.get('http://' + this.restAddr2 + ':' + me.controlPort + '/cb')
          .then(response => {
            me.motorSpeed = (response.data.speed / 100.0).toFixed(2)
            me.setDynamicGaugeColorInvert(me.motorSpeed, 'gauge_motorSpee')
          })

        // rest for the conveyior belt led brightness
        axios.get('http://' + this.restAddr2 + ':' + me.controlPort + '/led')
          .then(response => {
            me.tempA72 = (response.data.brightness).toFixed(2)
            me.setDynamicGaugeColorInvert(me.tempA72, 'gauge_tempA72Color')
          })
      }, 2000)
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
      this.gpumemloading = false
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
    console.log('Created')
  }
}
</script>
