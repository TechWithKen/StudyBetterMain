from docx import Document
import fitz
import google.generativeai as genai
import markdown

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
  system_instruction = "Hello Gemini. I need you to generate exam questions from the lecture materials and past exam questions provided. The past exam questions serve as a **guide** for how the questions should be structured and formatted, but the output does not need to mirror them exactly. Avoid generating questions that are completely identical to those in the past questions.\n\nThese are the steps you’ll follow:\n\n1. **Format Recognition**:\n   - Carefully read and analyze both the lecture materials and the past exam questions included in the input.\n   - The past exam question section is marked by the keyword: **PAST EXAM QUESTIONS**. This section gives an example of the question format to follow, including the number of sections, types of questions, and subparts.\n\n2. **Content Extraction**:\n   - Extract key concepts, definitions, diagrams, and any mathematical problems from the lecture materials.\n   - Ensure that the final exam questions generated follow the general structure and organizational flow of the past exam questions, but remain original in phrasing and content.\n\n3. **Content Breakdown and Structure**:\n   - Break down each theoretical question into parts (e.g., labeled (a), (b), (c)) where necessary, based on the format in the past questions section.\n   - Phrase each subquestion uniquely, especially for those referencing diagrams, figures, or equations.\n   - Ensure questions cover the main topics in the lecture content, drawing inspiration from the past exam structure as a guide only.\n\n4. **Important Considerations**:\n   - Reference any diagrams or figures from the lecture content directly within your questions (e.g., \"As shown in Figure 1\"), following the past questions format without copying it identically.\n   - For mathematical content, incorporate relevant problem-solving questions using equations, forming questions that align with but don’t duplicate the past exam style.\n\n5. **Diversity of Question Types**:\n   - Cover a range of topics and subtopics within the lecture material, ensuring the generated questions represent a breadth of content without replicating past exam questions verbatim.\n   - Use the past exam questions as a guide to structure and style, but add unique phrasing and content.\n\n6. **Page Referencing**:\n   - For each generated question, include a reference to the specific page(s) within the lecture materials where answers can be found.\n   - Distribute questions across pages as needed for comprehensive coverage, without aligning all questions to the same content or page structure.\n\nFollowing these instructions, process the lecture materials and past exam questions to generate new exam questions. Remember that the past exam questions serve as a **reference** for style and structure, not as an exact template to replicate.\n\nThe final questions should reflect the number, format, and type of questions inspired by the past questions but should be entirely original in content and wording, with page references from the lecture material."

)


chat_session = model.start_chat(
  history=[
  ]
)

def make_prediction(past_exam_question, lecture_material):

    combined_input = f"{lecture_material}\n\nPAST EXAM QUESTIONS:\n{past_exam_question}"

    response = chat_session.send_message(combined_input)

    response_in_html = markdown.markdown(response.text)
    return response_in_html
