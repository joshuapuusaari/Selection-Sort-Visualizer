# CISC121_FinalProject - Selection Sort Demonstration
# December 2025

# AI-use disclaimer:
# I did not use any AI-generated code. However, I did ask ChatGPT questions about
# how to use Gradio's different components, and how to fix some bugs in my program.

# ----------------------------------------------------------------------------------------------------------

import gradio as gr
from Step import Step

# A function that returns an empty array and zero
# Used to reset the steps array and the stepCounter
def reset_step_counter():
        return [], 0


# A function that adds an input to the list
# Returns the edited list and its corresponding system message
def create_list(input, listopher, steps, stepCounter):
        if input == None or input == "":
                return listopher, "Please enter a valid number.", steps, stepCounter
        listopher.append(input)
        steps, stepCounter = reset_step_counter()
        return listopher, f"Added {input} to the list.", steps, stepCounter


# A function that clears the list
# Returns the cleared list and its corresponding system message
def clear_list(listopher, steps, stepCounter):
        listopher = []
        steps, stepCounter = reset_step_counter()
        return listopher, listopher, "Cleared list.", "[]", steps, stepCounter


# The Selection Sort Algorithm
# Returns the sorted list and its corresponding system message
def selection_sort(listopher, steps, stepCounter):
        steps, stepCounter = reset_step_counter()
        if len(listopher) == 0:
                return "Nothing to sort!", "[]", steps, stepCounter
        n = len(listopher)
        i = 0 # i is the first unsorted index
        while i < (n-1):
                min = i # min will become the index of the minimum value
                j = i + 1
                while j < n: # Finds the minimum value's index
                        if listopher[j] < listopher[min]:
                                min = j
                        j += 1
                steps.append(Step("select",listopher,min,i))
                if min != i: # If min has changed, a swap is needed
                        listopher[i], listopher[min] = listopher[min], listopher[i] # Swap
                        steps.append(Step("swap",listopher,min,i))
                i += 1
        steps.append(Step("complete",listopher,-1,-1))
        
        if steps:
                return "Sorting started.", reformat_list(steps[0].currentList), steps, stepCounter
        return "List is already sorted!", reformat_list(listopher), steps, stepCounter


# Finds the largest sized number (string) in the list to calculate max possible gap between elements
# (The gap will be used to format the display)
def find_max_gap(listopher):
        maxGap = 2
        for z in listopher:
                if len(z)+1 > maxGap:
                        maxGap = len(z)+1
        return maxGap


# Reformats the list for formatting purposes for the algorithm visualisation
def reformat_list(listopher):
        contents = [str(i) for i in listopher]
        maxGap = find_max_gap(contents)
        output = ""
        for i in contents:
                output += (" " * (maxGap - len(i))) + i
        return output


# Generates the pointer arrows in the visualisation
def generateArrows(i, min, listopher):
        contents = [str(i) for i in listopher]
        maxGap = find_max_gap(contents)
        output = ""
        for z in range(len(contents)):
                if z==i or z==min: # Add spaces and an arrow if at target index
                        output += (" "*(maxGap-1)) + "↑"
                else: # Otherwise just fill gap entirely with spaces
                        output += (" " * (maxGap))
        return output


# The main function that displays the process steps for the visualisation
def show_steps(s):
        output = f"{reformat_list(s.currentList)}"
        # Show index comparisons
        if s.actionType == "select":
                output += f"\n{generateArrows(s.i,s.min,s.currentList)}"
                output += f"\nSelecting index {s.i}\nThrough iteration, we find that the minimum value is at index {s.min}"
                if s.i == s.min:
                        output += "\nSince the lowest value is already in the correct place, there is no need to swap."
        # Show swaps
        elif s.actionType == "swap":
                output += f"\nSwapped indices {s.i} and {s.min}, so the found minimum is now in place."
        # Show sort completion
        else:
                contents = [str(i) for i in s.currentList]
                maxGap = find_max_gap(contents)
                output+="\n"
                for z in range(len(contents)):
                        output += (" "*(maxGap-1)) + "↑"
                output += f"\nAfter all swaps have been made, the list is fully sorted, and thus the program terminates."
        return(output)


# This function detects where in the process the visualisation is, and chooses the display accordingly
def find_steps(steps, stepCounter):
        if not steps: # Empty Case
                return "No steps done yet!", listopher, steps, stepCounter, listopher
        
        # Go through Steps
        if stepCounter<(len(steps)):
                stepCounter+=1
                return f"Showing step {stepCounter}/{len(steps)}", show_steps(steps[stepCounter-1]), steps, stepCounter, steps[stepCounter-1].currentList
        
        # All steps complete
        else:
                return "Sorting complete.", steps[-1].currentList, steps, stepCounter, str(steps[-1].currentList)

# Gradio ---------------------------------------------------------------------------------------------------

# Font needs to be a monospace for the arrows to be spaced correctly in the visualisation
custom_css = """
<style>
body, .gradio-container, .gr-block, .gr-input, .gr-textbox textarea, .gr-textbox input, .gr-markdown, .gr-button, .gr-number input {font-family: 'Courier New', Courier, monospace !important;}
#visual_box textarea {
    white-space: pre !important;        /* preserve spacing */
    overflow-x: auto !important;        /* allow for horizontal scroll */
    overflow-y: auto;                  
    word-wrap: normal !important;       /* prevent line-wrapping */
}
</style>
"""

with gr.Blocks() as demo:
        gr.HTML(custom_css)

        # State Variables
        listopher = gr.State([])
        steps = gr.State([])
        stepCounter = gr.State(0)

        # UI Elements
        gr.Markdown("# Selection Sort Demonstration")
        gr.Markdown("This program allows the user to create a list and visually demonstrates and explains selection sort using said list.")

        with gr.Row():
                input = gr.Number(label="Input a number")
                result = gr.Textbox(label="List", lines=3)
                feedback = gr.Textbox(label="System", lines=3)
   
        with gr.Row():     
                addButton = gr.Button("Add Number to List")
                clearButton = gr.Button("Clear List")

        # Animation Components
        visual = gr.Textbox(label="Visualisation", lines=5, elem_id="visual_box")
        with gr.Row():
                sortButton = gr.Button("Start sorting!")
                nextButton = gr.Button("Show next step")

        # Button Functionality
        addButton.click(create_list, inputs=[input, listopher, steps, stepCounter], outputs=[result,feedback,steps,stepCounter])
        clearButton.click(clear_list, inputs=[listopher, steps, stepCounter], outputs=[listopher,result,feedback,visual,steps,stepCounter])
        sortButton.click(selection_sort, inputs=[listopher, steps, stepCounter], outputs=[feedback,visual,steps,stepCounter])
        nextButton.click(find_steps, inputs=[steps, stepCounter], outputs=[feedback,visual,steps,stepCounter,result])

demo.launch(share=True)