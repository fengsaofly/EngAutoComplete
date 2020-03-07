# Extends Sublime Text autocompletion to find matches in all open
# files. By default, Sublime only considers words from the current file.

import sublime_plugin
import sublime
import re
import time
from os.path import basename

MAX_VIEWS = 20
MAX_WORDS_PER_VIEW = 100
MAX_FIX_TIME_SECS_PER_VIEW = 0.01
MAX_POPUP_HEIGHT = 500
MAX_POPUP_WIDTH = 500

def plugin_loaded():
    global settings
    settings = sublime.load_settings('EngAutocomplete.sublime-settings')
    # print ("when loaded:" + settings.get("min_word_size", 3))

class EngAutocomplete(sublime_plugin.EventListener):

    def on_query_completions(self, view, prefix, locations):#locations代表当前鼠标在当前文件（view）中的坐标
        # if not is_included(view.scope_name(locations[0]), settings.get("apply_sources", [])):
        #     return []
        words = []

        # 添加其他活跃视图到自动补全
        other_views = [
            v
            for v in sublime.active_window().views()
            # if v.id != view.id and is_included(v.scope_name(0), settings.get("include_sources", []))
            if v.id != view.id
            
        ]

        views = [view] + other_views
        views = views[0:MAX_VIEWS]

        for v in views:
            if len(locations) > 0 and v.id == view.id:
                view_words = v.extract_completions(prefix, locations[0])
            else:
                view_words = v.extract_completions(prefix)
            view_words = filter_words(view_words) #裁剪单词
            view_words = fix_truncation(v, view_words) 
            words += [(w, v) for w in view_words]

        words = without_duplicates(words)

        matches = []
        for w, v in words:
            trigger = w
            
            if v.id != view.id and v.file_name():
                trigger += '\t(%s)' % basename(v.file_name())
            if v.id == view.id:
                trigger += '\tabc'
 
        return matches
    def on_hover(self, view, point, hover_zone):
        # if not view.match_selector(point, "source.erlang"): 
        if not is_included(view.scope_name(point), settings.get("apply_sources", [])):
            return
        # 搜索所选单词相关语句
        search_word(view, point, hover_zone)

def is_included(scope, included_scopes):
    for included_scope in included_scopes:
        if included_scope in scope:
            return True
    return False

def filter_words(words):
    MIN_WORD_SIZE = settings.get("min_word_size", 3)
    MAX_WORD_SIZE = settings.get("max_word_size", 50)
    return [w for w in words if MIN_WORD_SIZE <= len(w) <= MAX_WORD_SIZE][0:MAX_WORDS_PER_VIEW]

# keeps first instance of every word and retains the original order, O(n)
def without_duplicates(words):
    result = []
    used_words = set()
    for w, v in words:
        if w not in used_words:
            used_words.add(w)
            result.append((w, v))
    return result

# Ugly workaround for truncation bug in Sublime when using view.extract_completions()
# in some types of files.
def fix_truncation(view, words):
    fixed_words = []
    start_time = time.time()

    for i, w in enumerate(words):
        #The word is truncated if and only if it cannot be found with a word boundary before and after

        # this fails to match strings with trailing non-alpha chars, like
        # 'foo?' or 'bar!', which are common for instance in Ruby.
        match = view.find(r'\b' + re.escape(w) + r'\b', 0)
        truncated = is_empty_match(match)
        # print (str(i+1)+':'+w)
        if truncated:
            #Truncation is always by a single character, so we extend the word by one word character before a word boundary
            extended_words = []
            view.find_all(r'\b' + re.escape(w) + r'\w\b', 0, "$0", extended_words)
            if len(extended_words) > 0:
                fixed_words += extended_words
                # print (str(i+1)+':'+w+':'+extended_words)
            else:
                # to compensate for the missing match problem mentioned above, just
                # use the old word if we didn't find any extended matches
                fixed_words.append(w)
        else:
            #Pass through non-truncated words
            fixed_words.append(w)

        # if too much time is spent in here, bail out,
        # and don't bother fixing the remaining words
        if time.time() - start_time > MAX_FIX_TIME_SECS_PER_VIEW:
            return fixed_words + words[i+1:]

    return fixed_words

def search_word(view, point, hover_zone):
    # pop_up设置
    _definition_style = 'font-weight:bold;font-size:9;margin:5 0'
    _line_style = 'margin:5 0'
    _max_col = 30

    # 获取hover_word
    line_region = view.line(point)
    line_str = view.substr(line_region)
    word_region = view.word(point)
    hover_word = view.substr(word_region)
    # 规定单词最小长度为4
    if len(hover_word) < 4:
        return False
    # 获取语句视图
    other_views = [
        v
        for v in sublime.active_window().views()
        if v.id != view.id and is_included(v.scope_name(0), settings.get("include_sources", []))
    ]

    other_views = other_views[0:MAX_VIEWS]
    matches = find_match(other_views, hover_word)

    if len(matches) == 0:
        return False
    # 构造pop-up视图
    html_content = '<div style={}><h3>Quotes:</h3><ul>'.format(_definition_style)
    col = 0
    row = 1
    for entry in matches:
        add_str = '<li style={0}>{1} <a href="{2}:{3}:0">{2}:{3}</a></li>'.format(_line_style, entry['refer'], entry['filename'], entry['pos'])
        html_content += add_str
        col = min(len(add_str), _max_col)
        row += len(add_str)/_max_col # delta row = 增加字数/一行的字数
    html_content += '</ul></div>'

    # 显示pop-up视图 
    view.show_popup(html_content, max_height = get_height(row), max_width = get_width(col), 
        flags = sublime.HIDE_ON_MOUSE_MOVE_AWAY, location = point,on_navigate = navigate_cb)
    return True
    
def get_height(row):
        return min(row * 20, MAX_POPUP_HEIGHT)

def get_width(col):
        return min(col * 20, MAX_POPUP_WIDTH)

def navigate_cb(address):
    sublime.active_window().open_file(address, sublime.ENCODED_POSITION)

# 寻找匹配
def find_match(views, word):

    matches = []
    for v in views:
        cur_matches = []
        regions = v.find_all(r'(\s*)\n(.*)' + re.escape(word) + r'(.*?).*\n', sublime.IGNORECASE, "$0", cur_matches)

        i = 0
        while i < len(cur_matches):
            startrow, startcol = v.rowcol(regions[i].end())
            # print (sentences[i]+" : "+str(startrow+0)+"," + str(startcol + 0))
            entry = {'refer':cur_matches[i], 'pos':startrow, 'filename': v.file_name()} 
            matches.append(entry)
            i += 1

    return matches

if sublime.version() >= '3000':
    def is_empty_match(match):
        return match.empty()
else:
    plugin_loaded()
    def is_empty_match(match):
        return match is None

class EngCommand(sublime_plugin.TextCommand):

    # 进入指定语句
    def on_done(self, index):
        if index == -1:
            return 

        record_address = '{0}:{1}:0'.format(self.items[index]['filename'], self.items[index]['pos'])
        sublime.active_window().open_file(record_address, sublime.ENCODED_POSITION)

    def run(self, edit):
        other_views = [
            v
            for v in sublime.active_window().views()
            if v.id != self.view.id and is_included(v.scope_name(0), settings.get("include_sources", []))
            
        ]
        other_views = other_views[0:MAX_VIEWS]
        self.items = find_match(other_views,'.')
        sentences = [ entry['refer'] for entry in self.items ]
        
        sublime.active_window().show_quick_panel(
            sentences, 
            self.on_done
        )