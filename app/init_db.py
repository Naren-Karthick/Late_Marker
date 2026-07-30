import json
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash
from .database import engine, SessionLocal
from . import models

models.Base.metadata.create_all(bind=engine)

student_data_json = """
{
  "college": "Sri Muthukumaran Institute of Technology",
  "department": "Information Technology",
  "academic_year": "2026-2027",
  "years": {
    "2nd_year": {
      "semester": "3rd Semester (Odd)",
      "batch": "2025-2029",
      "students": [
        { "s_no": 1, "register_no": "212625205001", "name": "Aishwarya A" },
        { "s_no": 2, "register_no": "212625205002", "name": "Aishwarya J" },
        { "s_no": 3, "register_no": "212625205003", "name": "Anu Sri K" },
        { "s_no": 4, "register_no": "212625205004", "name": "Aravind M" },
        { "s_no": 5, "register_no": "212625205005", "name": "Aswin Kumar M" },
        { "s_no": 6, "register_no": "212625205006", "name": "Balaji E" },
        { "s_no": 7, "register_no": "212625205007", "name": "Barath S G" },
        { "s_no": 8, "register_no": "212625205009", "name": "Gayathri M (H)" },
        { "s_no": 9, "register_no": "212625205010", "name": "Grascy Jennifer J R" },
        { "s_no": 10, "register_no": "212625205011", "name": "Gunal S" },
        { "s_no": 11, "register_no": "212625205012", "name": "Hema Sathana M S" },
        { "s_no": 12, "register_no": "212625205013", "name": "Ilakiya B" },
        { "s_no": 13, "register_no": "212625205014", "name": "Ilakkiya M" },
        { "s_no": 14, "register_no": "212625205015", "name": "Jagan S" },
        { "s_no": 15, "register_no": "212625205016", "name": "Janavi M" },
        { "s_no": 16, "register_no": "212625205017", "name": "Jawahar M" },
        { "s_no": 17, "register_no": "212625205018", "name": "Karthik A" },
        { "s_no": 18, "register_no": "212625205019", "name": "Kaviya D" },
        { "s_no": 19, "register_no": "212625205020", "name": "Kaviya Priya V" },
        { "s_no": 20, "register_no": "212625205021", "name": "Keerthika B" },
        { "s_no": 21, "register_no": "212625205023", "name": "Mohammed Aashik Ali S" },
        { "s_no": 22, "register_no": "212625205024", "name": "Mohammed Nayeemudeen N" },
        { "s_no": 23, "register_no": "212625205025", "name": "Mohd Arif Z" },
        { "s_no": 24, "register_no": "212625205026", "name": "Mukesh Kumar K" },
        { "s_no": 25, "register_no": "212625205027", "name": "Muthu Kumaran R" },
        { "s_no": 26, "register_no": "212625205028", "name": "Nandimandalam Balaji" },
        { "s_no": 27, "register_no": "212625205029", "name": "Naren Karthick G" },
        { "s_no": 28, "register_no": "212625205030", "name": "Neethin K" },
        { "s_no": 29, "register_no": "212625205031", "name": "Nishanth S" },
        { "s_no": 30, "register_no": "212625205032", "name": "Nithishgiri S" },
        { "s_no": 31, "register_no": "212625205033", "name": "Nithish Raj R" },
        { "s_no": 32, "register_no": "212625205034", "name": "Pandiselvi R" },
        { "s_no": 33, "register_no": "212625205035", "name": "Pavithra T" },
        { "s_no": 34, "register_no": "212625205036", "name": "Ponmozhi D" },
        { "s_no": 35, "register_no": "212625205037", "name": "Prakash M" },
        { "s_no": 36, "register_no": "212625205038", "name": "Prakash R (H)" },
        { "s_no": 37, "register_no": "212625205039", "name": "Praveen S" },
        { "s_no": 38, "register_no": "212625205040", "name": "Praveena M" },
        { "s_no": 39, "register_no": "212625205041", "name": "Premkumar M" },
        { "s_no": 40, "register_no": "212625205044", "name": "Priyadharshini A (H)" },
        { "s_no": 41, "register_no": "212625205045", "name": "Priyadharshini P" },
        { "s_no": 42, "register_no": "212625205046", "name": "Priyanka S" },
        { "s_no": 43, "register_no": "212625205047", "name": "Ranjan S" },
        { "s_no": 44, "register_no": "212625205048", "name": "Reshma Parveen J" },
        { "s_no": 45, "register_no": "212625205049", "name": "Sakthi K" },
        { "s_no": 46, "register_no": "212625205050", "name": "Sathish A" },
        { "s_no": 47, "register_no": "212625205051", "name": "Srigar K" },
        { "s_no": 48, "register_no": "212625205052", "name": "Sundar S" },
        { "s_no": 49, "register_no": "212625205053", "name": "Thasif Yahiya T" },
        { "s_no": 50, "register_no": "212625205054", "name": "Vasantha Krishnan V" },
        { "s_no": 51, "register_no": "212625205055", "name": "Vasanth Kumar S" },
        { "s_no": 52, "register_no": "212625205056", "name": "Vetriganesh G" },
        { "s_no": 53, "register_no": "212625205057", "name": "Vishal K" },
        { "s_no": 54, "register_no": "212625205058", "name": "Roobini Dj" },
        { "s_no": 55, "register_no": "N/A1", "name": "Abhinaya" },
        { "s_no": 56, "register_no": "N/A2", "name": "Vignesh" },
        { "s_no": 57, "register_no": "N/A3", "name": "Vinothini" }
      ]
    },
    "3rd_year": {
      "semester": "5th Semester (Odd)",
      "batch": "2024-2028",
      "students": [
        { "s_no": 1, "register_no": "212624205001", "name": "Ashwinmaran S" },
        { "s_no": 2, "register_no": "212624205002", "name": "Bharanikumar S" },
        { "s_no": 3, "register_no": "212624205003", "name": "Deepika D" },
        { "s_no": 4, "register_no": "212624205004", "name": "Divya Priya K" },
        { "s_no": 5, "register_no": "212624205005", "name": "Elavarasan A" },
        { "s_no": 6, "register_no": "212624205006", "name": "Ellammal P" },
        { "s_no": 7, "register_no": "212624205007", "name": "Gokulraja M" },
        { "s_no": 8, "register_no": "212624205008", "name": "Harithra A" },
        { "s_no": 9, "register_no": "212624205009", "name": "Jayashree" },
        { "s_no": 10, "register_no": "212624205010", "name": "Jetson G" },
        { "s_no": 11, "register_no": "212624205011", "name": "Kaarki Che P S" },
        { "s_no": 12, "register_no": "212624205012", "name": "Madhusri J V" },
        { "s_no": 13, "register_no": "212624205013", "name": "Manikandan R" },
        { "s_no": 14, "register_no": "212624205014", "name": "Mohan Raj P" },
        { "s_no": 15, "register_no": "212624205015", "name": "Nethra R" },
        { "s_no": 16, "register_no": "212624205016", "name": "Senthil Arasu A" },
        { "s_no": 17, "register_no": "212624205017", "name": "Santhosh Selvam G" },
        { "s_no": 18, "register_no": "212624205018", "name": "Shyam Sundar" },
        { "s_no": 19, "register_no": "212624205019", "name": "Suriyadharan R" },
        { "s_no": 20, "register_no": "212624205020", "name": "Velan V S" },
        { "s_no": 21, "register_no": "212624205021", "name": "Vimal Raj G" },
        { "s_no": 22, "register_no": "212624205022", "name": "Vinoth A" },
        { "s_no": 23, "register_no": "212624205301", "name": "Manikandan S" },
        { "s_no": 24, "register_no": "212624205302", "name": "Manoj Kumar B" },
        { "s_no": 25, "register_no": "212624205303", "name": "Shalini V" },
        { "s_no": 26, "register_no": "212624205701", "name": "Kavi Priya S" }
      ]
    },
    "4th_year": {
      "semester": "7th Semester (Odd)",
      "batch": "2023-2027",
      "students": [
        { "s_no": 1, "register_no": "212623205001", "name": "Abinaya K" },
        { "s_no": 2, "register_no": "212623205002", "name": "Amsavarthini A" },
        { "s_no": 3, "register_no": "212623205003", "name": "Arikrishnan R" },
        { "s_no": 4, "register_no": "212623205004", "name": "Balamurugan S" },
        { "s_no": 5, "register_no": "212623205005", "name": "Bhuvaneshkumar M" },
        { "s_no": 6, "register_no": "212623205006", "name": "Blessi V" },
        { "s_no": 7, "register_no": "212623205008", "name": "Cibichozhan L" },
        { "s_no": 8, "register_no": "212623205009", "name": "Dharshini M V" },
        { "s_no": 9, "register_no": "212623205010", "name": "Dinesh A" },
        { "s_no": 10, "register_no": "212623205011", "name": "Dravid Kumar R" },
        { "s_no": 11, "register_no": "212623205012", "name": "Ebenezer Issac I" },
        { "s_no": 12, "register_no": "212623205013", "name": "Gopi P" },
        { "s_no": 13, "register_no": "212623205014", "name": "Haakesh R V" },
        { "s_no": 14, "register_no": "212623205015", "name": "Hari Prasanth S" },
        { "s_no": 15, "register_no": "212623205016", "name": "Helen Sharon A" },
        { "s_no": 16, "register_no": "212623205017", "name": "Janani B" },
        { "s_no": 17, "register_no": "212623205018", "name": "Kayalvizhi P" },
        { "s_no": 18, "register_no": "212623205019", "name": "Kirubakaran M" },
        { "s_no": 19, "register_no": "212623205020", "name": "Lokesh B" },
        { "s_no": 20, "register_no": "212623205021", "name": "Madhan Kumar B" },
        { "s_no": 21, "register_no": "212623205022", "name": "Madhumitha S" },
        { "s_no": 22, "register_no": "212623205023", "name": "Nadesan S" },
        { "s_no": 23, "register_no": "212623205024", "name": "Nandhini P" },
        { "s_no": 24, "register_no": "212623205025", "name": "Nandhini S" },
        { "s_no": 25, "register_no": "212623205026", "name": "Pooja K" },
        { "s_no": 26, "register_no": "212623205027", "name": "Preethi S" },
        { "s_no": 27, "register_no": "212623205028", "name": "Raghuraj R" },
        { "s_no": 28, "register_no": "212623205029", "name": "Rajavikram V" },
        { "s_no": 29, "register_no": "212623205030", "name": "Rajeswari R" },
        { "s_no": 30, "register_no": "212623205031", "name": "Ruban V" },
        { "s_no": 31, "register_no": "212623205032", "name": "Sagithan K" },
        { "s_no": 32, "register_no": "212623205033", "name": "Sanjay R" },
        { "s_no": 33, "register_no": "212623205034", "name": "Sathiyamoorthi S" },
        { "s_no": 34, "register_no": "212623205035", "name": "Tamilarasan M" },
        { "s_no": 35, "register_no": "212623205036", "name": "Thiruselvam J" },
        { "s_no": 36, "register_no": "212623205037", "name": "Vanishree E" },
        { "s_no": 37, "register_no": "212623205038", "name": "Vanjinathan L" },
        { "s_no": 38, "register_no": "212623205039", "name": "Vinotha K" },
        { "s_no": 39, "register_no": "212623205301", "name": "Jeeva A" }
      ]
    }
  }
}
"""

def seed_db():
    db = SessionLocal()
    
    # Create default users
    users_data = [
        {"username": "hod", "password": "password123", "role": "HOD", "assigned_year": None},
        {"username": "Naren", "password": "Narenguru", "role": "HOD", "assigned_year": None},
        {"username": "staff1", "password": "password123", "role": "Staff", "assigned_year": None},
        {"username": "Gracsy Jennifer", "password": "212625205010", "role": "Rep", "assigned_year": "2nd_year"},
        {"username": "Mohan", "password": "212624205014", "role": "Rep", "assigned_year": "3rd_year"},
        {"username": "Divya", "password": "212624205004", "role": "Rep", "assigned_year": "3rd_year"},
        {"username": "Blessy", "password": "212623205006", "role": "Rep", "assigned_year": "4th_year"},
    ]
    
    for u in users_data:
        existing = db.query(models.User).filter(models.User.username == u["username"]).first()
        if not existing:
            user = models.User(
                username=u["username"],
                password_hash=generate_password_hash(u["password"]),
                role=u["role"],
                assigned_year=u["assigned_year"]
            )
            db.add(user)
    
    # Seed students
    data = json.loads(student_data_json)
    for year_key, year_data in data["years"].items():
        for student_dict in year_data["students"]:
            existing_student = db.query(models.Student).filter(models.Student.register_no == student_dict["register_no"]).first()
            if not existing_student:
                student = models.Student(
                    register_no=student_dict["register_no"],
                    name=student_dict["name"],
                    year=year_key,
                    semester=year_data["semester"],
                    batch=year_data["batch"]
                )
                db.add(student)
                
    db.commit()
    db.close()
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_db()
