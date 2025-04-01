# Vogue Nest 🌟

**Redefining Fashion E-Commerce**  
![main-page](docs/images/responsive.png)

## ***Note***: 
In checkout, please use this credit card number
``` 4242 4242 4242 4242 ``` with any later date and a CVC.

## Table of Contents
- [Vogue Nest 🌟](#vogue-nest-)
  - [***Note***:](#note)
  - [Table of Contents](#table-of-contents)
- [👗 About](#-about)
- [✨ Key Features](#-key-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [👥 User Stories](#-user-stories)
- [The Scope Plan](#the-scope-plan)
- [The Structure Plane](#the-structure-plane)
- [📝Testing](#testing)
- [©️ Credits](#️-credits)
- [💌 Acknowledgments](#-acknowledgments)


# 👗 About
Vogue Nest is a cutting-edge fashion e-commerce platform that combines modern web technologies with AI-powered recommendations to deliver a personalized shopping experience. Designed for fashion enthusiasts who value both style and convenience, our platform offers:

- Curated collections from emerging designers
- Sustainable fashion marketplace

**Live Demo:** https://vogue-nest-bb4c62d54744.herokuapp.com/

# ✨ Key Features
  - ## 🛍️ Core Functionality
    - **Smart Product Catalog** with dynamic filtering
    - **User Authentication System** (Email & Social Login)
    - **Advanced Shopping Cart** with session persistence
    - **Secure Checkout** with Stripe integration
    - **Order Tracking & History**
    - **Product Reviews & Ratings**
    - **Admin Dashboard** with analytics


# 🛠️ Tech Stack
  - ## Backend
    - **Framework:** Django 3.2.25
    - **Database:** PostgreSQL
    - **Authentication:** Django Allauth
    - **Payments:** Stripe API

  - ## Frontend
    - **CSS Framework:** Bootstrap 5.3
    - **JavaScript:** Vanilla JS + HTMX
    - **Templating:** Django Templates
    - **Icons:** Font Awesome 6
    - **Animations:** CSS3 + Animate.css

  - ## Infrastructure
    - **Hosting:** AWS
    - **Storage:** AWS S3
    - **CI/CD:** GitHub Actions
    - **Wireframes:** Miro/ Figma
    - **Entry-Relationship Diagram Design (ERD):** [mermaidchart](https://www.mermaidchart.com)
    - **AI chatbots:** [chatbots](https://app.fastbots.ai/)
    - **Creating and styling the logo:** [Canva](https://www.canva.com/)
    - **Converting logo image into favicon:** [Favicon](https://favicon.io/)

# 👥 User Stories
  - ## 🎯 First Time Visitor Goals
  As a first time visitor, I want to be able to:
    -  **Discover the Platform**
        - Browse products without creating an account.
        - View featured collections, trending items and promotions.
        - Explore the blog for fashion tips, trends, and inspiration.

    - **Registration & Onboarding**
      - Easily create an account (email)
      - Receive welcome email with style guide
      - Access quick tour of platform features, including the blog and contact page.

    - **Initial Exploration**
      - Filter products by category/price/size
      - View detailed product descriptions, images, and specifications.
      - Read customer reviews and ratings for products.
      - Explore blog posts for additional insights and recommendations.

    - **Trust Building**
      - View SSL security verification
      - See recognized payment method icons for secure transactions.
      - Access the contact page to reach out for inquiries or support.
    
    - **Engagement with Blog**
      - Read articles on fashion trends, styling tips, and product highlights.
      - Read customer comments and thier contributions.

    - **Contact and Support**
      - Easily find the contact page for customer support or inquiries.
      - Use a contact form to submit questions or feedback.


  - ## 🔄 Regular User (Customer) Goals
  As a Regular User, I want to be able to:
  - **Shopping Experience**
      - Browse and search for products using filters (category, price, size, etc.).
      - Add products to the shopping cart.
      - View detailed product descriptions, images, and reviews.
      - Place orders with a secure checkout process.
      - Track order status and view order history.
    
  - **Account Management**
      - Log in using email or social login.
      - Update personal information, shipping address, and payment details.

  - **Engagement with Blog**
      - Read blog posts for fashion tips, trends, and product recommendations.
      - Comment on blog posts and engage with other users.
    
  - **Customer Support**
      - Access the contact page for inquiries or support.
      - Use the contact form to submit questions or feedback.

    - **Trust and Security**
      - View SSL security verification and trusted payment icons.
      - Receive email notifications for order confirmation and updates.

  - ## 👔 Manager/Admin Goals
    - **Product Management**
      - Add, update, or delete products in the catalog.
      - Manage product categories, sizes, and colors.
      - Upload and manage product images.

    - **Order Management**
      - View and manage customer orders.
      - Update order statuses (e.g., processing, shipped, delivered).
      - Handle order cancellations and refunds.

    - **User Management**
      - View and manage customer accounts.
      - Handle user inquiries or complaints submitted via the contact form.

    - **Blog Management**
      - Create, edit, or delete blog posts.
      - Moderate comments on blog posts.
      - Analyze blog engagement metrics (e.g., views, shares, comments).

    - **Security and Compliance**
      - Ensure SSL certificates and secure payment integrations are active.
      - Monitor for suspicious activities or fraudulent transactions.

    - **Customer Support**
      - Respond to customer inquiries submitted via the contact page.
      - Resolve escalated issues or disputes.
      - Provide updates to customers regarding their orders or concerns.

    - **Platform Maintenance**
      - Manage website settings and configurations.
      - Perform regular backups and updates to the platform
      - Ensure uptime and resolve technical issues promptly.



# The Scope Plan
  - Responsive  Design
      - Ensure the app is fully functional and visually consistent across all devices (mobile, tablet, desktop).
  - Intuitive Navigation
      - Implement a collapsible hamburger menu for tablet/mobile users to simplify access to core features (e.g., shops, contact, blogs).
  - User/Admin Management
    - CRUD for products: Allow superusers to easily create, update, and delete products, with secure authentication and profile customization.



# The Structure Plane
  - ## 💪 Features

    All pages have:
    - #### A header:
    ![Home](docs/images/header.png)
    - #### A Footer
    ![Home](docs/images/footer.png)
    - #### Home page
    ![Home](docs/images/home1.png)
    ![Home](docs/images/home2.png)
    ![Home](docs/images/home3.png)

    - #### Shops Page
    ![Shops](docs/images/products.png)
    - #### Register Page
    ![Register](docs/images/signup.png)
    - #### Sign in Page
    ![signin](docs/images/signin.png)

    - #### Profile Page
    ![Profie](docs/images/profile.png)
    - #### Product Detail
    ![Product Detail](docs/images/product_detail.png)
    - #### Add Product as an dmin
    ![Add Product](docs/images/add-product.png)
    - #### Edit Product as an admin
    ![Edit product](docs/images/edit-product.png)
    - #### Confirm/Delete Product as an admin
    ![Delete product](docs/images/confirmdelet.png)
    - #### Delete Product as an admin
    ![Delete product](docs/images/delete-product.png)
    - #### Cart
    ![Cart](docs/images/cart.png)
    - #### Cart/ Adding Discount
    ![Discount](docs/images/adding-discount.png)
    - #### Cart/ Removing Discount
    ![Discount](docs/images/remove-discount.png)
    - #### Checkout process
    ![Checkout](docs/images/checkout.png)
    - #### Checkout Success
    ![Checkout](docs/images/checkout-success.png)
    - #### Invoice
    ![invoice](docs/images/invoice.png)
    - #### Blog Page
    ![Contact-us](docs/images/blog.png)
    - #### Article Page
    ![Article](docs/images/article1.png)
    - #### Contact Us Page
    ![Contact-us](docs/images/contact.png)
    - #### Thank You Page
    ![Thank-you-page](docs/images/thank-you.png)
    - #### Admin Page
    ![Admin](docs/images/admin-panel.png)

  
  - ## ✎ Wireframes
      The app’s wireframes outline a user-centric design across key screens, including:
      - Home page 
          - ![main-page](docs/main-page.pdf)
          - ![main-page](docs/main-page-wf.pdf)

      - blog page
        - ![blog-page](docs/blog.pdf)
      - Contact Page
        - ![contact-pages](docs/contact.pdf)
      - Products Page
        - ![products-page](docs/products.pdf)

  - ## 🛢️ Database:
  ![RED](docs/images/ERD.png)

      - ### Key Relationships:
        - User has one UserProfile (1:1)
        - User can have many Reviews and Comments (1:M)
        - UserProfile can have many Orders (1:M)
        - Order contains multiple OrderLineItems (1:M)
        - Product can appear in multiple OrderLineItems (1:M)
        - Product belongs to a Category (M:1)
        - Category can have sub-categories (self-referential)
        - Product has M:M relationships with Size and Color
        - Category defines available Sizes and Colors (M:M)
        - Product has multiple ProductImages (1:M)
        - Product can have multiple Reviews (1:M)

  - ## 🚀 Installation
    - ### Prerequisites
      - Python 3.10+
      - PostgreSQL 15
      - Cloud Storage

    - ### Setup Instructions
      1. Clone the repository:
           ```bash
           git clone https://github.com/Jawahir01/VogueNest
           cd vogue-nest

      2. Create virtual environment:
          ```
          python -m venv venv
          source venv/bin/activate  # Linux/MacOS
          venv\Scripts\activate     # Windows
          ```
      3. Install dependencies:
          ```
          pip install -r requirements.txt
          ```
      4. Configure environment variables (create .env file):
          ```
          DEBUG=False
          SECRET_KEY=your-secret-key
          DATABASE_URL=postgres://user:password@localhost/voguenest
          STRIPE_PUBLIC_KEY=your-stripe-key
          STRIPE_SECRET_KEY=your-stripe-secret
          AWS_ACCESS_KEY_ID=your-aws-key
          AWS_SECRET_ACCESS_KEY=your-aws-secret
          ```
      5. Run migrations:
          ```
          python manage.py migrate
          ```
      6. Create superuser:
          ```
          python manage.py createsuperuser
          ```
      7. Start development server:
          ```
          python manage.py runserver
          ```

# 📝Testing
  The was tested on every step to make sure it's functioning well. Due to time consuming, I was not able to document my testing.

# ©️ Credits
- [gitpod](https://gitpod.com/): the IDE used to develop the website.
- [ThemeWagon](https://themewagon.com/themes/): For providing a free Responsive HTML5 Bootstrap 5 Educational Website Templates.
- [ChatGPT](https://chat.openai.com/): was used to write the update form code, username joind with user-icon and to give more formal sentences for the website and README file.
- [Favicon.io](https://favicon.io/): was used to convert the logo image into favicon.
- [Stack Overflow](www.stackoverflow.com): was used to search for code related errors and bugs.
- [Stripe](https://stripe.com/gb): was used to accept credit and debit card test payments. 
- [Amazon](www.amazon.com): for the produts images and products data.
- [amazon AWS](https://aws.amazon.com/): for cloud storages to the static and media files.
- [Heroku](https://dashboard.heroku.com/apps): for deployment



# 💌 Acknowledgments
  - **[Iuliia Konovalova](https://github.com/IuliiaKonovalova)** :My Mentor Guidance at Code Institute for her professional teaching and helping throughout the project time.
  - **[Manu Perez](https://github.com/Manuperezro)** : My supervisor at City of Bristol College for his patience, support and encouragement all the time.