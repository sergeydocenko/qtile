local wezterm = require 'wezterm'

return {
    color_scheme = "Tokyo Night",

    font      = wezterm.font("Source Code Pro"),
    font_size = 14,

    window_padding = {
        left   = 5,
        right  = 5,
        top    = 5,
        bottom = 5
    },

    use_fancy_tab_bar = false,
    hide_tab_bar_if_only_one_tab = false,
    tab_bar_at_bottom = true,
}