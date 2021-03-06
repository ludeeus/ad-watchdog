# ad-watchdog

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

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
        - entity: sensor.battery
          below: 30
        - entity: binary_sensor.heat_bedroom
        - entity: sensor.battery2
          above: 80
    - name: livingroom
      entities:
        - entity: sensor.battery
          state: unknown
          below: 30
        - entity: binary_sensor.heat_bedroom
          state: off
        - entity: sensor.battery2
          above: 80
```

key | optional | type | default | description
-- | -- | -- | -- | --
`module` | False | string | | The module name of the app.
`class` | False | string | | The name of the Class.
`state_normal` | True | string | All good | The state that will be used for the watchdog entity when everything is OK.
`state_offline` | True | string | Something is wrong! | The state that will be used for the watchdog entity when one or more watched entity are offline.
`watchdogs` | False | list | | A list of watchdogs.
`watchdogs[name]` | False | string | | The name of the watchdog.
`watchdogs[icon]` | True | string | "mdi:eye" | The name of the watchdog.
`watchdogs[entities]` | False | string | | A list of entites for the watchdog to monitor.
`watchdogs[entities][entity]` | False | string | | The entity ID of an entity to monitor.
`watchdogs[entities][above]` | True | string | off | A state to match for the trigger
`watchdogs[entities][below]` | True | int | | A int to match for the trigger
`watchdogs[entities][state]` | True | int | | A int to match for the trigger
