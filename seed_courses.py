import sqlite3
import os

DB_PATH = os.path.join('database', 'database.db')

def insert_courses():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    courses = [
        ("Python Masterclass Part 5", 
         "Complete Python Programming from beginner to advanced. Learn coding from scratch, data structures, object-oriented programming, and build real-world projects.",
         "https://cdn.fs.teachablecdn.com/ju5fq6mRwOVwoMkb4B0g", 29.99),
        
        ("Data Science Bootcamp Part 5", 
         "Learn data analysis, machine learning, artificial intelligence concepts with hands-on case studies and capstone projects. Excel in the booming data field.",
         "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRP3Bt_xDlpi1YCUeKijBq7_a0erGw2DsYd9uAvkDCZ9EfwW6S4fA1AFAKjag51V7xVHuA&usqp=CAU", 39.99),
        
        ("Web Development Full Stack Part 5", 
         "Master front-end and back-end web development including HTML5, CSS3, JavaScript, React.js, Node.js, and MongoDB. Build responsive websites and apps.",
         "https://jaro-website.s3.ap-south-1.amazonaws.com/2024/04/0-cl7fc6pt1MHjIF4K.png", 35.00),
        
        ("Cloud Computing with AWS Part 5", 
         "Learn cloud computing with Amazon AWS. Understand EC2, S3, RDS, Lambda, and build scalable applications on the cloud platform.",
         "https://miro.medium.com/v2/resize:fit:2000/1*vLNbKAWbGtFLC7tUBYb50A.png", 45.00),
        
        ("Excel Data Analysis Part 5", 
         "Master Excel for data analysis. Learn pivot tables, charts, VLOOKUPs, dashboards, macros and automate workflows effectively using Microsoft Excel.",
         "https://process.fs.teachablecdn.com/ADNupMnWyR7kCWRvm76Laz/resize=width:705/https://cdn.filestackcontent.com/MEeDmR7RRC12EzjJtTQQ", 19.99),
        
        ("Android App Development Part 5", 
         "Design and build Android mobile applications using Android Studio and Kotlin. Publish your own apps to Google Play Store successfully.",
         "https://www.pankajkumarseo.com/wp-content/uploads/2022/06/Android-App-Development-Course.png", 27.99),
        
        ("Cybersecurity Essentials Part 5", 
         "Understand network security fundamentals, ethical hacking, penetration testing, cyberattack defenses, and build a career in cybersecurity.",
         "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRoZqHUhXsp6dq1Dhj5CfuScq8dohDEZgDWHQ&s", 33.00),
        
        ("Artificial Intelligence Basics Part 5", 
         "Introduction to AI, deep learning, computer vision, robotics, and reinforcement learning. Start your journey into the world of intelligent machines.",
         "https://microsoft.github.io/AI-For-Beginners/lessons/sketchnotes/ai-overview.png", 40.00),
        
        ("Financial Accounting Fundamentals Part 5", 
         "Understand key accounting principles, financial statements, cash flows, income statements, and balance sheets for businesses and startups.",
         "https://sophiacollege.ac.in/wp-content/uploads/2023/04/B-Com-Accounting-and-Finance-900x550.png", 22.50),
        
        ("Business Communication Skills Part 5", 
         "Develop effective communication techniques for business environments. Master emails, reports, presentations, public speaking, and negotiation skills.",
         "https://zeroinfy.in/cdn/shop/products/BC.jpg?v=1644236493", 18.00)
    ]

    for title, desc, img, price in courses:
        c.execute("INSERT INTO courses (title, description, image, price) VALUES (?, ?, ?, ?)", (title, desc, img, price))

    conn.commit()
    conn.close()
    print("10 Courses inserted successfully!")

if __name__ == "__main__":
    insert_courses()
