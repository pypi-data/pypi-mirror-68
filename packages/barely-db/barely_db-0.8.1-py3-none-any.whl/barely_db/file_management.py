# elan == electroanalytical methods

import os
# import cProfile
import logging
import subprocess


import attr
import cattr
import json
import typing

# import pandas as pd
# import numpy as np
import json
import re
import zipfile
from pathlib import Path
import shutil
import filecmp

import functools

from enum import Enum, IntEnum

from .parser import *

__all__ = ['extend_long_path_on_windows', 'open_in_explorer', 'FileManager', 'FileNameAnalyzer', 'copy_files_with_jupyter_button', 'serialize_to_file', 'RevisionFile', 'ClassFileSerializer', 'cattr_json_serialize']

# from chunked_object import *
# from message_dump import *

# create logger
module_logger = logging.getLogger(__name__)
module_logger.setLevel(logging.DEBUG)

# general useful module components
def _reload_module():
    import sys
    import importlib
    current_module = sys.modules[__name__]
    module_logger.info('Reloading module %s' % __name__)
    importlib.reload(current_module)


def extend_long_path_on_windows(fn, long_windows_path_limit=150):
    prefix = '\\\\?\\'

    if os.name == 'nt':
        if fn[0:4] != prefix and len(fn) > long_windows_path_limit:
            return prefix + fn

    return fn
    

def open_in_explorer(path, start=False):
    p = Path(path)
    if p.is_dir():
        module_logger.info(f'Opening explorer for folder {path}')
        subprocess.Popen(rf'explorer {path}')
    elif start:
        module_logger.info(f'Opening file {path}')
        subprocess.Popen(rf'explorer /start, {path}')
    else:
        module_logger.info(f'Opening explorer for file {path}')
        subprocess.Popen(rf'explorer /select, {path}')

    
    
    

class FileManager(object):
    def __init__(self, raw_path = './RAW', 
                 export_path = './export',  
                 export_prefix = '',
                 secondary_data_paths = [],
                 auto_string = True, 
                 auto_remove_duplicates = True,
                 long_windows_path_limit = 150):

        self.long_windows_path_limit = long_windows_path_limit
        
        self.set_raw_path(raw_path)
        self.set_export_path(export_path, export_prefix)
        self.set_secondary_data_paths(secondary_data_paths)
        self.auto_string = auto_string
        self.auto_remove_duplicates = auto_remove_duplicates
        
    def set_raw_path(self, raw_path):
        if not isinstance(raw_path, list):
            raw_path = [raw_path]

        self.raw_path = [Path(extend_long_path_on_windows(str(p), self.long_windows_path_limit)) for p in raw_path]

        for p in self.raw_path:
            if not p.exists():
                raise FileNotFoundError(str(p))        
        
    def set_export_path(self, export_path, export_prefix = ''):
        self.export_prefix = extend_long_path_on_windows(str(export_prefix), self.long_windows_path_limit)
        self.export_path = Path(export_path)
        self.export_path.mkdir(parents=True, exist_ok=True)

    def set_secondary_data_paths(self, secondary_data_paths):
        if not isinstance(secondary_data_paths, list):
            secondary_data_paths = [secondary_data_paths]

        self.secondary_data_paths = [Path(extend_long_path_on_windows(str(p), self.long_windows_path_limit)) for p in secondary_data_paths]        

        for p in self.secondary_data_paths:
            if not p.exists():
                raise FileNotFoundError(str(p))        

    def add_secondary_data_paths(self, secondary_data_paths):
        if not isinstance(secondary_data_paths, list):
            secondary_data_paths = [secondary_data_paths]

        new_paths = self.secondary_data_paths + secondary_data_paths
        self.set_secondary_data_paths(new_paths)       
            
    def _get_files(self, file_glob, paths, directories_only=False, files_only=False):
        from itertools import product
        
        if not isinstance(file_glob, list):
            file_glob = [file_glob]

        fns = []
        for p, g in product(paths, file_glob):
            fns += list(p.glob(g))

        if directories_only:
            fns = [fn for fn in fns if fn.is_dir()]
        
        if files_only:
            fns = [fn for fn in fns if not fn.is_dir()]
            
        if self.auto_string: 
            fns = [str(f) for f in fns]
        
        if self.auto_remove_duplicates:
            fns = self.remove_gdrive_duplicates(fns)
        
        return fns

    def get_files(self, file_glob, directories_only=False, files_only=False):
        return self._get_files(file_glob, self.raw_path, directories_only=directories_only,
                                                         files_only=files_only)   

    def get_directories(self, dir_glob):
        return self._get_files(dir_glob, self.raw_path, directories_only=True)   
    
    def get_export_files(self, file_glob):
        all_secondary_paths = [self.export_path] + self.secondary_data_paths
        return self._get_files(file_glob, all_secondary_paths)   
       
    def remove_gdrive_duplicates(self, fns):
        # remove stupid google drive duplicates
        fns_filtered = []
        for fn in fns:
            if bool(re.findall(' \(1\)', fn)):
                module_logger.warning(f'Removed google drive dupplicate from result! ({fn})')
            else:
                fns_filtered.append(fn)

        return fns_filtered.copy()     

    def _get_valid_filename(self, fn):
        # fn = str(fn).strip().replace(' ', '_')
        return re.sub(r'[\\/:"*?<>|]+', '', fn)

    def make_export_file_name(self, base_file, extension = '', absolute=True):
        bfn = Path(base_file)
        
        fn = self.export_prefix + bfn.name + extension
        fn_val = self._get_valid_filename(fn)
        if fn_val != fn:
            fn = fn_val
            module_logger.warning('Filename has been regularized! (%s)' % fn)

        exp_fn = Path(self.export_path, fn)
        if absolute:
            exp_fn = exp_fn.absolute()
        exp_fn = str(exp_fn)        
            
        exp_fn = extend_long_path_on_windows(exp_fn, self.long_windows_path_limit)

        if not self.auto_string: 
            exp_fn = Path(exp_fn)
               
        return exp_fn    


class FileNameAnalyzer(object):
    '''
    Extracts information from file names

    Usage example:
    fn_an = elan.FileNameAnalyzer()
    fn_an.add_regex('(CL\d{2,4})', 'cell_type', required=True)
    fn_an.add_regex('CL\d{2,4}-(C\d{1,2})', 'cell_number', required=True)
    fn_an.add_regex('(\d{2,4})degC', 'temp', numeric=True, required=False)
    fn_an.add_regex('(\dp\dV)', 'volt_nom_raw', numeric=False, required=True)

    fn_an.add_prior_knowledge('CL0041-C02', comment='C02 dropped to the floor')
    fn_an.add_prior_knowledge('CL0041-C03', comment='C03 looks nice')

    fn_an.analyze('EE0071b_CL0041-C03_0p8ml-RM261_25degC_0p25C_4p4V_02_GCPL_C03.mpt.x.fc_an.hdf')

    fn_an.test_regex('(CL\d{2,4})')
    fn_an.test_regex('CL\d{2,4}-(C\d{1,2})')

    '''

    def __init__(self):
        self.prio_entries = []
        self.regex_entries = []
        self.logger = module_logger
        self.last_filename = ''
        
    def add_regex(self, regex, param_name, numeric = False, required = True, converter=None):
        regex_entry = {'regex': regex, 
                       'param_name': param_name, 
                       'numeric': numeric, 
                       'required': required,
                       'converter': converter,
                       }
        self.regex_entries.append(regex_entry)
        pass

    def add_prior_knowledge(self, match_regex, **kwd):
        prio_entry = {'regex': match_regex, 'values': dict(**kwd)}
        self.prio_entries.append(prio_entry)
        pass

    def analyze(self, filename):
        info = {'filename': filename}
        self.last_filename = filename
        
        info['file_mod_time'] = os.path.getmtime(filename)
        
        for r in self.regex_entries:
            results = re.findall(r['regex'], filename)
            results = list(set(results)) # remove dupplicates!
                        
            if len(results) == 0:
                if r['required']:
                    self.logger.warning('Required parameter (%s) not found!' % r['param_name'])
            elif len(results) >= 1:
                if len(results) > 1:
                    # self.logger.warning('Parameter (%s) ambiguous! Using first of %s.' % (r['param_name'], str(results)))
                    # see if we only look in the filename itself we get uniqueness
                    results_name_only = re.findall(r['regex'], Path(filename).name)
                    results_name_only = list(set(results_name_only)) # remove dupplicates!

                    if len(results_name_only) == 1:
                        results = results_name_only
                    elif len(results_name_only) == 0:
                        self.logger.warning('Parameter (%s) ambiguous in the path, with no info in the filename! This might be a problem. Using first of %s.' % (r['param_name'], str(results)))
                    else:
                        results = results_name_only                        
                        self.logger.warning('Parameter (%s) ambiguous in the filename! This might be a problem. Using first of %s.' % (r['param_name'], str(results)))                   

                if r['converter']:
                    results[0] = r['converter'](results[0])

                if r['numeric']:
                    info[r['param_name']] = float(results[0])
                else:
                    info[r['param_name']] = results[0]
                
        for p in self.prio_entries:
            if re.findall(p['regex'], filename):
                # self.logger.debug('Parameter (%s) matches %s!' % (p['regex'], filename))                
                info.update(p['values'])               
        
        return info

    def test_regex(self, regex, filename = None):
        if filename is None:
            filename = self.last_filename
        
        self.last_filename = filename
        self.logger.info('Using %s' % filename)

        result =  re.findall(regex, filename)

        self.logger.info('%s yields %s' % (regex, str(result)))

        return result
    
    def add_battrion_defaults(self):
        self.add_regex('(EE\d{2,4})', 'experiment_number', required=True)
        self.add_regex('(EE\d{2,4}[a-zA-Z]?)', 'experiment_number_sub', required=False)
        self.add_regex('(CL\d{2,4})', 'cell_type', required=False)
        self.add_regex('CL\d{2,4}-(C\d{1,2})', 'cell_number', required=False)
        self.add_regex('(CL\d{2,4}-C\d{1,2})', 'cell_number_full', required=False)
        self.add_regex('(\d{2,4})degC', 'temp', numeric=True, required=False)
        self.add_regex('([6-9]\d)degC', 'temp_cutoff', numeric=True, required=False)
        self.add_regex('(\dp\dV)', 'volt_nom_raw', numeric=False, required=False)
        self.add_regex('(\d{2,4})_MB', 'step_number_mb', numeric=False, required=False)


        
        
        
def copy_files_with_jupyter_button(fns, target_path, dry_run=False, show_button=True):
    from ipywidgets import widgets

    def copy_files(button):
        import shutil

        progress = widgets.IntProgress(min=0, max=len(fns), value=0, description='Copying...')
        display(progress)
        
        for fn in fns:
            t_fn = target_path.joinpath(Path(fn).name) 
            if dry_run:
                # print(f'shutil.copyfile({fn}, {t_fn})')    
                pass
            else:
                shutil.copyfile(fn, t_fn)    
            progress.value += 1
        
        progress.description = 'Done!'

    
    button = widgets.Button(description = f'Copy files ({len(fns)}) to {target_path}',
                           layout=widgets.Layout(width='90%')
                           )
    button.on_click(copy_files)
    
    if show_button:
        display(button)
    else:
        copy_files(button)
                


@attr.s(frozen=True,kw_only=True)
class RevisionFile(object):

    base_name = attr.ib()
    revision = attr.ib(default=None)
    full_name = attr.ib(default=None)

    def __attrs_post_init__(self):
        if self.revision is None:
            object.__setattr__(self, "full_name", f'{self.base_name}')
        else:
            object.__setattr__(self, "full_name", f'{self.base_name}.{self.revision:d}')

    def exists(self):
        return Path(self.full_name).exists()

    def get_next_revision_file(self):
        current_revision = 0 if self.revision is None else self.revision
        return RevisionFile(base_name=self.base_name,
                            revision=current_revision+1,
                            )

    def get_new_revision(self):
        if not self.exists():
            return self
        
        old_rev_exists, path_to_old_rev = self.old_revision_folder_exists()
        
        if not old_rev_exists:
            os.mkdir(path_to_old_rev)
        
        if self.revision is None :
            fn_name =Path(self.base_name).name
            new_name = path_to_old_rev.joinpath(fn_name)
            rf = RevisionFile(base_name=new_name,
                              revision=0)
        else :
            fn_name =Path(self.base_name).name
            new_name = path_to_old_rev.joinpath(fn_name)
            rf = RevisionFile(base_name=new_name,
                                   revision=self.revision)

        while rf.exists():
            # pray to god that this converges ;)
            rf = rf.get_next_revision_file()
        return rf
    
    def old_revision_folder_exists(self):
            path_to_file = Path(self.full_name).parent
            path_to_old_rev = path_to_file.joinpath('.bdb_old')
            return path_to_old_rev.exists(), path_to_old_rev

    def create_new_revision(self):
        if self.exists():
            new_rev = self.get_new_revision()
            shutil.move(self.base_name, new_rev.full_name)
            module_logger.info(f'Created new revision ({new_rev.revision}) of file {self.base_name}!')

    def get_last_revision(self):
        old_rev_exists, path_to_old_rev = self.old_revision_folder_exists()
        if not old_rev_exists:
            return None
    
        last_rev = None
        fn_name = Path(self.base_name).name
        new_path = path_to_old_rev.joinpath(fn_name)
        rf = RevisionFile(base_name=new_path, revision=0)

        while rf.exists():
            # pray to god that this converges ;)
            last_rev = rf
            rf = rf.get_next_revision_file()

        return last_rev

    def reduce_last_revision(self):
        if not RevisionFile(base_name=self.base_name).exists():
            return None
        
        last_rev = self.get_last_revision()

        if last_rev is not None:
            if filecmp.cmp(self.base_name, last_rev.full_name, shallow=False):
                os.unlink(last_rev.full_name)
                module_logger.info(f'Last revision of {self.base_name} matches current version and is removed!')




class ClassFileSerializer(object):

    cls_registry = {}
    filename_pattern_registry = {}

    cls=None

    base_file_identifier=None
    prepend_buid=False
    prefix='' 
    suffix=''
    serialize_method = 'serialize'
    deserialize_classmethod = 'deserialize'
    allow_parent=False
    binary=False

    def __init__(self, base_file_identifier=None, 
                      prepend_buid=False, 
                      prefix='', suffix='',
                      serialize_method = 'serialize',
                      deserialize_classmethod = 'deserialize',
                      allow_parent=False,
                      binary=False,):

        self.base_file_identifier = base_file_identifier
        self.prepend_buid = prepend_buid
        self.prefix = prefix
        self.suffix = suffix
        self.serialize_method = serialize_method
        self.deserialize_classmethod = deserialize_classmethod
        self.allow_parent = allow_parent
        self.binary = binary


    @classmethod
    def get_class_from_filename(cls, fn):
        found_cls = None

        for class_name, cfs in cls.cls_registry.items():
            if cfs.match_filename(fn):
                found_cls = cfs.cls
                module_logger.debug(f'Found class {found_cls.__qualname__} for file {Path(fn).name}')
        
        return found_cls


    def set_class(self, cls):        
        self.cls = cls

        if self.prefix or self.suffix or self.base_file_identifier:
            ClassFileSerializer.cls_registry[cls.__qualname__] = self
            ClassFileSerializer.filename_pattern_registry[self.get_filename_regex()] = self

    def get_filename_regex(self, file_identifier=None):
        rg = r''
        if self.prepend_buid:
            rg += GenericBUIDParser.buid_comp_regex.pattern+'_'
        if self.prefix:
            rg += self.prefix
        if file_identifier:
            rg += file_identifier
        elif self.base_file_identifier:
            rg += self.base_file_identifier
        else:
            rg += '(.*)'

        if self.suffix:
            rg += self.suffix

        return rg

    def match_filename(self, fn, file_identifier=None):
        rg = self.get_filename_regex(file_identifier=file_identifier)
        return re.match(rg, Path(fn).name)



    def get_serialization_filename_from_entity(self, entity, file_identifier=None):
        if file_identifier is None:
            file_identifier = self.base_file_identifier

        if file_identifier is None:
            raise ValueError('No file_identifier given. Either set base_file_identifier in serialize_to_file'
                                ', or provide file_identifier to this function call.')

        export_prefix = f'{entity.buid_with_component}_' if self.prepend_buid else ''
        export_prefix += self.prefix

        fm = entity.make_file_manager(export_prefix=export_prefix)

        filename = fm.make_export_file_name(file_identifier)

        if self.suffix:
            filename += self.suffix

        return filename


    def save_to_file(self, obj, filename, override=False, revision=True, use_suffix=False):
        if self.serialize_method is None:
            module_logger.error(f'Object from class {obj.__class__.__qualname__} cannot be deserialized!')
            return None

        serialize = getattr(obj, self.serialize_method)
        serial_data = serialize() 

        if use_suffix:
            filename += self.suffix

        self.save_raw_to_file(serial_data, filename, override=override, revision=revision)


    def save_raw_to_file(self, raw_data, filename, override=False, revision=True):
        serial_data = raw_data

        if filename is None:
            raise ValueError('(Filename cannot be None!)')

        filename = extend_long_path_on_windows(str(filename))

        if revision:
            revision_file = RevisionFile(base_name=filename)
            revision_file.create_new_revision()

        if Path(filename).exists() and not override:
            module_logger.warning('File already exists. Skip. (consider override=True).')
        else:
            serial_data_binary = serial_data if self.binary else serial_data.encode()                    

            with open(filename, 'wb') as f:
                f.write(serial_data_binary)
                module_logger.info(f'Config written to {filename}')

            if revision:
                revision_file.reduce_last_revision()        



    def load_raw_from_file(self, filename):
        if filename is None:
            raise FileNotFoundError('(Filename cannot be None!)')

        filename = extend_long_path_on_windows(str(filename))

        with open(filename, 'rb') as f:
            file_data_binary = f.read()
            file_data = file_data_binary if self.binary else file_data_binary.decode()
        
        return file_data


    def load_from_file(self, filename, default=None, fail_to_default=False):           
        if self.deserialize_classmethod is None:
            module_logger.error(f'Class {self.cls.__qualname__} cannot be deserialized!')
            return None

        deserialize = getattr(self.cls, self.deserialize_classmethod)
        
        try:
            file_data = self.load_raw_from_file(filename)

        except FileNotFoundError:
            if default is None and not fail_to_default:
                raise
            else:
                module_logger.info(f'Using default, because file not found ({filename}).')
                return default

        try:
            return deserialize(file_data)
        except BaseException as e:
            raise RuntimeError(f'Deserialization failed for file {filename}')


    def save_to_entity(self, obj, entity, file_identifier=None, override=False, revision=True, open_in_explorer=False):
        filename = self.cls.get_serialization_filename(entity, file_identifier=file_identifier)
        self.save_to_file(obj, filename, override=override, revision=revision)            
        if open_in_explorer:
            self.open_in_explorer(entity)
        return filename


    def resolve_file_from_entity(self, entity, file_identifier=None, allow_parent=None, force_parent=False):        
        if entity is None: 
            return None

        if allow_parent is None:
            allow_parent = self.allow_parent

        if force_parent:
            entity = entity.parent

        try:
            filename = self.cls.get_serialization_filename(entity, file_identifier=file_identifier)
            load_parent = not Path(filename).exists()
        except FileNotFoundError:
            filename = None
            load_parent = True

        if load_parent and allow_parent:
            filename = self.cls.get_serialization_filename(entity.parent, 
                                                        file_identifier=file_identifier)
        
        return filename


    def load_from_entity(self, entity, file_identifier=None, allow_parent=None, force_parent=False, default=None, fail_to_default=False):           
        if entity is None and fail_to_default:
            return default

        filename = self.resolve_file_from_entity(entity, file_identifier=file_identifier, allow_parent=allow_parent, force_parent=force_parent)

        obj = self.load_from_file(filename, default=default, fail_to_default=fail_to_default)

        # Check if object buid is consistent with entity:
        try:
            obj_buid = obj.buid
            ent_buid = entity.buid_with_component
            if obj_buid is None:
                module_logger.warning(f'Loaded object ({self.cls.__qualname__}) has empty buid, while the entity it was loaded from has not ({ent_buid})! Consider to fix this!')
            elif obj_buid not in ent_buid:
                module_logger.warning(f'Loaded object ({self.cls.__qualname__}) has different buid ({obj_buid}) then the entity it was loaded from ({ent_buid})! Consider to fix this!')

        except AttributeError as e:
            pass

        return obj


    def _open_in_explorer(self, entity, file_identifier=None):
        global open_in_explorer
        filename = self.get_serialization_filename_from_entity(entity, file_identifier=file_identifier)
        open_in_explorer(filename)            

    

def serialize_to_file(base_file_identifier=None, 
                      prepend_buid=False, 
                      prefix='', suffix='',
                      serialize_method = 'serialize',
                      deserialize_classmethod = 'deserialize',
                      allow_parent=False,
                      binary=False,
                      ):
    ''' Decorator for attrs based classes to serialize them to a file.
    Serialization is performed by class methods .serialize() and .deserialize().
    '''

    file_serializer = ClassFileSerializer(base_file_identifier=base_file_identifier, 
                      prepend_buid=prepend_buid, 
                      prefix=prefix, suffix=suffix,
                      serialize_method = serialize_method,
                      deserialize_classmethod = deserialize_classmethod,
                      allow_parent=allow_parent,
                      binary=binary)

    def decorate_class(cls):

        file_serializer.set_class(cls)

        cls.file_serializer = file_serializer

        cls.get_serialization_filename = functools.partialmethod(file_serializer.get_serialization_filename_from_entity)
        cls.save_to_file = functools.partialmethod(file_serializer.save_to_file)
        cls.save_to_entity = functools.partialmethod(file_serializer.save_to_entity)
        cls.load_from_file = functools.partialmethod(file_serializer.load_from_file)
        cls.load_from_entity = functools.partialmethod(file_serializer.load_from_entity)
        cls.open_in_explorer = functools.partialmethod(file_serializer._open_in_explorer)

        return cls
       

    return decorate_class





def cattr_json_serialize(cls):
    ''' A simple json serialize/deserialize class decorator. '''

    def serialize(self):
        return json.dumps(cattr.unstructure(self), indent=4)

    @classmethod
    def deserialize(cls, data):
        return cattr.structure(json.loads(data), cls)

    cls.serialize = serialize
    cls.deserialize = deserialize
    
    return cls


