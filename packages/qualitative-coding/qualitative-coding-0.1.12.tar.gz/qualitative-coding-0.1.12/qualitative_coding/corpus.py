# Qualitative Coding corpus
# -------------------------
# (c) 2019 Chris Proctor

# Expects codes files to be named something like [^\.]+(\.[^\.]+)?\.txt
# Corpus and codes are separated because maybe you want to keep your raw data
# and your analysis separate.

# Decided not to make a separate codebook because the codebook and the codes are tightly bound.

# TODO
# - add logging
# ensure uniqueness of corpus text paths

from itertools import chain
from collections import defaultdict
from pathlib import Path
import yaml
from qualitative_coding.tree_node import TreeNode
from qualitative_coding.logs import get_logger
from qualitative_coding.helpers import prepare_corpus_text
import numpy as np

DEFAULT_SETTINGS = {
    'corpus_dir': 'corpus',
    'codes_dir': 'codes',
    'logs_dir': 'logs',
    'memos_dir': 'memos',
    'codebook': 'codebook.yaml',
}

class QCCorpus:
    
    @classmethod
    def initialize(cls, settings_file="settings.py"):
        """
        If the settings file does not exist, creates it. Otherwise, uses the settings
        file to initialize the expected directories and files.
        """
        if not Path(settings_file).exists():
            Path(settings_file).write_text(yaml.dump(DEFAULT_SETTINGS))
            return
        settings_path = Path(settings_file)
        try: 
            settings = yaml.safe_load(settings_path.read_text())
        except FileNotFoundError:
            message = "Settings file {} was not found. qc must be run from its project directory. If you are starting a new qc project, run `qc init`.".format(settings_file)
            raise FileNotFoundError(message)
        for required_setting in DEFAULT_SETTINGS.keys():
            path = Path(settings[required_setting])
            path = path if path.is_absolute() else settings_path.parent / path
            if required_setting.endswith("dir"):
                if path.exists():
                    if not path.is_dir():
                        raise ValueError(f"Expected {path} to be a directory")
                else:
                    path.mkdir(parents=True)
            else:
                if path.exists():
                    if path.is_dir():
                        raise ValueError(f"Expected {path} to be a file, not a directory")
                else:
                    path.touch()

    def __init__(self, settings_file="settings.yaml"):
        """
        We need the actual settings file instead of just settings because it also
        provides a default (portable) working directory for relative links
        """
        self.settings_file = Path(settings_file)
        try: 
            self.settings = yaml.safe_load(self.settings_file.read_text())
        except FileNotFoundError:
            message = "Settings file {} was not found. qc must be run from its project directory. If you are starting a new qc project, run `qc init`.".format(settings_file)
            raise FileNotFoundError(message)
        self.log = get_logger(__name__, self.settings['logs_dir'], self.settings.get('debug'))

        for required_setting in DEFAULT_SETTINGS.keys():
            path = Path(self.settings[required_setting])
            path = path if path.is_absolute() else self.settings_file.resolve().parent / path
            setattr(self, required_setting, path)

    def validate(self):
        "Checks that files are as they should be"
        # TODO: Verify code file lengths are correct
        errors = []
        for attr in DEFAULT_SETTINGS.keys():
            if not getattr(self, attr).exists():
                errors.append("settings['{}'] ({}) does not exist".format(attr, getattr(self, attr)))
            if attr.endswith('dir') and not getattr(self, attr).is_dir():
                errors.append("settings['{}'] ({}) is not a directory".format(attr, getattr(self, attr)))
            if not attr.endswith('dir') and getattr(self, attr).is_dir():
                errors.append(("settings['{}'] ({}) is a directory".format(attr, getattr(self, attr))))
        for error in errors:
            self.log.error(error)
        if any(errors):
            raise ValueError("\n".join(errors))

    def prepare_corpus(self, pattern=None, file_list=None, invert=False, preformatted=False):
        "Wraps texts at 80 characters"
        for f in self.iter_corpus(pattern=pattern, file_list=file_list, invert=invert):
            f.write_text(prepare_corpus_text(f.read_text(), width=80, preformatted=preformatted))

    def get_code_file_path(self, corpus_file_path, coder):
        text_path = corpus_file_path.relative_to(self.corpus_dir) 
        return self.codes_dir / (str(text_path) + "." + coder + ".codes")

    def prepare_code_files(self, coder, pattern=None, file_list=None, invert=False):
        "For each text in corpus, creates a blank file of equivalent length"
        for f in self.iter_corpus(pattern=pattern, file_list=file_list, invert=invert):
            with open(f) as inf:
                file_len = len(list(inf))                
            code_path = self.get_code_file_path(f, coder)
            code_path.parent.mkdir(parents=True, exist_ok=True)
            if code_path.exists():
                print("Skipping {} because it already exists".format(code_path))
            else:
                code_path.write_text("\n" * file_len)

    def iter_corpus(self, pattern=None, file_list=None, invert=False):
        "Iterates over files in the corpus"
        if pattern:
            glob = '*' + pattern + '*.txt'
        else:
            glob = '*.txt'
        if not invert:
            for f in Path(self.corpus_dir).rglob(glob):
                if file_list is None or str(f.relative_to(self.corpus_dir)) in file_list:
                    yield f
        else:
            matches = set(self.iter_corpus(pattern=pattern, file_list=file_list))
            for f in Path(self.corpus_dir).rglob(glob):
                if f not in matches:
                    yield f

    def iter_corpus_codes(self, pattern=None, file_list=None, invert=False, coder=None, merge=False):
        "Iterates over (f, codes) for code files"
        for f in self.iter_corpus(pattern, file_list=file_list, invert=invert):
            yield f, self.get_codes(f, coder=coder, merge=merge)

    def iter_code_files(self, coder=None):
        "Iterates over all files containing codes, optionally filtered by coder"
        pattern = f"*.{coder}.codes" if coder else "*.codes"
        for f in self.codes_dir.glob(pattern):
            yield f

    def get_code_files_for_corpus_file(self, corpus_text_path, coder=None):
        "Returns an iterator over code files pertaining to a corpus file"
        text_path = corpus_text_path.relative_to(self.corpus_dir)
        name_parts = text_path.name.split('.')
        return self.codes_dir.glob(str(text_path) + '.' + (coder or '*') + '.codes')

    def get_codes(self, corpus_text_path, coder=None, merge=False, unit='line'):
        """
        Returns codes pertaining to a corpus text.
        Returns a dict like {coder_id: [(line_num, code)...]}. 
        If merge or coder, there is no ambiguity;instead returns a list of [(line_num, code)...]
        If unit is 'document', returns a set of codes when coder or merge is given, otherwise
        returns a dict mapping coders to sets of codes.
        """
        codes = {}
        for f in self.get_code_files_for_corpus_file(corpus_text_path, coder=coder):
            codes[self.get_coder_from_code_path(f)] = self.read_codes(f, unit=unit)
        if coder:
            return codes.get(coder, {})
        elif merge:
            if unit == 'line': 
                return sum(codes.values(), [])
            elif unit == 'document': 
                return set().union(*codes.values())
            else:
                raise NotImplementedError("Unit must be 'line' or 'document'.")
        else:
            return codes

    def get_code_matrix(self, codes, 
        recursive_codes=False,
        recursive_counts=False,
        depth=None, 
        unit='line',
        pattern=None,
        file_list=None,
        invert=False,
        coder=None,
        expanded=False,
    ):
        tree = self.get_codebook()
        if codes:
            nodes = sum([tree.find(c) for c in codes], [])
            if recursive_codes:
                nodes = set(sum([n.flatten(depth=depth) for n in nodes], []))
        else:
            nodes = tree.flatten(depth=depth)

        if recursive_counts:
            code_sets = [(n.name, set(n.flatten(names=True))) for n in nodes]
        else:
            code_sets = [(n.name, set([n.name])) for n in nodes]

        rows = []    
        for corpus_file in self.iter_corpus(pattern=pattern, file_list=file_list, invert=invert):
            if unit == "document":
                doc_codes = self.get_codes(corpus_file, coder=coder, merge=True, unit='document')
                rows.append([int(bool(doc_codes & matches)) for code, matches in code_sets])
            elif unit == "line":
                # Need a windowing/chunking strategy.
                # Perhaps a delimiter (e.g. paragraphs break on blank lines)
                raise NotImplementedError("Crosstab with unit='line' not yet implemented.")
            else:
                raise NotImplementedError("Unit must be 'line' or 'document'.")
        return [n.expanded_name() if expanded else n.name for n in nodes], np.array(rows)

    def write_codes(self, corpus_text_path, coder, codes):
        "Writes a list of (line_num, code) to file"
        with open(corpus_text_path) as f:
            file_len = len(list(f))
        lines = defaultdict(list)
        for line_num, code in codes:
            lines[line_num] += [code]
        text_path = corpus_text_path.relative_to(self.corpus_dir)
        codes_path = Path(str(self.codes_dir / text_path) + '.' + coder + '.codes')
        codes_path.parent.mkdir(parents=True, exist_ok=True)
        with open(codes_path, 'w') as outf:
            for line_num in range(file_len):
                outf.write(", ".join(lines[line_num]) + "\n")

    def read_codes(self, code_file_path, unit='line'):
        """When passed a file object, returns a list of (line_num, code) if unit is 'line'. 
        When unit is 'document', Returns a set of codes.
        """
        codes = []
        with open(code_file_path) as inf:
            for line_num, line in enumerate(inf):
                codes += [(line_num, code.strip()) for code in line.split(",") if code.strip()]
        if unit == 'line': 
            return codes
        elif unit == 'document': 
            return set(code for i, code in codes)
        else:
            raise NotImplementedError("Unit must be 'line' or 'document'.")

    def get_all_codes(self, pattern=None, coder=None):
        "Returns a list of all unique codes used in the corpus"
        all_codes = set()
        for f, codes in self.iter_corpus_codes(pattern=pattern, coder=coder, merge=True):
            for line_num, code in codes:
                all_codes.add(code)
        return all_codes

    def get_code_counts(self, pattern=None, file_list=None, invert=False, coder=None, unit='line'):
        "Returns a defaultdict of {code: number of uses in codefiles}"
        if unit not in ['line', 'document']:
            raise NotImplementedError("Unit of analysis not supported: {}".format(unit))

        all_codes = defaultdict(int)
        for f, codes in self.iter_corpus_codes(pattern=pattern, file_list=file_list, invert=invert, 
                coder=coder, merge=True):
            codes_in_doc = defaultdict(int)
            for line_num, code in codes:
                codes_in_doc[code] += 1
            if unit == 'document':
                codes_in_doc = {code: 1 for code in codes_in_doc.keys()}
            for code, count in codes_in_doc.items():
                all_codes[code] += count
        return all_codes

    def get_code_tree_with_counts(self, 
        pattern=None,
        file_list=None,
        invert=False,
        coder=None,
        unit='line',
    ):
        tree = self.get_codebook()
        story_sets = self.get_code_story_sets(pattern=pattern, file_list=file_list, 
                invert=invert, coder=coder, unit=unit)
        for node in tree.flatten():
            node.story_set = story_sets[node.name]
            node.count = len(node.story_set)

        def agg_union(node):
            for child in node.children:
                agg_union(child)
            node.recursive_story_set = set() if node.is_root() else set(node.story_set)
            for child in node.children:
                node.recursive_story_set |= child.recursive_story_set

        agg_union(tree)
        for node in tree.flatten():
            node.total = len(node.recursive_story_set)
        return tree

    def get_code_story_sets(self, pattern=None, file_list=None, invert=False, coder=None, unit='line'):
        """Returns {code: stories}, where stories is a set of story ids when unit is document 
        and stories is a set of (story_id, story_line) tuples when unit is line
        """
        code_story_sets = defaultdict(set)
        for f, codes in self.iter_corpus_codes(pattern=pattern, file_list=file_list, invert=invert, 
                coder=coder, merge=True):
            if unit == 'document':
                for line_num, code in codes:
                    code_story_sets[code].add(str(f))
            elif unit == 'line':
                for line_num, code in codes:
                    code_story_sets[code].add((str(f), line_num))
        return code_story_sets

    def get_coder_from_code_path(self, code_file_path):
        "Maps Path('some_interview.txt.cp.codes') -> 'cp'"
        parts = code_file_path.name.split('.')
        return parts[-2]

    def get_codebook(self):
        """
        Reads a tree of codes from the codebook file.
        """
        return TreeNode.read_yaml(self.codebook)

    def update_codebook(self):
        """
        Updates the codebook by adding any new codes used in the codefiles.
        Does not remove unused codes.
        """
        all_codes = self.get_all_codes()
        code_tree = self.get_codebook()
        new_codes = all_codes - set(code_tree.flatten(names=True))
        for new_code in new_codes:
            code_tree.add_child(new_code)
        TreeNode.write_yaml(self.codebook, code_tree)

    def rename_codes(self, old_codes, new_code, pattern=None, file_list=None, invert=False, coder=None,
                update_codebook=False):
        """
        Updates the codefiles and the codebook, replacing the old code with the new code. 
        Removes the old code from the codebook.
        """
        for corpus_path in self.iter_corpus(pattern=pattern, file_list=file_list, invert=invert):
            for code_file_path in self.get_code_files_for_corpus_file(corpus_path, coder=coder):
                existing_codes = self.read_codes(code_file_path)
                if len(existing_codes) == 0: 
                    continue
                line_nums, codes = zip(*self.read_codes(code_file_path))
                if set(old_codes) & set(codes):
                    new_codes = [(ln, new_code if code in old_codes else code) for ln, code in zip(line_nums, codes)]
                    existing_coder = self.get_coder_from_code_path(code_file_path)
                    self.write_codes(corpus_path, existing_coder, new_codes)

        global_rename = pattern is None and file_list is None and invert is None and coder is None
        if global_rename or update_codebook:
            code_tree = self.get_codebook()
            for old_code in old_codes:
                code_tree.rename(old_code, new_code)
                code_tree.remove_children_by_name(old_code)
                self.log.info(f"Renamed code {old_code} to {new_code}")
            TreeNode.write_yaml(self.codebook, code_tree)
            self.update_codebook()
                

            

        




