export default function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { name, phone, email, service, message } = req.body || {};

  if (!name || !phone) {
    return res.status(400).json({ error: "Name and phone are required." });
  }

  // Build the WhatsApp redirect URL for the clinic
  const targetNumber = "918177955821";
  const textMessage =
    `Hello Sovilo Aesthetics Baner, I would like to book an appointment / make an inquiry via the website form. Here are my details:\n\n` +
    `■ PATIENT INQUIRY DETAILS\n` +
    `- Name: ${name}\n` +
    `- Contact Number: ${phone}\n` +
    `- Email: ${email || "N/A"}\n` +
    `- Selected Service: ${service || "General Consultation"}\n\n` +
    `■ MESSAGE / REMARKS\n` +
    `"${message || ""}"\n\n` +
    `Please verify availability and connect me with Dr. Suryawanshi's team.`;

  const whatsappUrl = `https://wa.me/${targetNumber}?text=${encodeURIComponent(textMessage)}`;

  return res.status(200).json({
    success: true,
    message: "Inquiry received. Redirecting to WhatsApp.",
    whatsappUrl,
  });
}
