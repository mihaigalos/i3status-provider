# i3status-provider

One may choose to use the purely awesome i3 window manager. Change the `/etc/i3status.conf` so it contains:

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
