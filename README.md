**"Product Recommendation Library"** 

This application is a web-based decision support and product recommendation platform built using **Streamlit (Python)**, utilizing **Google Sheets** as its database storage. The application is designed to streamline the searching, comparing, and analyzing of user interactions with an industrial cleaning equipment product catalog.

### Key Features of the Application

* **Smart Catalog & Filtering:** Users can filter equipment (such as Gausium or Fiorentini brands) based on highly specific technical parameters, including environment type, floor type, target cleaning area, maximum floor slope, aisle width, as well as waste types and obstacles.


* **Product Details & Comparison:** Provides a pop-up interface to view detailed product specifications, watch demo videos, and download PDF brochures. It includes features to share product specifications directly via WhatsApp or Email, as well as a *Compare Product* feature to compare the specifications of multiple tools side-by-side.


* **User Management (Role-Based Access Control):** Secures the system with login authentication that divides users into **Admin** and **User** roles. New users can sign up (requiring a company email domain), but their accounts are set to *Pending* status and require Admin approval via the *User Management* page.


* **Analytics Dashboard & Activity Logging:** Proactively logs every operational activity within the application, ranging from login history and filter combinations used by users, to the most frequently downloaded and shared products. This data is visualized in interactive charts using **Plotly** on the *Product Analytics* and *Filter Analytics* pages.


