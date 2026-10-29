# Frontend Integration Guide: Contact Enquiry Form

This document provides the full API specification, ready-to-use AI generation prompts, and frontend code implementations for connecting to the EasyPack Contact Enquiry API.

---

## 1. Quick Copy-Paste Prompt (For AI Coding Assistants / Frontend Devs)

```markdown
Please create a responsive, modern "Contact Us" form component that integrates with our Django REST Framework backend API.

### API Specifications
- **Endpoint**: `/api/easypack/contact/` (Full dev URL: `http://localhost:8000/api/easypack/contact/`)
- **HTTP Method**: `POST`
- **Request Headers**:
  {
    "Content-Type": "application/json"
  }

- **Request Body (JSON)**:
  {
    "name": "Customer Name",
    "email": "customer@example.com",
    "phone_number": "+91 9876543210",
    "subject": "Inquiry Subject",
    "message": "Detailed message here..."
  }

- **Success Response (HTTP 201 Created)**:
  {
    "message": "Your contact enquiry has been submitted successfully.",
    "email_status": {
      "admin_sent": true,
      "customer_sent": true
    },
    "data": {
      "id": 1,
      "name": "Customer Name",
      "email": "customer@example.com",
      "phone_number": "+91 9876543210",
      "subject": "Inquiry Subject",
      "message": "Detailed message here...",
      "created_at": "2026-10-29T07:35:00Z",
      "updated_at": "2026-10-29T07:35:00Z"
    }
  }

- **Validation Error Response (HTTP 400 Bad Request)**:
  {
    "name": ["This field may not be blank."],
    "email": ["Enter a valid email address."],
    "subject": ["This field may not be blank."],
    "message": ["This field may not be blank."]
  }

### Form Requirements & Behavior
1. **Fields**:
   - `name`: Text input (required, max 100 characters)
   - `email`: Email input (required, valid email pattern)
   - `phone_number`: Phone input (optional, max 20 characters, e.g. "+91 9876543210")
   - `subject`: Text input (required, max 100 characters)
   - `message`: Textarea (required, min 4 rows)
2. **States to Handle**:
   - **Idle**: Clean initial state.
   - **Submitting / Loading**: Disable the submit button and show a spinner or "Sending..." label.
   - **Success**: Display a friendly alert / toast notifying the customer that their message was sent and an email confirmation was dispatched to their inbox. Reset form fields.
   - **Error**: Display field-level validation errors under the respective inputs or a general error toast.
3. **Styling**:
   - Clean, modern packaging-themed card design.
   - Fully responsive on mobile, tablet, and desktop screens.
```

---

## 2. API Contract Details

| Property | Value |
|---|---|
| **Base URL** | `http://127.0.0.1:8000` (or production domain) |
| **Endpoint** | `/api/easypack/contact/` |
| **HTTP Methods** | `POST` (Submit enquiry), `GET` (List enquiries) |
| **Auth Required** | None (Public endpoint) |
| **Automated Emails Sent** | 1. Admin notification (includes Phone Number) to `info2easypack@gmail.com`<br>2. Acknowledgment reply to `customer.email` |

---

## 3. Implementation Example 1: React / Next.js (TypeScript + Tailwind CSS)

```tsx
import React, { useState } from 'react';
import axios from 'axios';

interface ContactFormData {
  name: string;
  email: string;
  phone_number: string;
  subject: string;
  message: string;
}

const ContactForm: React.FC = () => {
  const [formData, setFormData] = useState<ContactFormData>({
    name: '',
    email: '',
    phone_number: '',
    subject: '',
    message: '',
  });

  const [loading, setLoading] = useState<boolean>(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [errors, setErrors] = useState<Record<string, string[]>>({});

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    if (errors[e.target.name]) {
      setErrors((prev) => {
        const next = { ...prev };
        delete next[e.target.name];
        return next;
      });
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setSuccessMessage(null);
    setErrors({});

    try {
      const response = await axios.post(
        'http://localhost:8000/api/easypack/contact/',
        formData,
        {
          headers: { 'Content-Type': 'application/json' },
        }
      );

      setSuccessMessage(
        "Thank you! Your message has been sent successfully. We've sent a confirmation to your email."
      );
      setFormData({ name: '', email: '', phone_number: '', subject: '', message: '' });
    } catch (err: any) {
      if (err.response && err.response.data) {
        setErrors(err.response.data);
      } else {
        alert("Unable to send message. Please check your internet connection.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto p-6 md:p-8 bg-white rounded-2xl shadow-xl border border-gray-100">
      <h2 className="text-2xl font-bold text-gray-800 text-center mb-2">Get in Touch</h2>
      <p className="text-sm text-gray-500 text-center mb-6">
        Have questions or need custom packaging? Send us a message and our team will get back to you shortly.
      </p>

      {successMessage && (
        <div className="mb-6 p-4 rounded-lg bg-green-50 border border-green-200 text-green-700 text-sm">
          {successMessage}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Full Name *</label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="John Doe"
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none"
          />
          {errors.name && <p className="text-red-500 text-xs mt-1">{errors.name[0]}</p>}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Email Address *</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="john@example.com"
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none"
          />
          {errors.email && <p className="text-red-500 text-xs mt-1">{errors.email[0]}</p>}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Phone Number</label>
          <input
            type="tel"
            name="phone_number"
            value={formData.phone_number}
            onChange={handleChange}
            placeholder="+91 98765 43210"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none"
          />
          {errors.phone_number && <p className="text-red-500 text-xs mt-1">{errors.phone_number[0]}</p>}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Subject *</label>
          <input
            type="text"
            name="subject"
            value={formData.subject}
            onChange={handleChange}
            placeholder="Enquiry regarding corrugated boxes"
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none"
          />
          {errors.subject && <p className="text-red-500 text-xs mt-1">{errors.subject[0]}</p>}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Message *</label>
          <textarea
            name="message"
            rows={4}
            value={formData.message}
            onChange={handleChange}
            placeholder="Please specify box sizes, quantity, or any custom branding requirements..."
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none"
          />
          {errors.message && <p className="text-red-500 text-xs mt-1">{errors.message[0]}</p>}
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full py-3 bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-semibold rounded-lg shadow-md hover:opacity-95 transition-opacity disabled:opacity-50 cursor-pointer"
        >
          {loading ? "Sending..." : "Send Message"}
        </button>
      </form>
    </div>
  );
};

export default ContactForm;
```

---

## 4. Implementation Example 2: Vanilla JavaScript & HTML (Fetch API)

```html
<form id="contactForm">
  <input type="text" id="name" placeholder="Your Name *" required />
  <input type="email" id="email" placeholder="Your Email *" required />
  <input type="tel" id="phone_number" placeholder="Phone Number (Optional)" />
  <input type="text" id="subject" placeholder="Subject *" required />
  <textarea id="message" placeholder="Your Message *" required></textarea>
  <button type="submit" id="submitBtn">Send Message</button>
  <div id="statusMessage"></div>
</form>

<script>
  const form = document.getElementById('contactForm');
  const btn = document.getElementById('submitBtn');
  const statusDiv = document.getElementById('statusMessage');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    btn.disabled = true;
    btn.innerText = 'Sending...';
    statusDiv.innerText = '';

    const payload = {
      name: document.getElementById('name').value,
      email: document.getElementById('email').value,
      phone_number: document.getElementById('phone_number').value,
      subject: document.getElementById('subject').value,
      message: document.getElementById('message').value,
    };

    try {
      const res = await fetch('http://localhost:8000/api/easypack/contact/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      const data = await res.json();

      if (res.ok) {
        statusDiv.style.color = 'green';
        statusDiv.innerText = data.message || 'Message sent successfully!';
        form.reset();
      } else {
        statusDiv.style.color = 'red';
        statusDiv.innerText = Object.values(data).flat().join(', ');
      }
    } catch (err) {
      statusDiv.style.color = 'red';
      statusDiv.innerText = 'Network error. Please try again later.';
    } finally {
      btn.disabled = false;
      btn.innerText = 'Send Message';
    }
  });
</script>
```
