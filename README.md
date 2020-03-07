# EngAutoComplete: A LaTeX Plugin for Sublime Text 3
Sublime Plugin for latex writing based on AllAutoComplete, which can easily import English Examples by inputting the keyword

# EngAutoComplete: 

by Sean

*Latest revision:* v1.0 (2020-03-07).



*Headline features*:

- Pop-up window shows the relevant English examples(i.e., English Library) on hover any words in tex files
- Quickpanel now shows just the active relevant documents (*.md) when using (super/ctrl+shift+alt+s)
- keep AllAutoComplete Features (AutoComplete from all active views)

## Preview

1.**Pop-up window** with relevant English examples show up when your mouse hover on a word in tex file, you can select one to navigate to the source.

2.**Quickpanel** show up by pressing ctrl+alt+shift+s (windows) or super+alt+shift+s (Mac) , you can input keywords to filter and navigate to the source.

![EngAutoComplete](/Users/flyln/Documents/个人/EngAutoComplete.gif)



## Overview

This plugin provides several features that simplify working with LaTeX files:

- **Pop-up window** with relevant English examples show up when your mouse hover on a word in tex file, you can select one to navigate to the source
- **Quickpanel** show up by pressing ctrl+alt+shift+s (windows) or super+alt+shift+s (Mac) , you can input keywords to filter and navigate to the source
- **AutoComplete** from all active documents which is offered by AllAutoComplete

## Requirements and Setup

The easiest way to install EngAutoComplete is via [Package Control](https://packagecontrol.io/). See [the Package Control installation instructions](https://packagecontrol.io/installation) for details on how to set it up (it's very easy.) Once you have Package Control up and running, invoke it (via the **Command Palette** from the Tools menu, or from Preferences), select the **Install Package** command, and find **EngAutoComplete**.

If you prefer a more hands-on approach, you can always clone the git repository, or else just grab this plugin's .zip file from GitHub and extract it to your Packages directory (you can open it easily from ST, by clicking on **Preferences > Browse Packages**). Then, (re)launch ST. Please note that if you do a manual installation, the Package **must** be named **EngAutoComplete**.

Before you start to work, as shown below, you should open your English Libraries  (be active in ST3) and make sure every example is splitted by empty line. **Markdown** is only supported by default, which is configurable by Package Settings.

![image-20200307160446453](/Users/flyln/Library/Application Support/typora-user-images/image-20200307160446453.png)

Finally, you'll need to have a working TeX installation and a PDF viewer. For detailed instructions on how to set these up, please email me(xyf_uestc@163.com).

## Bugs, issues & feature requests

Help for troubleshooting common issues can be found in the [Troubleshooting](#troubleshooting) section at the end of this README. For other bugs, issues or to request new features, please get in touch with us via [Github](https://github.com/SublimeText/LaTeXTools).

**Please** [search for existing issues and pull requests](https://github.com/SublimeText/LaTeXTools/issues/?q=is%3Aopen)before [opening a new issue](https://github.com/SublimeText/LaTeXTools/issues/new).

## Acknowledgements

Thank Xiongyu Zhu, who contributed for coding support. 

*If you have contributed and I haven't acknowledged you, email me!*