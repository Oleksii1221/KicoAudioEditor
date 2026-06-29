# Installation

## Windows

Use the installer from the latest GitHub Release:

1. Download `KAE-Setup-<version>.exe`.
2. Run the installer.
3. Keep the desktop shortcut option enabled if desired.
4. Launch KAE from the Start Menu or desktop.

The installer is per-user by default and does not require administrator rights.

## Portable Windows

1. Download `KAE-<version>-windows-x64-portable.zip`.
2. Extract it.
3. Run `KAE.exe`.

## Ubuntu / Debian

Download the `.deb` package and install it:

```bash
sudo apt install ./kae_<version>_amd64.deb
```

## Fedora / RHEL

Download the `.rpm` package and install it:

```bash
sudo dnf install ./kae-<version>-1.x86_64.rpm
```

## AppImage

Download the AppImage, make it executable, and run it:

```bash
chmod +x KAE-<version>-x86_64.AppImage
./KAE-<version>-x86_64.AppImage
```

## Arch Linux

Use `packaging/linux/PKGBUILD` as the packaging template for an Arch build.
