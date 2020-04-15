# Tasmota Switch

[![Donate on Liberapay](https://liberapay.com/assets/widgets/donate.svg)](https://liberapay.com/chaptergy/donate)
<a href="https://www.buymeacoffee.com/chaptergy" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-yellow.png" alt="Donate on Buy Me A Coffee" height="30" width="127"></a>

_Component to integrate with [Tasmota](https://tasmota.github.io/docs) switches._

**This component will set up the following platforms:**

Platform | Description
-- | --
`switch` | Switch the device on or off.

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `tasmota_switch`.
4. Download _all_ the files from the `custom_components/tasmota_switch/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. Choose:
   - In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Tasmota Switch"
   - Add `tasmota_switch:` to your HA configuration.

## Example configuration.yaml

```yaml
tasmota_switch:
  - url: 192.168.1.20
    name: My Tasmota Plug
  - url: 192.168.1.21
  - url: 192.168.1.22
    username: admin
    password: mysupersecretpassword
```

## Configuration options

Key | Type | Required | Description
-- | -- | -- | --
`url` | `string` | `True` | The IP-address or domain of the Tasmota device.
`name` | `string` | `False` | A display name for the device. If not set, the friendly name set in Tasmota will be used.
`username` | `string` | `False` | If a webUI password is set, authentication is required. The username is usually _admin_.
`password` | `string` | `False` | If a webUI password is set, authentication is required.

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)
