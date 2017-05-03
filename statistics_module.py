# -*- coding: utf-8 -*-
import time
import os
import itertools
import urlparse
import html_injector
import webbrowser
import json
import difflib

class Statistics:

    def __init__(self, source, target, output_directory):
        self.source_text = source
        self.target_text = target
        self.output_directory = output_directory
    def calculate_time_per_segment(self):
            seconds_spent_by_segment = {}
            percentaje_spent_by_segment = {}
            total_time_spent = 0
            #again with the closure, lets see how it plays out.
            def pairwise(iterable):
                a, b = itertools.tee(iterable)
                next(b, None)
                return itertools.izip(a, b)

            now = int(time.time()*1000)
            myList = sorted(self.log.keys())
            my_source_log = self.log
            my_source_log[now] = self.log[myList[-1]]

            #calculate time spent by segment
            for current_timestamp,next_timestamp in pairwise(sorted(my_source_log.keys())):
                #for current_timestamp,next_timestamp in sorted(self.source_log.keys()):
                delta = (int(next_timestamp) - int(current_timestamp))/1000
                delta += 1000
                for segment_index in my_source_log[current_timestamp]:
                    if segment_index in seconds_spent_by_segment:
                        seconds_spent_by_segment[segment_index] += delta
                    else:
                        seconds_spent_by_segment[segment_index] = delta
            #calculate total time spent
            for a in seconds_spent_by_segment:
                total_time_spent += seconds_spent_by_segment[a]
            #calculate percentajes
            for a in seconds_spent_by_segment:
                percentaje_spent_by_segment[a] = float(seconds_spent_by_segment[a]) *100 / float(max(1,total_time_spent))


            title = "<th>Segment </th><th>" + '%'+ " of the time spent </th>"
            return self.build_pie_as_json_string(percentaje_spent_by_segment),self.build_table(percentaje_spent_by_segment),title
    def calculate_time_per_segmentv2(self):
        seconds_spent_by_segment = {}
        percentaje_spent_by_segment = {}
        total_time_spent = 0
        #again with the closure, lets see how it plays out.
        def pairwise(iterable):
            a, b = itertools.tee(iterable)
            next(b, None)
            return itertools.izip(a, b)

        #calculate time spent by segment
        for current_timestamp,next_timestamp in pairwise(sorted(self.log.keys())):
            #for current_timestamp,next_timestamp in sorted(self.log.keys()):
            delta = (int(next_timestamp) - int(current_timestamp))/1000
            for segment_index in self.log[current_timestamp]:
                if segment_index in seconds_spent_by_segment:
                    seconds_spent_by_segment[segment_index] += delta
                else:
                    seconds_spent_by_segment[segment_index] = delta
        #calculate total time spent
        for a in seconds_spent_by_segment:
            total_time_spent += seconds_spent_by_segment[a]
        #calculate percentajes
        for a in seconds_spent_by_segment:
            percentaje_spent_by_segment[a] = float(seconds_spent_by_segment[a]) *100 / float(total_time_spent)


        title = "<th>Segment </th><th>" + '%'+ " of the time spent </th>"
        return self.build_pie_as_json_string(percentaje_spent_by_segment),self.build_table(percentaje_spent_by_segment),title

    def get_insertion_and_deletions(self, original, modified):
        s = difflib.SequenceMatcher(None, original.strip(), modified.strip())
        insertions = []
        deletions = []
        for tag, i1, i2, j1, j2 in s.get_opcodes():
            if tag == "insert" or tag == "replace":insertions.append((j1,j2))
            if tag == "delete"or tag == "replace": deletions.append((i1,i2))
        return (insertions,deletions)

    def calculate_insertions_or_deletions_percentajes(self, get_removals_percentaje = True):

        total_insertions_or_deletions = 0
        insertions_or_deletions_per_segment = {}
        source_segments = self.source_text
        modified_segments = self.target_text

        for index, (a,b) in enumerate(zip(source_segments, modified_segments)):
            insertions_or_deletions = self.get_insertion_and_deletions(a,b)[get_removals_percentaje]
            for c in insertions_or_deletions:
                if index not in insertions_or_deletions_per_segment:
                    insertions_or_deletions_per_segment[index] = c[1] - c[0]
                else:
                    insertions_or_deletions_per_segment[index] += c[1] - c[0]
        #get total
        for a in insertions_or_deletions_per_segment:
            total_insertions_or_deletions += insertions_or_deletions_per_segment[a]
        #get percentajes
        for a in insertions_or_deletions_per_segment:
            insertions_or_deletions_per_segment[a] =  insertions_or_deletions_per_segment[a] * 100 / float(total_insertions_or_deletions)

        return insertions_or_deletions_per_segment

    def calculate_deletions_per_segment(self):
        percentaje_spent_by_segment=self.calculate_insertions_or_deletions_percentajes(1)
        title = "<th>Segment </th><th>" + '%'+ " of deletions made</th>"
        return self.build_pie_as_json_string(percentaje_spent_by_segment),self.build_table(percentaje_spent_by_segment),title
    def calculate_insertions_per_segment(self):
        percentaje_spent_by_segment=self.calculate_insertions_or_deletions_percentajes(0)
        title = "<th>Segment </th><th>" + '%'+ " of insertions made</th>"
        return self.build_pie_as_json_string(percentaje_spent_by_segment),self.build_table(percentaje_spent_by_segment),title
    def format_table_data(self, segment_index):
        segment_source = self.source_text[int(segment_index)]
        segment_modified =  self.target_text[int(segment_index)]
        id_source = int(segment_index)
        id_target = id_source + 100000
        final_output = '<a href='+ '"' + "javascript:showhide('" +str(id_source)+ "')" + '"' + '><input type="button" value="Source"></a>'
        final_output += '<a href='+ '"' + "javascript:showhide('" +str(id_target)+ "')" + '"' + '><input type="button" value="Target"></a>'
        final_output += '<div id="%d" style="display: none;height:200px;width:400px;border:1px solid #ccc;font:16px/26px Georgia, Garamond, Serif;overflow:auto;">%s</div>' % (id_source,segment_source)
        final_output += '<div id="%d" style="display: none;height:200px;width:400px;border:1px solid #ccc;font:16px/26px Georgia, Garamond, Serif;overflow:auto;">%s</div>' % (id_target,segment_modified)
        return final_output
    def build_table(self, percentaje_spent_by_segment):
        table_data_list = []
        for segment_index in percentaje_spent_by_segment:
            string = "<tr><td>"+str(segment_index)
            string += self.format_table_data(segment_index)+"</td>"
            string += "<td>"+str(percentaje_spent_by_segment[segment_index])+"</td></tr>"
            table_data_list.append(string)
        return ''.join(table_data_list)
    def build_pie_as_json_string(self, percentaje_spent_by_segment):
        pie_as_json_string_list = []
        for a in percentaje_spent_by_segment:
            string = '{label: "' + str(a) + '", data: ' + str(percentaje_spent_by_segment[a]) + '}'
            pie_as_json_string_list.append(string)
        return ','.join(pie_as_json_string_list)

    def calculate_statistics_event(self, button, statistics_name):
        self.tables["translation_table"].statistics_button.hide()
        if statistics_name == "statistics_in_general":
            self.show_the_available_stats(False)
        else:
            self.calculate_statistics(statistics_name)
            self.notebook.set_current_page(6)
    def calculate_statistics(self, statistics_name):
        with open(self.output_directory + "/log.json") as json_data:
            self.log = json.load(json_data)

        pie_as_json_string = ""
        if statistics_name == "time_per_segment":
            pie_as_json_string,table_data,title = self.calculate_time_per_segment()
        elif statistics_name == "insertions":
            pie_as_json_string,table_data,title = self.calculate_insertions_per_segment()
        elif statistics_name == "deletions":
            pie_as_json_string,table_data,title = self.calculate_deletions_per_segment()
        if pie_as_json_string:
            html_injector.inject_into_html(pie_as_json_string, table_data, title, statistics_name)
