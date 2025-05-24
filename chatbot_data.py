from difflib import get_close_matches

faq_responses = {
    "hi": "Hello! How can I assist you today?",
    "hello": "Hi there! How can I help you?",
    "hey": "Hey! What can I do for you?",
    "thank you": "You're welcome!",
    "thanks": "Glad to help!",
    "how to register": "To register, visit the Courses page, select your course, and click 'Enroll'.",
    "how to login": "Click the login button at the top-right and enter your email and password.",
    "how to enroll": "First login, then choose a course and click 'Enroll Now'.",
    "how to make payment": "Go to your cart after enrolling and proceed with payment via available options.",
    "how to view my dashboard": "Click on 'Dashboard' in the top menu to see your enrolled courses.",
    "how to search courses": "Use the 'Search' tab to find a course by name or topic.",
    "how to contact support": "Use the contact form at the bottom or email support@nanoversity.com.",
    "where is my cart": "Your cart is available via the 'Cart' link in the navigation bar.",
    "how to reset password": "Click 'Forgot password?' on the login page and follow the instructions.",
    "what are the available courses": "Visit the Courses page to view all offerings.",
    "can I edit my profile": "Yes, go to your Dashboard and click on 'Edit Profile'.",
    "is this platform free": "Many courses are free, but some may require payment.",
    "can I cancel enrollment": "Please contact support for enrollment cancellation policies.",
    "how do I track my progress": "Your dashboard displays progress for each course.",
    "can I download certificates": "Yes, certificates are available after course completion in your dashboard.",
    "is there a mobile app": "Currently, we support only the web version.",
    "what is the refund policy": "Refunds are issued based on course terms. Please see the payment page for details.",
    "how to apply coupon": "Coupons can be applied during checkout in the cart."
}

def get_bot_response(message):
    message = message.lower()
    matches = get_close_matches(message, faq_responses.keys(), n=1, cutoff=0.4)
    if matches:
        return faq_responses[matches[0]]
    return "I'm sorry, I didn't understand that. You can ask about registration, login, payment, or course details."
