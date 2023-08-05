# Copyright 2020 Oliver Smith
# SPDX-License-Identifier: GPL-3.0-or-later
import configparser
import logging
import os

import pmb.config
import pmb.helpers.git


def check_legacy_folder():
    # Existing pmbootstrap/aports must be a symlink
    link = pmb.config.pmb_src + "/aports"
    if os.path.exists(link) and not os.path.islink(link):
        raise RuntimeError("The path '" + link + "' should be a"
                           " symlink pointing to the new pmaports"
                           " repository, which was split from the"
                           " pmbootstrap repository (#383). Consider"
                           " making a backup of that folder, then delete"
                           " it and run 'pmbootstrap init' again to let"
                           " pmbootstrap clone the pmaports repository and"
                           " set up the symlink.")


def clone(args):
    # Explain sudo-usage before using it the first time
    logging.info("pmbootstrap does everything in Alpine Linux chroots, so your"
                 " host system does not get modified. In order to work with"
                 " these chroots, pmbootstrap calls 'sudo' internally. To see"
                 " the commands it runs, you can run 'pmbootstrap log' in a"
                 " second terminal.")
    logging.info("Setting up the native chroot and cloning the package build"
                 " recipes (pmaports)...")

    # Set up the native chroot and clone pmaports
    pmb.helpers.git.clone(args, "pmaports", False)


def symlink(args):
    # Create the symlink
    # This won't work when pmbootstrap was installed system wide, but that's
    # okay since the symlink is only intended to make the migration to the
    # pmaports repository easier.
    link = pmb.config.pmb_src + "/aports"
    try:
        os.symlink(args.aports, link)
        logging.info("NOTE: pmaports path: " + link)
    except:
        logging.info("NOTE: pmaports path: " + args.aports)


def check_version_pmaports(args):
    # Compare versions
    real = args.pmaports["version"]
    min = pmb.config.pmaports_min_version
    if pmb.parse.version.compare(real, min) >= 0:
        return

    # Outated error
    logging.info("NOTE: your pmaports folder has version " + real + ", but" +
                 " version " + min + " is required.")
    raise RuntimeError("Run 'pmbootstrap pull' to update your pmaports.")


def check_version_pmbootstrap(args):
    # Compare versions
    real = pmb.config.version
    min = args.pmaports["pmbootstrap_min_version"]
    if pmb.parse.version.compare(real, min) >= 0:
        return

    # Show versions
    logging.info("NOTE: you are using pmbootstrap version " + real + ", but" +
                 " version " + min + " is required.")

    # Error for git clone
    pmb_src = pmb.config.pmb_src
    if os.path.exists(pmb_src + "/.git"):
        raise RuntimeError("Please update your local pmbootstrap repository."
                           " Usually with: 'git -C \"" + pmb_src + "\" pull'")

    # Error for package manager installation
    raise RuntimeError("Please update your pmbootstrap version (with your"
                       " distribution's package manager, or with pip, "
                       " depending on how you have installed it). If that is"
                       " not possible, consider cloning the latest version"
                       " of pmbootstrap from git.")


def read_config_into_args(args):
    """ Read and verify pmaports.cfg, add the contents to args.pmaports_cfg """
    # Migration message
    if not os.path.exists(args.aports):
        raise RuntimeError("We have split the aports repository from the"
                           " pmbootstrap repository (#383). Please run"
                           " 'pmbootstrap init' again to clone it.")

    # Require the config
    path_cfg = args.aports + "/pmaports.cfg"
    if not os.path.exists(path_cfg):
        raise RuntimeError("Invalid pmaports repository, could not find the"
                           " config: " + path_cfg)

    # Load the config into args.pmaports
    cfg = configparser.ConfigParser()
    cfg.read(path_cfg)
    setattr(args, "pmaports", cfg["pmaports"])

    # Version checks
    check_version_pmaports(args)
    check_version_pmbootstrap(args)


def init(args):
    check_legacy_folder()
    if not os.path.exists(args.aports):
        clone(args)
    symlink(args)
    read_config_into_args(args)
