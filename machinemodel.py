from docx import Document
import fitz
import google.generativeai as genai

genai.configure(api_key="")

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction=" Hello Gemini. I need you to generate exam questions from the lecture materials and previous exam questions I provide. The questions should follow the exact format of the previous exam questions provided to you. For example, if the provided exam questions have eight theoretical questions with two sections, and each question has parts (a), (b), and (c), I need you to replicate that structure in your response.\n\nThese are the steps you’ll follow:\n\n1. **Format Recognition**:\n   - You need to read the lecture materials and any past exam question data provided to you.\n   - You will extract key concepts, definitions, diagrams, and any mathematical problems.\n   - The final exam questions you generate should have the same number of theoretical questions as in the provided example (for instance, 8 questions) and should follow the structure of two sections with multiple parts for each question.\n\n2. **Content Breakdown**:\n   - For each theoretical question, you will divide it into three parts: (a), (b), and (c).\n   - For questions involving diagrams or mathematical content, you should phrase the subquestions accordingly, ensuring they reference figures or equations where needed.\n\n3. **Example Structure**:\n   If the previous exam had 8 theoretical questions divided into 2 sections with parts (a), (b), and (c), your response should look like this:\n\n   - **Section A**:\n     - **1.** (a) What is the definition of [concept]?  \n         (b) Explain the significance of [concept] in [context].  \n         (c) Provide an example where [concept] is applied.\n     \n     - **2.** (a) What are the steps involved in [process]?  \n         (b) How does [factor] influence [process]?  \n         (c) Explain why [factor] is crucial to understanding [concept].\n\n     - **...**\n\n   - **Section B**:\n     - **1.** (a) Using [formula], calculate [value].  \n         (b) What does the result signify in relation to [theory]?  \n         (c) How would the result change if [condition] was altered?\n\n     - **2.** (a) What is the role of [element] in [system]?  \n         (b) Compare and contrast [two related concepts].  \n         (c) Discuss the importance of [concept] in solving [problem].\n\n     - **...**\n\n4. **Important Considerations**:\n   - When there are references to diagrams, such as “Figure 1” or “Diagram 2,” your questions should refer to these images in your generated questions. Use terms like \"As shown in Figure 1,\" or \"From the diagram above,\" in your questions.\n   - Mathematical content should involve problem-solving and the application of equations, such as calculating values using formulas. You must create parts (a), (b), and (c) around these calculations and interpretations.\n   \n5. **Question Diversity**:\n   - Your questions should cover a range of topics from the lecture materials, ensuring the breadth of the exam content.\n   - Keep the questions in alignment with typical exam formats: theoretical questions, practical applications, and calculations.\n\n6. **Final Output Example**:\n   After analyzing the provided content, your output should be structured exactly like the example below:\n\n   **Generated Exam Question Output**:\n\n   **Section A**:\n   1. (a) Define the term \"photosynthesis.\"  \n      (b) Explain how chlorophyll plays a role in photosynthesis.  \n      (c) Provide an example of an organism that uses photosynthesis and describe its importance in nature.\n\n   2. (a) What is the equation for calculating kinetic energy?  \n      (b) Calculate the kinetic energy of an object with a mass of 10 kg moving at a speed of 5 m/s.  \n      (c) How would the kinetic energy change if the speed of the object were doubled?\n\n   3. (a) Discuss the principles of Newton’s third law of motion.  \n      (b) Provide a real-world example where this law is applied.  \n      (c) Explain why Newton’s third law is fundamental to understanding motion.\n\n   **Section B**:\n   1. (a) What are the four chambers of the human heart, and what role does each play in circulation?  \n      (b) Describe how blood flows through the heart during a heartbeat.  \n      (c) How does the heart’s structure contribute to its function?\n\n   2. (a) Using the formula E = mc², calculate the energy of an object with a mass of 5 kg.  \n      (b) What is the significance of the speed of light in this equation?  \n      (c) How would the energy change if the object’s mass increased to 10 kg?\n      \nI’ve outlined everything. Now, whenever you receive new lecture materials or past exam questions, you will process them to generate predictions based on the above structure. Remember, the final exam should mirror the number of questions, sections, and parts from the past exam while also incorporating the relevant content from the provided lecture materials. Finally, add the answer to each question there, and also the page where the answer is from the overall pdf, note that each question donesnt have to be on the same page, you can scatter as much as possible.",
)

chat_session = model.start_chat(
  history=[
  ]
)

def read_word_file(file_path):
    """Reads a Microsoft Word (.docx) file and returns its content as text."""
    doc = Document(file_path)
    content = []
    for para in doc.paragraphs:
        content.append(para.text)
    return "\n".join(content)

def read_pdf_file(file_path):
    """Reads a PDF file and returns its content as text."""
    pdf_content = []
    with fitz.open(file_path) as pdf:
        for page_num in range(pdf.page_count):
            page = pdf[page_num]
            pdf_content.append(page.get_text())
    return "\n".join(pdf_content)

# Usage example
file_path = "java.pdf"
file_type = file_path.split('.')[-1].lower()

file_content = ""
try:
    if file_type == 'docx':
        content = read_pdf_file(file_path)
        file_content = content
    elif file_type == 'pdf':
        content = read_pdf_file(file_path)
        file_content = content
    else:
        print("Unsupported file type. Please use a .docx or .pdf file.")
except Exception as e:
    print("Error reading file:", e)


past_exam_question = file_content
lecture_material = None 

response = chat_session.send_message(past_exam_question)

print(response.text)