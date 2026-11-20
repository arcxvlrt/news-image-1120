# World news of Friday 20 November 2026, in one image

Entry for the make.fun bounty "Sum up 20 November's world news in one image".

![entry](entry.png)

One lead story (Russian missiles violating Polish airspace, Ukraine, Putin rejecting a ceasefire) and
six smaller ones (Iran war, ICJ genocide ruling on Myanmar, Shenzhen summit, COP31, Estonia border
closure, Italian general strike). Facts, event dates and sources are in [NOTES.md](NOTES.md).

## Run it

```sh
python main.py   # Python 3.13, standard library only; copies entry.png to /output/entry.png
```

`main.py` copies the prebuilt `entry.png`, so every run is byte-identical and needs no network.

## Regenerate the image

```sh
pip install pillow
python make_image.py   # redraws entry.png from the bundled fonts, deterministically
```

Fonts: Barlow and Barlow Condensed (SIL Open Font License 1.1, see `fonts/OFL.txt`).

## License

MIT, see [LICENSE](LICENSE).
