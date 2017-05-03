import os
import subprocess
from commands import *

class PreProcessing:
    def __init__(self,source,target,output_directory):
        self.source = str(source)
        self.target = str(target)
        self.output_directory = str(output_directory)

    def _prepare_corpus(self):
            # Change directory to the self.output_directory. TODO revert this once finished!
            os.chdir(self.output_directory)
            cmds = []

            # 1) Tokenization
            # a) self.target text
            self.target_tok = generate_input_tok_fn(self.target_lang,
                                                    self.output_directory)

            cmds.append(get_tokenize_command(self.moses_dir,
                                             self.target_lang,
                                             self.target,
                                             self.target_tok))
            # b) self.source text
            self.source_tok = generate_input_tok_fn(self.source_lang,
                                                    self.output_directory)
            cmds.append(get_tokenize_command(self.moses_dir,
                                             self.source_lang,
                                             self.source,
                                             self.source_tok))
            # c) Language model
            self.lm_tok = generate_lm_tok_fn(self.output_directory)
            cmds.append(get_tokenize_command(self.moses_dir,
                                             self.source_lang,
                                             self.target,
                                             self.lm_tok))

            # 2) Truecaser training
            # a) self.target text
            cmds.append(get_truecaser_train_command(self.moses_dir,
                                                    self.target_tok))
            # b) self.source text
            cmds.append(get_truecaser_train_command(self.moses_dir,
                                                    self.source_tok))
            # c) Language model
            cmds.append(get_truecaser_train_command(self.moses_dir,
                                                    self.lm_tok))

            # 3) Truecaser
            self.input_true = self.output_directory + "/input.true"
            # a) self.target text
            self.target_true = generate_input_true_fn(self.target_lang,
                                                      self.output_directory)
            cmds.append(get_truecaser_command(self.moses_dir),
                                              self.target_tok,
                                              self.target_true)
            # b) self.source text
            self.source_true = generate_input_true_fn(self.source_lang,
                                                      self.output_directory)
            cmds.append(get_truecaser_command(self.moses_dir),
                                              self.source_tok,
                                              self.source_true)
            # c) Language model
            self.lm_true = generate_lm_true_fn(self.output_directory)
            cmds.append(get_truecaser_command(self.moses_dir),
                                              self.target_tok, self.lm_true)

            # 4) Cleaner
            # a) self.target text
            self.input_clean = generate_input_clean_fn(self.output_directory)
            self.source_clean = self.input_true + "." + self.source_lang
            self.target_clean = self.input_true + "." + self.target_lang
            cmds.append(get_cleaner_command(self.moses_dir),
                                             self.source_lang,
                                            self.target_lang,
                                            self.input_true,
                                            self.input_clean)

            # Start threads
            all_ok = True
            for cmd in cmds:
                print cmd
                # all_ok = all_ok and (os.system(cmd) == 0)
                proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
                all_ok = all_ok and (proc.wait() == 0)
                # print "returncode:", proc.returncode, "\n\n\n"
                out, err = proc.communicate()
            if all_ok:
                self.is_corpus_preparation_ready = True
