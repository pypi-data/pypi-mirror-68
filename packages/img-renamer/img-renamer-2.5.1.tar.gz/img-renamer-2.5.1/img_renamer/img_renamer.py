#!/usr/bin/env python
from os import listdir
from os import path
from os import rename as osrename
from re import compile

from click import command, argument, option, version_option, Choice, confirm
from pkg_resources import require


@command()
@argument("folder", type=str)
@option("-l", "--logfile", default=False, is_flag=True, type=bool,
        help="Save logfile [rename.log].")
@option("-y", default=False, is_flag=True, type=bool,
        help='Automatic yes to prompts; assume "yes" as answer to all prompts'
             'and run non-interactively.')
@option("-n", "--nro", default=0, type=int,
        help="Define custom number to start counting from.")
@option("-z", "--zeroes", default=7, type=int,
        help="Define custom number of zeroes before number.")
@option("-m", "--mode", default="0", type=Choice(["0", "1"]),
        help="Choose what renaming mode to use.")
@version_option(version=require("img_renamer")[0].version)
def main(folder, logfile, y, nro, zeroes, mode):
    """img_renamer is a command line interface for renaming images in numberic
    order.
    Full documentation available at
    <https://gitlab.com/miicat/img-renamer/-/wikis/>


    Programmed by /u/Miicat_47"""
    args = {
        "logfile": logfile,
        "yes": y,
        "nro": nro,
        "zeroes": zeroes,
        "mode": mode
    }
    # regex variables
    img_extension = compile(r"\.[pngje]+$")
    img_numbers = compile(r"(^\d+)\.[pngje]+$")

    args = _check_args(**args)
    folder = _check_folder(folder)
    images, nro_total = _get_images(folder, img_extension)
    images_to_rename, nro_to_skip = _get_images_to_rename(images, nro_total,
                                                          img_extension,
                                                          img_numbers, **args)
    _rename_images(images_to_rename, folder, nro_total, nro_to_skip,
                   img_extension, **args)


def _check_args(**kwargs):
    nro = kwargs["nro"]
    zeroes = kwargs["zeroes"]
    kwargs["mode"] = int(kwargs["mode"])
    mode = kwargs["mode"]
    if zeroes < 0:
        print("Error: you can't have negative number of zeroes")
        exit(0)
    if nro < 0:
        print("Error: you can't start counting from negative number")
        exit(0)
    if not nro == 0 and mode == 1:
        print("Error: you can't change nro when fixing numbering")
        exit(0)
    if not zeroes == 7 and mode == 1:
        print("Error: you can't change zeroes when fixing numbering")
        exit(0)
    return kwargs


def _check_folder(folder):
    """Check that given folder exists. And adds slash to end if missing"""
    if path.exists(folder):
        if folder.endswith("/"):
            return folder
        else:
            return "{}/".format(folder)
    else:
        print("{}: No such directory".format(folder))
        exit(0)


def _get_images(folder, img_extension):
    """Get list of images in given folder"""
    imgs = listdir(folder)
    images = list()
    for image in imgs:
        if img_extension.search(image):
            images.append(image)
    return images, len(images)


def _get_images_to_rename(images, nro_total, img_extension, img_numbers,
                          **kwargs):
    """Get images that needs to be renamed"""
    mode = kwargs["mode"]
    zeroes = kwargs["zeroes"]
    nro = kwargs["nro"]
    nmax = nro_total
    images_to_rename = list()
    nro_to_skip = list()
    if mode == 1:
        # Find all numbers
        nros = list()
        nros_missing = list()
        # Get numbers to list
        for image in images:
            try:
                i = img_numbers.search(image).group(1)
            except AttributeError or IndexError:
                # a None would cause an AttributeError here;
                # IndexError by .group()
                continue
            if len(i) == zeroes:
                nros.append(int(i))
        # Findout what numbers are missing
        nros = sorted(nros)
        for i, n in enumerate(nros, start=nro + 1):
            while True:
                if not i == n:
                    nros_missing.append(i)
                    i += 1
                    break
                else:
                    i += 1
                    break
                i += 1
        # Create list what to rename to what
        images = sorted(images)
        if not len(nros_missing) == 0:
            for image in images:
                try:
                    i = img_numbers.search(image).group(1)
                except AttributeError or IndexError:
                    # a None would cause an AttributeError here;
                    # IndexError by .group()
                    # skip other images for now
                    continue
                if int(i) < nros_missing[0]:
                    continue
                ext = img_extension.search(image).group()
                images_to_rename.append([image, _generate_name(nros_missing[0],
                                        zeroes) + ext])
                del nros_missing[0]
                if int(i) not in nros_missing:
                    nros_missing.append(int(i))
                nros_missing = sorted(nros_missing)
        # Add other images to the end of the list
        i = nro_total
        for image in images:
            try:
                img_numbers.search(image).group(1)
            except AttributeError or IndexError:
                ext = img_extension.search(image).group()
                images_to_rename.append([image, _generate_name(i, zeroes)
                                        + ext])
                i += 1
    elif mode == 0:
        for image in images:
            try:
                i = img_numbers.search(image).group(1)
            except AttributeError or IndexError:
                images_to_rename.append(image)
                continue
            if int(i) > nmax + nro or int(i) < nro:
                # the range needs to be the range of numbers to use in renaming
                images_to_rename.append(image)
            elif not len(i) == zeroes:
                images_to_rename.append(image)
            else:
                nro_to_skip.append(int(i))
    if len(images_to_rename) == 0:
        print("Nothing to rename")
        exit(0)
    return images_to_rename, nro_to_skip


def _rename_images(images_to_rename, folder, nro_total, nro_to_skip,
                   img_extension, **kwargs):
    """Rename the images"""
    mode = kwargs["mode"]
    nro = kwargs["nro"]
    zeroes = kwargs["zeroes"]
    yes = kwargs["yes"]
    log = kwargs["logfile"]
    n = nro + 1
    rename = list()
    rename_total = 0
    # Create list of images to rename with name to rename to
    if mode == 1:
        # The list is already created in the previous function,
        #  so only copying
        for image in images_to_rename:
            rename.append([image[0], image[1]])
        rename_total = len(rename)
    elif mode == 0:
        for i in range(n, nro_total + n):
            # the range needs to be the range of numbers to use in renaming
            if i not in nro_to_skip:
                ext = img_extension.search(images_to_rename[0]).group()
                rename.append([images_to_rename[0], _generate_name(i, zeroes)
                              + ext])
                images_to_rename.remove(images_to_rename[0])
                rename_total += 1
            if len(images_to_rename) == 0:
                break
    # Ask about renaming
    if not yes:
        print("These will be renamed:")
        for n, x in enumerate(rename):
            print("{r0} -> {r1}".format(r0=rename[n][0], r1=rename[n][1]))
        print("_" * 20)
        print("Renaming {nro} of {total}".format(nro=rename_total,
                                                 total=nro_total))
        y = confirm("Are you sure you want to rename")
        if not y:
            print("Aborting")
            exit(0)
        if not log:
            y = confirm("Do you want to save a log file")
            if y:
                _create_log(rename)
        else:
            _create_log(rename)
    elif log:
        _create_log(rename)
    if yes:
        print("Renaming:")
        for n, x in enumerate(rename):
            print("{r0} -> {r1}".format(r0=rename[n][0], r1=rename[n][1]))
        print("_" * 20)
        print("Renaming {nro} of {total}".format(nro=rename_total,
                                                 total=nro_total))
    # Rename images with xxx prefix
    for n, x in enumerate(rename):
        osrename("{folder}{r0}".format(folder=folder, r0=rename[n][0]),
                 "{folder}xxx{r1}".format(folder=folder, r1=rename[n][1]))
    # Rename images to correct name
    for n, x in enumerate(rename):
        osrename("{folder}xxx{r1}".format(folder=folder, r1=rename[n][1]),
                 "{folder}{r1}".format(folder=folder, r1=rename[n][1]))


def _generate_name(number, zeroes):
    """Generate the number name of the image"""
    n = zeroes - len(str(number))
    return "0" * n + str(number)


def _create_log(rename_list):
    """Create list of what was renamed to what"""
    text = ""
    for n, x in enumerate(rename_list):
        text += "{r0} -> {rl1}\n".format(r0=rename_list[n][0],
                                         rl1=rename_list[n][1])
    with open("rename.log", "w+") as f:
        f.write(text)


if __name__ == "__main__":
    main()
