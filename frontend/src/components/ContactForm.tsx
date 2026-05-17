import React, { useState } from 'react';

const ContactForm: React.FC = () => {
  const [formData, setFormData] = useState({
    fullName: '',
    whatsappPhone: '',
    emailAddress: '',
    serviceSelect: 'Laser Hair Removal',
    userMessage: ''
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const { fullName, whatsappPhone, emailAddress, serviceSelect, userMessage } = formData;
    
    // Target Clinic WhatsApp Number
    const targetNumber = "918177955821"; 
    
    // Construct the structured text block
    const textMessage = `Hello Sovilo Aesthetics Baner, I would like to book an appointment / make an inquiry via the website form. Here are my details:\n\n` +
                        `■ PATIENT INQUIRY DETAILS\n` +
                        `- Name: ${fullName.trim()}\n` +
                        `- Contact Number: ${whatsappPhone.trim()}\n` +
                        `- Email: ${emailAddress.trim()}\n` +
                        `- Selected Service: ${serviceSelect}\n\n` +
                        `■ MESSAGE / REMARKS\n` +
                        `"${userMessage.trim()}"\n\n` +
                        `Please verify availability and connect me with Dr. Suryawanshi's team.`;
    
    // Encode for safe URL transport
    const encodedMessage = encodeURIComponent(textMessage);
    
    // Direct link generation
    const whatsappUrl = `https://wa.me/${targetNumber}?text=${encodedMessage}`;
    
    // Seamless application redirect
    window.open(whatsappUrl, '_blank');
  };

  return (
    <div className="max-w-2xl mx-auto p-6 md:p-8 bg-white shadow-card rounded-2xl">
      <div className="text-center mb-8">
        <h2 className="text-3xl md:text-4xl font-heading font-bold text-charcoal mb-3">
          Get in Touch
        </h2>
        <p className="text-gray-600 font-sans">
          Fill out the form below to book an appointment or ask a question.
        </p>
      </div>

      <form id="contactForm" onSubmit={handleSubmit} className="space-y-6 font-sans">
        <div className="space-y-2">
          <label htmlFor="fullName" className="block text-sm font-medium text-charcoal">Full Name</label>
          <input
            type="text"
            id="fullName"
            name="fullName"
            value={formData.fullName}
            onChange={handleChange}
            placeholder="Enter your full name"
            required
            className="w-full px-4 py-3 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all duration-200 bg-soft-gray focus:bg-white"
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <label htmlFor="whatsappPhone" className="block text-sm font-medium text-charcoal">WhatsApp Number</label>
            <input
              type="tel"
              id="whatsappPhone"
              name="whatsappPhone"
              value={formData.whatsappPhone}
              onChange={handleChange}
              placeholder="Enter your WhatsApp number"
              required
              className="w-full px-4 py-3 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all duration-200 bg-soft-gray focus:bg-white"
            />
          </div>

          <div className="space-y-2">
            <label htmlFor="emailAddress" className="block text-sm font-medium text-charcoal">Email Address</label>
            <input
              type="email"
              id="emailAddress"
              name="emailAddress"
              value={formData.emailAddress}
              onChange={handleChange}
              placeholder="Enter your email address"
              required
              className="w-full px-4 py-3 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all duration-200 bg-soft-gray focus:bg-white"
            />
          </div>
        </div>

        <div className="space-y-2">
          <label htmlFor="serviceSelect" className="block text-sm font-medium text-charcoal">Service Interested In</label>
          <select
            id="serviceSelect"
            name="serviceSelect"
            value={formData.serviceSelect}
            onChange={handleChange}
            required
            className="w-full px-4 py-3 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all duration-200 bg-soft-gray focus:bg-white appearance-none"
          >
            <option value="Laser Hair Removal">Laser Hair Removal</option>
            <option value="Hydrafacial / Medi-facials">Hydrafacial / Medi-facials</option>
            <option value="PRP Hair Treatment">PRP Hair Treatment</option>
            <option value="Weight Loss & Slimming Programs">Weight Loss & Slimming Programs</option>
            <option value="PCOS & Hormonal Wellness">PCOS & Hormonal Wellness</option>
            <option value="Pain Management">Pain Management</option>
            <option value="Other / General Consultation">Other / General Consultation</option>
          </select>
        </div>

        <div className="space-y-2">
          <label htmlFor="userMessage" className="block text-sm font-medium text-charcoal">Your Message</label>
          <textarea
            id="userMessage"
            name="userMessage"
            value={formData.userMessage}
            onChange={handleChange}
            placeholder="How can we help you today?"
            required
            rows={4}
            className="w-full px-4 py-3 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all duration-200 bg-soft-gray focus:bg-white resize-y"
          ></textarea>
        </div>

        <button
          type="submit"
          className="w-full py-4 px-6 text-white font-semibold rounded-lg bg-primary hover:bg-primary-light transform transition-all duration-200 hover:scale-[1.02] shadow-lg hover:shadow-xl flex items-center justify-center space-x-2"
        >
          <span>Submit Inquiry via WhatsApp</span>
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
          </svg>
        </button>
      </form>
    </div>
  );
};

export default ContactForm;
