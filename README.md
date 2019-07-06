# ad-watchdog

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

_Watchdog app for AppDaemon._

This will create a new entity for each watchdog that you can use in automations.
You can add the same entity to multiple watchdogs.

## Installation

Download the `watchdog` directory from inside the `apps` directory here to your local `apps` directory, then add the configuration to enable the `watchdog` module.

## Example App configuration

```yaml
watchdog:
  module: watchdog
  class: Watchdog
  state_normal: All good
  state_offline: Something is wrong!
  watchdogs:
    - name: bedroom
      entities:
        - binary_sensor.heat_bedroom
        - binary_sensor.heat_bedroom1
        - binary_sensor.heat_bedroom2
    - name: livingroom
      entities:
        - binary_sensor.heat_livingroom
        - binary_sensor.heat_livingroom1
        - binary_sensor.heat_livingroom2
```

key | optional | type | default | description
-- | -- | -- | -- | --
`module` | False | string | | The module name of the app.
`class` | False | string | | The name of the Class.
`state_normal` | True | string | All good | The state that will be used for the watchdog entity when everything is OK.
`state_offline` | True | string | Something is wrong! | The state that will be used for the watchdog entity when one or more watched entity are offline.
`watchdogs` | False | list | | A list of watchdogs.
`watchdogs[name]` | False | string | | The name of the watchdog.
`watchdogs[entities]` | False | string | | A list of entity_id's for the watchdog to monitor.
