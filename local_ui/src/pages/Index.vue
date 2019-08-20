<template>
  <!--<q-page class="flex flex-center">
    <img alt="Quasar logo" src="~assets/quasar-logo-full.svg">
  </q-page> -->
  <q-page class="q-pa-md row items-start q-gutter-md flex flex-center">

    <!-- A72 temperatures  -->
    <q-card class="my-card text-white">
      <q-item>
        <q-item-section avatar>
          <q-avatar size="48px">
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
        font-size="50px"
        size="300px"
        :thickness="0.25"
        track-color="grey-3"
        class="text-white q-ma-md"
        :color="gcor"
      >
        {{ tempA72 }} ºC
      </q-knob>
    </q-card>

    <!-- A53 temperatures  -->
    <q-card class="my-card text-white">
      <q-item>
        <q-item-section avatar>
          <q-avatar size="48px">
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
        font-size="50px"
        size="300px"
        :thickness="0.25"
        track-color="grey-3"
        :color="gcor"
        class="text-white q-ma-md"
      >
        {{ tempA53 }} ºC
      </q-knob>
    </q-card>

  </q-page>
</template>

<style lang="stylus" scoped>
.my-card {
  background: radial-gradient(circle, #444444 0%, #232323 100%);
}
</style>

<script>
import axios from 'axios'

export default {
  name: 'PageIndex',
  data () {
    return {
      tempA72: 0.0,
      tempA53: 0.0,
      gcor: 'blue'
    }
  },
  methods: {
    consolo () {
      setInterval(() => {
        const me = this
        axios.get('http://10.42.0.248:5001/cpu')
          .then(response => {
            if (response.data.temperatures !== undefined) {
              me.tempA72 = response.data.temperatures.A72
              me.tempA53 = response.data.temperatures.A53
            }
          })

        if (this.tempA72 > 80.0) {
          this.gcor = 'red'
        } else if (this.tempA72 > 50) {
          this.gcor = 'warning'
        }
      }, 1000)
    }
  },
  created () {
    this.consolo()
  }
}
</script>
