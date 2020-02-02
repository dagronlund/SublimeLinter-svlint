SublimeLinter-svlint
================================

Originally forked from (https://github.com/likewise/SublimeLinter-contrib-xsvlog) which further forked from (https://github.com/BrunoJJE/SublimeLinter-contrib-xvhdl)

This linter plugin for [SublimeLinter][docs] provides an interface to [xvlog (from Xilinx Vivado Simulator)](http://www.xilinx.com/products/design-tools/vivado.html) and other SystemVerilog linters, with some added project management facilities.

## Installation
SublimeLinter 4 must be installed in order to use this plugin. If SublimeLinter 4 is not installed, please follow the instructions [here][installation].

### Linter installation
Before using this plugin, you must ensure that Vivado is installed on your system and `xvlog` is on your path. To install Vivado, follow the instruction given in [this PDF document](http://www.xilinx.com/support/documentation/sw_manuals/xilinx2014_4/ug973-vivado-release-notes-install-license.pdf) page.

**Note:** This plugin requires `xvlog` from Xilinx Vivado 2014.4 or later.

### Linter configuration
In order for `xvlog` to be executed by SublimeLinter, you must ensure that its path is available to SublimeLinter. Before going any further, please read and follow the steps in [“Finding a linter executable”](http://sublimelinter.readthedocs.org/en/latest/troubleshooting.html#finding-a-linter-executable) through “Validating your PATH” in the documentation.

Once you have installed and configured `xvlog`, you can proceed to install the SublimeLinter-contrib-xvhdl plugin if it is not yet installed.

### Plugin installation
Please use [Package Control][pc] to install the linter plugin. This will ensure that the plugin will be updated when new versions are available. If you want to install from source so you can modify the source code, you probably know what you are doing so we won’t cover that here.

To install via Package Control, do the following:

1. Within Sublime Text, bring up the [Command Palette][cmd] and type `install`. Among the commands you should see `Package Control: Install Package`. If that command is not highlighted, use the keyboard or mouse to select it. There will be a pause of a few seconds while Package Control fetches the list of available plugins.

1. When the plugin list appears, type `xvhdl`. Among the entries you should see `SublimeLinter-contrib-xvhdl`. If that entry is not highlighted, use the keyboard or mouse to select it.

## Settings
For general information on how SublimeLinter works with settings, please see [Settings][settings]. For information on generic linter settings, please see [Linter Settings][linter-settings].

[docs]: http://sublimelinter.readthedocs.org
[installation]: http://sublimelinter.readthedocs.org/en/latest/installation.html
[locating-executables]: http://sublimelinter.readthedocs.org/en/latest/usage.html#how-linter-executables-are-located
[pc]: https://sublime.wbond.net/installation
[cmd]: http://docs.sublimetext.info/en/sublime-text-3/extensibility/command_palette.html
[settings]: http://sublimelinter.readthedocs.org/en/latest/settings.html
[linter-settings]: http://sublimelinter.readthedocs.org/en/latest/linter_settings.html
[inline-settings]: http://sublimelinter.readthedocs.org/en/latest/settings.html#inline-settings
