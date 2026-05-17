const services = [
  {
    id: 1,
    name: "Laser Hair Removal",
    description: "Advanced laser technology for permanent hair reduction across all skin types.",
    category: "Laser",
  },
  {
    id: 2,
    name: "Hydrafacial / Medi-facials",
    description: "Deep cleansing, exfoliation, and hydration for radiant, glowing skin.",
    category: "Skin",
  },
  {
    id: 3,
    name: "PRP Hair Treatment",
    description: "Platelet-rich plasma therapy to stimulate natural hair growth and thickness.",
    category: "Hair",
  },
  {
    id: 4,
    name: "Weight Loss & Slimming Programs",
    description: "Medically supervised weight management and body contouring programs.",
    category: "Wellness",
  },
  {
    id: 5,
    name: "PCOS & Hormonal Wellness",
    description: "Comprehensive hormonal assessment and personalized treatment plans.",
    category: "Wellness",
  },
  {
    id: 6,
    name: "Pain Management",
    description: "Non-invasive pain relief therapies for chronic and acute conditions.",
    category: "Therapy",
  },
];

export default function handler(req, res) {
  res.status(200).json({ services });
}
