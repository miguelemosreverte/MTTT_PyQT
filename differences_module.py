import os
import json
import difflib

class Differences:

         
         
    def __init__(self, unmodified_target, modified_target):
        self.modified_target = modified_target
        self.unmodified_target = unmodified_target

   
    def get_insertion_and_deletions(self, original_segment, modified_segment):
        """Create a tagged diff."""
        #print original_segment
        nl = "<NL>"
        delTag = "<span style=\"background-color:#FE2E2E; font-weight:600\">%s</span>"
        insTag = "<span style=\"background-color:#04B404; font-weight:600\">%s</span>"
        diffs = []
        stats = []
        
        diffText = None

        #print original_segment
        for i in range (0, len(original_segment)):
            deleteCount, insertCount, replaceCount = 0, 0, 0
            diffText = ""
            statText = ""
            mt = original_segment[i].replace("\n", "\n%s" % nl).split()
            pe = modified_segment[i].replace("\n", "\n%s" % nl).split()
            s = difflib.SequenceMatcher(None, mt, pe)
            
            outputList = []
            for tag, alo, ahi, blo, bhi in s.get_opcodes():
                if tag == 'replace':
                    # Text replaced = deletion + insertion
                    outputList.append(delTag % " ".join(mt[alo:ahi]))
                    outputList.append(insTag % " ".join(pe[blo:bhi]))
                    replaceCount += 1
                elif tag == 'delete':
                    # Text deleted
                    outputList.append(delTag % " ".join(mt[alo:ahi]))
                    deleteCount += 1
                elif tag == 'insert':
                    # Text inserted
                    outputList.append(insTag % " ".join(pe[blo:bhi]))
                    insertCount += 1
                elif tag == 'equal':
                    # No change
                    outputList.append(" ".join(mt[alo:ahi]))
            diffText = " ".join(outputList)
            diffText = " ".join(diffText.split())
            diffText = diffText.replace(nl, "\n")
            
            statText = str( "Deletions: %d, Insertions: %d, Replacements: %d" % (insertCount, deleteCount, replaceCount))
            diffs.append(diffText)   
            stats.append(statText)  
       
        return (diffs, stats)
