# This file should go in ~/Library/Application Support/SublimeText2/Packages/User/
# Additionally, lines like this:
#   { "keys": ["ctrl+alt+a"], "command": "record_audio" },
#   { "keys": ["ctrl+alt+l"], "command": "add_vo_line_numbers" }
# should be added to the keymap file (accessible from the preferences menu)

import sublime, sublime_plugin, os, re

record_script_template = """
#! /bin/bash

rec {0} rate 32k silence 1 0.1 3% 1 00:00:01.0 1% pad 0.5 0.5 &

echo Recording {0}

p=$!
sleep 1
until [ "$var1" != "$var2" ]; do
    var1=`du "{0}"`
    sleep 1
    var2=`du "{0}"`
done
echo "Sound Detected"
until [ "$var1" == "$var2" ]; do
    var1=`du "{0}"`
    sleep 0.25
    var2=`du "{0}"`
done
echo "Silence Detected"
kill $p

open -a "Sublime Text 2"

"""


class RecordAudioCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print('here')
        for region in self.view.sel():
            if region.empty():
                line = self.view.line(region)
                line_contents = self.view.substr(line) + '\n'
            else:
                line = self.view.line(region)
                self.view.run_command("expand_selection", {"to": line.begin()})
                line_contents = self.view.substr(self.view.line(region)) + '\n'

            (filename, number, l) = self.line_to_filename(line_contents)

            if filename is None:
                return

            os.system('mkdir -p ~/Desktop/recordings')

            filepath = '~/Desktop/recordings/%s' % filename
            with open('/tmp/recordvo.sh', 'w') as f:
                f.write(record_script_template.format(os.path.expanduser(filepath)))

            os.system('chmod +x /tmp/recordvo.sh')
            os.system('open -a iTerm.app /tmp/recordvo.sh')

            self.view.replace(edit, line, '[* %s]\t%s' % (number, l))


    def line_to_filename(self, line, maxchars=64):

        r = re.match(r'\[(\*\s)?(\d*)\]\s*(.*)', line)

        if not r:
            sublime.error_message('No line number!')
            return None

        n = r.groups()[1]
        original_line = r.groups()[2]

        l = re.sub(r"[\s+-:><,']", '_', original_line)

        if len(l) > maxchars:
            l = l[0:maxchars]

        filename = n + '_' + l + '.wav'

        return (filename, n, original_line)


class AddVoLineNumbersCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print('here here')
        region = sublime.Region(0, self.view.size())

        text = self.view.substr(region)
        numbered_text = self.add_line_numbers(text)

        self.view.replace(edit, region, numbered_text)

    def add_line_numbers(self, text, starting_number=0):
        all_lines = text.split('\n')

        # filter out blank lines
        lines = []
        for l in all_lines:
            if re.match('\s*$', l):
                continue
            else:
                lines.append(l)

        current_number = starting_number

        for i, l in enumerate(lines):

            r1 = re.match(r'\[(\*\s)?(\d*)\]\s*(.*)', l)
            r2 = re.match(r'\s*#', l)

            if r1 is None and r2 is None:
                lines[i] = '[%.5d]\t%s' % (current_number, l)
                current_number += 10

        return '\n\n'.join(lines)
