# i3status-provider

The i3status-provider is an easily extendable provider for the i3status to display in the i3wm's bar.
Current integrations are the ones which reference the various submodules in the repo.

#Usage

Change the `/etc/i3status.conf` so it contains:

```
general {
        colors = true
        interval = 60
        output_format = "i3bar"
}
```

Next, edit your `/.config/i3/config` remove the `bar` block and replace it with:
```
bar {
    status_command <i3wm_wrapper>/i3wm_wrapper.sh
}
```
