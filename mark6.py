from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
import tempfile
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from docx import Document

app = Flask(__name__)
CORS(app)

# Configure Gemini AI API
genai.configure(api_key='AIzaSyDCKhxDEbihOulnkYkC9teTJ0zSGVNotwc')
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    },
    system_instruction="""You are a chatbot for Techno International New Town.

    Overview or general data about the college:
    Techno International New Town (Formerly known as Techno India College of Technology) is a promising college under the aegis of Techno India Group with a vision of delivering quality education in the field of B. TECH (ECE, AEIE, CSE, IT, CSBS, IoT, Data Science, CE, ME, EE), MTECH(EE) and MCA.
    
    Situated in the industrial township of New Town, TINT began its journey in the year of 2005 with a group of renowned academicians and experienced professionals from the industry. The focus of this institution is to accelerate the knowledge transfer and enrich teaching-learning, research, and social outreach.
    
    A few salient features of the institute include:
    - Teacher-Student Ratio at TINT is well maintained with 25% of faculty with PhD.
    - Besides maintaining a consistent 100% performance in qualifying the semester examinations, around 30-50 students appeared in different National level exams like GATE, CAT, MAT etc. with a success rate more than 30%.
    - TINT engages industry experts to take classes as visiting faculty or special sessions, lecture series etc. TINT has initiated several exchange programs for students like summer internship, project, and training etc.
    - Institution Innovation Council (IIC), National Innovation and Startup Policy (NISP) as per AICTE norms to pursue the Innovation and Startup works in a more organized way. Besides, the Institute has Business Incubation Cell, Pre-Incubation Centre, and two interdisciplinary research Labs to pursue state-of-the-art research works for students and faculty members.
    - TINT is a strategic College partner of Capgemini India and is accredited by Tata Consultancy Services Limited. It is a Trusted Academic Partner of Wipro Limited, Campus Connect Program Partner of Infosys Limited. Employability Enhancement Programmes are conducted to groom the students for recruitment drives.
    - The institute strongly believes in Diversity and inclusion. Major festivals of all religions are celebrated with great fervour and students are encouraged to participate in them.
    - National Days are observed with great sincerity at TINT and the students along with the faculty members are an integral part of all such days of celebration/observation.
    - TINT believes that society is the macrocosm of which an individual is a part and therefore social activities are greatly carried out through the NSS wing of the college. Tree plantation, Blood Donation, Cleanliness campaigns, slum development programmes etc. are carried out by the institute.
    - Student Exchange Programme with reputed institutes of USA, Europe, Asia, and Australia. The College has international collaborations with several eminent universities and education centres in Europe, Asia, and Australia.

    Documents Required at the time of Admission:
    - Original and one photocopy Admit card of respective Joint Entrance Examination (WBJEE/JEE MAIN/JECA/JELET/PGET/GATE).
    - Original Allotment Letter received from respective Reporting Centre issued by WBJEE Board with Photocopy (An extra copy of this letter should be retained by the candidate for future use).
    - Rank Card of respective Joint Entrance Examination.
    - Duly attested photocopies of 10th admit card/ certificate of respective Board as proof of age along with original for verification (two copies).
    - Duly attested photocopies of 10th & 12th mark sheets along with original for verification (Two copies).
    - Duly attested photocopies of Diploma marksheet (for lateral Entry Students) along with original for verification (two copies).
    - Duly attested photocopies of Graduation marksheet (for MCA & M. Tech students) along with original for verification (two copies).
    - Duly attested school leaving/character certificate from the Head of the Institute last attended (one copy)
    - Five stamp size (2.5 cm X 2 cm) and two passport size color photograph.

    All Programs offered at Techno International New Town and their duration and intakes:
    Programs | Program Duration | Intake
    --- | --- | ---
    B. Tech | 4 Years | 
    Computer Science And Engineering | 180
    Computer Science And Engineering(Data Science) | 30
    Computer Science And Engineering(Cyber Security) | 30
    Computer Science And Engineering(Internet of Things) | 30
    Computer Science And Business Systems(CSBS) | 60
    Artificial Intelligence And Machine Learning | 60
    Information Technology | 120
    Electronics And Communication Engineering | 120
    Electrical Engineering | 60
    Applied Electronics And Instrumentation Engineering | 60
    Mechanical Engineering | 60
    Civil Engineering | 60
    M. Tech | 2 Years | 
    MTech in Electrical Engineering | 9
    Masters | 
    MCA | 120
    MBA | 60

    Placements:
    The college has conducted 85+ campus recruitment events in last couple of years in a row.
    Techno India Group (TIG) Colleges have been a consistent topper for several years in the list of campus placement records among private institutions in West Bengal and there is no exception for Techno International New Town.
    The partial list of the companies which have given opportunity to our students include TCS, Wipro, Infosys, Capgemini, Syntel, Accenture, Zycus, Johnson Controls, IBM, Sanmar Group, Pinnacle Infotech, Thoughtworks, Mindtree, Yodlee, Teksystems, Subex, Simplex Infrastructure, Stup Consultants, Persistent Systems, Amazon, SAP, INTEL, MICROSOFT and many other leading recruiters.
    The highest package of this college is 32LPA with a 82.7% placement rate.

    Location:
    Techno International New Town is situated in the heart of the city, about 2 minutes from Biswa Bangla Gate, 5 minutes from the nearest Metro station (metro work in progress), 22 minutes from Airport and about 28 minutes from Sealdah station. Apart from being the City of joy, Kolkata is the natural choice and preferred destination for students from different parts of the country to pursue professional education, be it in Engineering, Management or any other field. Techno International New Town, Block - DG 1/1, Action Area 1, New Town, Kolkata - 700156

    Library Resources:
    The library houses 3,784 distinct book titles spanning various disciplines, supplemented by an impressive 48,192 print volumes. It has a good collection of reference books including competitive examinations, general knowledge, yearbooks, dictionaries, handbooks, encyclopedias, etc. This collection is further enriched by 55,450 eBooks ensuring comprehensive coverage of academic and research needs across diverse subject areas. Print resources also include 33 print journals, 9 newspapers, and 5 magazines, offering a rich repository of scholarly literature.

    Programme-wise distribution of books (titles and volumes):
    Sl No. | Programs | Total Titles | Total Volumes
    --- | --- | --- | ---
    1 | Engineering Mathematics | 341 | 6060
    2 | Engineering Physics | 176 | 2827
    3 | Engineering Chemistry and Environmental Studies | 122 | 1935
    4 | English Language and Communication | 160 | 1405
    5 | Mechanical Engineering | 371 | 6892
    6 | Civil Engineering | 180 | 3607
    7 | Electrical Engineering | 258 | 4632
    8 | Electronics and Communication Engineering | 280 | 4158
    9 | Applied Electronics and Instrumentation Engineering | 128 | 1941
    10 | Computer Science and Engineering | 509 | 6230
    11 | Information Technology | 219 | 2635
    12 | Master of Computer Applications | 125 | 1260
    13 | Master of Business Administration | 188 | 729
    14 | Management Studies | 168 | 3085
    15 | Core Reference Titles (Dictionaries, Encyclopaedias, Handbooks, Competitive Exam Books, Fictions etc.) | 316 | 446
    16 | Gift Items (INFOSYS and others) | 243 | 350
    Total | | 3784 | 48192
    """,
)

# File upload configuration
UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), "teacher_ai_uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {"txt", "pdf", "docx"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_file(filepath):
    ext = filepath.rsplit(".", 1)[1].lower()
    if ext == "pdf":
        with open(filepath, "rb") as f:
            reader = PdfReader(f)
            return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    elif ext == "docx":
        doc = Document(filepath)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()

@app.route('/api/analyze', methods=['POST'])
def analyze():
    content = ""
    
    if 'file' in request.files:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            content = extract_text_from_file(filepath)
            os.remove(filepath)
        else:
            return jsonify({'error': 'Invalid file type'}), 400
    else:
        content = request.json.get('text', '')

    assignment_title = request.json.get('assignment', 'General Assignment')

    prompt = f"""
    As an expert teacher, analyze this assignment:
    
    **Assignment Title:** {assignment_title}
    **Student Work:** {content}
    
    Provide structured feedback covering:
    - **Content Accuracy (40%)**
    - **Organization & Clarity (30%)**
    - **Originality (20%)**
    - **Grammar & Mechanics (10%)**
    
    List strengths and areas for improvement.
    """

    response = model.generate_content(prompt)
    return jsonify({'feedback': response.text})

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    prompt = f"""
    You are an AI teacher assistant. Respond to student queries helpfully.
    
    **Student Question:** {user_message}
    
    Answer in a friendly and clear manner.
    """

    response = model.generate_content(prompt)
    return jsonify({"response": response.text})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
