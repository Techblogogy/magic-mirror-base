# Magic Mirror (ReadMe is still WIP)

[![Version](https://img.shields.io/badge/version-1.0.0-brightgreen.svg)]()
[![licence](https://img.shields.io/badge/licence-GPLv3-blue.svg)]()
[![OpenSource](https://badges.frapsoft.com/os/v2/open-source.svg?v=102)]()

Open Source Smart Mirror software for Raspberry PI.

## Installation

Open up terminal on raspberry pi and type this in.

```bash
curl -sL https://raw.githubusercontent.com/Techblogogy/magic-mirror-base/master/installer/install.sh | bash
```

This will automatically download magic mirror software and install it. Before use you'll have to edit this `~/.local/share/mirror_server/config.cfg` with correct API keys and modify camera preview position based on your screen resolution.

To start the interface simply use this command

```bash
mirror
```


## Authors

Developed by [Fedor Bobylev](https://techblogogy.github.io), [Tanya Batsenko](https://www.facebook.com/tanya.batsenko), [Zhenya Kravchenko](https://www.facebook.com/profile.php?id=100003291290867)
