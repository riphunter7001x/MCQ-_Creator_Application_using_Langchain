import os  
import PyPDF2
import json
import traceback 

def read_file(file):
    try:
        if file.name.endswith(".pdf"):
            pdf_reader = PyPDF2.PdfFileReader(file)
            text = ""
            for page in range(pdf_reader.numPages):
                text += pdf_reader.getPage(page).extractText()
            return text
            
        elif file.name.endswith(".txt"):
            return file.read().decode("utf-8")
        
        else:
            raise Exception(
                "Unsupported file format. Only PDF and text file formats are supported."
            )
    except Exception as e:
        raise Exception("Error while reading file:", str(e))
    

def get_table_data(quiz_str):
    try:
        # Convert quiz from str to dict
        quiz_dict = json.loads(quiz_str)
        
        quiz_table_data = []
        for key, value in quiz_dict.items():  # Changed 'quiz' to 'quiz_dict'
            mcq = value["question"]
            options = " | ".join(
                [
                    f"{option}: {option_value}"  # Added a colon between option and option_value
                    for option, option_value in value["options"].items()
                ]  # Added closing square bracket
            )  # Added closing parenthesis
            
            correct = value["answer"]
            quiz_table_data.append({"MCQ": mcq, "choices": options, "correct": correct})
        
        return quiz_table_data
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False
