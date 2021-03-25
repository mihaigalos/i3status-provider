## i3status-provider

The i3status-provider is an easily extendable provider for the i3status to display in the i3wm's bar.
Current integrations are the ones which reference the various submodules in the repo.

## Screenshot

![](i3status_bar.png)

## Usage

Change the `/etc/i3status.conf` so it contains:

```
general {
        colors = true
        interval = 60
        output_format = "i3bar"
}
```


```
ln -s $(realpath config/i3/config) ~/.config/i3/config
```
