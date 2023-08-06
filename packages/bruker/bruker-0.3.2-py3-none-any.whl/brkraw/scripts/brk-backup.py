#!/usr/scripts/env python

from .. import __version__, load
from ..lib.backup import BackupCacheHandler
import argparse
import os


def main():
    parser = argparse.ArgumentParser(prog='brk-backup',
                                     description="Command line tool for Bruker rawdata backup")
    parser.add_argument("-v", "--version", action='version', version='%(prog)s v{}'.format(__version__))

    subparsers = parser.add_subparsers(title='Sub-commands',
                                       description='brk-backup provides convenient tool for backup rawdata',
                                       help='description',
                                       dest='function',
                                       metavar='command')

    scan = subparsers.add_parser("scan", help='Scan the backup status')
    scan.add_argument("raw_path",
                      help="Folder location of the Bruker raw datasets",
                      type=str)
    scan.add_argument("backup_path",
                      help="Folder location of the backed-up datasets",
                      type=str)
    scan.add_argument("-l", "--logging",
                      help="option for logging output instead printing",
                      action='store_true')



    args = parser.parse_args()

    if args.function == 'scan':
        from os.path import join as opj, isdir, isfile, exists
        import brkraw
        import tqdm
        import pickle
        import zipfile

        rpath = os.path.expanduser(args.raw_path)
        bpath = os.path.expanduser(args.backup_path)
        bar_fmt = '{l_bar}{bar:20}{r_bar}{bar:-20b}'

        if args.logging:
            import datetime
            today = datetime.date.today().strftime("%y%m%d")
            fobj = open(opj(bpath, '{}_backup_status.log'.format(today)), 'w')
        else:
            import sys
            fobj = sys.stdout

        # load backed-up cache
        backup_cache = opj(bpath, '.brkraw_cache')
        if exists(backup_cache):
            with open(backup_cache, 'rb') as f:
                cached_dataset = pickle.load(f)
            if 'duplicated' not in cached_dataset.keys():  # this component added later, so need update for old version
                cached_dataset['duplicated'] = dict()
        else:
            cached_dataset = dict(failed_backup=[],  # data backup failed (indicates the crashed file)
                                  failed_raw=[],  # failed data acquisition
                                  duplicated=dict(),  #
                                  completed=dict(),  # data backup completed
                                  incompleted=dict(),  # data backup incompleted (need to re-run)
                                  backup_required=dict(),  # data backup is needed (backup data is not exist)
                                  garbages=dict())  # garbage data (no scan info)

        # parse list of datasets
        list_of_raw = sorted([d for d in os.listdir(rpath) if isdir(opj(rpath, d))])
        list_of_candidates = [d for d in os.listdir(bpath) if
                              (isfile(opj(bpath, d)) and (d.endswith('zip') or d.endswith('PvDatasets')))]
        list_of_candidates = [d for d in list_of_candidates if d not in cached_dataset['completed'].keys()]

        print('-- Updating cache --')
        if len(cached_dataset['incompleted'].items()):
            print('Updating incompleted backup dataset list in cache...')
            incmp_list = cached_dataset['incompleted'].copy()
            for bck_path, raw_path in incmp_list.items():
                if not exists(opj(bpath, bck_path)):
                    print(" -'{}' has been removed.".format(bck_path))
                    del cached_dataset['incompleted'][bck_path]
                else:
                    bck_data = brkraw.load(opj(bpath, bck_path))
                    raw_data = brkraw.load(opj(rpath, raw_path))
                    if bck_data.num_recos == raw_data.num_recos:
                        del cached_dataset['incompleted'][bck_path]
                        cached_dataset['completed'][bck_path] = raw_path

        if len(cached_dataset['duplicated']):
            print('Updating duplicated backup dataset list in cache...')
            dup_list = cached_dataset['duplicated'].copy()
            for raw_path, bck_paths in dup_list.items():
                for bck_path in bck_paths:
                    if not os.path.exists(os.path.join(bpath, bck_path)):
                        cached_dataset['duplicated'][raw_path].remove(bck_path)
                        del cached_dataset['completed'][bck_path]
                        print(" -'{}'[duplicated backup for {}] has been removed.".format(bck_path, raw_path))
                if len(cached_dataset['duplicated'][raw_path]) == 1:
                    del cached_dataset['duplicated'][raw_path]

        if len(cached_dataset['failed_backup']):
            print('Updating failed backup dataset list in cache...')
            for bck_path in cached_dataset['failed_backup'][:]:
                if not exists(opj(bpath, bck_path)):
                    print(" -'{}' has been removed.".format(bck_path))
                    cached_dataset['failed_backup'].remove(bck_path)

        if len(cached_dataset['failed_raw']):
            print('Updating failed raw dataset list in cache...')
            for raw_path in cached_dataset['failed_raw'][:]:
                if not exists(opj(rpath, raw_path)):
                    print(" -'{}' has been removed.".format(raw_path))
                    cached_dataset['failed_raw'].remove(raw_path)
                else:
                    if raw_path in cached_dataset['completed'].values():
                        print(" -'{}' has been backed-up.".format(raw_path))
                        cached_dataset['failed_raw'].remove(raw_path)

        if len(cached_dataset['garbages'].items()):
            print('Updating garbages dataset list in cache...')
            gbg_list = cached_dataset['garbages'].copy()
            for bck_path, raw_path in gbg_list.items():
                if not exists(opj(bpath, bck_path)):
                    print(" -'{}' has been removed.".format(bck_path))
                    if not exists(opj(rpath, raw_path)):
                        print(" -'{}' has been removed.".format(raw_path))
                        del cached_dataset['garbages'][bck_path]
                    else:
                        print(" -'{}' was not removed.".format(raw_path))

        print('\n-- Inspecting Backup Status --')
        print('Checking condition of backup datasets...')
        # this step will test the zip files that not listed in completed list
        for bck_path in tqdm.tqdm(list_of_candidates,
                                  bar_format=bar_fmt):
            if not zipfile.is_zipfile(opj(bpath, bck_path)):
                # crashed zip file
                if bck_path not in cached_dataset['failed_backup']:
                    cached_dataset['failed_backup'].append(bck_path)
            else:
                # indicated as zip file
                bck_data = brkraw.load(opj(bpath, bck_path))
                raw_path = bck_data._pvobj.path

                if bck_data.is_pvdataset:
                    if exists(opj(rpath, raw_path)):
                        # if the rawdata still exists, check backed data is same as original
                        raw_data = brkraw.load(opj(rpath, raw_path))
                        if raw_data.num_recos == bck_data.num_recos:
                            cached_dataset['completed'][bck_path] = raw_path
                        else:
                            cached_dataset['incompleted'][bck_path] = raw_path
                    else:
                        cached_dataset['completed'][bck_path] = raw_path
                        if bck_data.num_recos < 1:
                            cached_dataset['garbages'][bck_path] = raw_path
                else:
                    cached_dataset['completed'][bck_path] = raw_path
                    cached_dataset['garbages'][bck_path] = raw_path

        if len(cached_dataset['completed'].items()):
            print('Checking any duplicated backup data...')
            cache_tested = []
            complist = cached_dataset['completed'].copy()
            for bck_path, raw_path in tqdm.tqdm(complist.items(),
                                                bar_format=bar_fmt):
                if raw_path not in cache_tested:
                    raw_in_list = [rp for rp in cached_dataset['completed'].values() if rp == raw_path]
                    if len(raw_in_list) > 1:
                        if raw_path not in cached_dataset['duplicated'].keys():
                            cached_dataset['duplicated'][raw_path] = []
                        if bck_path not in cached_dataset['duplicated'][raw_path]:
                            cached_dataset['duplicated'][raw_path].append(bck_path)
                    else:
                        pass
                    cache_tested.append(raw_path)
                else:
                    if bck_path not in cached_dataset['duplicated'][raw_path]:
                        cached_dataset['duplicated'][raw_path].append(bck_path)
            del cache_tested

        cached_dataset['backup_required'] = dict()  # reset the list

        print('Checking backup status of raw datasets...')
        for raw_path in tqdm.tqdm(list_of_raw,
                                  bar_format=bar_fmt):
            if raw_path not in cached_dataset['completed'].values():
                try:
                    raw_data = brkraw.load(opj(rpath, raw_path))
                    if raw_data.is_pvdataset:
                        cached_dataset['backup_required'][raw_path] = raw_data._pvobj.user_name
                except:
                    if raw_path not in cached_dataset['failed_raw']:
                        cached_dataset['failed_raw'].append(raw_path)
            else:
                raw_data = brkraw.load(opj(rpath, raw_path))
                print(raw_data.is_pvdataset)

        print('**** Summary ****', file=fobj)
        if len(cached_dataset['backup_required'].keys()):
            print('>> The list of raw datasets need backup... [no backup file]', file=fobj)
            for raw_path, user_name in cached_dataset['backup_required'].items():
                print(' -{} (user:{})'.format(raw_path, user_name), file=fobj)
        if len(cached_dataset['incompleted'].keys()):
            print(
                '\n>> The list of raw datasets need re-backup... [number of reconstructed image mismatch between raw and backup]',
                file=fobj)
            for bck_path, raw_path in cached_dataset['incompleted'].items():
                print(' -{} (backup:{})'.format(raw_path, bck_path), file=fobj)
        if len(cached_dataset['duplicated'].keys()):
            print('\n>> The list of duplicated backup datasets... [the same rawdata backed up on separate file]',
                  file=fobj)
            for raw_path, bck_paths in cached_dataset['duplicated'].items():
                print(' -{}: {}'.format(raw_path, bck_paths), file=fobj)
        if len(cached_dataset['garbages'].keys()):
            print('\n>> The raw datasets can be removed... [no reconstructed image]', file=fobj)
            for bck_path, raw_path in cached_dataset['garbages'].items():
                print(' -{} (backup:{})'.format(raw_path, bck_path), file=fobj)
        if len(cached_dataset['failed_raw']):
            print('\n>> The list of failed raw datasets... [issue found in rawdata]', file=fobj)
            for raw_path in cached_dataset['failed_raw']:
                print(' -{}'.format(raw_path), file=fobj)
        if len(cached_dataset['failed_backup']):
            print('\n>> The list of failed backup datasets... [crashed backup file]', file=fobj)
            for raw_path in cached_dataset['failed_backup']:
                print(' -{}'.format(raw_path), file=fobj)

        # save cache
        with open(backup_cache, 'wb') as f:
            pickle.dump(cached_dataset, f)