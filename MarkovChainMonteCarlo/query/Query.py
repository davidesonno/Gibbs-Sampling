import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from inference import StateCounter

class QueryResult:
    """
    Formats the StateCounter holding the approximate inference
    computed.

    Parameters
    -
    counts: StateCounter
        the object used to store the counts of the states
    rounding: int 
        optional parameter to be able to print smaller 
        probabilities
        
    """
    def __init__(self, counts: StateCounter,rounding:int):
        self.variables = counts.variables # vars of the query
        self.values = counts.values # possible values of the vars
        self.counts = counts.counter # counts for each state, to be normalized soon
        # normalize the counts
        tot=sum(list(self.counts.values()))
        for state in self.counts.keys():
            self.counts[state]/=tot
        self.rounding=rounding

    def __str__(self):
        # lets see how "large" the words to print will be
        max_widths={}
        for var in self.variables:
            max_widths[var]=max(len(f"{var}({v})") for v in self.values[var])
        vars_text=','.join(str(var) for var in self.variables)
        query_text=f'phi({vars_text})'
        max_widths['probability']=len(query_text)+2

        # create the separator for the rows
        row_line=''
        for var in self.variables:
            row_line+=f"+{'-'*(max_widths[var]+2)}"
        row_line+=f"+{'-'*(max_widths['probability']+2)}+\n"

        # create the table header
        header=''
        for var in self.variables:
            header+=f"| {var:<{max_widths[var]}} "
        header+=f"| {query_text:>{max_widths['probability']}} |\n"

        # create the separator between the header and the probabilities
        thick_row_line=''
        for var in self.variables:
            thick_row_line+=f"+{'='*(max_widths[var]+2)}"
        thick_row_line+=f"+{'='*(max_widths['probability']+2)}+\n"

        table=''
        for state in list(self.counts.keys()):
            # create the states
            values = [f"{var}({probability})".ljust(max_widths[var]) for var, probability in zip(self.variables, state)]
            formatted_values = ' | '.join(values)
            formatted_counts = f"{self.counts[state]:.{self.rounding}f}" 
            # create the row
            formatted_row = f"| {formatted_values} | {' ' * (max_widths['probability'] - len(formatted_counts))}{formatted_counts} |"
            table+=formatted_row+'\n'+row_line

        return row_line+header+thick_row_line+table

    def get_nparray(self):
        import numpy as np
        return np.array(list(self.counts.values()))