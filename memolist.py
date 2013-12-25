import os
import datetime
import subprocess
import sublime
import sublime_plugin

class MemolistOpenCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel(
            "Memo title:",
            self.default_filename(),
            self.open_memo_file,
            None, None)

    def settings(self):
        return sublime.load_settings("memolist.sublime-settings")

    def open_memo_file(self, filename):
        dir_path = self.prepare_memo_dir()
        self.window.open_file(dir_path + "/" + filename + '.md')

    def prepare_memo_dir(self):
        memo_dir = os.path.expandvars(self.settings().get('memo_dir'))

        self.makedir(memo_dir)

        return memo_dir + '/'

    def makedir(self, path):
        if not os.path.isdir(path):
            os.mkdir(path)

    def default_filename(self):
        return datetime.datetime.today().strftime("%Y-%m-%d-")

class MemolistShowCommand(sublime_plugin.WindowCommand):
    def run(self):
        memo_dir = os.path.expandvars(self.settings().get('memo_dir'))
        files = os.listdir(memo_dir)
 
        for file in files:
            print(file)

    def settings(self):
        return sublime.load_settings("memolist.sublime-settings")

class MemolistSearchCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel(
            "MemoGrep word:",
            '',
            self.search_memo_file,
            None, None)

    def search_memo_file(self, query):
        self.results = []
        self.memo_dir = os.path.expandvars(self.settings().get('memo_dir'))

        cmd = ['grep', '-nrl', query, self.memo_dir]
        output = subprocess.check_output(cmd, stderr=subprocess.PIPE)

        for line in output.decode().splitlines():
            try:
                self.results.append(line.replace(self.memo_dir + '/', ''))
            except:
                pass

        self.window.show_quick_panel(self.results, self.on_chosen)

    def settings(self):
        return sublime.load_settings("memolist.sublime-settings")

    def on_chosen(self, index):
        if index == -1:
          return

        self.window.open_file(self.memo_dir + '/' + self.results[index])
