# aws-nxp-ai-at-the-edge-gui #

Local graphical user interface (GUI) for the collaborative demo with Amazon
and NXP to plug a [Toradex](https://www.toradex.com/) Computer on Module using
the embedded Linux [Torizon](https://www.toradex.com/operating-systems/torizon)
platform to AWS services such as AWS IoT Greengrass and Amazon SageMaker Neo.

# How to Use #

This software is part of the [AWS AI at the Edge Pasta Detection Demo](https://developer.toradex.com/knowledge-base/object-detection-demo-with-aws-sagemaker-neo-and-torizon)
designed to run on the [Apalis iMX8 Embedded Vision Kit with Allied Vision](https://developer.toradex.com/knowledge-base/apalis-imx8-embedded-vision-kit-with-allied-vision).

You can find additional information about this demonstration on the following
resources of the [Toradex developer website](https://developer.toradex.com/):

- How to use the demo and additional resources:
[AWS AI at the Edge Pasta Detection Demo](https://developer.toradex.com/knowledge-base/object-detection-demo-with-aws-sagemaker-neo-and-torizon)
- [Apalis iMX8 Embedded Vision Kit with Allied Vision](https://developer.toradex.com/knowledge-base/apalis-imx8-embedded-vision-kit-with-allied-vision)

# Developer Information #

A Quasar Framework app

## Install the dependencies ##
```bash
npm install
```

### Start the app in development mode (hot-code reloading, error reporting, etc.) ###
```bash
quasar dev
```

### Lint the files ###
```bash
npm run lint
```

### Build the app for production ###
```bash
quasar build
```

### Customize the configuration ###
See [Configuring quasar.conf.js](https://quasar.dev/quasar-cli/quasar-conf-js).
