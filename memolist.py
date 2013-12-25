import sublime
import sublime_plugin
import os, datetime, subprocess

insert_text = [
    "title: ",
    "==========",
    "date: ",
    "tags: []",
    "categories: []",
    "- - -"
]

class MemolistInsertCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        global insert_text
        self.view.insert(edit, 0, '\n'.join(insert_text))

class MemolistOpenCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel(
            "Memo title:",
            self.default_filename(),
            self.open_memo_file,
            None, None)

    def settings(self):
        return sublime.load_settings("memolist.sublime-settings")

    def open_memo_file(self, file_title):
        global insert_text

        if file_title == '':
            return None

        dir_path = self.prepare_memo_dir()
        insert_text[0] += file_title
        file_name = datetime.datetime.today().strftime("%Y-%m-%d-") + file_title

        self.window.open_file(dir_path + "/" + file_name + '.md')
        sublime.set_timeout(lambda:
                self.window.run_command("memolist_insert"), 0)

    def prepare_memo_dir(self):
        memo_dir = os.path.expandvars(self.settings().get('memo_dir'))

        self.makedir(memo_dir)

        return memo_dir + '/'

    def makedir(self, path):
        if not os.path.isdir(path):
            os.mkdir(path)

    def default_filename(self):
        global data
        data[2] += datetime.datetime.today().strftime("%Y-%m-%d %H:%M")
        return ''

class MemolistShowCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.memo_dir = os.path.expandvars(self.settings().get('memo_dir'))
        self.files = os.listdir(self.memo_dir)

        self.files.remove('.DS_Store')
 
        self.window.show_quick_panel(self.files, self.on_chosen)

    def on_chosen(self, index):
        if index == -1:
          return

        self.window.open_file(self.memo_dir + '/' + self.files[index])

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

        self.results.remove('.DS_Store')
        self.window.show_quick_panel(self.results, self.on_chosen)

    def settings(self):
        return sublime.load_settings("memolist.sublime-settings")

    def on_chosen(self, index):
        if index == -1:
          return

        self.window.open_file(self.memo_dir + '/' + self.results[index])

