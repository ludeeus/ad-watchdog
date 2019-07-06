"""Watchdog App for AppDaemon."""
import appdaemon.plugins.hass.hassapi as hass


class Watchdog(hass.Hass):
    """The Watchdog class."""
    def initialize(self):
        """initialize the app."""
        self.log("Starting watchdogs.")
        configuration = self.validate_config(self.args)
        if not configuration:
            return
        watchdogs = self.args['watchdogs']
        for watchdog in watchdogs:
            self.log("Configuring {} watchdog".format(watchdog["name"]))
            for entity in watchdog["entities"]:
                entity_state = self.get_state(entity, attribute="all")
                if entity_state is None:
                    self.log("{} does not exsist :(".format(entity))
                    continue
                attributes = entity_state.get("attributes", {})
                if not attributes.get("watchdogs"):
                    attributes["watchdogs"] = [watchdog["name"]]
                else:
                    if isinstance(attributes["watchdogs"], list):
                        if watchdog["name"] not in attributes["watchdogs"]:
                            attributes["watchdogs"].append(watchdog["name"])
                    else:
                        attributes["watchdogs"] = [attributes["watchdogs"]]
                self.set_state(entity, attributes=attributes)
                self.listen_state(self.update_watchdog, entity)
                self.update_watchdog(entity, None, None, entity_state.get("state"), None)


    def update_watchdog(self, entity, attribute, old, new, kwargs):
        """Update the watchdog info."""
        entity_state = self.get_state(entity, attribute="all")
        attributes = entity_state.get("attributes", {})
        self.log(attributes)
        if new == "on":
            for watchdog in attributes.get("watchdogs", []):
                watchdog_state = self.get_state("watchdog.{}".format(watchdog), attribute="all")
                watchdog_attributes = watchdog_state.get("attributes", {})
                entities = watchdog_attributes.get("entities", [])
                if entity in entities:
                    entities.remove(entity)
                if entities:
                    self.set_state("watchdog.{}".format(watchdog),
                                   state=self.state_offline,
                                   attributes={"entities": entities})
                else:
                    self.set_state("watchdog.{}".format(watchdog),
                                   state=self.state_normal,
                                   attributes={"entities": []})
        elif new == "off"::
            for watchdog in attributes.get("watchdogs", []):
                watchdog_state = self.get_state("watchdog.{}".format(watchdog), attribute="all")
                watchdog_attributes = watchdog_state.get("attributes", {})
                entities = watchdog_attributes.get("entities", [])
                if entity not in entities:
                    entities.append(entity)
                self.set_state("watchdog.{}".format(watchdog),
                               state=self.state_offline,
                               attributes={"entities": entities})

    def validate_config(self, config):
        """Validate the configuration."""
        self.state_normal = config.get("state_normal", "All good")
        self.state_offline = config.get("state_offline", "Something is wrong!")

        if not isinstance(config["watchdogs"], list):
            self.log("Config option 'watchdogs' is not a list!")
            return False

        for watchdog in config["watchdogs"]:
            if not isinstance(watchdog, dict):
                self.log("Config option 'watchdogs[{}]' is not a dictionary!".format(watchdog))
                return False

            if watchdog.get("name") is None:
                self.log("Required config option 'watchdogs[][name]' is missing!")
                return False

            if not isinstance(watchdog.get("entities"), list):
                self.log("Config option 'watchdogs[][entities]' is not a list!")
                return False

            if not watchdog.get("entities"):
                self.log("Required config option 'watchdogs[][entities]' is missing!")
                return False
        return True
