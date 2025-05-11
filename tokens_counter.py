import json
from  NotesProcessor import NotesProcessor

def count_tokens(filepath):
    """Counts the number of tokens in a text file.
    
    Args:
        filepath: The path to the text file.
    
    Returns:
        The number of tokens in the file.
    """
    try:
        processor = NotesProcessor(filepath)
        data = processor.process_notes()
        tokens = 0
        for item in data:
            print(item)
            length = len(item['note'].split())
            tokens += length
        return tokens
    except FileNotFoundError:
        return f"Error: File not found at '{filepath}'"
    except Exception as e:
        return f"An error occurred: {e}"

# Example usage:
file_path = 'data/graph_data/3topics_notes.xlsx'
token_count = count_tokens(file_path)

if isinstance(token_count, int):
    print(f"The file '{file_path}' contains {token_count} tokens.")
else:
    print(token_count)