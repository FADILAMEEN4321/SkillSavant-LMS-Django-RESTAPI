# Skill Savant e-Learning Platform

## Overview

Skill Savant is a powerful e-learning platform that provides a seamless and intuitive learning experience. This platform empowers instructors to create courses, facilitates student enrollment, offers progress tracking, and encourages engagement through discussion rooms. The integration of AI ensures the delivery of personalized learning roadmaps for each student.

## Key Features

- **JWT Authentication and Role Based Authorization:** Ensuring secure access and appropriate permissions with JSON Web Token authentication and role-based authorization.

- **Tri-tiered User Hierarchy:** The platform supports three user roles - Admin, Instructor, and Student - creating a structured and efficient learning environment.

- **OpenAI Integration:** Seamlessly integrated OpenAI to generate personalized learning roadmaps, enhancing the adaptability of the platform.

- **Real-time Discussion Room:** Utilizing Django Channels to provide a real-time discussion room, fostering collaboration and interaction among students.

- **Scheduled Tasks with Celery:** Employing Celery and Celery Beat for handling scheduled tasks, ensuring efficient background processing.

- **Course Progress Tracking:** Offering functionality to track the progress of courses, providing insights for both instructors and students.

- **Responsive and Modern UI:** The platform boasts a complete responsive and modern user interface built using Tailwind CSS, offering an aesthetically pleasing and user-friendly experience.

- **Secure Enrollment Transactions:** Enabling secure enrollment transactions through integration with Razorpay, ensuring the safety of financial transactions.

## Technologies Used

- **Frontend:** React JS
- **Backend:** Django Rest Framework
- **Authentication:** JWT
- **Version Control:** Git Flow
- **UI Design:** Tailwind CSS
- **Background Processing:** Celery
- **Real-time Communication:** Django Channels
- **Content API:** Utilized for seamless content delivery
- **Cloud Hosting:** AWS EC2
- **Deployment:** Netlify